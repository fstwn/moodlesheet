# PYTHON STANDARD LIBRARY IMPORTS ---------------------------------------------

from datetime import datetime
import os
import zipfile


# LOCAL MODULE IMPORTS --------------------------------------------------------

from moodlesheet import (extract_images,
                         extract_pdfs,
                         extract_tiles,
                         sanitize)


# LOCATION DEFINTIONS ---------------------------------------------------------

HERE = os.path.dirname(__file__)
"""str: Path to the root folder of this script."""

PLACEHOLDER = sanitize(os.path.join(HERE, "resources/placeholder.jpg"))
"""str: Path to the placeholder image for missing/corrupt images."""


# SCRIPT ----------------------------------------------------------------------

if __name__ == "__main__":
    # create timestamp for directory name
    timestamp = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    
    # declare output directory
    OUTPUT_DIR = sanitize(os.path.join(HERE, "output", timestamp))

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # settings
    mode = "average"
    factor = 1
    width_margin = 10
    height_margin = 10
    background = "white"
    mpmax = 32
    quality = 95
    optimize = True

    # PORTFOLIO CONTACT SHEETS ------------------------------------------------

    # declare input directory for portfolio exports
    INPUT_PORTFOLIO = sanitize(os.path.join(HERE, "input_portfolio"))

    # gather contents, unzip files if necessary
    contents = [os.path.join(INPUT_PORTFOLIO, d)
                for d in os.listdir(INPUT_PORTFOLIO)]
    portfolios = []
    for p in contents:
        # check if path is a directory or file
        if os.path.isdir(p):
            # add as portfolio dir if a directory
            portfolios.append(p)
        # else check if it's a .zip archive and extract the contents
        elif zipfile.is_zipfile(p):
            # remove .zip file ending from path
            exdir = p[:-4]
            # only if folder with the same name does not exist yet
            if not os.path.isdir(exdir):
                os.makedirs(exdir)
                with zipfile.ZipFile(p, "r") as zipobj:
                    zipobj.extractall(exdir)
            portfolios.append(exdir)

    # loop over all portfolios an extract images into contact sheet
    for p in portfolios:
        fn = os.path.basename(os.path.normpath(p)) + ".jpg"
        outfile = os.path.join(OUTPUT_DIR, fn)

        extract_images(p, outfile, PLACEHOLDER,
                       mode=mode,
                       factor=factor,
                       wm=width_margin,
                       hm=height_margin,
                       background=background,
                       mpmax=mpmax,
                       quality=quality,
                       optimize=optimize)

    # PDF CONTACT SHEET -------------------------------------------------------

    # declare input directory for images
    INPUT_PDF = sanitize(os.path.join(HERE, "input_pdf"))

    # gather contents, unzip files if necessary
    contents = [os.path.join(INPUT_PDF, d)
                for d in os.listdir(INPUT_PDF)]
    pdf_maindirs = []
    for p in contents:
        # check if path is a directory or file
        if os.path.isdir(p):
            # add as pdf task export dir to list
            pdf_maindirs.append(p)
        # else check if it's a .zip archive and extract the contents
        elif zipfile.is_zipfile(p):
            # remove .zip file ending from path
            exdir = p[:-4]
            # only if folder with the same name does not exist yet
            if not os.path.isdir(exdir):
                os.makedirs(exdir)
                with zipfile.ZipFile(p, "r") as zipobj:
                    zipobj.extractall(exdir)
            pdf_maindirs.append(exdir)

    # loop over all portfolios and extract images into contact sheet
    for p in pdf_maindirs:
        fn = os.path.basename(os.path.normpath(p)) + ".jpg"
        outfile = os.path.join(OUTPUT_DIR, fn)

        extract_pdfs(p, outfile, PLACEHOLDER,
                     mode=mode,
                     factor=factor,
                     wm=width_margin,
                     hm=height_margin,
                     background=background,
                     mpmax=mpmax,
                     quality=quality,
                     optimize=optimize)

    # PORTFOLIO TILES CONTACT SHEETS -----------------------------------------

    # declare input directory for portfolio exports
    INPUT_PORTFOLIO_TILES = sanitize(os.path.join(HERE, "input_tiles"))

    # gather contents, unzip files if necessary
    contents = [os.path.join(INPUT_PORTFOLIO_TILES, d)
                for d in os.listdir(INPUT_PORTFOLIO_TILES)]
    portfolios = []
    for p in contents:
        # check if path is a directory or file
        if os.path.isdir(p):
            # add as portfolio dir if a directory
            portfolios.append(p)
        # else check if it's a .zip archive and extract the contents
        elif zipfile.is_zipfile(p):
            # remove .zip file ending from path
            exdir = p[:-4]
            # only if folder with the same name does not exist yet
            if not os.path.isdir(exdir):
                os.makedirs(exdir)
                with zipfile.ZipFile(p, "r") as zipobj:
                    zipobj.extractall(exdir)
            portfolios.append(exdir)

    # loop over all portfolios an extract images into contact sheet
    for p in portfolios:
        fn = os.path.basename(os.path.normpath(p)) + ".jpg"
        outfile = os.path.join(OUTPUT_DIR, fn)

        extract_tiles(p, outfile, PLACEHOLDER,
                      mode=mode,
                      factor=factor,
                      wm=width_margin,
                      hm=height_margin,
                      background=background,
                      mpmax=mpmax,
                      quality=quality,
                      optimize=optimize)
