# PYTHON STANDARD LIBRARY IMPORTS ---------------------------------------------

import os
import zipfile


# LOCAL MODULE IMPORTS --------------------------------------------------------

from moodlesheet import extract_images, sanitize


# LOCATION DEFINTIONS ---------------------------------------------------------

HERE = os.path.dirname(__file__)
"""str: Path to the root folder of this script."""

INPUTDIR = sanitize(os.path.join(HERE, "input"))
"""str: Path to the input data directory in the repository root."""

PLACEHOLDER = sanitize(os.path.join(HERE, "resources/placeholder.jpg"))
"""str: Path to the placeholder image for missing/corrupt images."""


# SCRIPT ----------------------------------------------------------------------

if __name__ == "__main__":

    # gather contents, unzip files if necessary
    contents = [os.path.join(INPUTDIR, d) for d in os.listdir(INPUTDIR)]
    portfolios = []
    for p in contents:
        # check if path is a directory or file
        if os.path.isdir(p):
            # add as portfoli dir if a directory
            portfolios.append(p)
        # else check if it's a .zip archive and extract the contents
        elif zipfile.is_zipfile(p):
            exdir = p[:-4]
            # only if folder with the same name does not exist yet
            if not os.path.isdir(exdir):
                os.makedirs(exdir)
                with zipfile.ZipFile(p, "r") as zipobj:
                    zipobj.extractall(exdir)
            portfolios.append(exdir)

    # declare output directory
    OUTPUT_DIR = sanitize(os.path.join(HERE, "output"))

    # loop over all portfolios an extract images into contact sheet
    for p in portfolios:
        fn = os.path.basename(os.path.normpath(p)) + ".jpg"
        outfile = os.path.join(OUTPUT_DIR, fn)
        extract_images(p, outfile, PLACEHOLDER)
