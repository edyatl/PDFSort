#!/usr/bin/env python
import os
import pytest
from pdfsort import *


def test_list_files_recursive():
    pdf_files = list_files_recursive("tests/data")
    assert len(pdf_files) == 3
    assert os.path.abspath("tests/data/Binder1.pdf") in pdf_files
    assert os.path.abspath("tests/data/sub21/sub22/sub23/sub24/tst_highlights.pdf") in pdf_files
    assert os.path.abspath("tests/data/sub11/sub12/sub13/export_highlights.pdf") in pdf_files





