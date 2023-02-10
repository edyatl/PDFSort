#!/usr/bin/env python
import os
import pytest
from pdfsort import *

from pypdf._page import PageObject
from pypdf.generic import RectangleObject

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
    pages_data = [
        {
            "/CropBox": [0, 0, 595.32000000000005, 841.91999999999996],
            "/MediaBox": [0, 0, 595.32000000000005, 841.91999999999996],
        },
        {
            "/CropBox": [0, 0, 595.32000000000005, 841.91999999999996],
            "/MediaBox": [0, 0, 595.32000000000005, 841.91999999999996],
        },
    ]
    pages = []
    for page_data in pages_data:
        page = PageObject()
        page.mediabox = RectangleObject(page_data["/MediaBox"])
        page.cropbox = RectangleObject(page_data["/CropBox"])
        pages.append(page)
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
    assert find_fmt(842, 1785, False) == "A4х3"
    assert find_fmt(842, 2383, False) == "A4х4"
    assert find_fmt(842, 2978, False) == "A4х5"
    assert find_fmt(842, 3573, False) == "A4х6"
    assert find_fmt(842, 4168, False) == "A4х7"
    assert find_fmt(842, 4766, False) == "A4х8"
    assert find_fmt(842, 5361, False) == "A4х9"
    assert find_fmt(1190, 2526, False) == "A3х3"
    assert find_fmt(1190, 3371, False) == "A3х4"
    assert find_fmt(1190, 4213, False) == "A3х5"
    assert find_fmt(1190, 5055, False) == "A3х6"
    assert find_fmt(1190, 5897, False) == "A3х7"
    assert find_fmt(1684, 3573, False) == "A2х3"
    assert find_fmt(1684, 4766, False) == "A2х4"
    assert find_fmt(1684, 5956, False) == "A2х5"
    assert find_fmt(2384, 6742, False) == "A1х3"
    assert find_fmt(3370, 4768, False) == "A0х2"
    assert find_fmt(3370, 7152, False) == "A0х3"

def test_find_fmt_custom_sizes():
    # test for custom sizes
    assert find_fmt(600, 800) == "600x800 ~Letter-P(612x792)"
    assert find_fmt(620, 790) == "620x790 ~Letter-P(612x792)"
    assert find_fmt(820, 2380) == "820x2380 ~A4х4-P(842x2383)"
    assert find_fmt(1680, 2390) == "1680x2390 ~A1-P(1684x2384)"
    assert find_fmt(3360, 4760) == "3360x4760 ~A0х2-P(3370x4768)"

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
    assert find_fmt(842, 1785) == "A4х3-P"
    assert find_fmt(842, 2383) == "A4х4-P"
    assert find_fmt(842, 2978) == "A4х5-P"
    assert find_fmt(842, 3573) == "A4х6-P"
    assert find_fmt(842, 4168) == "A4х7-P"
    assert find_fmt(842, 4766) == "A4х8-P"
    assert find_fmt(842, 5361) == "A4х9-P"
    assert find_fmt(1190, 2526) == "A3х3-P"
    assert find_fmt(1190, 3371) == "A3х4-P"
    assert find_fmt(1190, 4213) == "A3х5-P"
    assert find_fmt(1190, 5055) == "A3х6-P"
    assert find_fmt(1190, 5897) == "A3х7-P"
    assert find_fmt(1684, 3573) == "A2х3-P"
    assert find_fmt(1684, 4766) == "A2х4-P"
    assert find_fmt(1684, 5956) == "A2х5-P"
    assert find_fmt(2384, 6742) == "A1х3-P"
    assert find_fmt(3370, 4768) == "A0х2-P"
    assert find_fmt(3370, 7152) == "A0х3-P"

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
    assert find_fmt(1785, 842) == "A4х3-L"
    assert find_fmt(2383, 842) == "A4х4-L"
    assert find_fmt(2978, 842) == "A4х5-L"
    assert find_fmt(3573, 842) == "A4х6-L"
    assert find_fmt(4168, 842) == "A4х7-L"
    assert find_fmt(4766, 842) == "A4х8-L"
    assert find_fmt(5361, 842) == "A4х9-L"
    assert find_fmt(2526, 1190) == "A3х3-L"
    assert find_fmt(3371, 1190) == "A3х4-L"
    assert find_fmt(4213, 1190) == "A3х5-L"
    assert find_fmt(5055, 1190) == "A3х6-L"
    assert find_fmt(5897, 1190) == "A3х7-L"
    assert find_fmt(3573, 1684) == "A2х3-L"
    assert find_fmt(4766, 1684) == "A2х4-L"
    assert find_fmt(5956, 1684) == "A2х5-L"
    assert find_fmt(6742, 2384) == "A1х3-L"
    assert find_fmt(4768, 3370) == "A0х2-L"
    assert find_fmt(7152, 3370) == "A0х3-L"
