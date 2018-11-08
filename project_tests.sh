#!/bin/bash

echo "Test suite"
tox
. .tox/py35/bin/activate

echo "Coverage analysis"
pip install coveralls
COVERALLS_REPO_TOKEN=$(cat /etc/coveralls/tokens/digest-parser) coveralls

echo "Integration testing of digest parsing"
python digestparser/parse.py 'tests/test_data/DIGEST 99999.docx'
