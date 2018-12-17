import fgo_mat_counter
import unittest
import os


class TestQPCounting(unittest.TestCase):
    def test1(self):
        expected = {'qp_gained': 9400, 'qp_total': 357256131,
                    'drops': [{'item': 'Manuscript (True)', 'x': 352, 'y': 7, 'score': '0.91605514'},
                              {'item': 'Manuscript (True)', 'x': 463, 'y': 7, 'score': '0.91863876'},
                              {'item': 'Manuscript (True)', 'x': 575, 'y': 7, 'score': '0.90524661'},
                              {'item': 'Manuscript (True)', 'x': 686, 'y': 7, 'score': '0.91897970'},
                              {'item': 'Manuscript (False)', 'x': 19, 'y': 121, 'score': '0.97181671'},
                              {'item': 'Manuscript (False)', 'x': 130, 'y': 121, 'score': '0.97235000'},
                              {'item': 'Manuscript (False)', 'x': 241, 'y': 121, 'score': '0.97120946'},
                              {'item': 'Manuscript (False)', 'x': 353, 'y': 121, 'score': '0.97239977'},
                              {'item': 'Manuscript (False)', 'x': 464, 'y': 121, 'score': '0.97294944'},
                              {'item': 'Manuscript (False)', 'x': 576, 'y': 121, 'score': '0.97055381'},
                              {'item': 'Manuscript (False)', 'x': 687, 'y': 121, 'score': '0.97198414'},
                              {'item': 'Manuscript (False)', 'x': 19, 'y': 236, 'score': '0.97227716'},
                              {'item': 'Manuscript (False)', 'x': 130, 'y': 236, 'score': '0.97235178'},
                              {'item': 'Lancer Piece', 'x': 131, 'y': 8, 'score': '0.89710170'},
                              {'item': 'Berserker Piece', 'x': 241, 'y': 9, 'score': '0.94229197'}]}

        test_image = os.path.join(os.getcwd(), 'test_data', 'test1.png')
        self.assertEqual(expected, fgo_mat_counter.run(test_image))


if __name__ == '__main__':
    unittest.main()
