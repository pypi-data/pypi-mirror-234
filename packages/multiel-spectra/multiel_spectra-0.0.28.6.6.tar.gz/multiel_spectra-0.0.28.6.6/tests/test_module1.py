# import unittest

# from multiel_spectra.multiel_spectra import Number


# class TestSimple(unittest.TestCase):

#     def test_add(self):
#         self.assertEqual((Number(5) + Number(6)).value, 11)


# if __name__ == '__main__':
#     unittest.main()
import unittest
import src.multiel_spectra as ms
import pandas as pd
import scipy 
import numpy as np 
import torch
import skbeam 
from skbeam.core.constants import XrfElement
from src.multiel_spectra import *
# from src.multiel_spectra import detector_eff
class TestYourPackage(unittest.TestCase):

    def test_primary_gen(self):
        print("Running test_primary_gen")
        # Define your expected output
        # expected_prim = np.zeros(580)  # Define the expected value for Prim_s
        # expected_brems = np.zeros(580)  # Define the expected value for bPrim_s

        # Call the function being tested
        Prim, brems = ms.Primary_gen(30, 46, 0.1, "casim", "nist", 1, 9, "Mo", [('Be', 0.127), ('Air', 10)])
        # Perform assertions to check the output
        # np.testing.assert_array_equal(Prim[0], expected_prim)
        # np.testing.assert_array_equal(brems[0], expected_brems)
        # self.assertIsInstance(Prim, (list, np.ndarray))
        # self.assertIsInstance(brems, (list, np.ndarray))

        # Check the shapes of Prim and brems
        # self.assertEqual(np.shape(Prim), (2, 580))
        # self.assertEqual(np.shape(brems), (2, 580))
        # Get the air density from the returned values
        # air_density = ms.air_density

        # Print the air density
        # print("Air density:", air_density)
        # print(ms.Narea_t(torch.tensor(np.full(300, 0.78))))
        # print(XrfElement(23).emission_line.all)
        # print(x_c[:10], y_c[:10])
        # print(ms.detector_eff(np.random.random(20), np.arange(3,23, 1)))
        # print(gaussian(np.random.random(20), 2, 2, 2))
        # print(eff_inter)
        print(spectra_gen(np.array([34,15,3]), Prim, brems, s_counts = 30000, escape = True, sum = True, decal = True, char_r = 15, brem_r = 5,noise_f = 1000, prop = "" ))


if __name__ == '__main__':
    unittest.main()
