#!/usr/bin/env python
import os
import pytest
from pdfsort import *

from pypdf._page import PageObject
from pypdf.generic import RectangleObject

from unittest.mock import patch, mock_open, MagicMock
import unittest.mock

def set_pdf_pages(n: int = 2) -> list:
    p = {
            "/CropBox": [0, 0, 595.32000000000005, 841.91999999999996],
            "/MediaBox": [0, 0, 595.32000000000005, 841.91999999999996],
        }
    pages_data = []
    for i in range(n):
        pages_data.append(p)
    
    pages = []
    for page_data in pages_data:
        page = PageObject()
        page.mediabox = RectangleObject(page_data["/MediaBox"])
        page.cropbox = RectangleObject(page_data["/CropBox"])
        pages.append(page)
    return pages

def test_list_files_recursive():
    pdf_files = list_files_recursive("tests/data")
    assert len(pdf_files) == 3
    assert os.path.abspath("tests/data/Binder1.pdf") in pdf_files
    assert os.path.abspath("tests/data/sub21/sub22/sub23/sub24/tst_highlights.pdf") in pdf_files
    assert os.path.abspath("tests/data/sub11/sub12/sub13/export_highlights.pdf") in pdf_files


def test_collect_pdf_content():
    # Test case 1: Check if the function returns the correct number of pages
    pdf_pages = collect_pdf_content([os.path.abspath("tests/data/Binder1.pdf")])
    assert len(pdf_pages) == 8
    
    # Test case 2: Check if the function returns an empty list when no PDF files are passed
    pdf_pages = collect_pdf_content([])
    assert len(pdf_pages) == 0

    # Test case 3: Check if the function returns the correct number of pages for multiple PDF files
    pdf_pages = collect_pdf_content(
        [
            os.path.abspath("tests/data/Binder1.pdf"), 
            os.path.abspath("tests/data/sub21/sub22/sub23/sub24/tst_highlights.pdf"),
        ]
    )
    assert len(pdf_pages) == 8 + 1

    # Test case 4: Check if the function correctly handles non-existent PDF files
    pdf_pages = collect_pdf_content(
        [
            os.path.abspath("tests/data/Binder1.pdf"), 
            os.path.abspath("tests/data/NonExistent.pdf"),
        ]
    )
    assert len(pdf_pages) == 8

def test_get_format_info():
    pages = set_pdf_pages()
    formats_dict = get_format_info(pages)
    expected_dict = {"A4": 2}
    assert formats_dict == expected_dict, f"Expected {expected_dict}, but got {formats_dict}"
    

def test_find_fmt_standard_paper_sizes():
    # test for standard paper sizes
    assert find_fmt(2384, 3370, False) == "A0"
    assert find_fmt(1684, 2384, False) == "A1"
    assert find_fmt(1190, 1684, False) == "A2"
    assert find_fmt(842, 1190, False) == "A3"
    assert find_fmt(595, 842, False) == "A4"
    assert find_fmt(420, 595, False) == "A5"
    assert find_fmt(298, 420, False) == "A6"
    assert find_fmt(210, 298, False) == "A7"
    assert find_fmt(148, 210, False) == "A8"
    assert find_fmt(2835, 4008, False) == "B0"
    assert find_fmt(2004, 2835, False) == "B1"
    assert find_fmt(1417, 2004, False) == "B2"
    assert find_fmt(1001, 1417, False) == "B3"
    assert find_fmt(709, 1001, False) == "B4"
    assert find_fmt(499, 709, False) == "B5"
    assert find_fmt(354, 499, False) == "B6"
    assert find_fmt(249, 354, False) == "B7"
    assert find_fmt(176, 249, False) == "B8"
    assert find_fmt(125, 176, False) == "B9"
    assert find_fmt(88, 125, False) == "B10"
    assert find_fmt(578, 1837, False) == "C2"
    assert find_fmt(578, 919, False) == "C3"
    assert find_fmt(649, 919, False) == "C4"
    assert find_fmt(459, 649, False) == "C5"
    assert find_fmt(323, 459, False) == "C6"
    assert find_fmt(396, 612, False) == "Invoice"
    assert find_fmt(522, 756, False) == "Executive"
    assert find_fmt(612, 792, False) == "Letter"
    assert find_fmt(612, 1008, False) == "Legal"
    assert find_fmt(792, 1224, False) == "Ledger"
    assert find_fmt(842, 1785, False) == "A4??3"
    assert find_fmt(842, 2383, False) == "A4??4"
    assert find_fmt(842, 2978, False) == "A4??5"
    assert find_fmt(842, 3573, False) == "A4??6"
    assert find_fmt(842, 4168, False) == "A4??7"
    assert find_fmt(842, 4766, False) == "A4??8"
    assert find_fmt(842, 5361, False) == "A4??9"
    assert find_fmt(1190, 2526, False) == "A3??3"
    assert find_fmt(1190, 3371, False) == "A3??4"
    assert find_fmt(1190, 4213, False) == "A3??5"
    assert find_fmt(1190, 5055, False) == "A3??6"
    assert find_fmt(1190, 5897, False) == "A3??7"
    assert find_fmt(1684, 3573, False) == "A2??3"
    assert find_fmt(1684, 4766, False) == "A2??4"
    assert find_fmt(1684, 5956, False) == "A2??5"
    assert find_fmt(2384, 6742, False) == "A1??3"
    assert find_fmt(3370, 4768, False) == "A0??2"
    assert find_fmt(3370, 7152, False) == "A0??3"

def test_find_fmt_custom_sizes():
    # test for custom sizes
    assert find_fmt(600, 800) == "600x800 ~Letter-P(612x792)"
    assert find_fmt(620, 790) == "620x790 ~Letter-P(612x792)"
    assert find_fmt(820, 2380) == "820x2380 ~A4??4-P(842x2383)"
    assert find_fmt(1680, 2390) == "1680x2390 ~A1-P(1684x2384)"
    assert find_fmt(3360, 4760) == "3360x4760 ~A0??2-P(3370x4768)"

def test_find_fmt_paper_orientation():
    # test for paper orientation
    assert find_fmt(2384, 3370) == "A0-P"
    assert find_fmt(1684, 2384) == "A1-P"
    assert find_fmt(1190, 1684) == "A2-P"
    assert find_fmt(842, 1190) == "A3-P"
    assert find_fmt(595, 842) == "A4-P"
    assert find_fmt(420, 595) == "A5-P"
    assert find_fmt(298, 420) == "A6-P"
    assert find_fmt(210, 298) == "A7-P"
    assert find_fmt(148, 210) == "A8-P"
    assert find_fmt(2835, 4008) == "B0-P"
    assert find_fmt(2004, 2835) == "B1-P"
    assert find_fmt(1417, 2004) == "B2-P"
    assert find_fmt(1001, 1417) == "B3-P"
    assert find_fmt(709, 1001) == "B4-P"
    assert find_fmt(499, 709) == "B5-P"
    assert find_fmt(354, 499) == "B6-P"
    assert find_fmt(249, 354) == "B7-P"
    assert find_fmt(176, 249) == "B8-P"
    assert find_fmt(125, 176) == "B9-P"
    assert find_fmt(88, 125) == "B10-P"
    assert find_fmt(578, 1837) == "C2-P"
    assert find_fmt(578, 919) == "C3-P"
    assert find_fmt(649, 919) == "C4-P"
    assert find_fmt(459, 649) == "C5-P"
    assert find_fmt(323, 459) == "C6-P"
    assert find_fmt(396, 612) == "Invoice-P"
    assert find_fmt(522, 756) == "Executive-P"
    assert find_fmt(612, 792) == "Letter-P"
    assert find_fmt(612, 1008) == "Legal-P"
    assert find_fmt(792, 1224) == "Ledger-P"
    assert find_fmt(842, 1785) == "A4??3-P"
    assert find_fmt(842, 2383) == "A4??4-P"
    assert find_fmt(842, 2978) == "A4??5-P"
    assert find_fmt(842, 3573) == "A4??6-P"
    assert find_fmt(842, 4168) == "A4??7-P"
    assert find_fmt(842, 4766) == "A4??8-P"
    assert find_fmt(842, 5361) == "A4??9-P"
    assert find_fmt(1190, 2526) == "A3??3-P"
    assert find_fmt(1190, 3371) == "A3??4-P"
    assert find_fmt(1190, 4213) == "A3??5-P"
    assert find_fmt(1190, 5055) == "A3??6-P"
    assert find_fmt(1190, 5897) == "A3??7-P"
    assert find_fmt(1684, 3573) == "A2??3-P"
    assert find_fmt(1684, 4766) == "A2??4-P"
    assert find_fmt(1684, 5956) == "A2??5-P"
    assert find_fmt(2384, 6742) == "A1??3-P"
    assert find_fmt(3370, 4768) == "A0??2-P"
    assert find_fmt(3370, 7152) == "A0??3-P"

    assert find_fmt(3370, 2384) == "A0-L"
    assert find_fmt(2384, 1684) == "A1-L"
    assert find_fmt(1684, 1190) == "A2-L"
    assert find_fmt(1190, 842) == "A3-L"
    assert find_fmt(842, 595) == "A4-L"
    assert find_fmt(595, 420) == "A5-L"
    assert find_fmt(420, 298) == "A6-L"
    assert find_fmt(298, 210) == "A7-L"
    assert find_fmt(210, 148) == "A8-L"
    assert find_fmt(4008, 2835) == "B0-L"
    assert find_fmt(2835, 2004) == "B1-L"
    assert find_fmt(2004, 1417) == "B2-L"
    assert find_fmt(1417, 1001) == "B3-L"
    assert find_fmt(1001, 709) == "B4-L"
    assert find_fmt(709, 499) == "B5-L"
    assert find_fmt(499, 354) == "B6-L"
    assert find_fmt(354, 249) == "B7-L"
    assert find_fmt(249, 176) == "B8-L"
    assert find_fmt(176, 125) == "B9-L"
    assert find_fmt(125, 88) == "B10-L"
    assert find_fmt(1837, 578) == "C2-L"
    assert find_fmt(919, 578) == "C3-L"
    assert find_fmt(919, 649) == "C4-L"
    assert find_fmt(649, 459) == "C5-L"
    assert find_fmt(459, 323) == "C6-L"
    assert find_fmt(612, 396) == "Invoice-L"
    assert find_fmt(756, 522) == "Executive-L"
    assert find_fmt(792, 612) == "Letter-L"
    assert find_fmt(1008, 612) == "Legal-L"
    assert find_fmt(1224, 792) == "Ledger-L"
    assert find_fmt(1785, 842) == "A4??3-L"
    assert find_fmt(2383, 842) == "A4??4-L"
    assert find_fmt(2978, 842) == "A4??5-L"
    assert find_fmt(3573, 842) == "A4??6-L"
    assert find_fmt(4168, 842) == "A4??7-L"
    assert find_fmt(4766, 842) == "A4??8-L"
    assert find_fmt(5361, 842) == "A4??9-L"
    assert find_fmt(2526, 1190) == "A3??3-L"
    assert find_fmt(3371, 1190) == "A3??4-L"
    assert find_fmt(4213, 1190) == "A3??5-L"
    assert find_fmt(5055, 1190) == "A3??6-L"
    assert find_fmt(5897, 1190) == "A3??7-L"
    assert find_fmt(3573, 1684) == "A2??3-L"
    assert find_fmt(4766, 1684) == "A2??4-L"
    assert find_fmt(5956, 1684) == "A2??5-L"
    assert find_fmt(6742, 2384) == "A1??3-L"
    assert find_fmt(4768, 3370) == "A0??2-L"
    assert find_fmt(7152, 3370) == "A0??3-L"

@patch("builtins.print")
def test_draw_format_info_tab_empty_dict(mock_print):
    draw_format_info_tab({})
    mock_print.assert_not_called

@patch("builtins.print")
def test_draw_format_info_tab_single_entry(mock_print):
    draw_format_info_tab({"A4": 5})
    expected = "                     Format     Count\n"
    expected += "---------------------------  --------\n"
    expected += "                         A4         5"
    mock_print.assert_called_with(expected)

@patch("builtins.print")
def test_draw_format_info_tab_multiple_entries(mock_print):
    draw_format_info_tab({"A4": 5, "Letter": 10})
    expected = "                     Format     Count\n"
    expected += "---------------------------  --------\n"
    expected += "                         A4         5\n"
    expected += "                     Letter        10"
    mock_print.assert_called_with(expected)

@patch("builtins.print")
def test_draw_format_info_tab_sorted_order(mock_print):
    draw_format_info_tab({"Letter": 10, "A4": 5})
    expected = "                     Format     Count\n"
    expected += "---------------------------  --------\n"
    expected += "                         A4         5\n"
    expected += "                     Letter        10"
    mock_print.assert_called_with(expected)


def test_mk_output_dir():
    with unittest.mock.patch("os.path.exists") as mocked_exists, unittest.mock.patch(
        "os.makedirs"
    ) as mocked_mkdirs:
        # arrange
        mocked_exists.return_value = False

        # act
        mk_output_dir("/tmp/test_mk_output_dir")

        # assert
        mocked_exists.assert_called_once_with("/tmp/test_mk_output_dir")
        mocked_mkdirs.assert_called_once_with("/tmp/test_mk_output_dir")


def test_mk_output_dir_already_exists():
    with unittest.mock.patch("os.path.exists") as mocked_exists, unittest.mock.patch(
        "os.makedirs"
    ) as mocked_mkdirs:
        # arrange
        mocked_exists.return_value = True

        # act
        mk_output_dir("/tmp/test_mk_output_dir")

        # assert
        mocked_exists.assert_called_once_with("/tmp/test_mk_output_dir")
        mocked_mkdirs.assert_not_called()

@patch("pdfsort.mk_output_dir")
@patch("pdfsort.open", mock_open())
@patch("pdfsort.PdfWriter")
def test_write_fmt_file(mock_pdf_writer, mock_mk_output_dir):
    pages = set_pdf_pages()
    writer = mock_pdf_writer.return_value
    writer.pages = pages
    writer.add_metadata.return_value = None

    write_fmt_file("A4", pages, 0)

    mock_mk_output_dir.assert_called_once()
    writer.add_metadata.assert_called_once()
    writer.write.assert_called_once()
    writer.close.assert_called_once()

@patch("pdfsort.subwrite_limit_fmt_file")
@patch("pdfsort.PdfWriter")
def test_write_fmt_file_with_limit(mock_pdf_writer, mock_subwrite_limit_fmt_file):
    metadata = {
        "/Creator": "PDFSort",
        "/Producer": "PDFSort",
    }
    pages = set_pdf_pages(5)
    writer = mock_pdf_writer.return_value
    writer.pages = pages
    writer.add_metadata.return_value = None

    write_fmt_file("A4", pages, 2)

    mock_subwrite_limit_fmt_file.assert_called()
    mock_subwrite_limit_fmt_file.assert_called_with("A4", pages, 4, 5, 2, metadata)
    writer.close.assert_called_once()

@patch("pdfsort.subwrite_limit_fmt_file")
@patch("pdfsort.PdfWriter")
def test_write_fmt_file_with_limit_even(mock_pdf_writer, mock_subwrite_limit_fmt_file):
    metadata = {
        "/Creator": "PDFSort",
        "/Producer": "PDFSort",
    }
    pages = set_pdf_pages(4)
    writer = mock_pdf_writer.return_value
    writer.pages = pages
    writer.add_metadata.return_value = None

    write_fmt_file("A4", pages, 2)

    mock_subwrite_limit_fmt_file.assert_called()
    mock_subwrite_limit_fmt_file.assert_called_with("A4", pages, 2, 4, 1, metadata)
    writer.close.assert_called_once()

@patch("pdfsort.mk_output_dir")
@patch("pdfsort.open", mock_open())
@patch("pdfsort.PdfWriter")
def test_subwrite_limit_fmt_file(mock_pdf_writer, mock_mk_output_dir):
    pages = set_pdf_pages(5)
    subwriter = mock_pdf_writer.return_value
    subwriter.add_page.return_value = None
    subwriter.add_metadata.return_value = None

    subwrite_limit_fmt_file("A4", pages, 0, 2, 0, {})

    mock_mk_output_dir.assert_called_once()
    subwriter.add_page.assert_called()
    subwriter.add_metadata.assert_called_once()
    subwriter.write.assert_called_once()
    subwriter.close.assert_called_once()
