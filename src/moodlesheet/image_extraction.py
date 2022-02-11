# PYTHON STANDARD LIBRARY IMPORTS ---------------------------------------------

import glob
import os
import shutil
import sys


# THIRD PARTY MODULE IMPORTS --------------------------------------------------

import bs4


# LOCAL MODULE IMPORTS --------------------------------------------------------

from moodlesheet.contactsheet import contactsheet


# LOGGING ---------------------------------------------------------------------

class Log(object):
    def __init__(self, out=sys.stdout, err=sys.stderr):
        self.out = out
        self.err = err

    def flush(self):
        self.out.flush()
        self.err.flush()

    def write(self, message):
        self.flush()
        self.out.write("%s\n" % message)
        self.out.flush()

    def prog(self, message):
        self.flush()
        self.out.write("[PROGRESS] %s\r" % message)
        self.out.flush()

    def info(self, message):
        self.write("[INFO] %s" % message)

    def warn(self, message):
        self.write("[WARNING] %s" % message)


log = Log()


# FUNCTION DEFINITIONS---------------------------------------------------------

def sanitize(path):
    """
    Return a sanitized absolute version of the input path.
    """
    return os.path.normpath(os.path.abspath(path))


def verify_img(filepath, placeholder):
    """
    Returns a valid image file or the specified placeholder file.
    """
    if os.path.isfile(filepath):
        return filepath
    
    if ".." in str(filepath):
        filepath = str(filepath).replace("..", ".")
    
    if os.path.isfile(filepath):
        return sanitize(filepath)
    
    log.warn(("Image file ...{0} not found! Inserting "
              "placeholder...").format(filepath[-45:]))
    return placeholder


def extract_images(inputdir, outputfile, placeholder,
                   mode="floor", factor=1, wm=0, hm=0, background="white"):
    """
    Extracts image file paths from moodle portfolio export.
    """
    # get the first html file in the directory
    try:
        filepath = glob.glob(sanitize(os.path.join(inputdir, "*.html")))[0]
    except IndexError:
        log.warn("No HTML file found in portfolio dir! Aborting...")
        return
    # init list for image paths
    image_sets = []
    # collect image paths as sets per <div> tag in the html file
    log.write("--------------------------------------------------------------")
    log.info("Extracting images for {0} ... ".format(inputdir))
    with open(filepath, "r") as f:
        # parse file using beautifulsoup
        soup = bs4.BeautifulSoup(f, "html.parser")
        # extract all divs from the file
        divs = soup.find_all("div")
        log.info("{0} entries found...".format(len(divs)))
        # loop over all divs
        for i, div in enumerate(divs):
            img_set = [img["src"] for img in div.find_all("img")]
            img_set = [verify_img(sanitize(os.path.join(inputdir, img)),
                                  placeholder) for img in img_set]
            image_sets.append(tuple(img_set))
    
    # create temporary directory
    tempdir = sanitize(os.path.join(inputdir,
                                    "__tempcontactsheet"))
    os.makedirs(tempdir, exist_ok=True)
    # loop over all image sets and create contactsheet
    preprocessed_set = []
    for i, img_set in enumerate(image_sets):
        if len(img_set) == 1:
            preprocessed_set.append(img_set[0])
        else:
            log.prog("Preprocessing image set {0} / {1}".format(
                                                           i, len(image_sets)))
            sfn = "tempsheet_{0}.jpg".format(str(i).zfill(
                                                    len(str(len(image_sets)))))
            sheetfile =  sanitize(os.path.join(tempdir, sfn))
            sheet = contactsheet.create_tiled_image(img_set,
                                                    mode=mode,
                                                    factor=factor,
                                                    wm=wm,
                                                    hm=hm,
                                                    background=background)
            sheet.convert("RGB").save(sheetfile)
            preprocessed_set.append(sheetfile)
    # specify output file
    log.info("Creating contact sheet {0}...".format(outputfile))
    sheet = contactsheet.create_tiled_image(preprocessed_set,
                                            mode=mode,
                                            factor=factor,
                                            wm=wm,
                                            hm=hm,
                                            background=background)
    sheet.convert("RGB").save(sanitize(outputfile))
    shutil.rmtree(tempdir)
    log.info("Contact sheet successfully created!")
    return outputfile
