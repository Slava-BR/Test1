import unittest
from PhoneBook import PhoneBook

OBJ = PhoneBook(path_to_file='', file_name='')

class TestWordIsValidFunctionCase(unittest.TestCase):

    def test_correct_data1(self):
        self.assertEqual(OBJ.word_is_valid('Vyacheslav'), True)

    def test_correct_data2(self):
        self.assertEqual(OBJ.word_is_valid('Вячеслав'), True)

    def test_first_symbol_is_lowercase1(self):
        self.assertEqual(OBJ.word_is_valid('vyacheslav'), False)

    def test_first_symbol_is_lowercase2(self):
        self.assertEqual(OBJ.word_is_valid('вячеслав'), False)

    def test_different_letters1(self):
        self.assertEqual(OBJ.word_is_valid('Вяchesлав'), False)

    def test_different_letters2(self):
        self.assertEqual(OBJ.word_is_valid('Vyaчеслав'), False)

    def test_different_letters3(self):
        self.assertEqual(OBJ.word_is_valid('вяchesлав'), False)

    def test_different_letters4(self):
        self.assertEqual(OBJ.word_is_valid('vyaчеслав'), False)

    def test_max_len_True(self):
        self.assertEqual(OBJ.word_is_valid('Vaaaaaaaaaaaaaaaaaaa'), True)

    def test_max_len_False(self):
        self.assertEqual(OBJ.word_is_valid('Vaaaaaaaaaaaaaaaaaaaa'), False)


class TestPhoneIsValidFunctionCase(unittest.TestCase):
    def test_correct_data1(self):
        self.assertEqual(OBJ.phone_is_valid('+79108466979'), True)

    def test_correct_data2(self):
        self.assertEqual(OBJ.phone_is_valid('79108466979'), True)

    def test_correct_data3(self):
        self.assertEqual(OBJ.phone_is_valid('89108466979'), True)

    def test_correct_len_9(self):
        self.assertEqual(OBJ.phone_is_valid('+7910846697'), False)

    def test_correct_len_11(self):
        self.assertEqual(OBJ.phone_is_valid('+791084669793'), False)
