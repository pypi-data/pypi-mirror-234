from gwdc_python.files.identifiers import match_file_suffix


def data_file(file_path):
    """Checks to see if the given file path points to a HDF5 file

    Parameters
    ----------
    file_path : ~pathlib.Path
        File path to check

    Returns
    -------
    bool
        True if path points to a HDF5 file, False otherwise
    """
    return match_file_suffix(file_path, 'h5')
