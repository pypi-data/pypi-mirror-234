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
import os
from app.dame_utils import DameUtils
from app.dame_statistics import DameStatistics
from app.dame_namsor import DameNamsor
from app.dame_gender import Gender
import collections
collections.Callable = collections.abc.Callable

du = DameUtils()
dn = DameNamsor()

if (dn.config['DEFAULT']['namsor'] == 'yes'):
    url = 'https://v2.namsor.com'
    if not(du.check_connection(url, error_message="", timeout=10)):
        exit("We can't reach https://v2.namsor.com. You need Internet connection executing NamSor tests")

class TddInPythonExample(unittest.TestCase):

    # init method is not being implemented, now
    # def test_dame_namsor_init(self):
    #     self.assertEqual(dn.males, 0)
    #     self.assertEqual(dn.females, 0)
    #     self.assertEqual(dn.unknown, 0)

    def test_dame_namsor_get(self):
        if (dn.config['DEFAULT']['namsor'] == 'yes'):
            l1 = dn.get("David", "Arroyo", gender_encoded=False)
            self.assertEqual(['male', -1.0], [l1[0], round(l1[1])])
            l2 = dn.get("David", "Arroyo", gender_encoded=True)
            self.assertEqual(['male', -1.0], [l2[0], round(l2[1])])
            l3 = dn.get("Karen", "Arroyo", gender_encoded=True)
            self.assertEqual(['female', 1.0], [l3[0], round(l3[1])])

    def test_dame_namsor_getGeo(self):
        if (dn.config['DEFAULT']['namsor'] == 'yes'):
            l1 = dn.get("David", "Arroyo", gender_encoded=False)
            self.assertEqual(['male', -1.0], [l1[0], round(l1[1])])

    def test_dame_namsor_scale(self):
        if (dn.config['DEFAULT']['namsor'] == 'yes'):
            self.assertEqual(-1.0, round(dn.scale("David", "Arroyo")))

    def test_dame_namsor_gender_guess(self):
        if (dn.config['DEFAULT']['namsor'] == 'yes'):
            self.assertEqual(1, dn.guess("David", "Arroyo", gender_encoded=True))
            self.assertEqual(0, dn.guess("Andrea", "Arroyo", gender_encoded=True))
            self.assertEqual(1, dn.guess("Asdf", "qwer", gender_encoded=True))
            # isoiec5218
            self.assertEqual("male", dn.guess("David", "Arroyo", gender_encoded=False, standard="isoiec5218"))
            self.assertEqual(2, dn.guess("Andrea", "Arroyo", gender_encoded=True, standard="isoiec5218"))
            self.assertEqual(1, dn.guess("Asdf", "qwer", gender_encoded=True, standard="isoiec5218"))
            # rfc6350
            self.assertEqual("m", dn.guess("David", "Arroyo", gender_encoded=True, standard="rfc6350"))
            self.assertEqual("f", dn.guess("Andrea", "Arroyo", gender_encoded=True, standard="rfc6350"))
            self.assertEqual("m", dn.guess("Asdf", "qwer", gender_encoded=True, standard="rfc6350"))

    def test_dame_namsor_csv2gender_list(self):
        gl = dn.csv2gender_list(path="files/names/partial.csv")
        self.assertEqual(gl,
                         [1, 1, 1, 1, 2, 1, 0, 0, 1, 1,
                          2, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1])
        self.assertEqual(len(gl), 21)
        self.assertEqual(dn.females, 3)
        self.assertEqual(dn.males, 16)
        self.assertEqual(dn.unknown, 2)

    def test_dame_namsor_features_list(self):
        fl = dn.features_list()
        self.assertTrue(len(fl) > 20)

    def test_dame_namsor_guess_list(self):
        if (dn.config['DEFAULT']['namsor'] == 'yes'):
            self.assertEqual(['male', 'male', 'male', 'male', 'male', 'male',
                              'female', 'female', 'male', 'male', 'male',
                              'male', 'male', 'male', 'male', 'male', 'male',
                              'male', 'female', 'male', 'male'],
                             dn.guess_list(path="files/names/partial.csv",
                                           gender_encoded=False))
            self.assertEqual([1, 1, 1, 1, 1, 1, 0, 0,
                              1, 1, 1, 1, 1, 1, 1, 1,
                              1, 1, 0, 1, 1],
                             dn.guess_list(path="files/names/partial.csv",
                                           gender_encoded=True))

    def test_dame_namsor_accuracy_score_dame(self):
        ds = DameStatistics()
        if (dn.config['DEFAULT']['namsor'] == 'yes'):
            gl1 = dn.csv2gender_list(path="files/names/partial.csv")
            gl2 = dn.guess_list(path="files/names/partial.csv",
                                gender_encoded=True)
            score1 = ds.accuracy_score_dame(gl1, gl2)
            self.assertTrue(score1 > 0.9)

    def test_dame_namsor_download(self):
        du = DameUtils()
        path1 = "files/names/min.csv"
        if (dn.config['DEFAULT']['namsor'] == 'yes'):
            g = dn.download(path1)
            self.assertTrue(
                os.path.isfile(
                    "files/names/namsor" + du.path2file(path1) + ".json"))

    def test_dame_namsor_json2gender_list(self):
        namsorpath = "files/names/namsorfiles_names_min.csv.json"
        j2gl = dn.json2gender_list(jsonf=namsorpath, gender_encoded=False)
        l1 = ['male', 'male', 'male', 'male', 'male', 'female']
        self.assertEqual(l1, j2gl)
        j2gl = dn.json2gender_list(jsonf=namsorpath, gender_encoded=True)
        l2 = [1, 1, 1, 1, 1, 0]
        self.assertEqual(l2, j2gl)

    def test_dame_namsor_json2names(self):
        l1 = dn.json2names(jsonf="files/names/namsorfiles_names_min.csv.json")
        self.assertEqual(['Pierre', 'Raul', 'Adriano', 'Ralf',
                          'Guillermo', 'Sabina'], l1)
