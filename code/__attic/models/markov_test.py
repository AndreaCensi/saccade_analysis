import unittest
from unittest import TestCase
import numpy
from markov import Markov


class TestMarkov(TestCase):
    def test_valid(self):
        valid = [
            [[0, 1], [1, 0]],
            [[1, 0], [0, 1]],
            [[0.5, 0], [0.5, 1]]
        ]
        
        for P in valid:
            P = numpy.array(P)
            Markov(P)

    def test_invalid(self):
        invalid = [
            [[0.5, 0.5], [0, 1]]
        ]
        
        for P in invalid:
            P = numpy.array(P)
            self.assertRaises(AssertionError, Markov, P)
