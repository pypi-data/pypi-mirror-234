"""
Command line interface for env_suite.
"""

import argparse
import re
from textwrap import dedent
import os
import numpy as np
from hpc_suite import parse_index
import gaussian_suite as gaussian
import xyz_py
import vasp_suite.structure as vasp

# from pymatgen.core.structure import Molecule, Structure

from . import ewald, plotter, utils, output
from . import cells


def ewald_func(args):
    """
    Wrapper function for ewald.

    Parameters
    ----------
    poscar : str
        Path to the POSCAR file.
    qm_region : str
        xyz file containing the QM region.
    charges : str
        .dat file containg the unit cell charges.
    central_atom : str
        The central atom of the QM region <Dy1>.
    expansion : list
        Supercell expansion <n n n>.
    r_cut : float
        Cutoff radius of the sphere region.
    n : list
        Summation cut off <n n n>.
    verbose : int
        Verbosity level.

    Returns
    -------
    ewald.out : file
        Output file containing charges to be entered into
        a muliconfiguration code.
    """
    # Import pymatgen
    p_structure = utils.ModuleImporter('pymatgen.core.structure')

    # Import class
    Structure = p_structure.Structure
    Molecule = p_structure.Molecule

    structure = Structure.from_file(args.poscar)
    central_idc = args.central_index

    if args.from_central:
        molecular_graph = cells.generate_molecular_graph(structure)
        qm_regions, shifts = zip(*map(lambda i: cells.generate_qm_region(i, molecular_graph, structure), central_idc))
        qm_region = Molecule.from_sites([site for mol in qm_regions for site in mol.sites])
        shift = np.mean(shifts, axis=0)
    elif args.qm_region is not None:
        qm_region = Molecule.from_file(args.qm_region)
        shift = np.zeros(3)
    elif args.coordination_sphere:
        poscar = vasp.Molecule(args.poscar, args.atom_index, args.max_bond_length)
        poscar.get_coordination_sphere(args.coordination_sphere_number)
        coords = poscar.cart_coords.astype(float)
        atoms = list(map(lambda x: str(x), poscar._atom_list))
        shift = np.zeros(3)
    else:
        raise NotImplementedError()

    if not args.coordination_sphere:
        coords = np.array([site.coords for site in qm_region.sites])
        atoms = [site.specie.symbol for site in qm_region.sites]

    coords -= shift
    utils.write_xyz('qm_region.xyz', coords, atoms)

    cluster = cells.build_cluster(args.poscar, central_idc=central_idc,
                                  cluster_expansion=args.cluster_expansion,
                                  cluster_cutoff=args.cluster_cutoff)

    calc_dict = ewald.ewald_potential(
            cluster=cluster,
            qm_region=coords,
            charges=args.charges,
            r_cut=args.r_cut,
            n=args.n,
            verbose=args.verbose)

    calc_dict.update({'qm atoms': atoms})

    h5out = output.OutputWriter('ewald.hdf5')
    h5out.write_h5(calc_dict)

    ewald.write_output(calc_dict['Sphere'],
                       calc_dict['Param'],
                       )


def plotter_func(args):
    """
    Wrapper function for plotter.

    Parameters
    ----------
    filename : str
        Path to the h5 file containing the charges.
    dim : int
        Dimension to plot the potential in /Å.
    num_points : int
        Number of points to evaluate the potential at.
    num_contours : int
        Number of contours to plot.
    show : bool
        Whether to show the plot or save it.

    Returns
    -------
    potential.png : file
        Potential plot.
    """
    if isinstance(args.num_points, list):
        num_points = args.num_points[0]
    else:
        num_points = args.num_points

    if isinstance(args.num_contours, list):
        num_contours = args.num_contours[0]
    else:
        num_contours = args.num_contours

    if not args.filename.split('.')[-1] == 'hdf5':
        raise ValueError('Input file must be a .hdf5 file')
    else:
        data = utils.parse_h5(args.filename)
        sphere, param = data['Sphere'], data['Param']
        coords = np.concatenate((sphere[:, :3], param[:, :3]), axis=0)
        q = np.concatenate((sphere[:, 4], param[:, 4]), axis=0)

    # evaluate the potential
    x, y, z = plotter.evaluate_potential(coords, q, num_points, args.dim)

    # plot the potential
    plotter.plot_potential(x, y, z, num_contours, args.show)


def plot_3d_model_func(args):
    """
    wrapper functions for plot_3d_model
    """
    if not args.filename.split('.')[-1] == 'hdf5':
        raise ValueError('Input file must be a .hdf5 file')
    else:
        data = utils.parse_h5(args.filename)
        sphere, param = data['Sphere'], data['Param']
        qm = data['qm region']

        sphere = np.array(sphere[:, :3], dtype=float)
        param = np.array(param[:, :3], dtype=float)

    plotter.plot_3d_model(sphere, param, qm)


def charges_func(args):
    """
    Wrapper function for cli call to charges
    """

    # pymatgen interface required as input to molecular graph generation
    # (could be pushed to back into the function by supplying generic structure
    # data and then converting it to a pymatgen Structure)

    p_structure = utils.ModuleImporter('pymatgen.core.structure')
    Structure = p_structure.Structure

    structure = Structure.from_file(args.poscar)

    if args.from_file is None:
        equivalent_positions, elements, mappings, entities = \
            cells.get_unique_entities(structure)
    else:
        elements = [x.symbol for x in structure.species]
        unitcell_charges = np.loadtxt(args.from_file)
        cells.write_molcas_basis(
            elements, dict(enumerate(unitcell_charges, start=1)), "ENV")

        print("\033[93m")
        print("Molcas basis set file for environment written to:")
        print("     ENV (basis set specification)\033[0m")
        return

    if args.gen:
        gen_charges_func(entities)
    elif args.parse:
        parse_charges_func(equivalent_positions, elements, mappings, entities)
    else:
        ValueError(f"{args.mode} mode not supported!")


def format_formula(formula):

    def split_symbol_number(x):
        elem = re.search('([a-zA-Z]+)', x).group(0)
        num = int(re.search('(\d+)', x).group(0))
        return (elem, num)

    def format_constituent(x):
        return x[0] + str("" if x[1] == 1 else x[1])

    constituents = map(split_symbol_number, formula.split(" "))
    ordered = map(format_constituent, sorted(constituents, key=lambda x: x[0]))
    return ''.join(ordered)


def gen_charges_func(entities):
    """
    Wrapper function for cli call to charges gen
    """

    print("******************************")
    print("The unique entities are")
    for mol in entities:
        print(mol.formula)
        mol.to(f"{format_formula(mol.formula)}.xyz")
    print("******************************")

    # Create gaussian inputs for CHELPG calculation, one for each
    # member of the ASU

    # All electron aug-cc-pvtz
    ae_pvtz = [
        'H', 'Li', 'Be', 'Na', 'Mg', 'B', 'C', 'N', 'O', 'F', 'He', 'Ne', 'Al',
        'Si', 'P', 'S', 'Cl', 'Ar', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr'
    ]
    ae_basis = {atom: "aug-cc-pvtz" for atom in ae_pvtz}

    unsupported = [
        "K", "Ca", "Rb", "Sr", "Cs", "Ba", "Ac", "Th", "Pa", "U", "Np",
        "Pu", "Am", "Cm"
    ]
    unsupported_basis = {atom: "????" for atom in unsupported}

    for lab in (site.specie.symbol for mol in entities for site in mol.sites):
        if lab in unsupported:
            print(f"\033[31m Warning, add basis for {lab} to .com file\033[0m \n")

    ae_basis = ae_basis | unsupported_basis

    # ECP
    pp_pvtz = [
        'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn'
    ]
    small_pp_basis = {atom: "aug-cc-pvtz-pp" for atom in pp_pvtz}

    stuttgart = {metal: "stuttgart rsc 1997"
                 for metal in xyz_py.atomic.lanthanides + xyz_py.atomic.transition_metals}

    psuedo = small_pp_basis | stuttgart

    try:
        os.mkdir("gaussian")
    except OSError:
        pass

    for idx, mol in enumerate(entities, start=1):
        gaussian.gen_input.gen_input(
            f"gaussian/{format_formula(mol.formula)}_{idx}.com",
            list(map(lambda site: site.specie.symbol, mol.sites)),
            list(map(lambda site: (site.x, site.y, site.z), mol.sites)),
            99,
            99,
            method="PBE",
            bs_spec=ae_basis,
            ecp_spec=psuedo,
            opt=False,
            freq=False,
            extra_title=f"{format_formula(mol.formula)} (molecule #{idx})",
            chelpg="charge"
        )
        print()

    print("\033[93mCharge and multiplicity set to 99 in all .com files")
    print("Please replace with actual values before submitting \033[0m \n")

    return


def parse_charges_func(equivalent_positions, elements, mappings, entities):
    """
    Wrapper function for cli call to charges parse
    """

    def read_charges(mol, idx):
        file = f"gaussian/{format_formula(mol.formula)}_{idx}.log"
        charges = gaussian.cd_extractor.get_chelpg_charges(file)

        if not charges:
            raise ValueError(f"{file} does not contain charges!")

        return np.array(charges)

    def symmetrize(mapping, charges):
        for val in np.unique(mapping):
            for idc in np.flatnonzero(mapping == val):
                yield val, np.mean(charges[idc])

    def neutralize(charges):
        return np.array(charges) - np.mean(charges)

    mol_mappings = enumerate(zip(mappings, entities), start=1)
    atomic_charges = {idx: chrg for mol_idx, (mapping, mol) in mol_mappings
                      for idx, chrg in symmetrize(mapping, read_charges(mol, mol_idx))}

    unitcell_charges = neutralize([
        atomic_charges[pos] for pos in equivalent_positions])

    np.savetxt("charges.dat", unitcell_charges)

    # Make molcas basis file for environment charges
    cells.write_molcas_basis(
        elements, dict(enumerate(unitcell_charges, start=1)), "ENV")

    print("\033[93m")
    print("Molcas basis set file for environment written to:")
    print("     ENV (basis set specification)\033[0m")


def cluster_func(args):

    p_structure = utils.ModuleImporter("pymatgen.core.structure")
    Structure = p_structure.Structure
    Molecule = p_structure.Molecule

    structure = Structure.from_file(args.poscar)
    central_idc = args.central_index

    if args.from_central:
        molecular_graph = cells.generate_molecular_graph(structure)
        qm_regions, shifts = zip(*map(lambda i: cells.generate_qm_region(i, molecular_graph, structure), central_idc))
        qm_region = Molecule.from_sites([site for mol in qm_regions for site in mol.sites])
        shift = np.mean(shifts, axis=0)
    elif args.qm_region is not None:
        qm_region = Molecule.from_file(args.qm_region)
        shift = np.zeros(3)
    elif args.coordination_sphere:
        poscar = vasp.Molecule(args.poscar, args.atom_index, args.max_bond_length)
        poscar.get_coordination_sphere(args.coordination_sphere_number)
        poscar.write_xyz("coordination_sphere.xyz")
        qm_region = Molecule.from_file("coordination_sphere.xyz")
        shift = np.zeros(3)
    else:
        raise NotImplementedError()

    cluster = cells.build_cluster(args.poscar, central_idc=central_idc,
                                  cluster_expansion=args.cluster_expansion,
                                  cluster_cutoff=args.cluster_cutoff)

    def format_label(args):
        idx, specie = args
        return f"{specie.symbol}.ENV.{idx}"

    labels = list(map(format_label, enumerate(structure.species, start=1))) * cluster.n_cell

    def generate_mapping(ref_coords):

        for idx, site in enumerate(qm_region.sites):

            coord = np.array([site.x, site.y, site.z]) - shift
            idc = np.flatnonzero(np.isclose(ref_coords, coord).all(axis=1))

            if len(idc) == 0:
                continue
            elif len(idc) == 1:
                yield idc[0]
            else:
                raise ValueError(f"Multiple instances of atom {coord}!")

    for idx in generate_mapping(cluster.cart_coords):
        labels[idx] = labels[idx].split('.')[0]

    xyz_py.save_xyz("cluster.xyz", labels, cluster.cart_coords)


cluster = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False
)

morph = cluster.add_mutually_exclusive_group()

morph.add_argument(
    '--cluster_expansion',
    nargs=3,
    metavar=('N_x', 'N_y', 'N_z'),
    type=int,
    help='Supercell expansion.'
)

morph.add_argument(
    '--cluster_cutoff',
    type=float,
    help='Cut-off distance for unit cell cluster.'
)

cluster.add_argument(
    '--central_index',
    type=parse_index,
    nargs='+',
    help='Index of the central spin center or list of atomic indices.'
)


def get_index(atoms: list,
              atom: str,
              natoms: list,
              ) -> np.ndarray:

    atom = re.split(r'(\d+)', atom)
    for ind, sym in enumerate(atoms):
        if sym == atom[0]:
            index = ind

    prev = np.sum(natoms[:index])
    return int(prev) + int(atom[1]) - 1


def read_args(arg_list=None):
    '''Reads the command line arguments.'''
    parser = argparse.ArgumentParser(
            prog='env_suite',
            description=dedent(
                '''
                Available programmes:
                    env_suite ewald ...
                    env_suite cluster ...
                    env_suite charges ...
                    env_suite plot_potential ...
                    env_suite visualise_ewald ...
                '''),
            epilog=dedent(
                '''
                To display options for a specific programme, use:
                    env_suite <programme> -h
                '''),
            formatter_class=argparse.RawDescriptionHelpFormatter,
            )

    subparsers = parser.add_subparsers(dest='prog')

    ewald_parser = subparsers.add_parser(
        'ewald',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[cluster],
        )

    ewald_parser.set_defaults(func=ewald_func)

    ewald_parser.add_argument(
        '--poscar',
        type=str,
        help='Path to the POSCAR file.',
        default='POSCAR',
        )

    ewald_qm = ewald_parser.add_mutually_exclusive_group(required=True)

    ewald_qm.add_argument(
        '--from_central',
        action='store_true',
        help=('QM region is built by completing the molecule around the '
              'central index.')
    )

    ewald_qm.add_argument(
        '--qm_region',
        type=str,
        help='Coordinates of the QM-region.'
    )

    ewald_qm.add_argument(
            '--coordination_sphere',
            action='store_true',
            help='Build QM region from coordination sphere.'
    )

    ewald_parser.add_argument(
            '--atom_index',
            type=str,
            help='Atom index of the central atom. eg "Dy1"'
    )

    ewald_parser.add_argument(
            '--max_bond_length',
            type=float,
            help='Maximum bond length for coordination sphere.',
            default=2.5,
    )

    ewald_parser.add_argument(
            '--coordination_sphere_number',
            type=int,
            help='Number of atoms in coordination sphere.'
    )

    ewald_parser.add_argument(
            '--charges',
            type=str,
            help='.dat file containg the unit cell charges.',
            )

    ewald_parser.add_argument(
            '--r_cut',
            type=float,
            help='Cutoff radius of the sphere region.',
            )

    ewald_parser.add_argument(
            '--n',
            type=int,
            nargs=3,
            help='Summation cut off.',
            metavar=('N_x', 'N_y', 'N_z'),
            default=[1, 1, 1],
            )

    ewald_parser.add_argument(
            '--verbose', '-v',
            type=int,
            help=dedent(
                '''
                Verbosity level
                0: No Output
                1: Summary of fitting
                2: Full fitting Output
                '''),
            default=1,
            )

    plotter_parser = subparsers.add_parser(
        'plot_potential',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        )

    plotter_parser.set_defaults(func=plotter_func)

    plotter_parser.add_argument(
        '--filename', '-i',
        type=str,
        help='Path to the file containing the charges.',
        default='ewald.hdf5',
        )

    plotter_parser.add_argument(
        '--num_points', '-np',
        type=int,
        help='Number of points to evaluate the potential at.',
        default=50,
        nargs=1,
        )

    plotter_parser.add_argument(
            '--num_contours', '-nc',
            type=int,
            help='Number of contours to plot.',
            default=100,
            nargs=1,
            )

    plotter_parser.add_argument(
        '--show', '-s',
        action='store_true',
        help='Shows the plot',
        )

    plotter_parser.add_argument(
        '--dim', '-d',
        type=int,
        help='Dimension to plot the potential in /Å.',
        metavar='DIM_X, DIM_Y',
        default=[10, 10],
        nargs=2,
        )

    plot3d = subparsers.add_parser(
            "visualise_ewald",
            description="""
            Plots a 3d model of the ewald zones
            """)

    plot3d.set_defaults(func=plot_3d_model_func)

    plot3d.add_argument(
            '--filename', '-f',
            type=str,
            help='hdf5 file from ewald calculation',
            default='ewald.hdf5',
            )

    charges = subparsers.add_parser(
        "charges",
        description="""
        Creates inputs for Gaussian CHELPG charge calculations of each
        entity in the unit cell of a VASP optimised structure and
        collects the resulting charges
        """)

    charges.set_defaults(func=charges_func)

    charges.add_argument(
        "poscar",
        type=str,
        help='Poscar containing optimised geometry'
    )

    build = subparsers.add_parser('cluster', parents=[cluster])
    build.set_defaults(func=cluster_func)

    build.add_argument(
        '--poscar',
        type=str,
        help='Unit cell POSCAR.'
    )

    build.add_argument(
        '--atom_index',
        type=str,
        help='Atom index of the central atom. eg "Dy1"'
    )

    build.add_argument(
        '--max_bond_length',
        type=float,
        help='Maximum bond length for coordination sphere.',
        default=2.5,
    )

    build.add_argument(
        '--coordination_sphere_number',
        type=int,
        help='Number of atoms in coordination sphere.'
    )

    mode = charges.add_mutually_exclusive_group(required=True)

    mode.add_argument(
        "--gen",
        action='store_true',
        help='Generate Gaussian ChelpG inputs.'
    )

    mode.add_argument(
        "--parse",
        action='store_true',
        help='Parse Gaussian ChelpG outputs.'
    )

    mode.add_argument(
        "--from_file",
        type=str,
        help='Parse charges from file.'
    )

    qm = build.add_mutually_exclusive_group(required=True)

    qm.add_argument(
        '--from_central',
        action='store_true',
        help=('QM region is built by completing the molecule around the '
              'central index.')
    )

    qm.add_argument(
        '--qm_region',
        type=str,
        help='Coordinates of the QM-region.'
    )

    qm.add_argument(
        '--coordination_sphere',
        action='store_true',
        help='Build QM region from coordination sphere.'
    )

    # Parse the arguments 
    parser.set_defaults(func=lambda args: parser.print_help())
    args = parser.parse_args(arg_list)

    # Select programme
    if args in ['ewald', 'plot_potential']:
        args.func(args)
    else:
        args = parser.parse_args(arg_list)
        args.func(args)


def main():
    read_args()
