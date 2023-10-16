"""
This script defines the function list_all_python_imports()
"""

import os
import re
from typing import Dict, Tuple
import warnings


def list_all_python_imports(dir_path: str) -> Dict[str, Tuple[str]]:
    """Searches every python script in a given folder and lists all python modules imported
    within those scripts\n
    (see "Example Usage")\n
    Parameters
    ----------
    dir_path: str
        Folder in which to find the python scripts\n
    Notes
    -----
    Package import statements are only searched for in files ending with .py or .ipynb
    Lines starting with a hash (i.e. commented lines) are ignored
    Any line of a script on which no modules were found although the line contains
    the word "import" raises a warning\n
    Example Usage
    -------------
    >>> from pprint import pprint
    >>> import joes_giant_toolbox.convenience
    >>> imports_found_dict = joes_giant_toolbox.convenience.list_all_python_imports( os.getcwd() )
    >>> pprint(imports_found_dict)
    {
        '__init__.py': (),
        'ascii_density_histogram.py': ('typing', 'math'),
        'conjugate_prior_beta_binomial.py': (),
        'cosine_similarity.py': ('numpy',),
    }
    Returns
    -------
    Dict[str, Tuple[str]]
        {file_name: tuple_of_module_names}
        Dictionary, with key=filename and values=(tuple containing list of modules found)
    """
    results_dict: Dict[str, Tuple[str]] = {
        filename: f"{dir_path}/{filename}"  # type: ignore
        for filename in os.listdir(dir_path)
        if filename != "list_all_python_imports.py"
        and (filename[-3:] == r".py" or filename[-6:] == r".ipynb")
    }

    for script in results_dict:
        with open(results_dict[script], "r", encoding="utf-8") as file:  # type: ignore
            temp_readlines = file.readlines()

        imports_found = []
        for line in temp_readlines:
            words_in_line = line.strip().split()
            if len(words_in_line) > 0:
                if words_in_line[0] == "#":
                    # ignore lines starting with a comment
                    pass
                elif words_in_line[0] == "import":
                    imports_found.append(words_in_line[1])
                elif words_in_line[0] == "from" and words_in_line[2] == "import":
                    imports_found.append(words_in_line[1])
                elif re.search(r"\bimport\b", line):
                    if ">>>" not in line:
                        warnings.warn(
                            f"possible import missed due to unexpected import pattern: {script} {line}"  # pylint: disable=line-too-long
                        )

        results_dict[script] = tuple(set(imports_found))  # type: ignore
        del imports_found, temp_readlines

    return results_dict
