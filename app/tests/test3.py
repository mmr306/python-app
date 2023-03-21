import sys
import os 
sys.path.append('./')
from app import TrailProcessing

def test_parse_multiple(tmpdir):
    file = tmpdir.join('output.csv')
    outputfile = open(r'./tests/test-data/outputtest.csv', 'r')
    TrailProcessing.parse_multiple("./tests/test-data", file.strpath)  # or use str(file)
    assert file.read() == outputfile.read()

