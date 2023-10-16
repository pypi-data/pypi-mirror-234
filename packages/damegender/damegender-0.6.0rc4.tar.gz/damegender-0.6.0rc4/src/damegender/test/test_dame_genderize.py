#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright (C) 2020  David Arroyo Menéndez (davidam@gmail.com)
# This file is part of Damegender.

# Author: David Arroyo Menéndez <davidam@gmail.com>
# Maintainer: David Arroyo Menéndez <davidam@gmail.com>

# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.

# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with DameGender; see the file GPL.txt.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA,

import unittest
from app.dame_genderize import DameGenderize
from app.dame_utils import DameUtils
import collections
collections.Callable = collections.abc.Callable

dg = DameGenderize()
du = DameUtils()

if (dg.config['DEFAULT']['genderize'] == 'yes'):
    url = 'https://genderize.io'
    if not(du.check_connection(url, error_message="", timeout=10)):
        exit("We can't reach %s. You need Internet connection executing Genderize tests" % url)


class TddInPythonExample(unittest.TestCase):

    def test_dame_genderize_get(self):
        if (dg.config['DEFAULT']['genderize'] == 'yes'):
            string1 = dg.get("peter")
            self.assertEqual(string1, {'probability': 1.0, 'count': 1094417,
                                       'name': 'peter', 'gender': 'male'})
            string2 = dg.get(name="peter", surname="smith", country_id="US")
            self.assertEqual(string2, {'count': 230056, 'country_id': 'US',
                                       'gender': 'male', 'name': 'peter',
                                       'probability': 1.0})

    def test_dame_genderize_get2to10(self):
        if (dg.config['DEFAULT']['genderize'] == 'yes'):
            string1 = dg.get2to10(["peter", "lois", "stevie"])
            self.assertEqual(string1, [{'count': 1094417, 'gender': 'male',
                                        'name': 'peter', 'probability': 1.0},
                                       {'count': 50141, 'gender': 'female',
                                        'name': 'lois', 'probability': 0.98},
                                       {'count': 2840, 'gender': 'male',
                                        'name': 'stevie',
                                        'probability': 0.86}])
            string2 = dg.get2to10(["peter", "lois", "stevie", "john",
                                   "paul", "mike", "mary", "anna"])
            self.assertEqual(string2, [{"name": "peter", "gender": "male",
                                        "probability": 1.0, "count": 1094417},
                                       {'count': 50141, 'gender': 'female',
                                        'name': 'lois', 'probability': 0.98},
                                       {'count': 2840, 'gender': 'male',
                                        'name': 'stevie', 'probability': 0.86},
                                       {"name": "john", "gender": "male",
                                        "probability": 1.0, "count": 2274744},
                                       {"name": "paul", "gender": "male",
                                        "probability": 1.0, "count": 1200479},
                                       {"name": "mike", "gender": "male",
                                        "probability": 1.0, "count": 970635},
                                       {"name": "mary", "gender": "female",
                                        "probability": 1.0, "count": 1011867},
                                       {"name": "anna", "gender": "female",
                                        "probability": 0.99,
                                        "count": 1149231}])

    def test_dame_genderize_guess(self):
        if (dg.config['DEFAULT']['genderize'] == 'yes'):
            self.assertEqual(dg.guess("David"), "male")
            self.assertEqual(dg.guess("David", gender_encoded=True), 1)

    def test_dame_genderize_prob(self):
        if (dg.config['DEFAULT']['genderize'] == 'yes'):
            self.assertEqual(dg.prob("David"), 1.0)

    def test_dame_genderize_guess_list(self):
        path1 = "files/names/genderizefiles_names_min.csv.json"
        gl1 = dg.json2gender_list(jsonf=path1,
                                  gender_encoded=True)
        self.assertEqual(gl1, [1, 1, 1, 1, 1, 0])
        path2 = "files/names/genderizefiles_names_partialnoundefined.csv.json"
        gl2 = dg.json2gender_list(jsonf=path2,
                                  gender_encoded=True)
        self.assertEqual(gl2, [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1,
                               1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1,
                               1, 1, 1, 1, 1])
        # path3 = "files/names/genderizefiles_names_allnoundefined0.csv.json"
        # gl3 = dg.json2gender_list(jsonf=path3,
        #                           gender_encoded=True)
        # self.assertEqual(gl3, [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        #                        0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        #                        1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1,
        #                        1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0,
        #                        1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        #                        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1,
        #                        1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0,
        #                        1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
        #                        1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1,
        #                        1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        #                        1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1,
        #                        1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1,
        #                        1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1,
        #                        0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        #                        1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1,
        #                        0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1,
        #                        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        #                        1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0,
        #                        1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1,
        #                        1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1,
        #                        1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1,
        #                        1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1,
        #                        1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1,
        #                        1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1,
        #                        1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1,
        #                        1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1,
        #                        1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0,
        #                        0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1,
        #                        1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        #                        1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1,
        #                        1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1,
        #                        1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0,
        #                        1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1,
        #                        1, 1, 1])

    # # def test_dame_genderize_limit_p(self):
    # #     dg = DameGenderize()
    # #     self.assertEqual(dg.limit_exceeded_p(), 1)

    def test_dame_genderize_csv2gender_list(self):
        gl = dg.csv2gender_list(path="files/names/partial.csv")
        self.assertEqual(gl, [1, 1, 1, 1, 2, 1, 0, 0, 1, 1,
                              2, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1])
        self.assertEqual(len(gl), 21)
        self.assertEqual(dg.females, 3)
        self.assertEqual(dg.males, 16)
        self.assertEqual(dg.unknown, 2)

    # def test_dame_genderize_guess_list(self):
    #     dg = DameGenderize()
    #     path1 = "files/names/partial.csv"
    #     l1 = dg.guess_list(path=path1, gender_encoded=False, total="us")[0:10]
    #     l2 = dg.guess_list(path=path1, gender_encoded=True, total="us")[0:10]
    #     if (dg.config['DEFAULT']['genderize'] == 'yes'):
    #         self.assertEqual(['male', 'male', 'male', 'male',
    #                           'male', 'male', 'female',
    #                           'female', 'male', 'male'], l1)
    #         self.assertEqual([1, 1, 1, 1, 1, 1, 0, 0, 1, 1], l2)

    def test_dame_genderize_json2names(self):
        path = "files/names/genderizefiles_names_min.csv.json"
        l1 = dg.json2names(jsonf=path)
        self.assertEqual(['Pierre', 'Raul', 'Adriano', 'Ralf',
                          'Guillermo', 'Sabina'], l1)
