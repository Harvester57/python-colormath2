# -*- coding: utf-8 -*-
"""
Tests for color difference (Delta E) equations.
"""

import unittest

from colormath2.color_objects import XYZColor


# noinspection PyPep8Naming
class chromaticAdaptationTestCase(unittest.TestCase):
    def setUp(self):
        self.color = XYZColor(0.5, 0.4, 0.1, illuminant="C")

    def test_adaptation_c_to_d65(self):
        self.color.apply_adaptation(target_illuminant="D65")
        self.assertIs(type(self.color.xyz_x), float)
        self.assertIs(type(self.color.xyz_y), float)
        self.assertIs(type(self.color.xyz_z), float)
        self.assertAlmostEqual(
            self.color.xyz_x, 0.491, 3, "C to D65 adaptation failed: X coord"
        )
        self.assertAlmostEqual(
            self.color.xyz_y, 0.400, 3, "C to D65 adaptation failed: Y coord"
        )
        self.assertAlmostEqual(
            self.color.xyz_z, 0.093, 3, "C to D65 adaptation failed: Z coord"
        )
        self.assertEqual(
            self.color.illuminant,
            "d65",
            "C to D65 adaptation failed: Illuminant transfer",
        )

    def test_invalid_observer_and_illuminant_exceptions(self):
        from colormath2.chromatic_adaptation import apply_chromatic_adaptation
        from colormath2.color_exceptions import (
            InvalidIlluminantError,
            InvalidObserverError,
        )

        with self.assertRaises(InvalidObserverError) as ctx:
            XYZColor(0.5, 0.4, 0.1, observer="99")
        self.assertIn("99", str(ctx.exception))

        with self.assertRaises(InvalidObserverError):
            apply_chromatic_adaptation(0.5, 0.4, 0.1, "c", "d65", observer="99")

        with self.assertRaises(InvalidIlluminantError) as ctx_illum:
            apply_chromatic_adaptation(0.5, 0.4, 0.1, "invalid_illum", "d65")
        self.assertIn("invalid_illum", str(ctx_illum.exception))

        with self.assertRaises(InvalidIlluminantError):
            apply_chromatic_adaptation(0.5, 0.4, 0.1, None, "d65")

        with self.assertRaises(InvalidIlluminantError):
            apply_chromatic_adaptation(0.5, 0.4, 0.1, "c", None)

        with self.assertRaises(InvalidIlluminantError):
            self.color.set_illuminant(None)
