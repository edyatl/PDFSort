#!/usr/bin/env python3
"""
    Developed by @edyatl <edyatl@yandex.ru> February 2023
    https://github.com/edyatl

"""
import os
import glob
from pypdf import PdfReader, PdfWriter

import sys
import getopt

__version__ = '0.1.0'

input_dir: str = os.path.abspath("./")
output_dir: str = os.path.join(input_dir, os.path.basename(input_dir) + "-PDFs")

PaperSizes = {  # add new: ensure that first number is <= second number
    "A0": [2384, 3370],
    "A1": [1684, 2384],
    "A2": [1190, 1684],
    "A3": [842, 1190],
    "A4": [595, 842],
    "A5": [420, 595],
    "A6": [298, 420],
    "A7": [210, 298],
    "A8": [148, 210],
    "B0": [2835, 4008],
    "B1": [2004, 2835],
    "B2": [1417, 2004],
    "B3": [1001, 1417],
    "B4": [709, 1001],
    "B5": [499, 709],
    "B6": [354, 499],
    "B7": [249, 354],
    "B8": [176, 249],
    "B9": [125, 176],
    "B10": [88, 125],
    "C2": [578, 1837],
    "C3": [578, 919],
    "C4": [649, 919],
    "C5": [459, 649],
    "C6": [323, 459],
    "Invoice": [396, 612],
    "Executive": [522, 756],
    "Letter": [612, 792],
    "Legal": [612, 1008],
    "Ledger": [792, 1224],
    "A4х3": [842, 1785],
    "A4х4": [842, 2383],
    "A4х5": [842, 2978],
    "A4х6": [842, 3573],
    "A4х7": [842, 4168],
    "A4х8": [842, 4766],
    "A4х9": [842, 5361],
    "A3х3": [1190, 2526],
    "A3х4": [1190, 3371],
    "A3х5": [1190, 4213],
    "A3х6": [1190, 5055],
    "A3х7": [1190, 5897],
    "A2х3": [1684, 3573],
    "A2х4": [1684, 4766],
    "A2х5": [1684, 5956],
    "A1х3": [2384, 5055],
    "A1х3": [2384, 6742],
    "A0х2": [3370, 4768],
    "A0х3": [3370, 7152],
}

def list_files_recursive(dirpath: str) -> list:
    """
    Recursively get all PDF filenames with full path from a given directory.

    :param dirpath: str
        The directory to start find PDF files recursively with all nested subdirectories.
    :return: list
        Returns a list of PDF filenames with full paths.
    """
    global input_dir
    global output_dir
    input_dir = os.path.abspath(dirpath)
    output_dir = os.path.join(input_dir, os.path.basename(input_dir) + "-PDFs")
    return glob.glob(
        os.path.join(os.path.abspath(dirpath), "**", "*.[pP][dD][fF]"), recursive=True
    )

def collect_pdf_content(file_paths: list) -> list:
    """
    Collect into the Reader content of several pdf files.

    :param file_paths: list
        A list of PDF filenames with full paths.
    :return: list
        Returns the list of pages from all PDF files received from `file_paths` param.
    """
    all_pages = []
    for file_path in file_paths:
        try:
            reader = PdfReader(file_path)
            all_pages.extend(reader.pages)
        except FileNotFoundError as err:
            print(f"Error: {err}\nFile ignored.")
    return all_pages

def find_fmt(iwidth: float, iheight: float, orient: bool = True) -> str:
    """
    Determine the page format from the `PaperSizes` dictionary, 
    based on the given width and height.

    :param iwidth: float
        Input width.
    :param iheight: float
        Input height.
    :param orient: bool, optional
        Determine the paper orientation (default is True).
    :return: str
        Returns the standard page format or the approximately closest format.
    """
    width: int = int(round(iwidth, 0))
    height: int = int(round(iheight, 0))

    w1, h1 = (width, height) if iwidth <= iheight else (height, width)

    str_width, str_height = str(w1), str(h1)

    distances = {
        (abs(w1 - s[0]) + abs(h1 - s[1])): key for key, s in PaperSizes.items()
    }
    closest_distance = min(distances.keys())
    paper_size_key = distances[closest_distance]

    if iwidth <= iheight:
        paper_orientation = paper_size_key + "-P" if orient else paper_size_key
        paper_size_str = (
            f"{PaperSizes[paper_size_key][0]}x{PaperSizes[paper_size_key][1]}"
        )
    else:
        paper_orientation = paper_size_key + "-L" if orient else paper_size_key
        paper_size_str = (
            f"{PaperSizes[paper_size_key][1]}x{PaperSizes[paper_size_key][0]}"
        )

    if closest_distance >= 0 and closest_distance <= 2:
        return paper_orientation

    return f"{str_width}x{str_height} ~{paper_orientation}({paper_size_str})"

def get_format_info(pages: list) -> dict:
    """
    Collect information of the total number of pages for each format into a dict.

    :param pages: list
        A list of PDF pages.
    :return: dict
        Returns the dictionary where page format as the key and 
        their amount as the value.
    """
    format_info = {}
    for pg in pages:
        fmt = find_fmt(pg.mediabox.width, pg.mediabox.height, False)
        if fmt in format_info:
            format_info[fmt] += 1
        else:
            format_info[fmt] = 1
    return format_info

def draw_format_info_tab(format_info: dict):
    """
    Draws a table with pages formats and their amount from a given dictionary.

    :param format_info: dict
        A dictionary where page format as a key and their amount as a value.
    """
    print("{:>27} {:>9}\n{}  --------".format("Format", "Count", ("-" * 27)))
    for fmt, cnt in sorted(format_info.items()):
        print(f"{fmt:>27} {cnt:>9}")

def mk_output_dir(dirpath: str):
    """
    Makes output directory if it doesn't exists.

    :param dirpath: str
        Output directory name with full path.
    """
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

def subwrite_limit_fmt_file(
    fmt: str, pages: list, start: int, stop: int, i: int, meta: dict
):
    """
    Writes a PDF file with pages of only one size (format) for a group of files,
    numbered with indexes and containing a limited number of pages.
    Subfunction of write_fmt_file()

    :param fmt: str
        A page format as string value.
    :param pages: list
        A list of PDF pages.
    :param start: int
        The starting index of the page list slice.
    :param stop: int
        The ending index of the page list slice.
    :param i: int
        The increment count of the current outer iteration to add an index to the filename.
    :param meta: dict
        Dictionary with metadata for the output PDF file.
    """
    subwriter = PdfWriter()
    for wpg in pages[start:stop]:
        subwriter.add_page(wpg)

    subwriter.add_metadata(meta)

    mk_output_dir(output_dir)
    dirname = os.path.basename(input_dir)

    # Save the new PDF to a file with index
    with open(os.path.join(output_dir, f"{dirname}_{fmt}_pdf-{i}.pdf"), "wb") as f:
        subwriter.write(f)
    subwriter.close()

def write_fmt_file(fmt: str, pages: list, limit: int = 0):
    """
    Writes PDF files with pages of only one size (format) or,
    if the `limit` parameter is specified, calls the subwrite_limit_fmt_file()
    subfunction to write files with indexes splitted by the page number limit.

    :param fmt: str
        A page format as string value.
    :param pages: list
        A list of PDF pages.
    :param limit: int, optional
        The maximum allowed number of pages per one output file.
    """
    writer = PdfWriter()
    for pg in pages:
        if find_fmt(pg.mediabox.width, pg.mediabox.height, False) == fmt:
            writer.add_page(pg)

    # Add the metadata
    metadata = {
        "/Creator": "PDFSort",
        "/Producer": "PDFSort",
    }
    writer.add_metadata(metadata)

    if limit > 0 and limit < len(writer.pages):
        np: int = len(writer.pages)
        fnum: int = np // limit + 1
        start: int = 0
        stop: int = limit
        for i in range(fnum):
            subwrite_limit_fmt_file(
                fmt, writer.pages, start, stop if stop <= np else np, i, metadata
            )
            start += limit
            stop += limit
    else:
        mk_output_dir(output_dir)
        dirname = os.path.basename(input_dir)

        # Save the new PDF to a file
        with open(os.path.join(output_dir, f"{dirname}_{fmt}_pdf.pdf"), "wb") as f:
            writer.write(f)
    writer.close()

def usage():
    """Show usage help screen and exit"""
    cli_name = os.path.basename(sys.argv[0])
    print(f'''
    PDFSort is a Python application that processes PDF files in a given directory. 
    It recursively retrieves all PDF files from the directory and its subdirectories, 
    determines the page sizes (formats), calculates the number of each format, 
    and draws a table with the totals. 
    It can also write new PDF files, each of which will have pages of only one size.

    USAGE: 
        {cli_name} [options] [<DIRECTORY>]

    Arguments:
        DIRECTORY Provide directory path as argument or leave blank to use current dir.

    Options:
        -h, --help      Shows this help message and exit
        -l, --limit     Adds to write option limit of pages number per a file
        -t, --table     Draw a table with pages formats and their amount
        -w, --write     Write PDF files with pages of only one size to output dir
        -v, --version   Shows current version of the program and exit
    ''')

def main():
    if len(sys.argv) > 1:
        try:
            # Parse the command line options and arguments
            opts, args = getopt.gnu_getopt(
                sys.argv[1:], "hl:twv", ["help", "limit=", "table", "write", "version"]
            )
        except getopt.GetoptError as err:
            # If there's an error, print the error message, help and exit
            print(err)  # will print something like "option -x not recognized"
            usage()
            sys.exit(2)

        if len(args) < 1:
            input_dir = os.path.abspath("./")
        else:
            input_dir = os.path.abspath(args[0])

        limit: int = 0
        write_flg: bool = False
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage()
                sys.exit()
            elif opt in ("-l", "--limit"):
                limit = int(arg) if arg.isdigit() else 0
            elif opt in ("-t", "--table"):
                draw_format_info_tab(
                    get_format_info(collect_pdf_content(list_files_recursive(input_dir)))
                )
            elif opt in ("-w", "--write"):
                write_flg = True
            elif opt in ("-v", "--version"):
                print('PDFSort version: %s' % __version__)
                sys.exit()
            else:
                # If an unknown option is passed, raise an error
                assert False, "Unhandled option"

        if write_flg:
            for fmt in get_format_info(collect_pdf_content(list_files_recursive(input_dir))):
                write_fmt_file(
                    fmt, collect_pdf_content(list_files_recursive(input_dir)), limit if limit else 0
                )

if __name__ == "__main__":
    main()
