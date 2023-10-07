from itertools import product
from functools import reduce
from math import ceil

# from pymatgen.core.structure import Molecule
# from pymatgen.analysis.graphs import StructureGraph
# from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
# from pymatgen.analysis.local_env import IsayevNN
import networkx as nx
import networkx.algorithms.isomorphism as iso

from phonopy.interface.vasp import read_vasp  # TODO: replace by alternative POSCAR parser
import numpy as np
import numpy.linalg as la

from .utils import ModuleImporter


def generate_molecular_graph(structure):

    # Imports pymatgen modules
    p_graphs = ModuleImporter('pymatgen.analysis.graphs')
    p_local_env = ModuleImporter('pymatgen.analysis.local_env')
    p_analyzer = ModuleImporter('pymatgen.symmetry.analyzer')

    # Import classes
    StructureGraph = p_graphs.StructureGraph
    IsayevNN = p_local_env.IsayevNN
    SpacegroupAnalyzer = p_analyzer.SpacegroupAnalyzer

    strategy = IsayevNN(cutoff=3.0, allow_pathological=True)
    graph = StructureGraph.with_local_env_strategy(structure, strategy, weights=True)

    sym_structure = SpacegroupAnalyzer(structure).get_symmetrized_structure()
    equivalent_positions = sym_structure.as_dict()['equivalent_positions']

    # build directed multi-graph
    twoway = nx.MultiDiGraph(graph.graph)
    # nodes are labelled by species
    nx.set_node_attributes(twoway,
        {node: {'symm_equiv': (structure[node].specie, equivalent_positions[node])} for node in twoway})

    def flip_edge(u, v, data):
        return v, u, {key: tuple(-i for i in val) if key == 'to_jimage'
                      else val for key, val in data.items()}

    # edges are labelled by periodic image crossing
    twoway.add_edges_from([flip_edge(*edge) for edge in twoway.edges(data=True)])

    return twoway


def split_molecular_graph(graph, filter_unique=False):

    connected = nx.connected_components(nx.Graph(graph))

    subgraphs = map(graph.subgraph, connected)

    def filter_unique_graphs(graphs):

        edge_match = iso.numerical_edge_match("weight", 1.0)
        node_match = iso.categorical_node_match("symm_equiv", None)

        unique_graphs = set()

        for graph in graphs:

            def graph_match(g):
                return nx.is_isomorphic(
                    graph, g, node_match=node_match, edge_match=edge_match)

            already_present = map(graph_match, unique_graphs)

            if not any(already_present):
                unique_graphs.add(graph)
                yield graph

    if filter_unique:
        return list(filter_unique_graphs(subgraphs))
    else:
        return list(subgraphs)


def extract_molecule(structure, graph, central_index=None):

    # Imports pymatgen modules
    p_structure = ModuleImporter('pymatgen.core.structure')
    Molecule = p_structure.Molecule

    # walk graph and consider to_jimage
    def generate_shifts():

        start = next(iter(graph.nodes())) if central_index is None else central_index

        def walk(shifts, edge):
            a, b = edge
            return shifts | {b: shifts[a] + graph[a][b][0]['to_jimage']}

        edges = nx.bfs_edges(graph, source=start)
        shifts = reduce(walk, edges, {start: np.zeros(3)})
        return dict(sorted(shifts.items()))

    shifts = generate_shifts()

    species = [structure.species[idx] for idx in shifts]
    coords = [structure.lattice.get_cartesian_coords(
        structure.frac_coords[idx] + shift) for idx, shift in shifts.items()]
    molecule = Molecule(species, coords)

    return list(shifts.keys()), molecule


def get_unique_entities(structure):

    # Imports pymatgen modules
    p_analyzer = ModuleImporter('pymatgen.symmetry.analyzer')
    SpacegroupAnalyzer = p_analyzer.SpacegroupAnalyzer

    sym_structure = SpacegroupAnalyzer(structure).get_symmetrized_structure()
    structure_dict = sym_structure.as_dict()
    equivalent_positions = structure_dict['equivalent_positions']

    molecular_graph = generate_molecular_graph(structure)
    connected_graphs = split_molecular_graph(molecular_graph, filter_unique=True)
    indices, molecules = zip(*map(lambda x: extract_molecule(structure, x), connected_graphs))

    elements = [site.specie.symbol for site in structure]

    mappings = [[equivalent_positions[idx] for idx in shift_dict]
                for shift_dict in indices]

    return equivalent_positions, elements, mappings, molecules


def generate_qm_region(idx, graph, structure):
    connected_graphs = split_molecular_graph(graph, filter_unique=False)
    central_graph = next(filter(lambda nodes: idx in nodes, connected_graphs))
    _, mol = extract_molecule(structure, central_graph, central_index=idx)
    central_site = structure.sites[idx]
    shift = np.array([central_site.x, central_site.y, central_site.z])
    return mol, shift


def build_cluster(poscar, central_idc=None, cluster_expansion=None,
                  cluster_cutoff=None):

    if cluster_expansion is not None:
        cluster = UnitSupercell.from_poscar(
            poscar, cluster_expansion, central_idc=central_idc)
    elif cluster_cutoff is not None:
        cluster = UnitSphere.from_poscar(
            poscar, cluster_cutoff, central_idc=central_idc)
    else:
        ValueError("Invalid cluster specification!")

    return cluster


class UnitCluster:
    """Base class for cluster of specific morphology made from unit cells.

    Parameters
    ----------
    lat_vecs : list
        Lattice vectors of unit cell as rows
    coords : list
        Coordinates of each atom in cell as fraction of cell parameters
    atom_numbers : list
        Atomic number of each atom in cell
    center : list
        Coordinates of the center of interest

    Attributes
    ----------
    unit_coords : list
        Fractional coordinates of the shifted unit cell structure
    cart_coords : list
        Cartesian coordinates of the expanded and shifted structure
    frac_coords : list
        Fractional coordinates of the expanded and shifted structure
    """
    def __init__(self, lat_vecs, coords, atom_numbers, center, *args, **kwargs):

        self.lat_vecs = lat_vecs
        # TODO: Do you need the atomic_numbers as an attribute? If not they can go!
        self.atom_numbers = atom_numbers
        # periodically pre-shift unit cell to center of interest
        self.unit_coords = self.recenter_unitcell(coords, center, *args)

        self.cart_coords = self.generate_cluster(*args)
        self.frac_coords = self.cart_coords @ la.inv(self.lat_vecs)
        self.n_atoms = len(atom_numbers)
        self.n_cell = self.frac_coords.shape[0] // self.unit_coords.shape[0]

        a1, a2, a3 = self.lat_vecs
        self.unit_volume = np.dot(a1, np.cross(a2, a3))

        # 2 PI is included in the summation
        self.recip_vecs = np.array([
            np.cross(a2, a3),
            np.cross(a3, a1),
            np.cross(a1, a2)
        ]) / self.unit_volume

    @classmethod
    def from_poscar(cls, poscar_name, *args, central_idc=None, center=None):
        atoms = read_vasp(poscar_name)

        coords = atoms.scaled_positions

        if center is not None:
            center = center
        elif central_idc is not None:
            center = np.mean(coords[list(central_idc)], axis=0)
        else:
            center = None

        return cls(atoms.cell, coords, atoms.numbers, center, *args)

    def generate_cluster(self, *args):

        def shift_coords(idc):
            return (self.unit_coords + np.array(idc)) @ self.lat_vecs

        coords = np.array([coord for idc in self.generate_cell_idc(*args)
                           for coord in shift_coords(idc)])

        return self.recenter_cluster(coords, *args)


class UnitSupercell(UnitCluster):

    def generate_cell_idc(self, expansion):

        def expansion_range(num):

            start = stop = num // 2

            if num % 2 == 0:  # even
                return range(-start, stop)
            elif num % 2 == 1:  # odd
                return range(-start, stop + 1)

        for nvec in product(*map(expansion_range, expansion)):
            yield nvec

    def recenter_cluster(self, cart, expansion):

        def shift(num, vec):
            if num % 2 == 0:  # even
                return 0.0
            elif num % 2 == 1:  # odd
                return vec / 2

        return cart - np.sum(list(map(shift, expansion, self.lat_vecs)), axis=0)

    def recenter_unitcell(self, frac, center, expansion):

        def shift(num):
            if num % 2 == 0:  # even
                return 0.0
            elif num % 2 == 1:  # odd
                return 1 / 2

        return (frac - center + np.array(list(map(shift, expansion)))) % 1.0


class UnitSphere(UnitCluster):

    def generate_cell_idc(self, cutoff):

        def expansion_range(vec1, vec2, vec3):
            norm_vec = np.cross(vec2, vec3)
            num = ceil(abs(cutoff /
                           np.dot(norm_vec / np.linalg.norm(norm_vec), vec1)))

            return range(-num, num + 1)

        cyc_perm = [[self.lat_vecs[i - j] for i in range(3)] for j in range(3)]

        for nvec in product(*map(expansion_range, *cyc_perm)):

            r = np.sum([ni * ci for ni, ci in zip(nvec, self.lat_vecs)], axis=0)

            if np.linalg.norm(r) <= cutoff:
                yield nvec

    def recenter_cluster(self, cart, *args):
        return cart - np.sum(self.lat_vecs, axis=0) / 2

    def recenter_unitcell(self, frac, center, *args):
        return (frac - center + 1 / 2) % 1.0


def write_molcas_basis(labels, charge_dict, name):
    """
    Writes dummy molcas basis file for environment charges to a textfile named
    according to the basis name.

    Parameters
    ----------
    labels : list[str]
        Atomic labels of environment with no indexing
    charge_dict : dict
        CHELPG charge of each environment atom
    name : str
        Root name of basis
    """

    with open(name, 'w') as f:

        f.write("* This file was generated by spin_phonon_suite\n")
        for elem, (lab, chrg) in zip(labels, charge_dict.items()):
            f.write(f"/{elem}.{name}.{lab}.0s.0s.\n")
            f.write("Dummy basis set for atomic charges of environment\n")
            f.write("no ref\n")
            f.write(f"{chrg:.9f} 0\n")
            f.write("0 0\n")

    return
