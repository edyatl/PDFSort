## PDFSort


>Developed by [@edyatl](https://github.com/edyatl) February 2023 <edyatl@yandex.ru>

PDFSort is a Python application that processes PDF files in a given directory. It recursively retrieves all PDF files from the directory and its subdirectories, determines the page sizes (formats), calculates the number of each format, and draws a table with the totals. It can also write new PDF files, each of which will have pages of only one size (format).
### Usage

```
    USAGE: 
        pdfsort.py [options] [<DIRECTORY>]

    Arguments:
        DIRECTORY Provide directory path as argument or leave blank to use current dir.

    Options:
        -h, --help      Shows this help message and exit
        -l, --limit     Adds to write option limit of pages number per a file
        -t, --table     Draw a table with pages formats and their amount
        -w, --write     Write PDF files with pages of only one size to output dir
        -v, --version   Shows current version of the program and exit
```

### Functions

The PDFSort application provides the following functions:

1. `list_files_recursive()` - Recursively gets all PDF filenames with full path from a given directory.

1. `collect_pdf_content()` - Collects the content of several pdf files into a list of pages.

1. `find_fmt()` - Determines the page format based on the given width and height using the PaperSizes dictionary.

1. `get_format_info()` - Collects information of the total number of pages for each format into a dictionary.

1. `draw_format_info_tab()` - Draws a table with pages formats and their amount from a given dictionary.

1. `subwrite_limit_fmt_file()` - Writes a PDF file with pages of only one size (format) for a group of files, numbered with indexes and containing a limited number of pages. This is a subfunction of write_fmt_file.

1. `write_fmt_file()` - Writes PDF files with pages of only one size (format) or, if the limit parameter is specified, calls the subwrite_limit_fmt_file subfunction to write files with indexes split by the page number limit.

### Purpose

The main purpose of the PDFSort application is to allow users easily manage and organize their PDF files.

### Strengths

1. Recursive search: This app can search for PDF files in a directory and its subdirectories, making it easier for users to find all the relevant PDFs in one place.


1. Page format determination: This app can determine the format of each page of a PDF file, allowing users to easily categorize their PDFs by size.


1. Total count calculation: This app can calculate the total number of pages for each format, making it easy for users to see at a glance the distribution of formats across their PDFs.


1. Table visualization: This app can draw a table that visualizes the format information, making it easy for users to understand the data.


1. Output file writing: This app can write new PDF files with pages of only one format, making it easier for users to sort and organize their PDFs.

### Weaknesses

1. No error handling: The function signatures and docstrings don't mention any error handling, which means that the app may not be robust in the face of unexpected errors or input.


1. Limited customization: The functions only provide basic functionality, which may not be enough for users who need more advanced features.


### Current view on possible future development

* Implementing a search function to allow users to quickly find specific PDF files based on certain criteria, such as file name or page format.

* Integrating the ability to merge multiple PDF files into one, with options for customizing the order of the pages and adding or removing pages as needed.

* Implementing the ability to add or edit metadata, such as the title, author, and keywords, of PDF files.

* Integrating a security feature, such as password protection or encryption, to protect sensitive PDF files from unauthorized access.

* Optimizing the performance of the app to handle larger numbers of PDF files and larger file sizes.

### Contributing

There are a number of ways that you could contribute to this project, including fixing bugs, adding new features, and improving the overall performance of the application. If you're interested in getting involved, I'd love to hear from you!

Any ideas, patches, bug reports and so on are always welcome.
