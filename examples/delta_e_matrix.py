# -*- coding: utf-8 -*-
"""
For a massive matrix of colors and color labels you can download
the follow two files

# http://lyst-classifiers.s3.amazonaws.com/color/lab-colors.pk
# http://lyst-classifiers.s3.amazonaws.com/color/lab-matrix.pk

lab-colors is a cPickled list of color names and lab-matrix is a
cPickled (n,3) numpy array LAB values such that row q maps to
index q in the lab color list
"""

import os
import csv
import bz2

import numpy as np

# Does some sys.path manipulation so we can run examples in-place.
# noinspection PyUnresolvedReferences
import example_config  # noqa

from colormath2.color_diff_matrix import delta_e_cie2000
from colormath2.color_objects import LabColor


# load list of 1000 random colors from the XKCD color chart
matrix_path = os.path.join(os.path.dirname(__file__), "lab_matrix.csv.bz2")
with bz2.open(matrix_path, mode="rt", encoding="utf-8") as matrix_file:
    reader = csv.DictReader(matrix_file)
    lab_matrix = np.array([list(map(float, row.values())) for row in reader])

color = LabColor(lab_l=69.34, lab_a=-0.88, lab_b=-52.57)
lab_color_vector = np.array([color.lab_l, color.lab_a, color.lab_b])
delta = delta_e_cie2000(lab_color_vector, lab_matrix)

print("%s is closest to %s" % (color, lab_matrix[np.argmin(delta)]))
