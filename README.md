# Compiling B322 moodle image galleries to contact sheet images

## About

This tool can create contact sheet images from moodle portfolio exports. It
uses `beautifulsoup4` for parsing the HTML files and extracting all image file
paths per `<div>`.
So if a participant has uploaded multiple images, they will stay together in
the final contact sheet.

After all image file paths have been extracted, `pillow` is used to create a
contact sheet of all the images. Like before, if a participant has uploaded
multiple images, the will be placed next to each other.

## Installation & Usage

## 1. Clone the repository into a directory of your choice

First off, clone or download this repository and unzip it (if needed) into a
working directory of your choice. For the purpose of this guide, I will use
`C:\source\repos\moodlesheet`.

## 2. Install the `moodlesheet` module and its dependencies

While inside the repository directory (for me it's
`C:\source\repos\moodlesheet`), call
```
pip install -e .
```

## 3. Export the moodle gallery as a portfolio (HTML with attachments)

Eport the moodle gallery as a portfolio (HTML with attachments). You should get
a `portfolio-export.zip` file. Unzip this into a new directory inside the
`input` directory. Your folder structure should then be something like this:
```
moodlesheet/
├─ input/
│  ├─ portfolio-export/
│  │  ├─ site_files
│  │  ├─ Portfolio-full.html (or similar name)
```

## 4. Run the script

With the repository directory as current working directory, run
```
python makesheets.py
```

Alternatively, have a look into `makesheets.py` and customize it to your needs.

## Licensing & References

- Original code is licensed under the MIT License.
- The `contactsheet` module is a modified version of contactsheet by Paul Butcher. This code is licensed under the MIT License found under `licenses/contactsheet`.