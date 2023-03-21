import sys
import os 
sys.path.append('./')
from app import TrailProcessing

def test_get_middle():
    outputfile = r'./tests/test-data/outputtest.csv'
    tp = TrailProcessing(outputfile)
    dt = tp.get_middle()
    assert dt  == {'latitude': 47.609036, 'longitude': -122.333911, 'zoom': 11.932467410982264}