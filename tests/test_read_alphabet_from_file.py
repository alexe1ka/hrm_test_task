from unittest import TestCase
import utils

class TestRead_alphabet_from_file(TestCase):
    def test_read_alphabet_from_file(self):
        filepath = "/home/alexe1ka/PycharmProjects/hrm_test_task/test1/alphabet.txt"
        expected_data ="ab"
        read_data = utils.read_alphabet_from_file(filepath)
        assert expected_data == read_data
