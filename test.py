import unittest
import os
import tempfile

import frontend
import fgo_mat_counter


DEBUG = False
LABEL = True

def remove_scores(dictionary):
    for drop in dictionary['drops']:
        drop.pop('score')

    return dictionary

def remove_qp_drops(dictionary):
    new_drops = []
    for drop in dictionary['drops']:
        if drop['id'] != 'qp.png':
            new_drops.append(drop)

    dictionary['drops'] = new_drops
    return dictionary


def remove_location(dictionary):
    for drop in dictionary['drops']:
        drop.pop('x')
        drop.pop('y')
    return dictionary

def remove_scroll_position(dictionary):
    dictionary.pop('scroll_position', None)
    return dictionary


class TestEvents(unittest.TestCase):
    def test_da_vinci(self):
        expected = {'qp_gained': 9400, 'qp_total': 357256131, 'drops': [
            {'id': 'Manuscript (True).png', 'x': 352, 'y': 7, 'score': '0.91605514', 'stack': 3},
            {'id': 'Manuscript (True).png', 'x': 463, 'y': 7, 'score': '0.91864091', 'stack': 3},
            {'id': 'Manuscript (True).png', 'x': 575, 'y': 7, 'score': '0.90524661', 'stack': 3},
            {'id': 'Manuscript (True).png', 'x': 686, 'y': 7, 'score': '0.91897970', 'stack': 3},
            {'id': 'Manuscript (False).png', 'x': 19, 'y': 121, 'score': '0.97181606', 'stack': 3},
            {'id': 'Manuscript (False).png', 'x': 130, 'y': 121, 'score': '0.97234934', 'stack': 3},
            {'id': 'Manuscript (False).png', 'x': 241, 'y': 121, 'score': '0.97120785', 'stack': 3},
            {'id': 'Manuscript (False).png', 'x': 353, 'y': 121, 'score': '0.97240418', 'stack': 3},
            {'id': 'Manuscript (False).png', 'x': 464, 'y': 121, 'score': '0.97294944', 'stack': 3},
            {'id': 'Manuscript (False).png', 'x': 576, 'y': 121, 'score': '0.97055381', 'stack': 3},
            {'id': 'Manuscript (False).png', 'x': 687, 'y': 121, 'score': '0.97198474', 'stack': 10},
            {'id': 'Manuscript (False).png', 'x': 19, 'y': 236, 'score': '0.97227716', 'stack': 3},
            {'id': 'Manuscript (False).png', 'x': 130, 'y': 236, 'score': '0.97235178', 'stack': 3},
            {'id': 'Lancer Piece.png', 'x': 131, 'y': 8, 'score': '0.89710170'},
            {'id': 'Berserker Piece.png', 'x': 241, 'y': 9, 'score': '0.94229006'}
        ]}

        test_image = os.path.join(os.getcwd(), 'test_data', 'da_vinci.png')
        self.assertEqual(remove_scores(remove_qp_drops(remove_location(remove_scroll_position(expected)))), remove_scores(remove_qp_drops(remove_location(remove_scroll_position(fgo_mat_counter.run(test_image, DEBUG, LABEL))))))

    def test_christmas_2018(self):
        expected = {'qp_gained': 6400, 'qp_total': 324783641, 'drops': [
            {'id': 'christmas_2018_stocking.png', 'x': 350, 'y': 8, 'score': 1.0, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 462, 'y': 8, 'score': 1.0, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 685, 'y': 8, 'score': 0.9913225, 'stack': 3},
            {'id': 'christmas_2018_gold_currency.png', 'x': 573, 'y': 9, 'score': 0.9727627, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 239, 'y': 122, 'score': 0.9948097, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 350, 'y': 122, 'score': 0.99124193, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 461, 'y': 122, 'score': 0.9732004, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 573, 'y': 122, 'score': 1.0, 'stack': 3},
            {'id': 'Yggdrassil Seed.png', 'x': 127, 'y': 8, 'score': 0.9358185},
            {'id': 'Caster Monument.png', 'x': 241, 'y': 9, 'score': 0.931241},
            {'id': 'christmas_2018_silver_currency.png', 'x': 17, 'y': 123, 'score': 0.9825888, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 128, 'y': 123, 'score': 0.99999964, 'stack': 2}]}

        test_image = os.path.join(os.getcwd(), 'test_data', 'christmas_2018.png')
        self.assertEqual(remove_scores(remove_qp_drops(remove_location(remove_scroll_position(expected)))),
                         remove_scores(remove_qp_drops(remove_location(remove_scroll_position(fgo_mat_counter.run(test_image, DEBUG, LABEL))))))

    @unittest.skipUnless(os.path.isdir(os.path.join(os.getcwd(), 'test_data', 'xmas_2018_expert_revo')), 'requries test data for 2018 christmas expert node')
    def test_christmas_2018_expoert_revo(self):
        expected = \
        {'01-6vBzFzW.png': {'qp_gained': 6400, 'qp_total': 324662697, 'drops': [
            {'id': 'Shining Gem of Rider.png', 'x': 350, 'y': 4, 'score': 0.98451334},
            {'id': 'christmas_2018_stocking.png', 'x': 461, 'y': 5, 'score': 0.9804248, 'stack': 2},
            {'id': 'christmas_2018_stocking.png', 'x': 572, 'y': 5, 'score': 0.9865965, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 685, 'y': 5, 'score': 0.9906629, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 17, 'y': 120, 'score': 0.96221656, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 128, 'y': 120, 'score': 0.9959503, 'stack': 3},
            {'id': 'christmas_2018_gold_currency.png', 'x': 239, 'y': 120, 'score': 0.9885471, 'stack': 3},
            {'id': 'Meteor Horseshoe.png', 'x': 129, 'y': 7, 'score': 0.91707414},
            {'id': 'Yggdrassil Seed.png', 'x': 238, 'y': 6, 'score': 0.94512475},
            {'id': 'christmas_2018_silver_currency.png', 'x': 351, 'y': 120, 'score': 0.9918008, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 462, 'y': 120, 'score': 0.997414, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 573, 'y': 120, 'score': 0.9702401, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 685, 'y': 120, 'score': 0.9978055, 'stack': 3},
            {'id': 'christmas_2018_silver_currency.png', 'x': 16, 'y': 235, 'score': 0.9817206, 'stack': 3},
            {'id': 'christmas_2018_silver_currency.png', 'x': 128, 'y': 235, 'score': 0.99912834, 'stack': 3}]},
        '01-bmlzv6z.png': {'qp_gained': 6400, 'qp_total': 324783641, 'drops': [
            {'id': 'christmas_2018_stocking.png', 'x': 350, 'y': 8, 'score': 1.0, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 462, 'y': 8, 'score': 1.0, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 685, 'y': 8, 'score': 0.9913225, 'stack': 3},
            {'id': 'christmas_2018_gold_currency.png', 'x': 573, 'y': 9, 'score': 0.9727627, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 239, 'y': 122, 'score': 0.9948097, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 350, 'y': 122, 'score': 0.99124193, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 461, 'y': 122, 'score': 0.9732004, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 573, 'y': 122, 'score': 1.0, 'stack': 3},
            {'id': 'Yggdrassil Seed.png', 'x': 127, 'y': 8, 'score': 0.9358185},
            {'id': 'Caster Monument.png', 'x': 241, 'y': 9, 'score': 0.931241},
            {'id': 'christmas_2018_silver_currency.png', 'x': 17, 'y': 123, 'score': 0.9825888, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 128, 'y': 123, 'score': 0.99999964, 'stack': 2}]},
        '01-GxW18aS.png': {'qp_gained': 6400, 'qp_total': 322856241, 'drops': [
            {'id': 'christmas_2018_stocking.png', 'x': 238, 'y': 8, 'score': 0.96391135, 'stack': 3},
            {'id': 'christmas_2018_stocking.png', 'x': 350, 'y': 8, 'score': 0.999998, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 462, 'y': 8, 'score': 0.9999991, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 685, 'y': 8, 'score': 0.9913195, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 573, 'y': 9, 'score': 0.9727501, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 17, 'y': 123, 'score': 0.9633587, 'stack': 3},
            {'id': 'christmas_2018_gold_currency.png', 'x': 128, 'y': 123, 'score': 0.99690706, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 461, 'y': 122, 'score': 0.9731538, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 573, 'y': 122, 'score': 0.99999934, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 684, 'y': 122, 'score': 0.98423046, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 16, 'y': 237, 'score': 0.9976314, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 127, 'y': 237, 'score': 0.9772536, 'stack': 3},
            {'id': 'Caster Monument.png', 'x': 129, 'y': 9, 'score': 0.9196835},
            {'id': 'christmas_2018_silver_currency.png', 'x': 239, 'y': 123, 'score': 0.981111, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 351, 'y': 123, 'score': 0.99220085, 'stack': 3}]},
        '01-hFeQVAp.png': {'qp_gained': 6400, 'qp_total': 322693641, 'drops': [
            {'id': 'christmas_2018_stocking.png', 'x': 127, 'y': 8, 'score': 0.9917377, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 239, 'y': 8, 'score': 0.9897186, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 351, 'y': 8, 'score': 0.9804832, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 462, 'y': 8, 'score': 0.99999535, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 461, 'y': 122, 'score': 0.97320855, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 573, 'y': 122, 'score': 0.99999774, 'stack': 3},
            {'id': 'christmas_2018_silver_currency.png', 'x': 573, 'y': 8, 'score': 0.9702901, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 685, 'y': 8, 'score': 0.9978891, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 17, 'y': 123, 'score': 0.98257923, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 128, 'y': 123, 'score': 0.99998873, 'stack': 3},
            {'id': 'christmas_2018_silver_currency.png', 'x': 239, 'y': 123, 'score': 0.98107976, 'stack': 3},
            {'id': 'christmas_2018_silver_currency.png', 'x': 351, 'y': 123, 'score': 0.9922004, 'stack': 3}]},
        '02-FD22Kwk.png': {'qp_gained': 6400, 'qp_total': 324669097, 'drops': [
            {'id': 'Shining Gem of Rider.png', 'x': 239, 'y': 7, 'score': 0.98786265},
            {'id': 'christmas_2018_stocking.png', 'x': 350, 'y': 8, 'score': 0.99999756, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 462, 'y': 8, 'score': 0.99999744, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 461, 'y': 122, 'score': 0.97316784, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 573, 'y': 122, 'score': 0.99999946, 'stack': 2},
            {'id': 'Meteor Horseshoe.png', 'x': 129, 'y': 10, 'score': 0.91826},
            {'id': 'christmas_2018_silver_currency.png', 'x': 573, 'y': 8, 'score': 0.97029674, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 685, 'y': 8, 'score': 0.99788207, 'stack': 3},
            {'id': 'christmas_2018_silver_currency.png', 'x': 17, 'y': 123, 'score': 0.9825938, 'stack': 3},
            {'id': 'christmas_2018_silver_currency.png', 'x': 128, 'y': 123, 'score': 0.9999915, 'stack': 3},
            {'id': 'christmas_2018_silver_currency.png', 'x': 239, 'y': 123, 'score': 0.9810531, 'stack': 3},
            {'id': 'christmas_2018_silver_currency.png', 'x': 351, 'y': 123, 'score': 0.99220395, 'stack': 3}]},
        '02-GiOatR2.png': {'qp_gained': 6400, 'qp_total': 324790041, 'drops': [
            {'id': 'Magic Gem of Berserker.png', 'x': 351, 'y': 9, 'score': 0.94785154},
            {'id': 'christmas_2018_stocking.png', 'x': 461, 'y': 8, 'score': 0.98070735, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 685, 'y': 8, 'score': 0.99131703, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 573, 'y': 9, 'score': 0.9727803, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 17, 'y': 123, 'score': 0.963349, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 128, 'y': 123, 'score': 0.9969291, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 239, 'y': 123, 'score': 0.9891505, 'stack': 3},
            {'id': 'Secret Gem of Berserker.png', 'x': 240, 'y': 11, 'score': 0.8657291},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 684, 'y': 122, 'score': 0.9844743, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 16, 'y': 237, 'score': 0.9976318, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 127, 'y': 237, 'score': 0.9770152, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 239, 'y': 237, 'score': 0.99477315, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 350, 'y': 237, 'score': 0.99080986, 'stack': 3},
            {'id': 'Meteor Horseshoe.png', 'x': 129, 'y': 10, 'score': 0.91825753},
            {'id': 'christmas_2018_silver_currency.png', 'x': 351, 'y': 123, 'score': 0.99232167, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 462, 'y': 123, 'score': 0.9976974, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 573, 'y': 123, 'score': 0.9707756, 'stack': 3}]},
        '02-tLmaw1B.png': {'qp_gained': 6400, 'qp_total': 322700041, 'drops': [
            {'id': 'christmas_2018_stocking.png', 'x': 127, 'y': 8, 'score': 0.9917398, 'stack': 2},
            {'id': 'christmas_2018_stocking.png', 'x': 238, 'y': 8, 'score': 0.9638939, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 351, 'y': 8, 'score': 0.9804904, 'stack': 3},
            {'id': 'christmas_2018_gold_currency.png', 'x': 462, 'y': 8, 'score': 0.9999977, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 350, 'y': 122, 'score': 0.9910094, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 461, 'y': 122, 'score': 0.9732148, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 573, 'y': 122, 'score': 1.0, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 684, 'y': 122, 'score': 0.98464537, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 573, 'y': 8, 'score': 0.9702725, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 685, 'y': 8, 'score': 0.99788916, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 17, 'y': 123, 'score': 0.9825792, 'stack': 3},
            {'id': 'christmas_2018_silver_currency.png', 'x': 128, 'y': 123, 'score': 0.9999912, 'stack': 3},
            {'id': 'christmas_2018_silver_currency.png', 'x': 239, 'y': 123, 'score': 0.981092, 'stack': 3}]},
        '02-YlcWZiO.png': {'qp_gained': 6400, 'qp_total': 322862641, 'drops': [
            {'id': 'christmas_2018_stocking.png', 'x': 461, 'y': 8, 'score': 0.9806902, 'stack': 3},
            {'id': 'christmas_2018_stocking.png', 'x': 572, 'y': 8, 'score': 0.98701394, 'stack': 2},
            {'id': 'christmas_2018_stocking.png', 'x': 684, 'y': 8, 'score': 0.99688655, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 17, 'y': 123, 'score': 0.9633106, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 128, 'y': 123, 'score': 0.9969046, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 239, 'y': 123, 'score': 0.9892185, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 351, 'y': 123, 'score': 0.9798204, 'stack': 3},
            {'id': 'christmas_2018_gold_currency.png', 'x': 462, 'y': 123, 'score': 0.9994351, 'stack': 3},
            {'id': 'Octuplet Twin Crystals.png', 'x': 240, 'y': 9, 'score': 0.9399472},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 127, 'y': 237, 'score': 0.97690994, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 239, 'y': 237, 'score': 0.99476546, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 350, 'y': 237, 'score': 0.9908457, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 461, 'y': 237, 'score': 0.97318333, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 573, 'y': 237, 'score': 0.9996485, 'stack': 3},
            {'id': 'Yggdrassil Seed.png', 'x': 350, 'y': 8, 'score': 0.9474659},
            {'id': 'Talon of Chaos.png', 'x': 129, 'y': 8, 'score': 0.89134276},
            {'id': 'christmas_2018_silver_currency.png', 'x': 573, 'y': 123, 'score': 0.9707562, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 685, 'y': 123, 'score': 0.99819475, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 17, 'y': 238, 'score': 0.98209727, 'stack': 3}]}
         }

        base_path = os.path.join(os.getcwd(), 'test_data', 'xmas_2018_expert_revo')
        for file in expected.keys():
            self.assertEqual(remove_scores(remove_location(remove_qp_drops(remove_scroll_position(expected[file])))),
                             remove_scores(remove_location(remove_qp_drops(remove_scroll_position(fgo_mat_counter.run(os.path.join(base_path, file), DEBUG, LABEL))))))


class TestSpecialCases(unittest.TestCase):
    def test_red_filter(self):
        expected = {'qp_gained': 2288900, 'qp_total': 106845904, 'drops': [
            {'id': 'Shining Gem of Saber.png', 'x': 350, 'y': 5, 'score': '0.97447186'},
            {'id': 'Bloodstone Tear.png', 'x': 129, 'y': 7, 'score': '0.92565679'},
            {'id': 'Void Dust.png', 'x': 239, 'y': 6, 'score': '0.97221052'}]}

        test_image = os.path.join(os.getcwd(), 'test_data', 'samsung_s9_red_filter_43_percent.jpg')
        self.assertEqual(remove_scores(remove_qp_drops(remove_location(remove_scroll_position(expected)))),
                         remove_scores(remove_qp_drops(remove_location(remove_scroll_position(fgo_mat_counter.run(test_image, DEBUG, LABEL))))))

    def test_blue_and_black_borders(self):
        expected = {'qp_gained': 668900, 'qp_total': 755521417, 'drops': [
            {'id': 'Shining Gem of Assassin.png', 'x': 350, 'y': 7, 'score': '0.97608447'},
            {'id': 'Magic Gem of Assassin.png', 'x': 240, 'y': 8, 'score': '0.95031976'},
            {'id': 'Homunculus Baby.png', 'x': 128, 'y': 9, 'score': '0.94004923'}]}

        test_image = os.path.join(os.getcwd(), 'test_data', 'black_and_blue_border.jpg')
        self.assertEqual(remove_scores(remove_qp_drops(remove_location(remove_scroll_position(expected)))),
                         remove_scores(remove_qp_drops(remove_location(remove_scroll_position(fgo_mat_counter.run(test_image, DEBUG, LABEL))))))


class TestScrollBarLocation(unittest.TestCase):
    def test_scroll_at_top(self):
        test_image = os.path.join(os.getcwd(), 'test_data', 'da_vinci.png')
        res = fgo_mat_counter.run(test_image, DEBUG, LABEL)
        self.assertNotEquals(-1, res['scroll_position'])

    def test_scroll_at_top2(self):
        test_image = os.path.join(os.getcwd(), 'test_data', 'Screenshot_20181205-153908_Fate_GO.jpg')
        res = fgo_mat_counter.run(test_image, DEBUG, LABEL)
        self.assertNotEquals(-1, res['scroll_position'])


class TestFrontend(unittest.TestCase):
    def test_location_normalization_one_row(self):
        input_data = [
            {'id': 'Shining Gem of Saber.png', 'x': 350, 'y': 5, 'score': '0.97447186'},
            {'id': 'Bloodstone Tear.png', 'x': 129, 'y': 7, 'score': '0.92565679'},
            {'id': 'Void Dust.png', 'x': 239, 'y': 6, 'score': '0.97221052'}]

        expected = [
            {'id': 'Shining Gem of Saber.png', 'x': 2, 'y': 0, 'score': '0.97447186'},
            {'id': 'Bloodstone Tear.png', 'x': 0, 'y': 0, 'score': '0.92565679'},
            {'id': 'Void Dust.png', 'x': 1, 'y': 0, 'score': '0.97221052'}]

        self.assertEqual(expected, frontend.normalize_drop_locations(input_data))


    def test_location_normalization_three_rows(self):
        input_data = [{'id': 'Manuscript (True).png', 'x': 352, 'y': 7, 'score': '0.91605514', 'stack': 3},
                {'id': 'Manuscript (True).png', 'x': 463, 'y': 7, 'score': '0.91864091', 'stack': 3},
                {'id': 'Manuscript (True).png', 'x': 575, 'y': 7, 'score': '0.90524661', 'stack': 3},
                {'id': 'Manuscript (True).png', 'x': 686, 'y': 7, 'score': '0.91897970', 'stack': 3},
                {'id': 'Manuscript (False).png', 'x': 19, 'y': 121, 'score': '0.97181606', 'stack': 3},
                {'id': 'Manuscript (False).png', 'x': 130, 'y': 121, 'score': '0.97234934', 'stack': 3},
                {'id': 'Manuscript (False).png', 'x': 241, 'y': 121, 'score': '0.97120785', 'stack': 3},
                {'id': 'Manuscript (False).png', 'x': 353, 'y': 121, 'score': '0.97240418', 'stack': 3},
                {'id': 'Manuscript (False).png', 'x': 464, 'y': 121, 'score': '0.97294944', 'stack': 3},
                {'id': 'Manuscript (False).png', 'x': 576, 'y': 121, 'score': '0.97055381', 'stack': 3},
                {'id': 'Manuscript (False).png', 'x': 687, 'y': 121, 'score': '0.97198474', 'stack': 10},
                {'id': 'Manuscript (False).png', 'x': 19, 'y': 236, 'score': '0.97227716', 'stack': 3},
                {'id': 'Manuscript (False).png', 'x': 130, 'y': 236, 'score': '0.97235178', 'stack': 3},
                {'id': 'Lancer Piece.png', 'x': 131, 'y': 8, 'score': '0.89710170'},
                {'id': 'Berserker Piece.png', 'x': 241, 'y': 9, 'score': '0.94229006'},
                {'id': 'qp.png', 'x': 0, 'y': 0, 'score': 1.0}]

        expected = [{'id': 'Manuscript (True).png', 'x': 3, 'y': 0, 'score': '0.91605514', 'stack': 3},
                {'id': 'Manuscript (True).png', 'x': 4, 'y': 0, 'score': '0.91864091', 'stack': 3},
                {'id': 'Manuscript (True).png', 'x': 5, 'y': 0, 'score': '0.90524661', 'stack': 3},
                {'id': 'Manuscript (True).png', 'x': 6, 'y': 0, 'score': '0.91897970', 'stack': 3},
                {'id': 'Manuscript (False).png', 'x': 0, 'y': 1, 'score': '0.97181606', 'stack': 3},
                {'id': 'Manuscript (False).png', 'x': 1, 'y': 1, 'score': '0.97234934', 'stack': 3},
                {'id': 'Manuscript (False).png', 'x': 2, 'y': 1, 'score': '0.97120785', 'stack': 3},
                {'id': 'Manuscript (False).png', 'x': 3, 'y': 1, 'score': '0.97240418', 'stack': 3},
                {'id': 'Manuscript (False).png', 'x': 4, 'y': 1, 'score': '0.97294944', 'stack': 3},
                {'id': 'Manuscript (False).png', 'x': 5, 'y': 1, 'score': '0.97055381', 'stack': 3},
                {'id': 'Manuscript (False).png', 'x': 6, 'y': 1, 'score': '0.97198474', 'stack': 10},
                {'id': 'Manuscript (False).png', 'x': 0, 'y': 2, 'score': '0.97227716', 'stack': 3},
                {'id': 'Manuscript (False).png', 'x': 1, 'y': 2, 'score': '0.97235178', 'stack': 3},
                {'id': 'Lancer Piece.png', 'x': 1, 'y': 0, 'score': '0.89710170'},
                {'id': 'Berserker Piece.png', 'x': 2, 'y': 0, 'score': '0.94229006'},
                {'id': 'qp.png', 'x': 0, 'y': 0, 'score': 1.0}]

        self.assertEqual(expected, frontend.normalize_drop_locations(input_data))


if __name__ == '__main__':
    unittest.main()
