# PYTHON STANDARD LIBRARY IMPORTS ---------------------------------------------

import glob
import math
import os
import shutil
import sys


# THIRD PARTY MODULE IMPORTS --------------------------------------------------

import bs4
import pdf2image
from pdf2image.exceptions import PDFPageCountError


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
                   mode="floor", factor=1, wm=0, hm=0, background="white",
                   mpmax=30, quality=100, optimize=True):
    """
    Extracts images from moodle portfolio export and combines them to create
    a contact sheet.
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
                                    ".__tempcontactsheet"))
    os.makedirs(tempdir, exist_ok=True)
    # loop over all image sets and create contactsheet
    preprocessed_set = []
    for i, img_set in enumerate(image_sets):
        if len(img_set) == 1:
            preprocessed_set.append(img_set[0])
        else:
            log.prog("Preprocessing image set {0} / {1} ({2} %)".format(
                                i + 1,
                                len(image_sets),
                                math.floor(((i + 1) / len(image_sets)) * 100)))
            sfn = "tempsheet_{0}.jpg".format(str(i).zfill(
                                                    len(str(len(image_sets)))))
            sheetfile = sanitize(os.path.join(tempdir, sfn))
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
                                            background=background,
                                            mpmax=mpmax)
    sheet.convert("RGB").save(sanitize(outputfile),
                              quality=quality,
                              optimize=optimize)
    shutil.rmtree(tempdir)
    log.info("Contact sheet {0} successfully created!".format(
                                                 os.path.basename(outputfile)))
    return outputfile


def extract_pdfs(inputdir, outputfile, placeholder,
                 mode="floor", factor=1, wm=0, hm=0, background="white",
                 mpmax=30, quality=100, optimize=True):
    """
    Extracts PDFs from a moodle task export and combines them to create
    a contact sheet. PDFs will be converted to images first.
    """
    # collect image paths as sets per <div> tag in the html file
    log.write("--------------------------------------------------------------")
    log.info("Extracting PDFs for {0} ... ".format(inputdir))

    # get the first pdf file in the directory
    pdfs = []

    # contents = all sub folders
    contents = [os.path.join(inputdir, d)
                for d in os.listdir(inputdir)]

    # for every path in contents
    for p in contents:
        # check if path is a directory or pdf file and append to list
        if os.path.isdir(p):
            try:
                pdf = glob.glob(sanitize(os.path.join(p, "*.pdf")))[0]
                pdfs.append(pdf)
            except IndexError:
                log.warn("No PDF file found in directory! "
                         "Checking for sub dir...")
                try:
                    pdf = glob.glob(sanitize(os.path.join(
                                            p, os.listdir(p)[0], "*.pdf")))[0]
                    pdfs.append(pdf)
                except IndexError:
                    log.warn("No PDF file found in sub directory! Skipping...")
                    continue
        elif os.path.isfile(p) and p.endswith(".pdf"):
            pdfs.append(pdf)

    images = []
    for i, pdf in enumerate(pdfs):
        log.prog("Preprocessing PDF {0} / {1} ({2} %)".format(
                                    i + 1,
                                    len(pdfs),
                                    math.floor(((i + 1) / len(pdfs)) * 100)))
        # convert pdf to single images
        try:
            pdfpages = pdf2image.convert_from_path(pdf)
            if len(pdfpages) > 1:
                log.warn(("PDF {0} has more than one page! Only first page "
                          "will be used!").format(pdf[-40:]))
            images.append(pdfpages[0])
        except PDFPageCountError:
            log.warn("PDF file is corrupt! Skipping...")
            continue

    log.info("Creating contact sheet {0}...".format(outputfile))
    sheet = contactsheet.create_tiled_image(images,
                                            mode=mode,
                                            factor=factor,
                                            wm=wm,
                                            hm=hm,
                                            background=background,
                                            mpmax=mpmax)
    sheet.convert("RGB").save(sanitize(outputfile),
                              quality=quality,
                              optimize=optimize)
    log.info("Contact sheet {0} successfully created!".format(
                                                 os.path.basename(outputfile)))
    return outputfile


def extract_tiles(inputdir, outputfile, placeholder,
                  mode="floor", factor=1, wm=0, hm=0, background="white",
                  mpmax=30, quality=100, optimize=True):
    """
    Extracts images from moodle portfolio export and combines them to create
    a contact sheet.
    """
    # get the first html file in the directory
    try:
        filepath = glob.glob(sanitize(os.path.join(inputdir, "*.html")))[0]
    except IndexError:
        log.warn("No HTML file found in portfolio dir! Aborting...")
        return
    # init list for image paths
    tile_set = []
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
            tile = [img["src"] for img in div.find_all("img")][0]
            tile = verify_img(sanitize(os.path.join(inputdir, tile)),
                              placeholder)
            tile_set.append(tile)

    # specify output file
    log.info("Creating contact sheet {0}...".format(outputfile))

    sheet = contactsheet.create_tiled_image(tile_set,
                                            mode=mode,
                                            factor=factor,
                                            wm=wm,
                                            hm=hm,
                                            background=background,
                                            mpmax=mpmax)
    sheet.convert("RGB").save(sanitize(outputfile),
                              quality=quality,
                              optimize=optimize)
    log.info("Contact sheet {0} successfully created!".format(
                                                 os.path.basename(outputfile)))
    return outputfile
