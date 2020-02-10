from unittest import TestCase

import numpy as np

import decoder


class TestDecoder(TestCase):
    def test_beam_search(self):
        alphabet = 'ab'
        probabilities = np.array([[0.4, 0, 0.6], [0.4, 0, 0.6]])
        expected = 'a'
        bs_decoder = decoder.Decoder()
        actual = bs_decoder.beam_search(probabilities, alphabet)
        self.assertEqual(actual, expected)
