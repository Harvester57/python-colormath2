# -*- coding: utf-8 -*-
import itertools
import numpy as np
import unittest
from colormath2 import color_conversions
from colormath2.color_conversions import (
    GraphConversionManager,
    XYZ_to_RGB,
    HSV_to_RGB,
    RGB_to_XYZ,
)
from colormath2.color_exceptions import UndefinedConversionError
from colormath2.color_objects import (
    XYZColor,
    BaseRGBColor,
    HSVColor,
    HSLColor,
    AdobeRGBColor,
    BT2020Color,
    sRGBColor,
)


class GraphConversionManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.manager = GraphConversionManager()
        self.manager.add_type_conversion(XYZColor, BaseRGBColor, XYZ_to_RGB)
        self.manager.add_type_conversion(BaseRGBColor, HSVColor, HSV_to_RGB)

    def test_basic_path_generation(self):
        path = self.manager.get_conversion_path(XYZColor, HSVColor)
        self.assertEqual(path, [XYZ_to_RGB, HSV_to_RGB])

    def test_self_conversion(self):
        path = self.manager.get_conversion_path(XYZColor, XYZColor)
        self.assertEqual(path, [])

    def test_invalid_path_response(self):
        self.assertRaises(
            UndefinedConversionError,
            self.manager.get_conversion_path,
            XYZColor,
            HSLColor,
        )

    def test_conversion_manager_is_abstract(self):
        self.assertRaises(TypeError, color_conversions.ConversionManager)


class ColorConversionTestCase(unittest.TestCase):
    def test_conversion_validity(self):
        """
        Make sure that all existing paths between colors are valid.
        """

        conversion_manager = color_conversions._conversion_manager
        color_spaces = conversion_manager.registered_color_spaces

        for start_space, target_space in itertools.product(color_spaces, repeat=2):
            try:
                path = conversion_manager.get_conversion_path(start_space, target_space)
            except UndefinedConversionError:
                # If there is no path we don't really care (e.g., conversion to
                # SpectralColor).
                continue

            if start_space == target_space:
                # If start and end color space are equal, the conversion path should
                # be empty.
                self.assertEqual(path, [])
                continue
            else:
                # Otherwise check that all the conversion functions math up
                for a, b in zip(path[:-1], path[1:]):
                    self.assertEqual(a.target_type, b.start_type)

    def test_transfer_functions(self):
        """
        Tests the transfer functions of the various RGB colorspaces.
        """

        for colorspace in (AdobeRGBColor, BT2020Color, sRGBColor):
            for a in (0.0, 0.01, 0.18, 1.0):
                RGB = [a] * 3
                np.testing.assert_allclose(
                    XYZ_to_RGB(
                        RGB_to_XYZ(colorspace(*RGB)), colorspace
                    ).get_value_tuple(),
                    RGB,
                    rtol=1e-5,
                    atol=1e-5,
                )

    def test_negative_gamma_rgb_to_xyz_and_observer_xyz_to_rgb(self):
        xyz = RGB_to_XYZ(AdobeRGBColor(-0.1, 0.5, 0.5))
        self.assertGreater(xyz.xyz_y, 0.0)
        rgb_2 = XYZ_to_RGB(
            XYZColor(0.3, 0.2, 0.3, observer="2", illuminant="d50"), sRGBColor
        )
        rgb_10 = XYZ_to_RGB(
            XYZColor(0.3, 0.2, 0.3, observer="10", illuminant="d50"), sRGBColor
        )
        self.assertNotAlmostEqual(rgb_2.rgb_r, rgb_10.rgb_r, places=4)
