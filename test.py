import unittest
import os
import operator

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
        expected = {'qp_gained': 9400, 'qp_total': 357256131, 'drop_count': 15, 'drops_found': 16, 'drops': [
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
            {'id': 'Lancer Piece.png', 'x': 131, 'y': 8, 'score': '0.89710170', 'stack': 0},
            {'id': 'Berserker Piece.png', 'x': 241, 'y': 9, 'score': '0.94229006', 'stack': 0}
        ]}

        test_image = os.path.join(os.getcwd(), 'test_data', 'da_vinci.png')
        self.assertEqual(remove_scores(remove_qp_drops(remove_location(remove_scroll_position(expected)))), remove_scores(remove_qp_drops(remove_location(remove_scroll_position(fgo_mat_counter.run(test_image, DEBUG, LABEL))))))

    def test_christmas_2018(self):
        expected = {'qp_gained': 6400, 'qp_total': 324783641, 'drop_count': 12, 'drops_found': 13, 'drops': [
            {'id': 'christmas_2018_stocking.png', 'x': 350, 'y': 8, 'score': 1.0, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 462, 'y': 8, 'score': 1.0, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 685, 'y': 8, 'score': 0.9913225, 'stack': 3},
            {'id': 'christmas_2018_gold_currency.png', 'x': 573, 'y': 9, 'score': 0.9727627, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 239, 'y': 122, 'score': 0.9948097, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 350, 'y': 122, 'score': 0.99124193, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 461, 'y': 122, 'score': 0.9732004, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 573, 'y': 122, 'score': 1.0, 'stack': 3},
            {'id': 'Yggdrassil Seed.png', 'x': 127, 'y': 8, 'score': 0.9358185, 'stack': 0},
            {'id': 'Caster Monument.png', 'x': 241, 'y': 9, 'score': 0.931241, 'stack': 0},
            {'id': 'christmas_2018_silver_currency.png', 'x': 17, 'y': 123, 'score': 0.9825888, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 128, 'y': 123, 'score': 0.99999964, 'stack': 2}]}

        test_image = os.path.join(os.getcwd(), 'test_data', 'christmas_2018.png')
        self.assertEqual(remove_scores(remove_qp_drops(remove_location(remove_scroll_position(expected)))),
                         remove_scores(remove_qp_drops(remove_location(remove_scroll_position(fgo_mat_counter.run(test_image, DEBUG, LABEL))))))

    @unittest.skipUnless(os.path.isdir(os.path.join(os.getcwd(), 'test_data', 'xmas_2018_expert_revo')), 'requries test data for 2018 christmas expert node')
    def test_christmas_2018_expert_revo(self):
        self.maxDiff = None
        expected = \
        {'01-6vBzFzW.png': {'qp_gained': 6400, 'qp_total': 324662697, 'drop_count': 15, 'drops_found': 16, 'drops': [
            {'id': 'Shining Gem of Rider.png', 'x': 350, 'y': 4, 'score': 0.98451334, 'stack': 0},
            {'id': 'christmas_2018_stocking.png', 'x': 461, 'y': 5, 'score': 0.9804248, 'stack': 2},
            {'id': 'christmas_2018_stocking.png', 'x': 572, 'y': 5, 'score': 0.9865965, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 685, 'y': 5, 'score': 0.9906629, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 17, 'y': 120, 'score': 0.96221656, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 128, 'y': 120, 'score': 0.9959503, 'stack': 3},
            {'id': 'christmas_2018_gold_currency.png', 'x': 239, 'y': 120, 'score': 0.9885471, 'stack': 3},
            {'id': 'Meteor Horseshoe.png', 'x': 129, 'y': 7, 'score': 0.91707414, 'stack': 0},
            {'id': 'Yggdrassil Seed.png', 'x': 238, 'y': 6, 'score': 0.94512475, 'stack': 0},
            {'id': 'christmas_2018_silver_currency.png', 'x': 351, 'y': 120, 'score': 0.9918008, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 462, 'y': 120, 'score': 0.997414, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 573, 'y': 120, 'score': 0.9702401, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 685, 'y': 120, 'score': 0.9978055, 'stack': 3},
            {'id': 'christmas_2018_silver_currency.png', 'x': 16, 'y': 235, 'score': 0.9817206, 'stack': 3},
            {'id': 'christmas_2018_silver_currency.png', 'x': 128, 'y': 235, 'score': 0.99912834, 'stack': 3}]},
        '01-bmlzv6z.png': {'qp_gained': 6400, 'qp_total': 324783641, 'drop_count': 12, 'drops_found': 13, 'drops': [
            {'id': 'christmas_2018_stocking.png', 'x': 350, 'y': 8, 'score': 1.0, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 462, 'y': 8, 'score': 1.0, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 685, 'y': 8, 'score': 0.9913225, 'stack': 3},
            {'id': 'christmas_2018_gold_currency.png', 'x': 573, 'y': 9, 'score': 0.9727627, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 239, 'y': 122, 'score': 0.9948097, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 350, 'y': 122, 'score': 0.99124193, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 461, 'y': 122, 'score': 0.9732004, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 573, 'y': 122, 'score': 1.0, 'stack': 3},
            {'id': 'Yggdrassil Seed.png', 'x': 127, 'y': 8, 'score': 0.9358185, 'stack': 0},
            {'id': 'Caster Monument.png', 'x': 241, 'y': 9, 'score': 0.931241, 'stack': 0},
            {'id': 'christmas_2018_silver_currency.png', 'x': 17, 'y': 123, 'score': 0.9825888, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 128, 'y': 123, 'score': 0.99999964, 'stack': 2}]},
        '01-GxW18aS.png': {'qp_gained': 6400, 'qp_total': 322856241, 'drop_count': 15, 'drops_found': 16, 'drops': [
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
            {'id': 'Caster Monument.png', 'x': 129, 'y': 9, 'score': 0.9196835, 'stack': 0},
            {'id': 'christmas_2018_silver_currency.png', 'x': 239, 'y': 123, 'score': 0.981111, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 351, 'y': 123, 'score': 0.99220085, 'stack': 3}]},
        '01-hFeQVAp.png': {'qp_gained': 6400, 'qp_total': 322693641, 'drop_count': 12, 'drops_found': 13, 'drops': [
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
        '02-FD22Kwk.png': {'qp_gained': 6400, 'qp_total': 324669097, 'drop_count': 12,'drops_found': 13,  'drops': [
            {'id': 'Shining Gem of Rider.png', 'x': 239, 'y': 7, 'score': 0.98786265, 'stack': 0},
            {'id': 'christmas_2018_stocking.png', 'x': 350, 'y': 8, 'score': 0.99999756, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 462, 'y': 8, 'score': 0.99999744, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 461, 'y': 122, 'score': 0.97316784, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 573, 'y': 122, 'score': 0.99999946, 'stack': 2},
            {'id': 'Meteor Horseshoe.png', 'x': 129, 'y': 10, 'score': 0.91826, 'stack': 0},
            {'id': 'christmas_2018_silver_currency.png', 'x': 573, 'y': 8, 'score': 0.97029674, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 685, 'y': 8, 'score': 0.99788207, 'stack': 3},
            {'id': 'christmas_2018_silver_currency.png', 'x': 17, 'y': 123, 'score': 0.9825938, 'stack': 3},
            {'id': 'christmas_2018_silver_currency.png', 'x': 128, 'y': 123, 'score': 0.9999915, 'stack': 3},
            {'id': 'christmas_2018_silver_currency.png', 'x': 239, 'y': 123, 'score': 0.9810531, 'stack': 3},
            {'id': 'christmas_2018_silver_currency.png', 'x': 351, 'y': 123, 'score': 0.99220395, 'stack': 3}]},
        '02-GiOatR2.png': {'qp_gained': 6400, 'qp_total': 324790041, 'drop_count': 17, 'drops_found': 18, 'drops': [
            {'id': 'Magic Gem of Berserker.png', 'x': 351, 'y': 9, 'score': 0.94785154, 'stack': 0},
            {'id': 'christmas_2018_stocking.png', 'x': 461, 'y': 8, 'score': 0.98070735, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 685, 'y': 8, 'score': 0.99131703, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 573, 'y': 9, 'score': 0.9727803, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 17, 'y': 123, 'score': 0.963349, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 128, 'y': 123, 'score': 0.9969291, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 239, 'y': 123, 'score': 0.9891505, 'stack': 3},
            {'id': 'Secret Gem of Berserker.png', 'x': 240, 'y': 11, 'score': 0.8657291, 'stack': 0},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 684, 'y': 122, 'score': 0.9844743, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 16, 'y': 237, 'score': 0.9976318, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 127, 'y': 237, 'score': 0.9770152, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 239, 'y': 237, 'score': 0.99477315, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 350, 'y': 237, 'score': 0.99080986, 'stack': 3},
            {'id': 'Meteor Horseshoe.png', 'x': 129, 'y': 10, 'score': 0.91825753, 'stack': 0},
            {'id': 'christmas_2018_silver_currency.png', 'x': 351, 'y': 123, 'score': 0.99232167, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 462, 'y': 123, 'score': 0.9976974, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 573, 'y': 123, 'score': 0.9707756, 'stack': 3}]},
        '02-tLmaw1B.png': {'qp_gained': 6400, 'qp_total': 322700041, 'drop_count': 13, 'drops_found': 14, 'drops': [
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
        '02-YlcWZiO.png': {'qp_gained': 6400, 'qp_total': 322862641, 'drop_count': 19, 'drops_found': 20, 'drops': [
            {'id': 'christmas_2018_stocking.png', 'x': 461, 'y': 8, 'score': 0.9806902, 'stack': 3},
            {'id': 'christmas_2018_stocking.png', 'x': 572, 'y': 8, 'score': 0.98701394, 'stack': 2},
            {'id': 'christmas_2018_stocking.png', 'x': 684, 'y': 8, 'score': 0.99688655, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 17, 'y': 123, 'score': 0.9633106, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 128, 'y': 123, 'score': 0.9969046, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 239, 'y': 123, 'score': 0.9892185, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 351, 'y': 123, 'score': 0.9798204, 'stack': 3},
            {'id': 'christmas_2018_gold_currency.png', 'x': 462, 'y': 123, 'score': 0.9994351, 'stack': 3},
            {'id': 'Octuplet Twin Crystals.png', 'x': 240, 'y': 9, 'score': 0.9399472, 'stack': 0},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 127, 'y': 237, 'score': 0.97690994, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 239, 'y': 237, 'score': 0.99476546, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 350, 'y': 237, 'score': 0.9908457, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 461, 'y': 237, 'score': 0.97318333, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 573, 'y': 237, 'score': 0.9996485, 'stack': 3},
            {'id': 'Yggdrassil Seed.png', 'x': 350, 'y': 8, 'score': 0.9474659, 'stack': 0},
            {'id': 'Talon of Chaos.png', 'x': 129, 'y': 8, 'score': 0.89134276, 'stack': 0},
            {'id': 'christmas_2018_silver_currency.png', 'x': 573, 'y': 123, 'score': 0.9707562, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 685, 'y': 123, 'score': 0.99819475, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 17, 'y': 238, 'score': 0.98209727, 'stack': 3}]}
         }

        base_path = os.path.join(os.getcwd(), 'test_data', 'xmas_2018_expert_revo')
        for file in expected.keys():
            expected_result = remove_scores(remove_location(remove_qp_drops(remove_scroll_position(expected[file]))))
            expected_result['drops'].sort(key=operator.itemgetter('id', 'stack'))
            result = remove_scores(remove_location(remove_qp_drops(remove_scroll_position(fgo_mat_counter.run(os.path.join(base_path, file), DEBUG, LABEL)))))
            result['drops'].sort(key=operator.itemgetter('id', 'stack'))
            self.assertEqual(expected_result, result)

    def test_valentine_2019_expert_knights(self):
        expected = {'qp_gained': 6400, 'qp_total': 170761518, 'scroll_position': 0, 'drop_count': 19, 'drops_found': 20, 'drops': [
            {'id': 'Archer Piece.png', 'x': 129, 'y': 24, 'score': 0.9497172, 'stack': 0},
            {'id': 'qp.png', 'x': 17, 'y': 18, 'score': 0.9961114, 'stack': 0},
            {'id': 'valentine_2019_saber_coin.png', 'x': 239, 'y': 21, 'score': 0.96185666, 'stack': 2},
            {'id': 'valentine_2019_saber_coin.png', 'x': 351, 'y': 21, 'score': 0.9453553, 'stack': 2},
            {'id': 'valentine_2019_saber_coin.png', 'x': 462, 'y': 21, 'score': 0.9788375, 'stack': 2},
            {'id': 'valentine_2019_saber_coin.png', 'x': 573, 'y': 21, 'score': 0.9396837, 'stack': 2},
            {'id': 'valentine_2019_lancer_coin.png', 'x': 128, 'y': 136, 'score': 0.95286167, 'stack': 2},
            {'id': 'valentine_2019_lancer_coin.png', 'x': 16, 'y': 137, 'score': 0.9263724, 'stack': 2},
            {'id': 'valentine_2019_all_coin.png', 'x': 462, 'y': 137, 'score': 0.9618784, 'stack': 2},
            {'id': 'valentine_2019_archer_coin.png', 'x': 684, 'y': 21, 'score': 0.9435896, 'stack': 2},
            {'id': 'valentine_2019_all_coin.png', 'x': 351, 'y': 131, 'score': 0.9674793, 'stack': 2},
            {'id': 'valentine_2019_all_coin.png', 'x': 239, 'y': 132, 'score': 0.93297756, 'stack': 2},
            {'id': 'valentine_2019_choco.png', 'x': 573, 'y': 128, 'score': 0.99094504, 'stack': 6},
            {'id': 'valentine_2019_choco.png', 'x': 685, 'y': 128, 'score': 0.99210346, 'stack': 7},
            {'id': 'valentine_2019_choco.png', 'x': 17, 'y': 243, 'score': 0.98842907, 'stack': 7},
            {'id': 'valentine_2019_choco.png', 'x': 128, 'y': 243, 'score': 0.9940306, 'stack': 7},
            {'id': 'valentine_2019_choco.png', 'x': 239, 'y': 243, 'score': 0.993614, 'stack': 6},
            {'id': 'valentine_2019_choco.png', 'x': 351, 'y': 243, 'score': 0.9881494, 'stack': 7},
            {'id': 'valentine_2019_choco.png', 'x': 462, 'y': 243, 'score': 0.995087, 'stack': 7},
            {'id': 'valentine_2019_choco.png', 'x': 573, 'y': 243, 'score': 0.99105835, 'stack': 7}]}

        expected_result = remove_scores(remove_location(remove_qp_drops(remove_scroll_position(expected))))
        expected_result['drops'].sort(key=operator.itemgetter('id', 'stack'))
        test_image = os.path.join(os.getcwd(), 'test_data', 'valentine_2019_expert_knight.png')
        result = remove_scores(remove_location(
            remove_qp_drops(remove_scroll_position(fgo_mat_counter.run(test_image, DEBUG, LABEL)))))
        result['drops'].sort(key=operator.itemgetter('id', 'stack'))
        self.assertEqual(expected_result, result)



class TestSpecialCases(unittest.TestCase):
    def test_red_filter(self):
        expected = {'qp_gained': 2288900, 'qp_total': 106845904, 'drop_count': 8, 'drops_found': 4, 'drops': [
            {'id': 'Shining Gem of Saber.png', 'x': 350, 'y': 5, 'score': '0.97447186', 'stack': 0},
            {'id': 'Bloodstone Tear.png', 'x': 129, 'y': 7, 'score': '0.92565679', 'stack': 0},
            {'id': 'Void Dust.png', 'x': 239, 'y': 6, 'score': '0.97221052', 'stack': 0}]}

        test_image = os.path.join(os.getcwd(), 'test_data', 'samsung_s9_red_filter_43_percent.jpg')
        self.assertEqual(remove_scores(remove_qp_drops(remove_location(remove_scroll_position(expected)))),
                         remove_scores(remove_qp_drops(remove_location(remove_scroll_position(fgo_mat_counter.run(test_image, DEBUG, LABEL))))))

    def test_blue_and_black_borders(self):
        expected = {'qp_gained': 668900, 'qp_total': 755521417, 'drop_count': 6, 'drops_found': 4, 'drops': [
            {'id': 'Shining Gem of Assassin.png', 'x': 350, 'y': 7, 'score': '0.97608447', 'stack': 0},
            {'id': 'Magic Gem of Assassin.png', 'x': 240, 'y': 8, 'score': '0.95031976', 'stack': 0},
            {'id': 'Homunculus Baby.png', 'x': 128, 'y': 9, 'score': '0.94004923', 'stack': 0}]}

        test_image = os.path.join(os.getcwd(), 'test_data', 'black_and_blue_border.jpg')
        self.assertEqual(remove_scores(remove_qp_drops(remove_location(remove_scroll_position(expected)))),
                         remove_scores(remove_qp_drops(remove_location(remove_scroll_position(fgo_mat_counter.run(test_image, DEBUG, LABEL))))))

    def test_blue_and_black_borders_light_background(self):
        expected = {'qp_gained': 668900, 'qp_total': 755521417, 'drop_count': 6, 'drops_found': 4, 'drops': [
            {'id': 'Shining Gem of Assassin.png', 'x': 350, 'y': 7, 'score': '0.97608447', 'stack': 0},
            {'id': 'Magic Gem of Assassin.png', 'x': 240, 'y': 8, 'score': '0.95031976', 'stack': 0},
            {'id': 'Homunculus Baby.png', 'x': 128, 'y': 9, 'score': '0.94004923', 'stack': 0}]}

        test_image = os.path.join(os.getcwd(), 'test_data', 'black_and_blue_border_light_bg.jpg')
        self.assertEqual(remove_scores(remove_qp_drops(remove_location(remove_scroll_position(expected)))),
                         remove_scores(remove_qp_drops(remove_location(remove_scroll_position(fgo_mat_counter.run(test_image, DEBUG, LABEL))))))

    def test_side_bottom_blue_border(self):
        self.maxDiff = None
        expected = {'qp_gained': 8400, 'qp_total': 710822575, 'scroll_position': 0, 'drop_count': 26, 'drops_found': 21, 'drops':
            [{'id': 'Magic Gem of Assassin.png', 'x': 351, 'y': 22, 'score': 0.96120733, 'stack': 0},
             {'id': 'Secret Gem of Assassin.png', 'x': 240, 'y': 24, 'score': 0.9222073, 'stack': 0},
             {'id': 'qp.png', 'x': 17, 'y': 18, 'score': 0.9790159, 'stack': 0},
             {'id': 'Forbidden Page.png', 'x': 128, 'y': 23, 'score': 0.8865578, 'stack': 0},
             {'id': 'valentine_2019_assassin_coin.png', 'x': 573, 'y': 18, 'score': 0.9447703, 'stack': 2},
             {'id': 'valentine_2019_assassin_coin.png', 'x': 685, 'y': 19, 'score': 0.97349775, 'stack': 2},
             {'id': 'valentine_2019_assassin_coin.png', 'x': 127, 'y': 133, 'score': 0.9399135, 'stack': 2},
             {'id': 'valentine_2019_assassin_coin.png', 'x': 350, 'y': 133, 'score': 0.93968415, 'stack': 2},
             {'id': 'valentine_2019_assassin_coin.png', 'x': 573, 'y': 133, 'score': 0.93755686, 'stack': 2},
             {'id': 'valentine_2019_assassin_coin.png', 'x': 16, 'y': 134, 'score': 0.9659351, 'stack': 2},
             {'id': 'valentine_2019_assassin_coin.png', 'x': 239, 'y': 134, 'score': 0.96467453, 'stack': 2},
             {'id': 'valentine_2019_assassin_coin.png', 'x': 462, 'y': 134, 'score': 0.9639296, 'stack': 2},
             {'id': 'valentine_2019_assassin_coin.png', 'x': 685, 'y': 134, 'score': 0.9667589, 'stack': 2},
             {'id': 'valentine_2019_all_coin.png', 'x': 238, 'y': 248, 'score': 0.94676495, 'stack': 2},
             {'id': 'valentine_2019_all_coin.png', 'x': 350, 'y': 248, 'score': 0.95076126, 'stack': 2},
             {'id': 'valentine_2019_all_coin.png', 'x': 461, 'y': 248, 'score': 0.9395817, 'stack': 2},
             {'id': 'valentine_2019_assassin_coin.png', 'x': 16, 'y': 249, 'score': 0.95510703, 'stack': 2},
             {'id': 'valentine_2019_assassin_coin.png', 'x': 127, 'y': 249, 'score': 0.9289505, 'stack': 2},
             {'id': 'valentine_2019_choco.png', 'x': 573, 'y': 244, 'score': 0.9911243, 'stack': 5},
             {'id': 'valentine_2019_choco.png', 'x': 684, 'y': 244, 'score': 0.98415077, 'stack': 6},
             {'id': 'valentine_2019_assassin_coin.png', 'x': 462, 'y': 18, 'score': 0.9705379, 'stack': 2}]}

        expected = remove_scores(remove_qp_drops(remove_scroll_position(expected)))
        frontend.normalize_drop_locations(expected['drops'])
        expected['drops'].sort(key=operator.itemgetter('y', 'x'))
        test_image = os.path.join(os.getcwd(), 'test_data', 'side_bottom_blue_borders.png')
        result = remove_scores(remove_qp_drops(remove_scroll_position(fgo_mat_counter.run(test_image, DEBUG, LABEL))))
        frontend.normalize_drop_locations(result['drops'])
        result['drops'].sort(key=operator.itemgetter('y', 'x'))
        self.assertEqual(expected, result)


class TestScrollBarLocation(unittest.TestCase):
    def test_scroll_at_top(self):
        test_image = os.path.join(os.getcwd(), 'test_data', 'da_vinci.png')
        res = fgo_mat_counter.run(test_image, DEBUG, LABEL)
        self.assertNotEqual(-1, res['scroll_position'])

    def test_scroll_at_top2(self):
        test_image = os.path.join(os.getcwd(), 'test_data', 'Screenshot_20181205-153908_Fate_GO.jpg')
        res = fgo_mat_counter.run(test_image, DEBUG, LABEL)
        self.assertNotEqual(-1, res['scroll_position'])

    def test_no_scroll_bar(self):
        test_image = os.path.join(os.getcwd(), 'test_data', 'black_and_blue_border.jpg')
        res = fgo_mat_counter.run(test_image, DEBUG, LABEL)
        self.assertEqual(-1, res['scroll_position'])

    def test_scroll_bar_at_bottom(self):
        test_image = os.path.join(os.getcwd(), 'test_data', 'scrolled_down.png')
        res = fgo_mat_counter.run(test_image, DEBUG, LABEL)
        self.assertLess(5, res['scroll_position'])


class TestFrontend(unittest.TestCase):
    def test_location_normalization_one_row(self):
        input_data = [
            {'id': 'Shining Gem of Saber.png', 'x': 350, 'y': 5, 'score': '0.97447186'},
            {'id': 'Bloodstone Tear.png', 'x': 129, 'y': 7, 'score': '0.92565679'},
            {'id': 'Void Dust.png', 'x': 239, 'y': 6, 'score': '0.97221052'}]

        expected = [
            {'id': 'Shining Gem of Saber.png', 'x': 3, 'y': 0, 'score': '0.97447186'},
            {'id': 'Bloodstone Tear.png', 'x': 1, 'y': 0, 'score': '0.92565679'},
            {'id': 'Void Dust.png', 'x': 2, 'y': 0, 'score': '0.97221052'}]

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
