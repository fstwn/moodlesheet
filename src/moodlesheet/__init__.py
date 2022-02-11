# PYTHON STANDARD LIBRARY IMPORTS ---------------------------------------------

from __future__ import (absolute_import, division, print_function)


# PACKAGE MODULE IMPORTS ------------------------------------------------------

from .__version__ import (__author__, __author_email__, __copyright__,
                          __description__, __license__, __title__, __url__,
                          __version__)

from moodlesheet.extract import (extract_images,
                                 extract_pdfs,
                                 sanitize)

__all__ = [
    "extract_images",
    "extract_pdfs",
    "sanitize",
    "__author__", "__author_email__", "__copyright__", "__description__",
    "__license__", "__title__", "__url__", "__version__",
]
