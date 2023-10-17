from animal_lib3 import Cat, Dog
import unittest

class TestAnimal(unittest.TestCase):
    def test_cat_sound(self):
        self.assertEqual(Cat().sound(), "Meow")

    def test_dog_sound(self):
        self.assertEqual(Dog().sound(), "Woof")

if __name__ == '__main__':
    unittest.main()
