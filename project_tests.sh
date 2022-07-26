#!/bin/bash
echo "Test suite"
set -e
. install.sh
source venv/bin/activate
coverage run -m pytest

echo "Integration testing of digest parsing"
python digestparser/parse.py 'tests/test_data/DIGEST 99999.docx'
