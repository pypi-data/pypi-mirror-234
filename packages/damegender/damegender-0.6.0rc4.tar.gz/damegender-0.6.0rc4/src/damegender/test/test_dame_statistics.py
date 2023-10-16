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

from app.dame_gender import Gender
from app.dame_statistics import DameStatistics

import unittest
import os
import collections
collections.Callable = collections.abc.Callable


class TddInPythonExample(unittest.TestCase):

    def test_count_true2guess(self):
        ds = DameStatistics()
        v1 = [1, 0, 1, 1, 0, 0]
        v2 = [1, 1, 1, 0, 0, 0]
        self.assertEqual(ds.count_true2guess(v1, v2, 0, 0), 2)  # femalefemale
        self.assertEqual(ds.femalefemale(v1, v2), 2)
        self.assertEqual(ds.count_true2guess(v1, v2, 1, 1), 2)  # malemale
        self.assertEqual(ds.malemale(v1, v2), 2)
        self.assertEqual(ds.count_true2guess(v1, v2, 0, 1), 1)  # femalemale
        self.assertEqual(ds.femalemale(v1, v2), 1)
        self.assertEqual(ds.count_true2guess(v1, v2, 1, 0), 1)  # malefemale
        self.assertEqual(ds.malefemale(v1, v2), 1)
        vv1 = [1, 0, 1, 1, 1]
        vv2 = [1, 1, 1, 0]
        self.assertEqual(ds.count_true2guess(vv2, vv1, 1, 1), 2)  # malemale
        self.assertEqual(ds.count_true2guess(vv2, vv1, 0, 1), 1)  # femalemale
        self.assertEqual(ds.count_true2guess(vv2, vv1, 1, 0), 1)  # malefemale
        vvv1 = [1, 0, 2, 2, 1, 2, 2]
        vvv2 = [2, 0, 1, 2, 0, 2, 1]
        t2g = ds.count_true2guess(vvv1, vvv2, 2, 2)  # undefinedundefined
        self.assertEqual(t2g, 2)
        uu = ds.undefinedundefined(vvv2, vvv1)
        self.assertEqual(uu, 2)
        t3g = ds.count_true2guess(vvv1, vvv2, 2, 1)
        self.assertEqual(t3g, 2)  # undefinedmale
        um = ds.undefinedmale(vvv1, vvv2)
        self.assertEqual(um, 2)
        t4g = ds.count_true2guess(vvv1, vvv2, 1, 2)
        self.assertEqual(t4g, 1)  # maleundefined
        mu = ds.maleundefined(vvv1, vvv2)
        self.assertEqual(mu, 1)
        vvv1 = [0, 0, 0, 0, 1]
        vvv2 = [2, 0, 1, 2, 1]
        t5g = ds.count_true2guess(vvv1, vvv2, 0, 2)
        self.assertEqual(t5g, 2)  # femaleundefined
        vvv1 = [2, 2, 0, 2, 1]
        vvv2 = [2, 0, 1, 2, 1]
        t6g = ds.count_true2guess(vvv1, vvv2, 2, 0)
        self.assertEqual(t6g, 1)  # undefinedfemale

    def test_error_coded(self):
        ds = DameStatistics()
        v1 = [1, 0, 1, 1]
        v2 = [1, 1, 1, 0]
        self.assertEqual(ds.error_coded(v1, v2), 0.5)
        v3 = [1, 0, 1, 1, 2, 1, 2, 0]
        v4 = [1, 1, 1, 0, 2, 0, 1, 0]
        self.assertEqual(ds.error_coded(v3, v4), 0.5)

    def test_error_coded_without_na(self):
        ds = DameStatistics()
        v1 = [1, 0, 1, 1]
        v2 = [1, 1, 1, 0]
        self.assertEqual(ds.error_coded_without_na(v1, v2), 0.5)

    def test_na_coded(self):
        ds = DameStatistics()
        v1 = [0, 1, 1, 1]
        v2 = [2, 0, 1, 1]
        self.assertEqual(ds.na_coded(v1, v2), 0.25)
        v3 = [1, 0, 1, 1, 2, 1, 2, 1]
        v4 = [1, 1, 1, 0, 2, 0, 1, 2]
        self.assertEqual(ds.na_coded(v3, v4), 0.25)

    def test_error_gender_bias(self):
        ds = DameStatistics()
        v1 = [0, 1, 1, 1]
        v2 = [0, 0, 1, 1]
        self.assertEqual(ds.error_gender_bias(v1, v2), 0.25)

    def test_weighted_error(self):
        ds = DameStatistics()
        v1 = [0, 1, 1, 1]
        v2 = [0, 0, 1, 1]
        self.assertEqual(ds.weighted_error(v1, v2, 2), 0.25)

    def test_accuracy_score_dame(self):
        ds = DameStatistics()
        score1 = ds.accuracy_score_dame([1, 1], [1, 1])
        self.assertEqual(score1, 1)
        score2 = ds.accuracy_score_dame([1, 1, 1, 0],
                                        [1, 1, 2, 0])
        self.assertEqual(score2, 0.75)
        score3 = ds.accuracy_score_dame([1, 1, 1, 1, 2, 1],
                                        [1, 1, 1, 1, 2, 1])
        self.assertEqual(score3, 1)
        score4 = ds.accuracy_score_dame([1, 1, 1, 1, 2, 1, 0,
                                         0, 1, 1, 2, 1, 1, 1,
                                         1, 1, 1, 1, 0, 1, 1],
                                        [1, 1, 1, 1, 2, 1, 0,
                                         0, 1, 1, 2, 1, 1, 1,
                                         1, 1, 1, 1, 0, 1, 1])
        self.assertEqual(score4, 1)
        v1 = [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1]
        v2 = [1, 1, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1]
        score5 = ds.accuracy_score_dame(v1, v2)
        self.assertEqual(round(score5, 3), 0.905)
        v1 = [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1]
        v2 = [1, 1, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1]
        score6 = ds.accuracy_score_dame(v1, v2)
        self.assertEqual(round(score6, 3), 0.905)

    def test_precision(self):
        ds = DameStatistics()
        score1 = ds.precision([1, 1], [1, 1])
        self.assertEqual(score1, 1)
        score2 = ds.precision([1, 1, 1, 0], [1, 1, 2, 0])
        self.assertEqual(score2, 1)
        score3 = ds.precision([1, 1, 1, 1, 2, 1], [1, 1, 1, 1, 2, 1])
        self.assertEqual(score3, 1)
        l1 = [1, 1, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1]
        l2 = [1, 1, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1]
        score4 = ds.precision(l1, l2)
        self.assertEqual(score4, 1)

    def test_recall(self):
        ds = DameStatistics()
        score1 = ds.recall([1, 1], [1, 1])
        self.assertEqual(score1, 1)
        score2 = ds.recall([1, 1, 1, 0], [1, 1, 2, 0])
        self.assertEqual(score2, 0.75)
        score3 = ds.recall([1, 1, 1, 1, 2, 1], [1, 1, 1, 1, 2, 1])
        self.assertEqual(score3, 1)
        l1 = [1, 1, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1]
        l2 = [1, 1, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1]
        score4 = ds.recall(l1, l2)
        self.assertEqual(score4, 1)

    def test_f1score(self):
        ds = DameStatistics()
        f1score1 = ds.f1score([1, 1], [1, 1])
        self.assertEqual(f1score1, 1)
        f1score2 = ds.f1score([1, 1, 1, 0], [1, 1, 2, 0])
        self.assertEqual(round(f1score2, 2), 0.86)
        f1score3 = ds.f1score([1, 1, 1, 1, 2, 1], [1, 1, 1, 1, 2, 1])
        self.assertEqual(f1score3, 1)
        l1 = [1, 1, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1]
        l2 = [1, 1, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1]
        f1score4 = ds.f1score(l1, l2)
        self.assertEqual(f1score4, 1)

    def test_confusion_matrix_table(self):
        ds = DameStatistics()
        cmt1 = ds.confusion_matrix_table([1, 2, 1, 1, 0], [1, 0, 0, 1, 0])
        self.assertEqual(cmt1, [[1, 0, 0], [1, 2, 0], [1, 2, 0]])
        l1 = [1, 1, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1]
        l2 = [1, 1, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1]
        cmt2 = ds.confusion_matrix_table(l1, l2)
        self.assertEqual(cmt2, [[3, 0, 0], [0, 16, 0], [0, 16, 0]])

    def test_true_positive(self):
        ds = DameStatistics()
        test = [1, 1, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1]
        guess = [1, 1, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1]
        res = ds.true_positive(test, guess)
        self.assertEqual(res, 16)

    def test_false_negative(self):
        ds = DameStatistics()
        test = [1, 1, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1]
        guess = [1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1]
        res = ds.false_negative(test, guess)
        self.assertEqual(res, 1)

    def test_false_positive(self):
        ds = DameStatistics()
        test = [1, 1, 1, 1]
        guess = [0, 0, 0, 1]
        res = ds.false_positive(test, guess)
        self.assertEqual(res, 3)

    def test_true_negative(self):
        ds = DameStatistics()
        test = [1, 1, 0, 0]
        guess = [1, 0, 0, 1]
        res = ds.true_negative(test, guess)
        self.assertEqual(res, 1)
