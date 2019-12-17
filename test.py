import unittest
import os
import operator
import pathlib

import frontend
import fgo_mat_counter


DEBUG = False
VERBOSE = False


def remove_scores(dictionary):
    for drop in dictionary['drops']:
        drop.pop('score', None)

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


def update(d):
    for drop in d['drops']:
        drop['x'] = drop['x'] + 40

    print(d)


def prepare_for_comparison(dictionary):

    dictionary = remove_scroll_position(dictionary)
    dictionary = remove_qp_drops(dictionary)
    dictionary = remove_scores(dictionary)
    dictionary['drops'] = frontend.normalize_drop_locations(dictionary['drops'])
    dictionary['drops'].sort(key=operator.itemgetter('y','x'))
    return dictionary


class TestEvents(unittest.TestCase):
    def test_da_vinci(self):
        expected = {'qp_gained': 9400, 'qp_total': 357256131, 'drop_count': 15, 'drops_found': 16, 'drops': [{'id': 'Manuscript (True).png', 'x': 392, 'y': 7, 'score': '0.91605514', 'stack': 3}, {'id': 'Manuscript (True).png', 'x': 503, 'y': 7, 'score': '0.91864091', 'stack': 3}, {'id': 'Manuscript (True).png', 'x': 615, 'y': 7, 'score': '0.90524661', 'stack': 3}, {'id': 'Manuscript (True).png', 'x': 726, 'y': 7, 'score': '0.91897970', 'stack': 3}, {'id': 'Manuscript (False).png', 'x': 59, 'y': 121, 'score': '0.97181606', 'stack': 3}, {'id': 'Manuscript (False).png', 'x': 170, 'y': 121, 'score': '0.97234934', 'stack': 3}, {'id': 'Manuscript (False).png', 'x': 281, 'y': 121, 'score': '0.97120785', 'stack': 3}, {'id': 'Manuscript (False).png', 'x': 393, 'y': 121, 'score': '0.97240418', 'stack': 3}, {'id': 'Manuscript (False).png', 'x': 504, 'y': 121, 'score': '0.97294944', 'stack': 3}, {'id': 'Manuscript (False).png', 'x': 616, 'y': 121, 'score': '0.97055381', 'stack': 3}, {'id': 'Manuscript (False).png', 'x': 727, 'y': 121, 'score': '0.97198474', 'stack': 10}, {'id': 'Manuscript (False).png', 'x': 59, 'y': 236, 'score': '0.97227716', 'stack': 3}, {'id': 'Manuscript (False).png', 'x': 170, 'y': 236, 'score': '0.97235178', 'stack': 3}, {'id': 'Lancer Piece.png', 'x': 171, 'y': 8, 'score': '0.89710170', 'stack': 0}, {'id': 'Berserker Piece.png', 'x': 281, 'y': 9, 'score': '0.94229006', 'stack': 0}]}


        test_image = os.path.join(os.getcwd(), 'test_data', 'da_vinci.png')
        expected = prepare_for_comparison(expected)
        result = prepare_for_comparison(fgo_mat_counter.run(test_image, DEBUG, VERBOSE))
        self.assertEqual(expected, result)

    def test_christmas_2018(self):
        self.maxDiff = None
        expected = {'qp_gained': 6400, 'qp_total': 324783641, 'scroll_position': -1, 'drop_count': 12, 'drops_found': 13,
         'drops': [{'id': 'christmas_2018_stocking.png', 'x': 392, 'y': 41, 'score': 0.97747153, 'stack': 2},
                   {'id': 'christmas_2018_gold_currency.png', 'x': 503, 'y': 42, 'score': 0.9664872, 'stack': 2},
                   {'id': 'christmas_2018_gold_currency.png', 'x': 615, 'y': 42, 'score': 0.95696086, 'stack': 3},
                   {'id': 'christmas_2018_gold_currency.png', 'x': 726, 'y': 42, 'score': 0.9410737, 'stack': 3},
                   {'id': 'qp.png', 'x': 59, 'y': 38, 'score': 0.9924508, 'stack': 0},
                   {'id': 'christmas_2018_bronze_currency.png', 'x': 280, 'y': 156, 'score': 0.98091036, 'stack': 2},
                   {'id': 'christmas_2018_bronze_currency.png', 'x': 391, 'y': 156, 'score': 0.9850108, 'stack': 3},
                   {'id': 'christmas_2018_bronze_currency.png', 'x': 503, 'y': 156, 'score': 0.95945466, 'stack': 3},
                   {'id': 'christmas_2018_bronze_currency.png', 'x': 614, 'y': 156, 'score': 0.9815003, 'stack': 3},
                   {'id': 'Yggdrassil Seed.png', 'x': 169, 'y': 42, 'score': 0.95376956, 'stack': 0},
                   {'id': 'Caster Monument.png', 'x': 282, 'y': 43, 'score': 0.9485099, 'stack': 0},
                   {'id': 'christmas_2018_silver_currency.png', 'x': 58, 'y': 157, 'score': 0.9581807, 'stack': 2},
                   {'id': 'christmas_2018_silver_currency.png', 'x': 170, 'y': 157, 'score': 0.9739899, 'stack': 2}]}

        test_image = os.path.join(os.getcwd(), 'test_data', 'christmas_2018.png')
        expected = prepare_for_comparison(expected)
        result = prepare_for_comparison(fgo_mat_counter.run(test_image, DEBUG, VERBOSE))
        self.assertEqual(expected, result)

    @unittest.skipUnless(os.path.isdir(os.path.join(os.getcwd(), 'test_data', 'xmas_2018_expert_revo')), 'requries test data for 2018 christmas expert node')
    def test_christmas_2018_expert_revo(self):
        self.maxDiff = None
        expected = \
        {'01-6vBzFzW.png': {'qp_gained': 6400, 'qp_total': 324662697, 'scroll_position': 10, 'drop_count': 15, 'drops_found': 16, 'drops': [
            {'id': 'Shining Gem of Rider.png', 'x': 432, 'y': 36, 'score': 0.9880161, 'stack': 0},
            {'id': 'christmas_2018_stocking.png', 'x': 543, 'y': 38, 'score': 0.9747999, 'stack': 2},
            {'id': 'christmas_2018_stocking.png', 'x': 654, 'y': 39, 'score': 0.9461687, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 766, 'y': 39, 'score': 0.94500816, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 98, 'y': 154, 'score': 0.95245135, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 209, 'y': 154, 'score': 0.9782748, 'stack': 3},
            {'id': 'christmas_2018_gold_currency.png', 'x': 321, 'y': 154, 'score': 0.9691067, 'stack': 3},
            {'id': 'qp.png', 'x': 99, 'y': 35, 'score': 0.9931328, 'stack': 0},
            {'id': 'Meteor Horseshoe.png', 'x': 211, 'y': 40, 'score': 0.9307036, 'stack': 0},
            {'id': 'Yggdrassil Seed.png', 'x': 320, 'y': 39, 'score': 0.96452254, 'stack': 0},
            {'id': 'christmas_2018_silver_currency.png', 'x': 432, 'y': 154, 'score': 0.9605768, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 544, 'y': 154, 'score': 0.97842664, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 655, 'y': 154, 'score': 0.95285255, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 766, 'y': 154, 'score': 0.9602521, 'stack': 3},
            {'id': 'christmas_2018_silver_currency.png', 'x': 98, 'y': 269, 'score': 0.96674824, 'stack': 3},
            {'id': 'christmas_2018_silver_currency.png', 'x': 210, 'y': 269, 'score': 0.98304373, 'stack': 3}]},
        '01-bmlzv6z.png': {'qp_gained': 6400, 'qp_total': 324783641, 'drop_count': 12, 'drops_found': 13, 'drops': [
            {'id': 'christmas_2018_stocking.png', 'x': 390, 'y': 8, 'score': 1.0, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 502, 'y': 8, 'score': 1.0, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 725, 'y': 8, 'score': 0.9913225, 'stack': 3},
            {'id': 'christmas_2018_gold_currency.png', 'x': 613, 'y': 9, 'score': 0.9727627, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 279, 'y': 122, 'score': 0.9948097, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 390, 'y': 122, 'score': 0.99124193, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 501, 'y': 122, 'score': 0.9732004, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 613, 'y': 122, 'score': 1.0, 'stack': 3},
            {'id': 'Yggdrassil Seed.png', 'x': 167, 'y': 8, 'score': 0.9358185, 'stack': 0},
            {'id': 'Caster Monument.png', 'x': 281, 'y': 9, 'score': 0.931241, 'stack': 0},
            {'id': 'christmas_2018_silver_currency.png', 'x': 57, 'y': 123, 'score': 0.9825888, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 168, 'y': 123, 'score': 0.99999964, 'stack': 2}]},
        '01-GxW18aS.png': {'qp_gained': 6400, 'qp_total': 322856241, 'drop_count': 15, 'drops_found': 16, 'drops': [
            {'id': 'christmas_2018_stocking.png', 'x': 278, 'y': 8, 'score': 0.96391135, 'stack': 3},
            {'id': 'christmas_2018_stocking.png', 'x': 390, 'y': 8, 'score': 0.999998, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 502, 'y': 8, 'score': 0.9999991, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 725, 'y': 8, 'score': 0.9913195, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 613, 'y': 9, 'score': 0.9727501, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 57, 'y': 123, 'score': 0.9633587, 'stack': 3},
            {'id': 'christmas_2018_gold_currency.png', 'x': 168, 'y': 123, 'score': 0.99690706, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 501, 'y': 122, 'score': 0.9731538, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 613, 'y': 122, 'score': 0.99999934, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 724, 'y': 122, 'score': 0.98423046, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 56, 'y': 237, 'score': 0.9976314, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 167, 'y': 237, 'score': 0.9772536, 'stack': 3},
            {'id': 'Caster Monument.png', 'x': 169, 'y': 9, 'score': 0.9196835, 'stack': 0},
            {'id': 'christmas_2018_silver_currency.png', 'x': 279, 'y': 123, 'score': 0.981111, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 391, 'y': 123, 'score': 0.99220085, 'stack': 3}]},
        '01-hFeQVAp.png': {'qp_gained': 6400, 'qp_total': 322693641, 'drop_count': 12, 'drops_found': 13, 'drops': [
            {'id': 'christmas_2018_stocking.png', 'x': 167, 'y': 8, 'score': 0.9917377, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 279, 'y': 8, 'score': 0.9897186, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 391, 'y': 8, 'score': 0.9804832, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 502, 'y': 8, 'score': 0.99999535, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 501, 'y': 122, 'score': 0.97320855, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 613, 'y': 122, 'score': 0.99999774, 'stack': 3},
            {'id': 'christmas_2018_silver_currency.png', 'x': 613, 'y': 8, 'score': 0.9702901, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 725, 'y': 8, 'score': 0.9978891, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 57, 'y': 123, 'score': 0.98257923, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 168, 'y': 123, 'score': 0.99998873, 'stack': 3},
            {'id': 'christmas_2018_silver_currency.png', 'x': 279, 'y': 123, 'score': 0.98107976, 'stack': 3},
            {'id': 'christmas_2018_silver_currency.png', 'x': 391, 'y': 123, 'score': 0.9922004, 'stack': 3}]},
        '02-FD22Kwk.png': {'qp_gained': 6400, 'qp_total': 324669097, 'drop_count': 12, 'drops_found': 13, 'drops': [
            {'id': 'Shining Gem of Rider.png', 'x': 279, 'y': 7, 'score': 0.98786265, 'stack': 0},
            {'id': 'christmas_2018_stocking.png', 'x': 390, 'y': 8, 'score': 0.99999756, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 502, 'y': 8, 'score': 0.99999744, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 501, 'y': 122, 'score': 0.97316784, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 613, 'y': 122, 'score': 0.99999946, 'stack': 2},
            {'id': 'Meteor Horseshoe.png', 'x': 169, 'y': 10, 'score': 0.91826, 'stack': 0},
            {'id': 'christmas_2018_silver_currency.png', 'x': 613, 'y': 8, 'score': 0.97029674, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 725, 'y': 8, 'score': 0.99788207, 'stack': 3},
            {'id': 'christmas_2018_silver_currency.png', 'x': 57, 'y': 123, 'score': 0.9825938, 'stack': 3},
            {'id': 'christmas_2018_silver_currency.png', 'x': 168, 'y': 123, 'score': 0.9999915, 'stack': 3},
            {'id': 'christmas_2018_silver_currency.png', 'x': 279, 'y': 123, 'score': 0.9810531, 'stack': 3},
            {'id': 'christmas_2018_silver_currency.png', 'x': 391, 'y': 123, 'score': 0.99220395, 'stack': 3}]},
        '02-GiOatR2.png': {'qp_gained': 6400, 'qp_total': 324790041, 'drop_count': 17, 'drops_found': 18, 'drops': [
            {'id': 'Magic Gem of Berserker.png', 'x': 391, 'y': 9, 'score': 0.94785154, 'stack': 0},
            {'id': 'christmas_2018_stocking.png', 'x': 501, 'y': 8, 'score': 0.98070735, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 725, 'y': 8, 'score': 0.99131703, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 613, 'y': 9, 'score': 0.9727803, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 57, 'y': 123, 'score': 0.963349, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 168, 'y': 123, 'score': 0.9969291, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 279, 'y': 123, 'score': 0.9891505, 'stack': 3},
            {'id': 'Secret Gem of Berserker.png', 'x': 280, 'y': 11, 'score': 0.8657291, 'stack': 0},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 724, 'y': 122, 'score': 0.9844743, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 56, 'y': 237, 'score': 0.9976318, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 167, 'y': 237, 'score': 0.9770152, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 279, 'y': 237, 'score': 0.99477315, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 390, 'y': 237, 'score': 0.99080986, 'stack': 3},
            {'id': 'Meteor Horseshoe.png', 'x': 169, 'y': 10, 'score': 0.91825753, 'stack': 0},
            {'id': 'christmas_2018_silver_currency.png', 'x': 391, 'y': 123, 'score': 0.99232167, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 502, 'y': 123, 'score': 0.9976974, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 613, 'y': 123, 'score': 0.9707756, 'stack': 3}]},
        '02-tLmaw1B.png': {'qp_gained': 6400, 'qp_total': 322700041, 'scroll_position': -1, 'drop_count': 13, 'drops_found': 14, 'drops': [
            {'id': 'christmas_2018_stocking.png', 'x': 169, 'y': 41, 'score': 0.9722836, 'stack': 2},
            {'id': 'christmas_2018_stocking.png', 'x': 280, 'y': 42, 'score': 0.94110185, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 392, 'y': 42, 'score': 0.94202393, 'stack': 3},
            {'id': 'christmas_2018_gold_currency.png', 'x': 503, 'y': 42, 'score': 0.9664916, 'stack': 3},
            {'id': 'qp.png', 'x': 59, 'y': 38, 'score': 0.99245167, 'stack': 0},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 391, 'y': 156, 'score': 0.9849315, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 503, 'y': 156, 'score': 0.9597115, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 614, 'y': 156, 'score': 0.9815834, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 725, 'y': 156, 'score': 0.985537, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 615, 'y': 42, 'score': 0.9412312, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 726, 'y': 42, 'score': 0.949545, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 58, 'y': 157, 'score': 0.9581784, 'stack': 3},
            {'id': 'christmas_2018_silver_currency.png', 'x': 170, 'y': 157, 'score': 0.9739863, 'stack': 3},
            {'id': 'christmas_2018_silver_currency.png', 'x': 281, 'y': 157, 'score': 0.94831735, 'stack': 3}]},
        '02-YlcWZiO.png': {'qp_gained': 6400, 'qp_total': 322862641, 'scroll_position': 7, 'drop_count': 19, 'drops_found': 20, 'drops': [
            {'id': 'christmas_2018_stocking.png', 'x': 503, 'y': 41, 'score': 0.97205406, 'stack': 3},
            {'id': 'christmas_2018_stocking.png', 'x': 726, 'y': 41, 'score': 0.97753465, 'stack': 2},
            {'id': 'christmas_2018_stocking.png', 'x': 614, 'y': 42, 'score': 0.94366634, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 58, 'y': 157, 'score': 0.9492307, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 169, 'y': 157, 'score': 0.97450423, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 281, 'y': 157, 'score': 0.9651268, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 392, 'y': 157, 'score': 0.94893163, 'stack': 3},
            {'id': 'christmas_2018_gold_currency.png', 'x': 503, 'y': 157, 'score': 0.97439176, 'stack': 3},
            {'id': 'Octuplet Twin Crystals.png', 'x': 281, 'y': 43, 'score': 0.9514849, 'stack': 0},
            {'id': 'qp.png', 'x': 59, 'y': 38, 'score': 0.9924515, 'stack': 0},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 169, 'y': 271, 'score': 0.9616293, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 280, 'y': 271, 'score': 0.9826795, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 391, 'y': 271, 'score': 0.98688877, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 503, 'y': 271, 'score': 0.96134824, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 614, 'y': 271, 'score': 0.98324305, 'stack': 3},
            {'id': 'Yggdrassil Seed.png', 'x': 391, 'y': 42, 'score': 0.9630994, 'stack': 0},
            {'id': 'Talon of Chaos.png', 'x': 172, 'y': 41, 'score': 0.9258257, 'stack': 0},
            {'id': 'christmas_2018_silver_currency.png', 'x': 615, 'y': 157, 'score': 0.948523, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 726, 'y': 157, 'score': 0.9562779, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 58, 'y': 272, 'score': 0.96317625, 'stack': 3}]}
         }

        base_path = os.path.join(os.getcwd(), 'test_data', 'xmas_2018_expert_revo')
        for file in expected.keys():
            expected_result = prepare_for_comparison(expected[file])
            result = prepare_for_comparison(fgo_mat_counter.run(os.path.join(base_path, file), DEBUG, VERBOSE))
            self.assertEqual(expected_result, result)

    @unittest.skip
    def test_valentine_2019_expert_knights(self):
        self.maxDiff = None
        expected = {'qp_gained': 6400, 'qp_total': 170761518, 'scroll_position': 0, 'drop_count': 19, 'drops_found': 20, 'drops': [{'id': 'Archer Piece.png', 'x': 169, 'y': 24, 'score': 0.9497172, 'stack': 0}, {'id': 'qp.png', 'x': 57, 'y': 18, 'score': 0.9961114, 'stack': 0}, {'id': 'valentine_2019_saber_coin.png', 'x': 279, 'y': 21, 'score': 0.96185666, 'stack': 2}, {'id': 'valentine_2019_saber_coin.png', 'x': 391, 'y': 21, 'score': 0.9453553, 'stack': 2}, {'id': 'valentine_2019_saber_coin.png', 'x': 502, 'y': 21, 'score': 0.9788375, 'stack': 2}, {'id': 'valentine_2019_saber_coin.png', 'x': 613, 'y': 21, 'score': 0.9396837, 'stack': 2}, {'id': 'valentine_2019_lancer_coin.png', 'x': 168, 'y': 136, 'score': 0.95286167, 'stack': 2}, {'id': 'valentine_2019_lancer_coin.png', 'x': 56, 'y': 137, 'score': 0.9263724, 'stack': 2}, {'id': 'valentine_2019_all_coin.png', 'x': 502, 'y': 137, 'score': 0.9618784, 'stack': 2}, {'id': 'valentine_2019_archer_coin.png', 'x': 724, 'y': 21, 'score': 0.9435896, 'stack': 2}, {'id': 'valentine_2019_all_coin.png', 'x': 391, 'y': 131, 'score': 0.9674793, 'stack': 2}, {'id': 'valentine_2019_all_coin.png', 'x': 279, 'y': 132, 'score': 0.93297756, 'stack': 2}, {'id': 'valentine_2019_choco.png', 'x': 613, 'y': 128, 'score': 0.99094504, 'stack': 6}, {'id': 'valentine_2019_choco.png', 'x': 725, 'y': 128, 'score': 0.99210346, 'stack': 7}, {'id': 'valentine_2019_choco.png', 'x': 57, 'y': 243, 'score': 0.98842907, 'stack': 7}, {'id': 'valentine_2019_choco.png', 'x': 168, 'y': 243, 'score': 0.9940306, 'stack': 7}, {'id': 'valentine_2019_choco.png', 'x': 279, 'y': 243, 'score': 0.993614, 'stack': 6}, {'id': 'valentine_2019_choco.png', 'x': 391, 'y': 243, 'score': 0.9881494, 'stack': 7}, {'id': 'valentine_2019_choco.png', 'x': 502, 'y': 243, 'score': 0.995087, 'stack': 7}, {'id': 'valentine_2019_choco.png', 'x': 613, 'y': 243, 'score': 0.99105835, 'stack': 7}]}

        test_image = os.path.join(os.getcwd(), 'test_data', 'valentine_2019_expert_knight.png')
        expected = prepare_for_comparison(expected)
        result = prepare_for_comparison(fgo_mat_counter.run(test_image, DEBUG, VERBOSE))
        self.assertEqual(expected, result)


class TestSpecialCases(unittest.TestCase):
    def test_red_filter(self):
        self.maxDiff = None
        expected = {'qp_gained': 2288900, 'qp_total': 106845904, 'drop_count': 8, 'drops_found': 4, 'drops': [
            {'id': 'Shining Gem of Saber.png', 'x': 390, 'y': 5, 'score': '0.97447186', 'stack': 0},
            {'id': 'Bloodstone Tear.png', 'x': 169, 'y': 7, 'score': '0.92565679', 'stack': 0},
            {'id': 'Void Dust.png', 'x': 279, 'y': 6, 'score': '0.97221052', 'stack': 0}]}

        test_image = os.path.join(os.getcwd(), 'test_data', 'samsung_s9_red_filter_43_percent.jpg')
        expected = prepare_for_comparison(expected)
        result = prepare_for_comparison(fgo_mat_counter.run(test_image, DEBUG, VERBOSE))
        self.assertEqual(expected, result)

    def test_blue_and_black_borders(self):
        expected = {'qp_gained': 668900, 'qp_total': 755521417, 'drop_count': 6, 'drops_found': 4, 'drops': [
            {'id': 'Shining Gem of Assassin.png', 'x': 390, 'y': 7, 'score': '0.97608447', 'stack': 0},
            {'id': 'Magic Gem of Assassin.png', 'x': 280, 'y': 8, 'score': '0.95031976', 'stack': 0},
            {'id': 'Homunculus Baby.png', 'x': 168, 'y': 9, 'score': '0.94004923', 'stack': 0}]}

        test_image = os.path.join(os.getcwd(), 'test_data', 'black_and_blue_border.jpg')
        expected = prepare_for_comparison(expected)
        result = prepare_for_comparison(fgo_mat_counter.run(test_image, DEBUG, VERBOSE))
        self.assertEqual(expected, result)

    def test_blue_and_black_borders_light_background(self):
        expected = {'qp_gained': 668900, 'qp_total': 755521417, 'drop_count': 6, 'drops_found': 4, 'drops': [
            {'id': 'Shining Gem of Assassin.png', 'x': 390, 'y': 7, 'score': '0.97608447', 'stack': 0},
            {'id': 'Magic Gem of Assassin.png', 'x': 280, 'y': 8, 'score': '0.95031976', 'stack': 0},
            {'id': 'Homunculus Baby.png', 'x': 168, 'y': 9, 'score': '0.94004923', 'stack': 0}]}

        test_image = os.path.join(os.getcwd(), 'test_data', 'black_and_blue_border_light_bg.jpg')
        expected = prepare_for_comparison(expected)
        result = prepare_for_comparison(fgo_mat_counter.run(test_image, DEBUG, VERBOSE))
        self.assertEqual(expected, result)

    def test_side_bottom_blue_border(self):
        self.maxDiff = None
        expected = {'qp_gained': 8400, 'qp_total': 710822575, 'scroll_position': 6, 'drop_count': 26, 'drops_found': 21, 'drops': [
            {'id': 'Magic Gem of Assassin.png', 'x': 434, 'y': 41, 'score': 0.96025664, 'stack': 0},
            {'id': 'Secret Gem of Assassin.png', 'x': 323, 'y': 43, 'score': 0.9598375, 'stack': 0},
            {'id': 'qp.png', 'x': 99, 'y': 38, 'score': 0.9829458, 'stack': 0},
            {'id': 'Forbidden Page.png', 'x': 211, 'y': 42, 'score': 0.8997853, 'stack': 0},
            {'id': 'valentine_2019_all_coin.png', 'x': 321, 'y': 272, 'score': 0.90158486, 'stack': 2},
            {'id': 'valentine_2019_all_coin.png', 'x': 432, 'y': 273, 'score': 0.9250845, 'stack': 2},
            {'id': 'valentine_2019_all_coin.png', 'x': 543, 'y': 273, 'score': 0.9201694, 'stack': 2},
            {'id': 'valentine_2019_choco.png', 'x': 655, 'y': 263, 'score': 0.9946576, 'stack': 5},
            {'id': 'valentine_2019_choco.png', 'x': 766, 'y': 263, 'score': 0.99599785, 'stack': 6},
            {'id': 'valentine_2019_assassin_coin.png', 'x': 544, 'y': 38, 'score': 0.98066664, 'stack': 2},
            {'id': 'valentine_2019_assassin_coin.png', 'x': 655, 'y': 38, 'score': 0.9589955, 'stack': 2},
            {'id': 'valentine_2019_assassin_coin.png', 'x': 766, 'y': 38, 'score': 0.95111924, 'stack': 2},
            {'id': 'valentine_2019_assassin_coin.png', 'x': 99, 'y': 153, 'score': 0.9761495, 'stack': 2},
            {'id': 'valentine_2019_assassin_coin.png', 'x': 210, 'y': 153, 'score': 0.96693873, 'stack': 2},
            {'id': 'valentine_2019_assassin_coin.png', 'x': 321, 'y': 153, 'score': 0.9287545, 'stack': 2},
            {'id': 'valentine_2019_assassin_coin.png', 'x': 432, 'y': 153, 'score': 0.96463794, 'stack': 2},
            {'id': 'valentine_2019_assassin_coin.png', 'x': 544, 'y': 153, 'score': 0.9754859, 'stack': 2},
            {'id': 'valentine_2019_assassin_coin.png', 'x': 655, 'y': 153, 'score': 0.95365816, 'stack': 2},
            {'id': 'valentine_2019_assassin_coin.png', 'x': 766, 'y': 153, 'score': 0.94732016, 'stack': 2},
            {'id': 'valentine_2019_assassin_coin.png', 'x': 99, 'y': 268, 'score': 0.9704671, 'stack': 2},
            {'id': 'valentine_2019_assassin_coin.png', 'x': 210, 'y': 268, 'score': 0.960992, 'stack': 2}]}

        test_image = os.path.join(os.getcwd(), 'test_data', 'side_bottom_blue_borders.png')
        expected = prepare_for_comparison(expected)
        result = prepare_for_comparison(fgo_mat_counter.run(test_image, DEBUG, VERBOSE))
        self.assertEqual(expected, result)

    def test_touch_mark(self):
        self.maxDiff = None
        expected = {'qp_gained': 9400, 'qp_total': 975005193, 'drop_count': 29, 'drops_found': 16, 'drops':
            [{'id': 'valentine_2019_saber_coin.png', 'x': 0, 'y': 0, 'stack': 2},
             {'id': 'valentine_2019_all_coin.png', 'x': 1, 'y': 0, 'stack': 3},
             {'id': 'valentine_2019_all_coin.png', 'x': 2, 'y': 0, 'stack': 3},
             {'id': 'valentine_2019_all_coin.png', 'x': 3, 'y': 0, 'stack': 3},
             {'id': 'valentine_2019_all_coin.png', 'x': 4, 'y': 0, 'stack': 3},
             {'id': 'valentine_2019_all_coin.png', 'x': 5, 'y': 0, 'stack': 3},
             {'id': 'valentine_2019_choco.png', 'x': 6, 'y': 0, 'stack': 6},
             {'id': 'valentine_2019_choco.png', 'x': 0, 'y': 1, 'stack': 6},
             {'id': 'valentine_2019_choco.png', 'x': 1, 'y': 1, 'stack': 6},
             {'id': 'valentine_2019_choco.png', 'x': 2, 'y': 1, 'stack': 6},
             {'id': 'valentine_2019_choco.png', 'x': 3, 'y': 1, 'stack': 6},
             {'id': 'valentine_2019_choco.png', 'x': 4, 'y': 1, 'stack': 6},
             {'id': 'valentine_2019_choco.png', 'x': 5, 'y': 1, 'stack': 6},
             {'id': 'valentine_2019_choco.png', 'x': 6, 'y': 1, 'stack': 6},
             {'id': 'valentine_2019_choco.png', 'x': 0, 'y': 2, 'stack': 6},
             {'id': 'valentine_2019_choco.png', 'x': 1, 'y': 2, 'stack': 6}]}

        test_image = pathlib.Path(__file__).parent / 'test_data' / 'touch_mark.png'
        result = prepare_for_comparison(fgo_mat_counter.run(test_image, DEBUG, VERBOSE))
        self.assertEqual(expected, result)

    def test_ui_overlay(self):
        self.maxDiff = None
        expected = {'drops_found': 19, 'qp_gained': 8400, 'qp_total': 640637232, 'drop_count': 25, 'drops': [
           {'id': 'guda2_shinsengumi_point.png', 'stack': 500, 'x': 0, 'y': 0},
           {'id': 'guda2_shinsengumi_point.png', 'stack': 500, 'x': 1, 'y': 0},
           {'id': 'guda2_shinsengumi_point.png', 'stack': 500, 'x': 2, 'y': 0},
           {'id': 'guda2_shinsengumi_point.png', 'stack': 1000, 'x': 3, 'y': 0},
           {'id': 'guda2_shinsengumi_point.png', 'stack': 1000, 'x': 4, 'y': 0},
           {'id': 'guda2_gold_currency.png', 'stack': 3, 'x': 5, 'y': 0},
           {'id': 'guda2_gold_currency.png', 'stack': 3, 'x': 6, 'y': 0},
           {'id': 'guda2_gold_currency.png', 'stack': 6, 'x': 0, 'y': 1},
           {'id': 'guda2_gold_currency.png', 'stack': 2, 'x': 1, 'y': 1},
           {'id': 'guda2_silver_currency.png', 'stack': 3, 'x': 2, 'y': 1},
           {'id': 'guda2_silver_currency.png', 'stack': 2, 'x': 3, 'y': 1},
           {'id': 'guda2_silver_currency.png', 'stack': 2, 'x': 4, 'y': 1},
           {'id': 'guda2_silver_currency.png', 'stack': 6, 'x': 5, 'y': 1},
           {'id': 'guda2_silver_currency.png', 'stack': 2, 'x': 6, 'y': 1},
           {'id': 'guda2_bronze_currency.png', 'stack': 3, 'x': 0, 'y': 2},
           {'id': 'guda2_bronze_currency.png', 'stack': 2, 'x': 1, 'y': 2},
           {'id': 'guda2_bronze_currency.png', 'stack': 6, 'x': 2, 'y': 2},
           {'id': 'guda2_bronze_currency.png', 'stack': 6, 'x': 3, 'y': 2},
           {'id': 'guda2_bronze_currency.png', 'stack': 2, 'x': 4, 'y': 2}]}

        test_image = pathlib.Path(__file__).parent / 'test_data' / 'Screenshot_20190329-114404_Fate_GO.jpg'
        result = prepare_for_comparison(fgo_mat_counter.run(test_image, DEBUG, VERBOSE))
        self.assertEqual(expected, result)


class TestScrollBarLocation(unittest.TestCase):
    def test_scroll_at_top(self):
        test_image = os.path.join(os.getcwd(), 'test_data', 'da_vinci.png')
        res = fgo_mat_counter.run(test_image, DEBUG, VERBOSE)
        self.assertNotEqual(-1, res['scroll_position'])

    def test_scroll_at_top2(self):
        test_image = os.path.join(os.getcwd(), 'test_data', 'Screenshot_20181205-153908_Fate_GO.jpg')
        res = fgo_mat_counter.run(test_image, DEBUG, VERBOSE)
        self.assertNotEqual(-1, res['scroll_position'])

    def test_no_scroll_bar(self):
        test_image = os.path.join(os.getcwd(), 'test_data', 'black_and_blue_border.jpg')
        res = fgo_mat_counter.run(test_image, DEBUG, VERBOSE)
        self.assertEqual(-1, res['scroll_position'])

    # Note: this is the test that fails to find the stack size of the valentine chocos and doesn't fail despite
    # generating long list of error messages.
    def test_scroll_bar_at_bottom(self):
        test_image = os.path.join(os.getcwd(), 'test_data', 'scrolled_down.png')
        res = fgo_mat_counter.run(test_image, DEBUG, VERBOSE)
        self.assertLess(0.05, res['scroll_position'])


class TestFrontend(unittest.TestCase):
    def test_location_normalization_one_row(self):
        input_data = [
            {'id': 'Shining Gem of Saber.png', 'x': 390, 'y': 5, 'score': '0.97447186', 'stack': 0},
            {'id': 'Bloodstone Tear.png', 'x': 169, 'y': 7, 'score': '0.92565679', 'stack': 0},
            {'id': 'Void Dust.png', 'x': 279, 'y': 6, 'score': '0.97221052', 'stack': 0}]

        expected = [
            {'id': 'Shining Gem of Saber.png', 'x': 3, 'y': 0, 'score': '0.97447186', 'stack': 0},
            {'id': 'Bloodstone Tear.png', 'x': 1, 'y': 0, 'score': '0.92565679', 'stack': 0},
            {'id': 'Void Dust.png', 'x': 2, 'y': 0, 'score': '0.97221052', 'stack': 0}]

        self.assertEqual(expected, frontend.normalize_drop_locations(input_data))

    def test_location_normalization_three_rows(self):
        input_data = [
            {'id': 'christmas_2018_stocking.png', 'x': 503, 'y': 41, 'score': 0.97205406, 'stack': 3},
            {'id': 'christmas_2018_stocking.png', 'x': 726, 'y': 41, 'score': 0.97753465, 'stack': 2},
            {'id': 'christmas_2018_stocking.png', 'x': 614, 'y': 42, 'score': 0.94366634, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 58, 'y': 157, 'score': 0.9492307, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 169, 'y': 157, 'score': 0.97450423, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 281, 'y': 157, 'score': 0.9651268, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 392, 'y': 157, 'score': 0.94893163, 'stack': 3},
            {'id': 'christmas_2018_gold_currency.png', 'x': 503, 'y': 157, 'score': 0.97439176, 'stack': 3},
            {'id': 'Octuplet Twin Crystals.png', 'x': 281, 'y': 43, 'score': 0.9514849, 'stack': 0},
            {'id': 'qp.png', 'x': 59, 'y': 38, 'score': 0.9924515, 'stack': 0},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 169, 'y': 271, 'score': 0.9616293, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 280, 'y': 271, 'score': 0.9826795, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 391, 'y': 271, 'score': 0.98688877, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 503, 'y': 271, 'score': 0.96134824, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 614, 'y': 271, 'score': 0.98324305, 'stack': 3},
            {'id': 'Yggdrassil Seed.png', 'x': 391, 'y': 42, 'score': 0.9630994, 'stack': 0},
            {'id': 'Talon of Chaos.png', 'x': 172, 'y': 41, 'score': 0.9258257, 'stack': 0},
            {'id': 'christmas_2018_silver_currency.png', 'x': 615, 'y': 157, 'score': 0.948523, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 726, 'y': 157, 'score': 0.9562779, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 58, 'y': 272, 'score': 0.96317625, 'stack': 3}]

        expected = [
            {'id': 'christmas_2018_stocking.png', 'x': 4, 'y': 0, 'score': 0.97205406, 'stack': 3},
            {'id': 'christmas_2018_stocking.png', 'x': 6, 'y': 0, 'score': 0.97753465, 'stack': 2},
            {'id': 'christmas_2018_stocking.png', 'x': 5, 'y': 0, 'score': 0.94366634, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 0, 'y': 1, 'score': 0.9492307, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 1, 'y': 1, 'score': 0.97450423, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 2, 'y': 1, 'score': 0.9651268, 'stack': 2},
            {'id': 'christmas_2018_gold_currency.png', 'x': 3, 'y': 1, 'score': 0.94893163, 'stack': 3},
            {'id': 'christmas_2018_gold_currency.png', 'x': 4, 'y': 1, 'score': 0.97439176, 'stack': 3},
            {'id': 'Octuplet Twin Crystals.png', 'x': 2, 'y': 0, 'score': 0.9514849, 'stack': 0},
            {'id': 'qp.png', 'x': 0, 'y': 0, 'score': 0.9924515, 'stack': 0},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 1, 'y': 2, 'score': 0.9616293, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 2, 'y': 2, 'score': 0.9826795, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 3, 'y': 2, 'score': 0.98688877, 'stack': 2},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 4, 'y': 2, 'score': 0.96134824, 'stack': 3},
            {'id': 'christmas_2018_bronze_currency.png', 'x': 5, 'y': 2, 'score': 0.98324305, 'stack': 3},
            {'id': 'Yggdrassil Seed.png', 'x': 3, 'y': 0, 'score': 0.9630994, 'stack': 0},
            {'id': 'Talon of Chaos.png', 'x': 1, 'y': 0, 'score': 0.9258257, 'stack': 0},
            {'id': 'christmas_2018_silver_currency.png', 'x': 5, 'y': 1, 'score': 0.948523, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 6, 'y': 1, 'score': 0.9562779, 'stack': 2},
            {'id': 'christmas_2018_silver_currency.png', 'x': 0, 'y': 2, 'score': 0.96317625, 'stack': 3}]

        self.assertEqual(expected, frontend.normalize_drop_locations(input_data))


if __name__ == '__main__':
    unittest.main()
