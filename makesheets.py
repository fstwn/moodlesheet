# PYTHON STANDARD LIBRARY IMPORTS ---------------------------------------------

import os


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

    # get all portfolio directories inside input dir
    portfolios = [os.path.join(INPUTDIR, d) for d in os.listdir(INPUTDIR)
                  if os.path.isdir(os.path.join(INPUTDIR, d))]
    
    # declare output directory
    OUTPUT_DIR = sanitize(os.path.join(HERE, "output"))

    # loop over all portfolios an extract images into contact sheet
    for p in portfolios:
        fn = os.path.basename(os.path.normpath(p)) + ".jpg"
        outfile = os.path.join(OUTPUT_DIR, fn)
        extract_images(p, outfile, PLACEHOLDER)
