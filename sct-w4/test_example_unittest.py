import unittest


class TestExampleUnitTests(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "results should be 6")

    def test_sum_example(self):
        self.assertEqual(2, 2, "2 should be equals to 2")

    def test_sum_example2(self):
        self.assertEqual(3, 3)


if __name__ == '__main__':
    unittest.main()
