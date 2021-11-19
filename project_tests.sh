#!/bin/bash
echo "Test suite"
set -e
. mkvenv.sh
source venv/bin/activate
pip install pip wheel pytest coverage --upgrade
pip install -r requirements.txt
coverage run -m pytest

echo "Integration testing of digest parsing"
python digestparser/parse.py 'tests/test_data/DIGEST 99999.docx'
