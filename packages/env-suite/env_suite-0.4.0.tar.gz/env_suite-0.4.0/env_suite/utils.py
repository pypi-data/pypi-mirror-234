"""
A module for utility functions.
"""

import h5py
import importlib


def parse_h5(h5_file):
    """
    Parse an HDF5 file and return a dictionary of the data.

    Parameters
    ----------
    h5_file : str

    Returns
    -------
    dictionary
    """
    with h5py.File(h5_file, 'r') as f:
        data = {key: f[key][()] for key in f.keys()}
    return data


def write_xyz(filename, coords, atoms):
    """
    Write a .xyz file.

    Parameters
    ----------
    filename : str
    coords : numpy.ndarray
    atoms : list
    """

    with open(filename, 'w') as f:
        f.write('{}\n'.format(len(atoms)))
        f.write('{}\n'.format(
            " ".join(set(atoms))))
        for atom, coord in zip(atoms, coords):
            f.write('{}\t{:.8f}\t{:.8f}\t{:.8f}\n'.format(
                atom, coord[0], coord[1], coord[2]))


class ModuleImporter:
    """
    A class for importing modules.
    """

    def __init__(self, module_name):
        self.module_name = module_name
        self._module = None

    def __getattr__(self, name):
        if self._module is None:
            self._module = importlib.import_module(self.module_name)
        return getattr(self._module, name)

masses = {
    'H': 1.00794,
    'He': 4.002602,
    'Li': 6.941,
    'Be': 9.012182,
    'B': 10.811,
    'C': 12.0107,
    'N': 14.0067,
    'O': 15.9994,
    'F': 18.9984032,
    'Ne': 20.1797,
    'Na': 22.98976928,
    'Mg': 24.305,
    'Al': 26.9815386,
    'Si': 28.0855,
    'P': 30.973762,
    'S': 32.065,
    'Cl': 35.453,
    'Ar': 39.948,
    'K': 39.0983,
    'Ca': 40.078,
    'Sc': 44.955912,
    'Ti': 47.867,
    'V': 50.9415,
    'Cr': 51.9961,
    'Mn': 54.938045,
    'Fe': 55.845,
    'Co': 58.933195,
    'Ni': 58.6934,
    'Cu': 63.546,
    'Zn': 65.38,
    'Ga': 69.723,
    'Ge': 72.63,
    'As': 74.9216,
    'Se': 78.96,
    'Br': 79.904,
    'Kr': 83.798,
    'Rb': 85.4678,
    'Sr': 87.62,
    'Y': 88.90585,
    'Zr': 91.224,
    'Nb': 92.90638,
    'Mo': 95.96,
    'Tc': 98,
    'Ru': 101.07,
    'Rh': 102.9055,
    'Pd': 106.42,
    'Ag': 107.8682,
    'Cd': 112.411,
    'In': 114.818,
    'Sn': 118.71,
    'Sb': 121.760,
    'Te': 127.6,
    'I': 126.90447,
    'Xe': 131.293,
    'Cs': 132.9054519,
    'Ba': 137.327,
    'La': 138.90547,
    'Ce': 140.116,
    'Pr': 140.90765,
    'Nd': 144.242,
    'Pm': 145,
    'Sm': 150.36,
    'Eu': 151.964,
    'Gd': 157.25,
    'Tb': 158.92535,
    'Dy': 162.5,
    'Ho': 164.93032,
    'Er': 167.259,
    'Tm': 168.93421,
    'Yb': 173.04,
    'Lu': 174.967,
    'Hf': 178.49,
    'Ta': 180.94788,
    'W': 183.84,
    'Re': 186.207,
    'Os': 190.23,
    'Ir': 192.217,
    'Pt': 195.084,
    'Au': 196.966569,
    'Hg': 200.59,
    'Tl': 204.3833,
    'Pb': 207.2,
    'Bi': 208.98040,
    'Po': 209,
    'At': 210,
    'Rn': 222,
    'Fr': 223,
    'Ra': 226,
    'Ac': 227,
    'Th': 232.03806,
    'Pa': 231.03588,
    'U': 238.02891,
    'Np': 237,
    'Pu': 244,
    'Am': 243,
    'Cm': 247,
    'Bk': 247,
    'Cf': 251,
    'Es': 252,
    'Fm': 257,
    'Md': 258,
    'No': 259,
    'Lr': 262,
    'Rf': 261,
    'Db': 262,
    'Sg': 266,
    'Bh': 264,
    'Hs': 277,
    'Mt': 268,
    'Ds': 281,
    'Rg': 272,
    'Cn': 285,
    'Nh': 284,
    'Fl': 289,
    'Mc': 288,
    'Lv': 292,
    'Ts': 294,
    }
