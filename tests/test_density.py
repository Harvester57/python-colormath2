# -*- coding: utf-8 -*-
import unittest

from colormath2.color_objects import SpectralColor
from colormath2.density import ansi_density, auto_density
from colormath2.density_standards import ANSI_STATUS_T_RED


class DensityTestCase(unittest.TestCase):
    def test_auto_and_ansi_density(self):
        color = SpectralColor(
            spec_450nm=0.1,
            spec_550nm=0.2,
            spec_650nm=0.3,
        )
        d_auto = auto_density(color)
        d_red = ansi_density(color, ANSI_STATUS_T_RED)
        self.assertIsInstance(d_auto, float)
        self.assertIsInstance(d_red, float)
        self.assertAlmostEqual(color.calc_density(), d_auto)
        self.assertAlmostEqual(color.calc_density(ANSI_STATUS_T_RED), d_red)

    def test_zero_spectral_raises_value_error(self):
        empty = SpectralColor()
        self.assertRaises(ValueError, auto_density, empty)
        self.assertRaises(ValueError, ansi_density, empty, ANSI_STATUS_T_RED)
