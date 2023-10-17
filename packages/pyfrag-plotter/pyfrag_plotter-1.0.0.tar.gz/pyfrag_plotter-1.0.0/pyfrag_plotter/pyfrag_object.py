""" Module that combines the data from inputfile and outputfile into a PyFragResultsObject object """
from collections import OrderedDict
from typing import (Annotated, Any, Callable, Dict, List, Literal, Optional, Protocol, Sequence,
                    Tuple, TypeVar, Union)

import numpy as np
import numpy.typing as npt
import pandas as pd
from attrs import define, field

from pyfrag_plotter.errors import PyFragResultsObjectError
from pyfrag_plotter.input.pyfrag_files import get_pyfrag_files
from pyfrag_plotter.input.read_inputfile import read_inputfile
from pyfrag_plotter.input.read_resultsfile import read_results_file
from pyfrag_plotter.processing_funcs import process_results_file

# Type alias for 1D numpy array with variable length but with a fixed dtype (np.float64)
DType = TypeVar("DType", bound=np.generic)
Array1D = Annotated[npt.NDArray[DType], Literal[1]]

# The following dictionary is used to map the standard terms to a nice-looking label, given by a LaTeX string
TERM_LABELS: dict[str, str] = {
    "EnergyTotal": "$\Delta$E",  # type: ignore # noqa: W605 since it is a LaTeX string
    "Int": "$\Delta$E$_{int}$",  # type: ignore # noqa: W605 since it is a LaTeX string
    "StrainTotal": "$\Delta$E$_{strain}$",  # type: ignore # noqa: W605 since it is a LaTeX string
    "Elstat": "$\Delta$V$_{elstat}$",  # type: ignore # noqa: W605 since it is a LaTeX string
    "Pauli": "$\Delta$E$_{Pauli}$",  # type: ignore # noqa: W605 since it is a LaTeX string
    "OI": "$\Delta$E$_{oi}$",  # type: ignore # noqa: W605 since it is a LaTeX string
    "Disp": "$\Delta$E$_{disp}$",  # type: ignore # noqa: W605 since it is a LaTeX string
    "frag1Strain": "$\Delta$E$_{strain,frag1}$",  # type: ignore # noqa: W605 since it is a LaTeX string
    "frag2Strain": "$\Delta$E$_{strain,frag2}$",  # type: ignore # noqa: W605 since it is a LaTeX string
}

# The following dictionary makes sure that the headers in the .txt file are mapped to the correct attribute in the PyFragResultsObject
pyfrag_headers_id_to_attribute_id_mapping: dict[str, str] = {
    "bondlength": "bondlength",
    "angle": "angle",
    "dihedral": "dihedral",
    "overlap": "overlap",
    "population": "population",
    "orbitalenergy": "orbitalenergy",
    "vdd": "vdd",
    "irrepOI": "irrep",
}


@define
class Property(Protocol):
    """ Base class for all properties using the Protocol functionality of python.
    "Properties" are classes that inheret from this class, which are:
        - Bondlength
        - BondAngle
        - DihedralAngle
        - Overlap
        - Population
        - OrbitalEnergy
        - VDD
        - Irrep
    """

    @property
    def label(self) -> str:
        """ Abstract method to be further specified in the individual classes. Returns the label for the property. """
        ...


@define
class Bondlength:
    """ Attrs class for the bond length property containing the atoms indices and the bond length."""
    atom1: int
    atom2: int
    bondlength: float

    def label(self) -> str:
        """ Returns the label for the bond length property. """
        return f"r {self.atom1}-{self.atom2}"


@define
class BondAngle:
    """ Attrs class for the bond angle property containing the atoms indices and the bond angle."""
    atom1: int
    atom2: int
    bondangle: float

    def label(self) -> str:
        """ Returns the label for the bond angle property. """
        return f"$\Theta${self.atom1}-{self.atom2}"  # type: ignore # noqa: W605 since it is a LaTeX string


@define
class DihedralAngle:
    """ Attrs class for the dihedral angle property containing the atoms indices and the dihedral angle."""
    atom1: int
    atom2: int
    atom3: int
    dihedralangle: float

    def label(self) -> str:
        """ Returns the label for the bond length property. """
        return f"r {self.atom1}-{self.atom2}-{self.atom3}"


@define
class Overlap:
    """ Attrs class for the overlap property containing the orbitals and irreps of the two fragments. """
    frag1_orb: str
    frag2_orb: str
    frag1_irrep: Optional[str] = None
    frag2_irrep: Optional[str] = None

    def label(self) -> str:
        """ Returns the label for the overlap property. """
        if self.frag1_irrep is None:
            return f"S {self.frag1_orb}-{self.frag2_orb}"
        return f"S {self.frag1_irrep} {self.frag1_orb}-{self.frag2_irrep} {self.frag2_orb}"


@define
class Population:
    """ Attrs class for the population property containing the orbitals and irreps of the two fragments."""
    orbital: float
    frag: int
    irrep: Optional[str] = None

    def label(self) -> str:
        """ Returns the label for the population property. """
        if self.irrep is None:
            return f"Pop {self.frag} {self.orbital}"
        return f"Pop {self.frag} {self.orbital} {self.irrep}"


@define
class OrbitalEnergy:
    """ Attrs class for the orbital energy property containing the orbitals and irreps of the two fragments."""
    orbital: float
    frag: int
    irrep: Optional[str] = None

    def label(self) -> str:
        """ Returns the label for the orbital energy property. """
        if self.irrep is None:
            return f"$\epsilon$ {self.frag} {self.orbital}"  # type: ignore # noqa: W605 since it is a LaTeX string
        return f"$\epsilon$ {self.frag} {self.orbital} {self.irrep}"  # type: ignore # noqa: W605 since it is a LaTeX string


@define
class VDD:
    atom: int

    def label(self) -> str:
        """ Returns the label for the VDD property. """
        return f"VDD {self.atom}"


@define
class Irrep:
    irrep: str

    def label(self) -> str:
        """ Returns the label for the irrep property. """
        return f"{self.irrep}"


@define
class PyFragResultsObject:
    """
    Attrs class containing all the data of one pyfrag calculation.

    It combines the data from the output file (i.e., the pyfrag_*.txt file) through binding a pandas DataFrame to the class, and the data from the input file through binding specific attributes.
    Examples of the specific attributes are bond lengths, bond angles, dihedral angles, overlaps, populations, orbital energies, VDD, and irreps.

    Attributes:
        name (str): The name of the PyFrag calculation.
        dataframe (pd.DataFrame): The data from the output file (i.e., the pyfrag_*.txt file).
        extra_strain (OrderedDict[str, Array1D[np.float64]]): The extra strain data for the PyFrag calculation.
        bondlength (List[Bondlength]): The bond length data for the PyFrag calculation.
        angle (List[BondAngle]): The bond angle data for the PyFrag calculation.
        dihedral (List[DihedralAngle]): The dihedral angle data for the PyFrag calculation.
        overlap (List[Overlap]): The overlap data for the PyFrag calculation.
        population (List[Population]): The population data for the PyFrag calculation.
        orbitalenergy (List[OrbitalEnergy]): The orbital energy data for the PyFrag calculation.
        vdd (List[VDD]): The VDD data for the PyFrag calculation.
        irrep (List[Irrep]): The irrep data for the PyFrag calculation.

    """
    name: str
    dataframe: pd.DataFrame
    extra_strain: OrderedDict[str, Array1D[np.float64]] = field(factory=dict)
    bondlength: List[Bondlength] = field(factory=list)
    angle: List[BondAngle] = field(factory=list)
    dihedral: List[DihedralAngle] = field(factory=list)
    overlap: List[Overlap] = field(factory=list)
    population: List[Population] = field(factory=list)
    orbitalenergy: List[OrbitalEnergy] = field(factory=list)
    vdd: List[VDD] = field(factory=list)
    irrep: List[Irrep] = field(factory=list)

    def get_data_of_key(self, key: str) -> Array1D[np.float64]:
        """ Returns the data found in the dataframe (from the .txt file) of the specified key."""
        return self.dataframe[key].to_numpy()

    def get_plot_labels(self, keys: Union[Sequence[str], str]) -> Sequence[str]:
        """ Returns the labels of the specified keys. There are two types of keys that should be handled differently:
        1. Standard terms such as "Int", "EnergyTotal", "StrainTotal", "Elstat", "Pauli", "OI", and "Disp"
        2. Non-standard terms such as "bondlength", "overlap", "orbitalenergy", and more.

        The former ones are handled by the TERM_LABELS dictionary, while the latter ones are handled by the label() method of the corresponding class.
        """
        if isinstance(keys, str):
            keys = [keys]

        labels = []
        for key in keys:
            if key in TERM_LABELS:
                labels.append(TERM_LABELS[key])
            else:
                # IrrepOI_1 -> IrrepOI, 1
                key, index = key.split("_")
                # IrrepOI, 1 -> irrep, 1
                key = pyfrag_headers_id_to_attribute_id_mapping[key]
                # irrep, 1 -> irrep[1], which is an instance of the Irrep class and part of the irrep attribute list of the PyFragResultsObject
                labels.append(getattr(self, key)[int(index)-1].label())

        return labels

    def get_x_axis(self, irc_coord: str) -> Array1D[np.float64]:
        """ Returns the x-axis data for the specified IRC coordinate."""
        return self.dataframe[irc_coord].to_numpy()

    def get_peak_of_key(self, key: str, peak: str = "max") -> Tuple[int, float]:
        """ Returns the index and corresponding peak value of the specified key. The peak can be either the maximum or minimum value. """
        if key not in self.dataframe.columns:
            raise PyFragResultsObjectError(f"Key '{key}' not found in PyFragResultsObject. Available keys are: {self.dataframe.columns}")

        data_of_key = self.dataframe[key].to_numpy()

        if peak == "max":
            return int(data_of_key.argmax()), data_of_key.max()
        return int(data_of_key.argmin()), data_of_key.min()


def _add_bondlength(obj: PyFragResultsObject, *bond_info) -> None:
    bondlength_obj = Bondlength(atom1=bond_info[0], atom2=bond_info[1], bondlength=bond_info[2])
    obj.bondlength.append(bondlength_obj)


def _add_bondangle(obj: PyFragResultsObject, *bondangle_info) -> None:
    bondangle_obj = BondAngle(atom1=bondangle_info[0], atom2=bondangle_info[1], bondangle=bondangle_info[2])
    obj.angle.append(bondangle_obj)


def _add_dihedralangle(obj: PyFragResultsObject, *dihedralangle_info) -> None:
    dihedral_obj = DihedralAngle(atom1=dihedralangle_info[0], atom2=dihedralangle_info[1], atom3=dihedralangle_info[2], dihedralangle=dihedralangle_info[3])
    obj.dihedral.append(dihedral_obj)


def _add_overlap(obj: PyFragResultsObject, *overlap_info) -> None:
    """ Adds an Overlap object to the PyFragResultsObject object. """
    if len(overlap_info) == 4:
        overlap_obj = Overlap(frag1_orb=overlap_info[1], frag2_orb=overlap_info[3], )
    else:
        overlap_obj = Overlap(frag1_irrep=overlap_info[0], frag1_orb=overlap_info[2], frag2_irrep=overlap_info[3], frag2_orb=overlap_info[5], )
    obj.overlap.append(overlap_obj)


def _add_population(obj: PyFragResultsObject, *population_info):
    """ Adds an Population object to the PyFragResultsObject object. """
    if len(population_info) == 2:
        pop_obj = Population(frag=population_info[0], orbital=population_info[1])
    else:
        pop_obj = Population(frag=population_info[1], orbital=population_info[0], irrep=population_info[2],)
    obj.population.append(pop_obj)


def _add_orbitalenergy(obj: PyFragResultsObject, *orbenergy_info):
    """ Adds an OrbitalEnergy object to the PyFragResultsObject object. """
    if len(orbenergy_info) == 2:
        orb_energy_obj = OrbitalEnergy(frag=orbenergy_info[0], orbital=orbenergy_info[1])
    else:
        orb_energy_obj = OrbitalEnergy(frag=orbenergy_info[1], orbital=orbenergy_info[0], irrep=orbenergy_info[2],)
    obj.orbitalenergy.append(orb_energy_obj)


def _add_vdd(obj: PyFragResultsObject, vdd_index: str):
    """ Adds an OrbitalEnergy object to the PyFragResultsObject object. """
    vdd_obj = VDD(atom=int(vdd_index))
    obj.vdd.append(vdd_obj)


def _add_irrep(obj: PyFragResultsObject, irrep: str):
    """ Adds an OrbitalEnergy object to the PyFragResultsObject object. """
    irrep_obj = Irrep(irrep=irrep)
    obj.irrep.append(irrep_obj)


key_to_func_mapping: dict[str, Callable[..., None]] = {
    "bondlength": _add_bondlength,
    "angle": _add_bondangle,
    "dihedral": _add_dihedralangle,
    "overlap": _add_overlap,
    "population": _add_population,
    "orbitalenergy": _add_orbitalenergy,
    "vdd": _add_vdd,
    "irrep": _add_irrep,
}


def create_pyfrag_object_from_processed_files(results_data: pd.DataFrame, inputfile_data: Dict[str, Any]) -> PyFragResultsObject:
    """Creates a PyFragResultsObject from the given results data and input file data.

    This function takes a pandas DataFrame containing the results file data and a dictionary containing the input file data and creates a PyFragResultsObject.
    The PyFragResultsObject contains data for various properties such as EDA, ASM, extra strain, bond lengths, bond angles, dihedral angles, overlaps, populations, orbital energies, VDD, and irreps.

    Args:
        results_data (pd.DataFrame): The data from the output file (i.e., the pyfrag_*.txt file).
        inputfile_data (Dict[str, Any]): The keys from the input file such as bondlength, overlap, orbitalenergy, and more.

    Returns:
        PyFragResultsObject: The dataclass containing all the data of one PyFrag calculation.

    Note: standard terms such "Int", "EnergyTotal", "StrainTotal", "Elstat", "Pauli", "OI", and "Disp" are automatically added to the PyFragResultsObject.
    Non-standard terms such as "bondlength", "overlap", "orbitalenergy", and more are added to the PyFragResultsObject by using the key_to_func_mapping dictionary.
    """
    obj = PyFragResultsObject(inputfile_data.pop("name"), results_data)

    for key, value in inputfile_data.items():

        # For non-standard terms such as overlap_[x], bondlength_[x] the term is split on the underscore
        # The first part (e.g., "overlap") determines which kind of instance of the corresponding class should be created
        # The second part (e.g., "x") is to keep track of the relative order
        try:
            key = key.split("_")[0]
        except Exception:
            pass

        # For both standard and non-standard terms the key is used to call the corresponding function in the key_to_func_mapping dictionary
        if key in key_to_func_mapping:
            key_to_func_mapping[key](obj, *value)

    return obj


def create_pyfrag_object_from_dir(results_dir: str, **kwargs) -> PyFragResultsObject:
    """Creates a PyFragResultsObject from the results in a directory.
    This function provides a shortcut for creating a PyFragResultsObject from the results in a directory by processing and creating the PyFragResultsObject in one function.

    Args:
        results_dir (str): The path to the directory containing the PyFrag results files.
        **kwargs: Additional keyword arguments to pass to the `process_results_file` function. These are:
            trim_parameter (Optional[Union[str, float, int]]): The parameter to use for trimming. Defaults to none.
            trim_key (Optional[str]): The key to use for reading the trim_parameter from the configuration file. Defaults to the "EnergyTotal" column.
            outlier_threshold: (Optional[float]): The threshold to use for removing outliers. If none is specified, the threshold from the configuration file is used. Defaults to None.

    Returns:
        PyFragResultsObject: A PyFragResultsObject containing the processed PyFrag results.

    This function reads the PyFrag input and output files from the given directory, processes the output file using the `process_results_file` function with any additional keyword arguments provided.
    Creates a PyFragResultsObject from the processed results and input data using the `create_pyfrag_object_from_processed_files` function.
    """

    input_file, output_file = get_pyfrag_files(results_dir)

    inputfile_data = read_inputfile(input_file)

    results_data = read_results_file(output_file)
    results_data = process_results_file(results_data, **kwargs)

    obj = create_pyfrag_object_from_processed_files(results_data, inputfile_data)

    return obj
