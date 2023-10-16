from typing import Tuple
import os


def get_pyfrag_files(pyfrag_dir: str) -> Tuple[str, str]:
    """Searches for pyfrag input files and pyfrag txt files in a given folder and returns a tuple containing the absolute path to the pyfrag input file and the pyfrag txt file

    Args:
        pyfrag_dir (Union[List[str], str]): The absolute path to the folder containing the pyfrag input files.

    Raises:
        FileNotFoundError: If the pyfrag input file or pyfrag txt file could not be found in the same folder.
        FileNotFoundError: If the returned list is empty.

    Returns:
        List[Tuple[str, str]]: A list of tuples containing the absolute path to the pyfrag input file and the pyfrag txt file.

    """
    if not os.path.isdir(pyfrag_dir):
        raise NotADirectoryError(f"{pyfrag_dir} is not a directory")

    files = os.listdir(pyfrag_dir)

    # Search for pyfrag input file and pyfrag txt file
    pyfrag_input_file = ""
    pyfrag_txt_file = ""
    for file in files:
        if file.endswith('.in'):
            pyfrag_input_file = os.path.join(pyfrag_dir, file)
        if file.startswith('pyfrag') and file.endswith('.txt'):
            pyfrag_txt_file = os.path.join(pyfrag_dir, file)

    # Check if both files were found
    if not (pyfrag_input_file and pyfrag_txt_file):
        raise FileNotFoundError(f"Could not find pyfrag input file or pyfrag txt file in {pyfrag_dir}")

    # Add the files to the list as a tuple
    return pyfrag_input_file, pyfrag_txt_file
