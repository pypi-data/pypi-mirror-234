from sklearn.utils import Bunch
from pathlib import Path
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def test_add_all():
    # test function add_all
    assert add_all(d, a, b, c)==(12, 10, 13)
def test_add():
    (d, a, b, c) = (10, 12, 13, 15)
    assert add_all(d, a, b, c)==(22, 23, 25)
