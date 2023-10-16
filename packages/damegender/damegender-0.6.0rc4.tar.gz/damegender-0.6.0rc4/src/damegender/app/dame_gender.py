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


import csv
import unidecode
import unicodedata
import configparser
import os
import re
import sys
import json
import datetime

from collections import OrderedDict
from app.dame_utils import DameUtils
from app.dame_statistics import DameStatistics
from app.dame_standards import DameGenderStandards

csv.field_size_limit(3000000)
du = DameUtils()
dst = DameStatistics()
dgs = DameGenderStandards()

class Gender(object):
    # That's the root class in the heritage,
    # apis classes and sexmachine is a gender
    def __init__(self):
        self.config = configparser.RawConfigParser()
        self.config.read('config.cfg')
        self.males = 0
        self.females = 0
        self.unknown = 0

# FEATURES METHODS #

    def features(self, name):
        # features method created to check the nltk classifier
        features = {}
        features["first_letter"] = name[0].lower()
        features["last_letter"] = name[-1].lower()
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            features["count({})".format(letter)] = name.lower().count(letter)
            features["has({})".format(letter)] = (letter in name.lower())
        return features

    def features_int(self, name):
        # features method created to check the scikit classifiers
        features_int = {}
        features_int["first_letter"] = ord(name[0].lower())
        features_int["last_letter"] = ord(name[-1].lower())
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            num = name.lower().count(letter)
            features_int["count({})".format(letter)] = num
        features_int["vocals"] = 0
        for letter1 in 'aeiou':
            for letter2 in name:
                if (letter1 == letter2):
                    features_int["vocals"] = features_int["vocals"] + 1
        features_int["consonants"] = 0
        for letter1 in 'bcdfghjklmnpqrstvwxyz':
            for letter2 in name:
                if (letter1 == letter2):
                    features_int["consonants"] = features_int["consonants"] + 1
        # FIRST LETTER
        if (name[0].lower() in 'aeiou'):
            features_int["first_letter_vocal"] = 1
        else:
            features_int["first_letter_vocal"] = 0
        if (name[0].lower() in 'bcdfghjklmnpqrstvwxyz'):
            features_int["first_letter_consonant"] = 1
        else:
            features_int["first_letter_consonant"] = 0
        # LAST LETTER
        if (name[-1].lower() in 'aeiou'):
            features_int["last_letter_vocal"] = 1
        else:
            features_int["last_letter_vocal"] = 0
        if (name[-1].lower() in 'bcdfghjklmnpqrstvwxyz'):
            features_int["last_letter_consonant"] = 1
        else:
            features_int["last_letter_consonant"] = 0
        # h = hyphen.Hyphenator('en_US')
        # features_int["syllables"] = len(h.syllables(name))
        if (name[-1].lower() == "a"):
            features_int["last_letter_a"] = 1
        else:
            features_int["last_letter_a"] = 0
        if (name[-1].lower() == "o"):
            features_int["last_letter_o"] = 1
        else:
            features_int["last_letter_o"] = 0
        return features_int

    def features_list(self, path='files/names/partial.csv', sexdataset=''):
        # Reads a CSV file specified by the path 'files/names/partial.csv'
        # and extracts the data for each row.
        flist = []
        with open(path) as csvfile:
            sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            next(sexreader, None)
            for row in sexreader:
                name = row[0].title()
                name = name.replace('\"', '')
                flist.append(list(self.features_int(name).values()))
        return flist

    def features_list_categorical(self, path='files/names/partial.csv'):
        # Read a specific CSV file (path='files/names/partial.csv') and
        # create a feature list for each name in the file.
        flist = []
        with open(path) as csvfile:
            sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            next(sexreader, None)
            for row in sexreader:
                name = row[0].title()
                name = name.replace('\"', '')
                l1 = list([self.features_int(name)["first_letter"],
                           self.features_int(name)["last_letter"],
                           self.features_int(name)["last_letter_a"],
                           self.features_int(name)["first_letter_vocal"],
                           self.features_int(name)["last_letter_vocal"],
                           self.features_int(name)["last_letter_consonant"]])
                flist.append(l1)
        return flist

    def features_list_no_categorical(self, path='files/names/partial.csv'):
        # Reads a CSV file specified by the 'path' parameter and extracts
        # non-categorical features from the names contained in it.
        # These features includes the number of letters a-z, the number of
        # vowels, and the number of consonants. The code creates a list
        # called "flist" to store these values, and then returns the list
        # at the end.
        flist = []
        with open(path) as csvfile:
            sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            next(sexreader, None)
            for row in sexreader:
                name = row[0].title()
                name = name.replace('\"', '')
                l1 = list([self.features_int(name)["count(a)"],
                           self.features_int(name)["count(b)"],
                           self.features_int(name)["count(c)"],
                           self.features_int(name)["count(d)"],
                           self.features_int(name)["count(e)"],
                           self.features_int(name)["count(f)"],
                           self.features_int(name)["count(g)"],
                           self.features_int(name)["count(h)"],
                           self.features_int(name)["count(i)"],
                           self.features_int(name)["count(j)"],
                           self.features_int(name)["count(k)"],
                           self.features_int(name)["count(l)"],
                           self.features_int(name)["count(m)"],
                           self.features_int(name)["count(n)"],
                           self.features_int(name)["count(o)"],
                           self.features_int(name)["count(p)"],
                           self.features_int(name)["count(q)"],
                           self.features_int(name)["count(r)"],
                           self.features_int(name)["count(s)"],
                           self.features_int(name)["count(t)"],
                           self.features_int(name)["count(u)"],
                           self.features_int(name)["count(v)"],
                           self.features_int(name)["count(w)"],
                           self.features_int(name)["count(x)"],
                           self.features_int(name)["count(y)"],
                           self.features_int(name)["count(z)"],
                           self.features_int(name)["vocals"],
                           self.features_int(name)["consonants"]])
                flist.append(l1)
        return flist

    def features_list_no_letters(self, path='files/names/partial.csv'):
        # Read a specific CSV file (path='files/names/partial.csv')
        # and create a feature list for each name in the file. These
        # features include the first and last letters of the name,
        # the number of vowels and consonants, whether the first and
        # last letters are vowels or consonants, whether the last
        # letter is "a" or "o".
        flist = []
        with open(path) as csvfile:
            sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            next(sexreader, None)
            for row in sexreader:
                name = row[0].title()
                name = name.replace('\"', '')
                l1 = list([self.features_int(name)["first_letter"],
                           self.features_int(name)["last_letter"],
                           self.features_int(name)["vocals"],
                           self.features_int(name)["consonants"],
                           self.features_int(name)["first_letter_vocal"],
                           self.features_int(name)["last_letter_vocal"],
                           self.features_int(name)["first_letter_consonant"],
                           self.features_int(name)["last_letter_consonant"],
                           self.features_int(name)["last_letter_a"],
                           self.features_int(name)["last_letter_o"]])
                flist.append(l1)
        return flist

    def features_list_no_undefined(self, path=''):
        # Reads a specific CSV file and returns a list of features.
        # The CSV file contains information about names, genders,
        # and other characteristics.
        flist = []
        with open(path) as csvfile:
            sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            next(sexreader, None)
            for row in sexreader:
                name = row[0].title()
                name = name.replace('\"', '')
                g = row[4].replace('\"', '')
                if ((g == "m") | (g == "f")):
                    flist.append(list(self.features_int(name).values()))
        return flist

    def features_list2csv(self, path, categorical="both"):
        # Creates a CSV file with the features list attributes
        # at the specified path. Depending on the value of the
        # "categorical" parameter, the function will create a
        # CSV file with different sets of attributes. If the
        # parameter is not specified, all attributes will be used.
        if (categorical == "categorical"):
            fl = self.features_list_categorical(path)
            first_line = "first_letter, last_letter, last_letter_a, " \
                         "first_letter_vocal, last_letter_vocal, " \
                         "last_letter_consonant"
            f = open('files/features_list_cat.csv', 'w')
        elif (categorical == "nocategorical"):
            fl = self.features_list_no_categorical(path)
            first_line = "a, b, c, d, e, f, g, h, i, j, k, l, m, " \
                         "n, o, p, q, r, s, t, u, v, w, x, y, z, " \
                         "vocals, consonants"
            f = open('files/features_list_no_cat.csv', 'w')
        elif (categorical == "noletters"):
            fl = self.features_list_no_letters(path)
            first_line = "first_letter, last_letter, vocals, " \
                         "consonants, first_letter_vocal," \
                         "last_letter_vocal, first_letter_consonant, " \
                         "last_letter_consonant," \
                         "last_letter_a, last_letter_o"
            f = open('files/features_list_no_letters.csv', 'w')
        elif (categorical == "noundefined"):
            fl = self.features_list_no_undefined(path)
            first_line = "first_letter, last_letter, a, b, c, d, e, " \
                         "f, g, h, i, j, k, l, m, n, o, p, q, r, s, " \
                         "t, u, v, w, x, y, z, vocals, consonants, " \
                         "first_letter_vocal, last_letter_vocal, " \
                         "first_letter_consonant, last_letter_consonant, " \
                         "last_letter_a, last_letter_o"
            f = open('files/features_list_no_undefined.csv', 'w')
        else:
            fl = self.features_list(path)
            first_line = "first_letter, last_letter, a, b, c, d, e, f, " \
                         "g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, " \
                         "v, w, x, y, z, vocals, consonants, " \
                         "first_letter_vocal, last_letter_vocal, " \
                         "first_letter_consonant, last_letter_consonant, " \
                         "last_letter_a, last_letter_o"
            f = open('files/features_list.csv', 'w')
        f.write(first_line+"\n")
        for i in fl:
            line = ""
            count = 0
            while (count < (len(i) - 1)):
                line = line + str(i[count]) + ", "
                count = count + 1
            f.write(line+str(i[count])+"\n")
        f.close()

    # DATASETS METHODS #

    def path_surname_dataset(self, locale):
        # Define a function called path_surname_dataset.
        # This function takes a location parameter as an
        # argument and returns a string with the path to
        # a specific CSV file. The text string contains
        # the location of the file, which is
        # "files/names/names_" followed by the location
        # parameter and then "/" followed by the location
        # parameter again and "surnames.csv".
        return "files/names/names_" + locale + "/" + locale + "surnames.csv"

    def males_list(self, corpus='es'):
        # A function called males_list is defined.
        # This function takes a corpus (default is "es")
        # as a parameter and returns a list of masculine
        # names.
        du = DameUtils()
        dicc_males = du.dicc_dataset("male")
        path_males = dicc_males[corpus]
        m = []
        if (corpus != 'all'):
            m = du.csvcolumn2list(path_males)
        elif (corpus == 'all'):
            m = []
            for i in dicc_males.keys():
                m = m + du.csvcolumn2list(i)
        m = du.delete_duplicated(m)
        return m

    def females_list(self, corpus='es'):
        # Defines a function called "females_list"
        # that is used to create a list of women.
        du = DameUtils()
        dicc_females = du.dicc_dataset("female")
        path_females = dicc_females[corpus]
        f = []
        if (corpus != 'all'):
            f = du.csvcolumn2list(path_females)
        elif (corpus == 'all'):
            f = []
            for i in dicc_females.keys():
                f = f + du.csvcolumn2list(i)
        f = du.delete_duplicated(f)
        return f

    def csv2names(self, path='files/names/partial.csv', *args, **kwargs):
        # make a list from a csv file
        surnames = kwargs.get('surnames', False)
        header = kwargs.get('header', True)
        delimiter = kwargs.get('delimiter', ',')
        name_position = kwargs.get('name_position', 0)
        surname_position = kwargs.get('surname_position', 2)
        csvlist = []
        with open(path) as csvfile:
            sexreader = csv.reader(csvfile, delimiter=delimiter, quotechar='|')
            if header:
                next(sexreader, None)
            for row in sexreader:
                name = row[name_position].title()
                name = name.replace('\"', '')
                # middlename = row[1].replace(' ', '')
                # middlename = row[1].replace('\"', '')

                # if (name_and_middlename == True):
                #     name = name + " " + middlename
                #     name = name.title()

                if surnames:
                    surname = row[surname_position].title()
                    surname = row[surname_position].replace('\"', '')
                    elem = [name, surname]
                    csvlist.append(elem)
                else:
                    csvlist.append(name)
        return csvlist

    def csv2json(self, path="", *args, **kwargs):
        # csv to json file
        surnames = kwargs.get('surnames', False)
        header = kwargs.get('header', True)
        gender_encoded = kwargs.get('gender_encoded', False)
        # l1 is a list, such as, guess_list or gender_list
        l1 = kwargs.get('l1', [])
        jsonf = kwargs.get('jsonf', 'files/names/csv2json.json')
        csv2names = self.csv2names(path=path, surnames=surnames, header=header)
        string = ""
        with open(path) as csvfile:
            sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            if header:
                next(sexreader, None)
            string = '['
            i = 0
            for row in sexreader:
                name = row[0].title()
                name = name.replace('\"', '')

                middlename = row[1].replace(' ', '')
                middlename = row[1].replace('\"', '')

                lastname = row[2].title()
                lastname = row[2].replace('\"', '')

                gender = row[4]
                gender = du.drop_quotes(gender)
                if ((gender == "m") or (gender == "male") or (gender == 1)):
                    if gender_encoded:
                        gender = 1
                    else:
                        gender = "male"
                elif ((gender == "f") or (gender == "female") or
                      (gender == 0)):
                    if gender_encoded:
                        gender = 0
                    else:
                        gender = "female"

                if surnames:
                    string = string + '{"name":"' + name
                    string = string + ' ' + middlename + '", \n'
                else:
                    string = string + '{"name":"' + name + '", \n'
                string = string + '"surname":"' + lastname + '", \n'
                string = string + '"probability": 1, \n'
                if (l1 == []):
                    string = string + '"gender":"' + gender + '"}, \n'
                elif (len(l1) > i):
                    # if l1 exists, we are adding the l1 element
                    string = string + '"gender":"' + str(l1[i]) + '"}, \n'
                i = i + 1
            string = string + ']'
            string = string.replace('}, \n]', '}]')
        file = open(jsonf, "w")
        file.writelines(str(string))
        file.close()

    # def csv_names_check(self, filepath):
    #     match_initials = re.search(r'([A-Z]\.| ){1,2}', str)
    #     match_empty = re.search(r'', str)
    #     with open(path) as csvfile:
    #         sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    #         next(sexreader, None)
    #     filepath="gpl-3.0.txt"
    #     with open(filepath) as fp:
    #         for cnt, line in enumerate(fp):
    #             if (cnt <= 10):
    #                 print("Line {}: {}".format(cnt, line))
    # Imprime línea y número de línea

    def name2gender_in_dataset(self, name, dataset=''):
        # This function is used to determine the gender
        # of a noun in a specific data set.
        guess = 2
        if (dataset == "names_es"):
            with open(dataset + "/" + "femeninos.txt") as csvfile:
                sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                next(sexreader, None)
                for row in sexreader:
                    datasetname = row.title()
                    if (datasetname == name):
                        guess = 0
            with open(dataset+"/"+"masculinos.txt") as csvfile:
                sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                next(sexreader, None)
                for row in sexreader:
                    datasetname = row.title()
                    if (datasetname == name):
                        guess = 1
        if (dataset == "files/names/nam_dict.txt"):
            cmd = 'grep -i "' + name
            cmd = cmd + ' " files/names/nam_dict.txt > files/logs/grep.tmp'
            os.system(cmd)
            results = [i for i in open('files/logs/grep.tmp', 'r').readlines()]
            for row in results:
                datasetname = row[1].title()
                if (datasetname == name):
                    guess = row[0].title()
                    if ((guess == 'F') | (guess == '?F')):
                        guess = 0
                    elif ((guess == 'M') | (guess == '?M')):
                        guess = 1
                    elif (guess == '='):
                        guess = 2
        if (dataset == "files/names/all.csv"):
            with open(dataset) as csvfile:
                sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                next(sexreader, None)
                for row in sexreader:
                    datasetname = row[0].title()
                    if (datasetname == name):
                        guess = row[4]
                        if (guess == 'm'):
                            guess = 1
                        elif (guess == 'f'):
                            guess = 0
                        elif (guess == 'u'):
                            guess = 2
        if (dataset == "files/names/yob2017.txt"):
            with open(dataset) as csvfile:
                sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                next(sexreader, None)
                for row in sexreader:
                    datasetname = row[0].title()
                    if (datasetname == name):
                        guess = row[1]
                        if (guess == 'M'):
                            guess = 1
                        elif (guess == 'F'):
                            guess = 0
        return guess

    def dataset2genderlist(self, dataset=''):
        # List of gender chars from a specific data set.
        # Read the data set and extract the information
        # needed to determine the gender.
        genderlist = []
        path_all = "files/names/all.csv"
        path_allnoun = "files/names/allnoundefined.csv"
        if ((dataset == path_all) or (dataset == path_allnoun)):
            with open(dataset) as csvfile:
                sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                next(sexreader, None)
                for row in sexreader:
                    datasetname = row[0].title()
                    guess = row[4]
                    guess = guess.replace('\"', '')
                    if (guess == 'm'):
                        guess = 1
                    elif (guess == 'f'):
                        guess = 0
                    elif (guess == 'u'):
                        guess = 2
                    genderlist.append(guess)
        if (dataset == "files/names/names_gb/orig/yob2017.txt"):
            with open(dataset) as csvfile:
                sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                next(sexreader, None)
                for row in sexreader:
                    datasetname = row[0].title()
                    guess = row[1]
                    guess = guess.replace('\"', '')
                    if (guess == 'M'):
                        guess = 1
                    elif (guess == 'F'):
                        guess = 0
                    genderlist.append(guess)
        return genderlist

    def name_frec(self, name, *args, **kwargs):
        # returns the number of ocurrencies of a name
        # from a dataset being us the defaul dataset
        dataset = kwargs.get('dataset', "us")
        force_whitespaces = kwargs.get('force_whitespaces', False)
        name = du.drop_accents(name)
        if force_whitespaces:
            name = du.force_whitespaces(name)
        dicc_males = du.dicc_dataset("male")
        path_males = dicc_males[dataset]
        file_males = open(path_males, 'r')
        readerm = csv.reader(file_males, delimiter=',', quotechar='|')
        males = 0
        for row in readerm:
            if ((len(row) > 1) and (row[0].lower() == name.lower())):
                males = row[1]
                males = du.drop_dots(males)

        dicc_females = du.dicc_dataset("female")
        path_females = dicc_females[dataset]
        file_females = open(path_females, 'r')
        readerf = csv.reader(file_females, delimiter=',', quotechar='|')
        females = 0
        for row in readerf:
            if ((len(row) > 1) and (row[0].lower() == name.lower())):
                females = row[1]
                females = du.drop_dots(females)
        dicc = {"females": females, "males": males}

        return dicc

    def name_frec_from_file(self, name, path):
        # This code looks up a specific name in a CSV
        # file and returns the frequency associated
        # with that name.
        filef = open(path, 'r')
        readerf = csv.reader(filef, delimiter=',', quotechar='|')
        cnt = 0
        for row in readerf:
            if (row[0].lower() == name.lower()):
                cnt = row[1]
                cnt = du.drop_dots(cnt)
        return cnt

    def inesurname_province_and_frec(self, surname, *args, **kwargs):
        # guess list method
        province = kwargs.get('province', 'madrid')
        if (province == 'acorugna'):
            spath = 'files/inesurnames/provincias/residencia/acorugna.csv'
        elif (province == 'alava'):
            spath = 'files/inesurnames/provincias/residencia/alava.csv'
        elif (province == 'albacete'):
            spath = 'files/inesurnames/provincias/residencia/albacete.csv'
        elif (province == 'alicante'):
            spath = 'files/inesurnames/provincias/residencia/alicante.csv'
        elif (province == 'almeria'):
            spath = 'files/inesurnames/provincias/residencia/almeria.csv'
        elif (province == 'asturias'):
            spath = 'files/inesurnames/provincias/residencia/asturias.csv'
        elif (province == 'avila'):
            spath = 'files/inesurnames/provincias/residencia/avila.csv'
        elif (province == 'badajoz'):
            spath = 'files/inesurnames/provincias/residencia/badajoz.csv'
        elif (province == 'baleares'):
            spath = 'files/inesurnames/provincias/residencia/baleares.csv'
        elif (province == 'barcelona'):
            spath = 'files/inesurnames/provincias/residencia/barcelona.csv'
        elif (province == 'bizkaia'):
            spath = 'files/inesurnames/provincias/residencia/bizkaia.csv'
        elif (province == 'burgos'):
            spath = 'files/inesurnames/provincias/residencia/burgos.csv'
        elif (province == 'caceres'):
            spath = 'files/inesurnames/provincias/residencia/caceres.csv'
        elif (province == 'cadiz'):
            spath = 'files/inesurnames/provincias/residencia/cadiz.csv'
        elif (province == 'cantabria'):
            spath = 'files/inesurnames/provincias/residencia/cantabria.csv'
        elif (province == 'castellon'):
            spath = 'files/inesurnames/provincias/residencia/castellon.csv'
        elif (province == 'ceuta'):
            spath = 'files/inesurnames/provincias/residencia/ceuta.csv'
        elif (province == 'ciudadreal'):
            spath = 'files/inesurnames/provincias/residencia/ciudadreal.csv'
        elif (province == 'cordoba'):
            spath = 'files/inesurnames/provincias/residencia/cordoba.csv'
        elif (province == 'cuenca'):
            spath = 'files/inesurnames/provincias/residencia/cuenca.csv'
        elif (province == 'girona'):
            spath = 'files/inesurnames/provincias/residencia/girona.csv'
        elif (province == 'granada'):
            spath = 'files/inesurnames/provincias/residencia/granada.csv'
        elif (province == 'guadalajara'):
            spath = 'files/inesurnames/provincias/residencia/guadalajara.csv'
        elif (province == 'guipuzkoa'):
            spath = 'files/inesurnames/provincias/residencia/guipuzkoa.csv'
        elif (province == 'huelva'):
            spath = 'files/inesurnames/provincias/residencia/huelva.csv'
        elif (province == 'huesca'):
            spath = 'files/inesurnames/provincias/residencia/huesca.csv'
        elif (province == 'jaen'):
            spath = 'files/inesurnames/provincias/residencia/jaen.csv'
        elif (province == 'larioja'):
            spath = 'files/inesurnames/provincias/residencia/larioja.csv'
        elif (province == 'leon'):
            spath = 'files/inesurnames/provincias/residencia/leon.csv'
        elif (province == 'lleida'):
            spath = 'files/inesurnames/provincias/residencia/lleida.csv'
        elif (province == 'lugo'):
            spath = 'files/inesurnames/provincias/residencia/lugo.csv'
        elif (province == 'madrid'):
            spath = 'files/inesurnames/provincias/residencia/madrid.csv'
        elif (province == 'malaga'):
            spath = 'files/inesurnames/provincias/residencia/malaga.csv'
        elif (province == 'melilla'):
            spath = 'files/inesurnames/provincias/residencia/melilla.csv'
        elif (province == 'murcia'):
            spath = 'files/inesurnames/provincias/residencia/murcia.csv'
        elif (province == 'navarra'):
            spath = 'files/inesurnames/provincias/residencia/navarra.csv'
        elif (province == 'ourense'):
            spath = 'files/inesurnames/provincias/residencia/ourense.csv'
        elif (province == 'palencia'):
            spath = 'files/inesurnames/provincias/residencia/palencia.csv'
        elif (province == 'pontevedra'):
            spath = 'files/inesurnames/provincias/residencia/pontevedra.csv'
        elif (province == 'salamanca'):
            spath = 'files/inesurnames/provincias/residencia/salamanca.csv'
        elif (province == 'segovia'):
            spath = 'files/inesurnames/provincias/residencia/segovia.csv'
        elif (province == 'sevilla'):
            spath = 'files/inesurnames/provincias/residencia/sevilla.csv'
        elif (province == 'soria'):
            spath = 'files/inesurnames/provincias/residencia/soria.csv'
        elif (province == 'tarragona'):
            spath = 'files/inesurnames/provincias/residencia/tarragona.csv'
        elif (province == 'tenerife'):
            spath = 'files/inesurnames/provincias/residencia/tenerife.csv'
        elif (province == 'teruel'):
            spath = 'files/inesurnames/provincias/residencia/teruel.csv'
        elif (province == 'toledo'):
            spath = 'files/inesurnames/provincias/residencia/toledo.csv'
        elif (province == 'valencia'):
            spath = 'files/inesurnames/provincias/residencia/valencia.csv'
        elif (province == 'valladolid'):
            spath = 'files/inesurnames/provincias/residencia/valladolid.csv'
        elif (province == 'zamora'):
            spath = 'files/inesurnames/provincias/residencia/zamora.csv'
        elif (province == 'zaragoza'):
            spath = 'files/inesurnames/provincias/residencia/zaragoza.csv'
        file_surnames = open(spath, 'r')
        readerf = csv.reader(file_surnames, delimiter=',', quotechar='|')
        quantity = 0
        for row in readerf:
            bool1 = (len(row) > 1)
            comp1 = du.drop_accents(row[0].lower())
            comp2 = du.drop_accents(surname.lower())
            bool2 = (comp1 == comp2)
            # the row is not empty and
            # row[0] is the surname
            if (bool1 and bool2):
                aux = row[1]
                quantity = int(du.drop_dots(aux))
        return quantity

    def name_prob_countries(self, name):
        # It calculates the probability that a
        # given name is used by men or women
        # in some countries
        du = DameUtils()
        es = self.name_frec(name, dataset="es")
        ie = self.name_frec(name, dataset="ie")
        isl = self.name_frec(name, dataset="is")
        uy = self.name_frec(name, dataset="uy")
        gb = self.name_frec(name, dataset="gb")
        us = self.name_frec(name, dataset="us")
        nz = self.name_frec(name, dataset="nz")
        ca = self.name_frec(name, dataset="ca")
        cn = self.name_frec(name, dataset="cn")
        fi = self.name_frec(name, dataset="fi")
        au = self.name_frec(name, dataset="au")
        pt = self.name_frec(name, dataset="pt")
        females = int(es["females"]) + int(ie["females"])
        females = females + int(isl["females"]) + int(uy["females"])
        females = females + int(gb["females"]) + int(us["females"])
        females = females + int(nz["females"]) + int(ca["females"])
        females = females + int(fi["females"]) + int(au["females"])
        females = females + int(pt["females"])
        males = int(es["males"]) + int(ie["males"])
        males = males + int(isl["males"]) + int(uy["males"])
        males = males + int(gb["males"]) + int(us["males"])
        males = males + int(nz["males"]) + int(ca["males"])
        males = males + int(fi["males"]) + int(au["males"])
        males = males + int(pt["males"])

        pfemales = {"es": du.round_and_not_zero_division(int(es["females"]),
                                                         int(females)),
                    "ie": du.round_and_not_zero_division(int(ie["females"]),
                                                         int(females)),
                    "is": du.round_and_not_zero_division(int(isl["females"]),
                                                         int(females)),
                    "uy": du.round_and_not_zero_division(int(uy["females"]),
                                                         int(females)),
                    "gb": du.round_and_not_zero_division(int(gb["females"]),
                                                         int(females)),
                    "us": du.round_and_not_zero_division(int(us["females"]),
                                                         int(females)),
                    "nz": du.round_and_not_zero_division(int(nz["females"]),
                                                         int(females)),
                    "ca": du.round_and_not_zero_division(int(ca["females"]),
                                                         int(females)),
                    "fi": du.round_and_not_zero_division(int(fi["females"]),
                                                         int(females)),
                    "au": du.round_and_not_zero_division(int(au["females"]),
                                                         int(females)),
                    "pt": du.round_and_not_zero_division(int(pt["females"]),
                                                         int(females))}

        pmales = {"es": du.round_and_not_zero_division(int(es["males"]),
                                                       int(males)),
                  "ie": du.round_and_not_zero_division(int(ie["males"]),
                                                       int(males)),
                  "is": du.round_and_not_zero_division(int(isl["males"]),
                                                       int(males)),
                  "uy": du.round_and_not_zero_division(int(uy["males"]),
                                                       int(males)),
                  "gb": du.round_and_not_zero_division(int(gb["males"]),
                                                       int(males)),
                  "us": du.round_and_not_zero_division(int(us["males"]),
                                                       int(males)),
                  "nz": du.round_and_not_zero_division(int(nz["males"]),
                                                       int(males)),
                  "ca": du.round_and_not_zero_division(int(ca["males"]),
                                                       int(males)),
                  "fi": du.round_and_not_zero_division(int(fi["males"]),
                                                       int(males)),
                  "au": du.round_and_not_zero_division(int(au["males"]),
                                                       int(males)),
                  "pt": du.round_and_not_zero_division(int(pt["males"]),
                                                       int(males))}

        prob = [{"females": pfemales, "males": pmales}]
        return prob

    def namdict2file(self):
        # it iterates through each line of the file and
        # extracts the characters from position 3 to 25
        filepath = 'files/names/nam_dict.txt'
        mylist = []
        with open(filepath) as fp:
            for cnt, line in enumerate(fp):
                # From 3 to 25
                if (cnt > 292):
                    name = ""
                    for i in range(3, 25):
                        name = name + str(line[i])
                    mylist += [name]
        file = open("files/names/nam_dict_list.txt", "w")
        file.writelines(mylist)
        file.close()

    def filenamdict2list(self):
        # It walks through the file and creates a list
        # with the names read from the file.
        names = []
        dataset = 'files/names/nam_dict_list.txt'
        with open(dataset, 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                names = names + row[0].split()
        return names

# GUESS #

    def guess(self, name, gender_encoded=False, dataset='us', *args, **kwargs):
        # guess method to check names dictionary
        nonamerange = kwargs.get('nonamerange', 0)
        force_whitespaces = kwargs.get('force_whitespaces', False)
        standard = kwargs.get('standard', 'damegender')
        name = unidecode.unidecode(name).title()
        name.replace(name, "")
        dicc = self.name_frec(name,
                              dataset=dataset,
                              force_whitespaces=force_whitespaces)
        m = int(dicc['males'])
        f = int(dicc['females'])
        # nonamerange must be greater than 500
        # otherwise where are considering that
        # name is a nick
        if ((m > nonamerange) or (f > nonamerange)):
            if ((m == 0) and (f == 0)):
                if gender_encoded:
                    guess_damegender = 2
                    guess_isoiec5218 = 0
                    guess_rfc6350 = "u"                    
                else:
                    guess_damegender = "unknown"
                    guess_isoiec5218 = "not know"
                    guess_rfc6350 = "undefined"
            elif (m > f):
                if gender_encoded:
                    guess_damegender = 1
                    guess_isoiec5218 = 1
                    guess_rfc6350 = "m"
                else:
                    guess_damegender = "male"
                    guess_isoiec5218 = "male"
                    guess_rfc6350 = "male"
            elif (f > m):
                if gender_encoded:
                    guess_damegender = 0
                    guess_isoiec5218 = 2
                    guess_rfc6350 = "f"
                else:
                    guess_damegender = "female"
                    guess_isoiec5218 = "female"
                    guess_rfc6350 = "female"
            else:
                if gender_encoded:
                    guess_damegender = 2
                    guess_isoiec5218 = 9
                    guess_rfc6350 = "u"
                else:
                    guess_damegender = "unknown"
                    gues_isoiec5218 = "not applicable"
                    guess_rfc6350 = "undefined"
        else:
            if gender_encoded:
                guess_damegender = 2
                guess_isoiec5128 = 0
                guess_rfc6350 = "u"                
            else:
                guess_damegender = "unknown"
                guess_isoiec5218 = "not know"
                guess_rfc6350 = "undefined"
        if (standard == "isoiec5218"):
            guess = guess_isoiec5218
        elif (standard == "rfc6350"):
            guess = guess_rfc6350
        else:
            guess = guess_damegender
        return guess

    def guess_surname(self, string, dataset):
        # Searches the CSV files corresponding to the specified
        # dataset for the last name matching the given string.
        counter = 0
        surname_position = 0
        counter_position = 1
        if ((dataset == "ine") or (dataset == "es")):
            path = 'files/names/names_es/essurnames.csv'
        elif ((dataset == "ru_en") or
              (dataset == "ru_ru") or
              (dataset == "ru")):
            path = 'files/names/names_ru/rusurnames.csv'
        else:
            path = 'files/names/names_' + dataset + '/'
            path = path + dataset + 'surnames.csv'
        boolean = False
        with open(path) as csvfile:
            surnamereader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in surnamereader:
                surname = row[surname_position]
                if (surname.lower() == du.drop_accents(string.lower())):
                    boolean = True
                    counter = int(row[counter_position])
        return [boolean, counter]

    def string2gender(self, string):
        # Given a string with name and surname returns the gender
        arr = du.string2array(string)
        name = ""
        i = 0
        while ((name == "") and (len(arr) > i)):
            surname = self.guess_surname(arr[i], dataset="inter")
            bool1 = surname[0]
            surname_frec_total = int(surname[1])
            name_frec = self.name_frec(arr[i], dataset="inter")
            n_males = int(name_frec["males"])
            n_females = int(name_frec["females"])
            name_frec_total = n_males + n_females
            sex = self.guess(arr[i], dataset="inter")
            if (not(bool1)
               and ((sex == 'male') or (sex == 'female'))
               and (len(string) > 0)):
                name = arr[i]
            elif (bool1 and (name_frec_total > surname_frec_total)):
                name = arr[i]
            i = i + 1
        return self.guess(name)

    def guess_list(self, path='files/names/partial.csv',
                   gender_encoded=False, dataset='us', *args, **kwargs):
        # returns a list of gender chars using the guess method
        header = kwargs.get('header', True)
        standard = kwargs.get('standard', 'damegender')        
        slist = []
        with open(path) as csvfile:
            sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            if header:
                next(sexreader, None)
            for row in sexreader:
                name = row[0].title()
                name = name.replace('\"', '')
                slist.append(self.guess(name, gender_encoded, dataset, standard=standard))
        return slist

    def csv2gender_list(self, path, *args, **kwargs):
        # generating a list of 0, 1, 2 as females, males and unknowns
        # NOT using guess, only reading numbers from the file
        # TODO: ISO/IEC 5218 proposes a norm about coding gender:
        # ``0 as not know'',``1 as male'', ``2 as female''
        # and ``9 as not applicable''
        header = kwargs.get('header', True)
        standard = kwargs.get('standard', 'damegender')        
        gender_column = kwargs.get('gender_column', 4)
        gender_f_chars = kwargs.get('gender_f_chars', 'f')
        gender_m_chars = kwargs.get('gender_m_chars', 'm')
        delimiter = kwargs.get('delimiter', ',')
        glist = []
        with open(path) as csvfile:
            sexreader = csv.reader(csvfile, delimiter=delimiter, quotechar='"')
            if header:
                next(sexreader, None)
            count_females = 0
            count_males = 0
            count_unknown = 0
            gender = ""
            for row in sexreader:
                try:
                    gender = row[gender_column]
                except IndexError:
                    print("The method csv2gender_list has not row[%s]" %
                          str(gender_column))
                    print("To review that gender row is set in the input")
                    os.kill(os.getpid(), signal.SIGUSR1)
                if (gender == gender_f_chars):
                    if (standard == 'damegender'):
                        g = 0
                    elif (standard == 'isoiec5218'):
                        g = 2
                    elif (standard == 'rfc6350'):
                        g = "f"
                    count_females = count_females + 1
                elif (gender == gender_m_chars):
                    if (standard == 'damegender'):
                        g = 1
                    elif (standard == 'isoiec5218'):
                        g = 1
                    elif (standard == 'rfc6350'):
                        g = "m"
                    count_males = count_males + 1
                else:
                    if (standard == 'damegender'):
                        g = 2
                    elif (standard == 'isoiec5218'):
                        g = 0
                    elif (standard == 'rfc6350'):
                        g = "u"
                    count_unknown = count_unknown + 1
                glist.append(g)
        self.females = count_females
        self.males = count_males
        self.unknown = count_unknown
        return glist

    def pretty_gg_list(self, guessf, testf, *args, **kwargs):
        # print the gender list and the guess list
        # with a measure (e.g: accuracy)
        # from a guessed file (guess list)
        # and a gender test file as base of truth (gender list)
        measure = kwargs.get('measure', 'accuracy')
        gender_encoded = kwargs.get('gender_encoded', True)
        ml = kwargs.get('ml', 'nltk')
        api = kwargs.get('api', 'damegender')
        header = kwargs.get('header', True)
        gender_test_row = kwargs.get('gender_test_row', 4)
        gender_guess_row = kwargs.get('gender_guess_row', 4)
        guess_f_chars = kwargs.get('guess_f_chars', 'f')
        guess_m_chars = kwargs.get('guess_m_chars', 'm')
        test_f_chars = kwargs.get('test_f_chars', 'f')
        test_m_chars = kwargs.get('test_m_chars', 'm')
        delimiter_testf = kwargs.get('delimiter_testf', ',')
        delimiter_guessf = kwargs.get('delimiter_guessf', ',')
        difflen = False
        if ((os.path.isfile(guessf)) and (os.path.isfile(testf))):
            if (du.is_json(guessf)):
                gl = self.json2gender_list(jsonf=guessf, gender_encoded=True)
                if (du.is_json(testf)):
                    tl = self.json2gender_list(jsonf=testf, gender_encoded=True)
                    if (len(gl) == len(tl)):
                        print("########################## " + api + "!!")
                        print("Gender Guess (guess list): " + str(gl))
                        print("Gender Test   (true list): " + str(tl))
                        dst.print_measures(tl, gl, measure, api)
                    else:
                        difflen = True
                        v = self.first_uneq_json_and_json_in_names(
                            json1=guessf, json2=testf)
                elif (du.is_csv(testf)):
                    tl = self.csv2gender_list(path=testf,
                                              gender_column=gender_test_row,
                                              gender_f_chars=test_f_chars,
                                              gender_m_chars=test_m_chars,
                                              delimiter=delimiter_testf)

                    if (len(gl) == len(tl)):
                        print("########################## " + api + "!!")
                        print("Gender Guess (guess list): " + str(gl))
                        print("Gender Test   (true list): " + str(tl))
                        dst.print_measures(tl, gl, measure, api)
                    else:
                        difflen = True
                        v = self.first_uneq_json_and_csv_in_names(jsonf=guessf,
                                                                  csvf=testf)

            elif (du.is_csv(guessf)):
                gl = self.csv2gender_list(path=guessf, gender_encoded=True,
                                          gender_column=gender_guess_row,
                                          gender_f_chars=guess_f_chars,
                                          gender_m_chars=guess_m_chars,
                                          delimiter=delimiter_guessf)
                if (du.is_json(testf)):
                    tl = self.json2gender_list(jsonf=testf, gender_encoded=True)
                    if (len(gl) == len(tl)):
                        print("########################## " + api + "!!")
                        print("Gender Guess (guess list): " + str(gl))
                        print("Gender Test   (true list): " + str(tl))
                        dst.print_measures(tl, gl, measure, api)
                    else:
                        difflen = True
                        v = self.first_uneq_json_and_csv_in_names(jsonf=testf,
                                                                  csvf=guessf)

                elif (du.is_csv(testf)):
                    tl = self.csv2gender_list(path=testf,
                                              gender_column=gender_test_row,
                                              gender_f_chars=test_f_chars,
                                              gender_m_chars=test_m_chars,
                                              delimiter=delimiter_testf)
                    if (len(gl) == len(tl)):
                        print("######################### " + api + "!!")
                        print("Guess Guess (guess list): " + str(gl))
                        print("Gender Test  (true list): " + str(tl))
                        dst.print_measures(tl, gl, measure, api)
                    else:
                        difflen = True
                        v = self.first_uneq_csv_and_csv_in_names(csv1=guessf,
                                                                 csv2=testf)

        else:
            print("Check arguments in pretty_gg_list:")
            print("You must introduce a file for test file")
            print(testf)
            print("a file for guessed file")
            print(guessf)

        if difflen:
            print("Names in test file and guessed file are differents")
            print("%s names in test file" %
                  len(tl))
            print("%s names in guessed file" %
                  len(gl))
            # print("The unmatched names starts in %s and the name is %s" %
            #       (v[1], v[0]))
            # print("Names in test file: %s:" %
            #       testnames)
            # print("Names in guessed file: %s:" %
            #       guessnames)
        return 1

    def pretty_cm(self, path, jsonf, *args, **kwargs):
        # printing a confusion matrix on a pretty way
        api = kwargs.get('api', 'damegender')
        reverse = kwargs.get('reverse', False)
        dimensions = kwargs.get('dimensions', '3x2')
        gl = self.csv2gender_list(path=path)
        print("%s confusion matrix:\n" % api)
#        self.print_confusion_matrix_gender(path=path, dimensions=dimensions)
        if (os.path.isfile(jsonf)):
            self.print_confusion_matrix_gender(path=path,
                                               dimensions=dimensions,
                                               jsonf=jsonf,
                                               reverse=reverse)
        elif (args.jsondownloaded == ''):
            self.print_confusion_matrix_gender(path=path,
                                               dimensions=dimensions,
                                               reverse=reverse)
        else:
            print("In the path %s doesn't exist file" % jsonf)

    def json2gender_list(self, jsonf="", gender_encoded=False):
        # generating a list of 0, 1, 2 as females, males and unknows
        # TODO: ISO/IEC 5218 proposes a norm about coding gender:
        # ``0 as not know'',``1 as male'', ``2 as female''
        # and ``9 as not applicable''
        jsondata = open(jsonf).read()
        json_object = json.loads(jsondata)
        guesslist = []

        for i in json_object:
            g = i['gender']
            if gender_encoded:
                if ((g == 'female') or (g == 'f') or (g == 0)):
                    guesslist.append(0)
                elif ((g == 'male') or (g == 'm') or (g == 1)):
                    guesslist.append(1)
                else:
                    guesslist.append(2)
            else:
                if ((g == 'female') or (g == 'f') or (g == 0)):
                    guesslist.append("female")
                elif ((g == 'male') or (g == 'm') or (g == 1)):
                    guesslist.append("male")
                else:
                    guesslist.append("unknown")
        return guesslist

    def json2names(self, jsonf="", surnames=False):
        # reads a JSON file and creates a list of names
        # from the data in the file.
        jsondata = open(jsonf).read()
        json_object = json.loads(jsondata)
        nameslist = []
        for i in json_object:
            if (i["name"] != ''):
                if surnames:
                    nameslist.append([i["name"], i["surname"]])
                else:
                    nameslist.append(i["name"])
        return nameslist

    def json_eq_csv_in_names(self, jsonf="", path="", *args, **kwargs):
        # it compares the names of a JSON file with the
        # names of a CSV file and returns True if it is
        # equal number in both
        header = kwargs.get('header', True)
        boolean = False
        json = self.json2names(jsonf=jsonf, surnames=False)
        json_lower = [element.lower() for element in json]
        csv = self.csv2names(path=path, header=header)
        csv_lower = [element.lower() for element in csv]
        count = 0
        i = 0
        maxi = len(json_lower) - 1
        if (maxi < len(csv_lower)):
            maxi = len(csv_lower) - 1
        while (maxi > i):
            if (json_lower[i] == csv_lower[i]):
                count = count + 1
            i = i + 1
        boolean = ((len(json_lower) == len(csv_lower))
                   and ((len(json_lower) - 1) == count))
        return boolean

    def first_uneq_json_and_csv_in_names(self, jsonf="", path="",
                                         *args, **kwargs):
        # it compares two files, one in JSON format and one in
        # CSV, to find the first name that doesn't match between
        # the two.
        header = kwargs.get('header', True)
        json = self.json2names(jsonf=jsonf, surnames=False)
        csv = self.csv2names(path=path, header=header)
        i = 0
        maxi_json = len(json) - 1
        maxi_csv = len(csv) - 1
        while ((i < maxi_json) and
               (i < maxi_csv) and
               (json[i].lower() == csv[i].lower())):
            i = i + 1
        ret = json[i].lower()
        if ((i > maxi_json) and (i > maxi_csv)):
            ret = ""
        elif (i > maxi_json):
            ret = csv[i].lower()
        elif (i > maxi_csv):
            ret = json[i].lower()
        elif (csv[i].lower() == json[i].lower()):
            ret = ""
        return [ret, i]

    def first_uneq_json_and_json_in_names(self, json1="", json2="",
                                          *args, **kwargs):
        # Find the first element of two JSONs that are not equal.
        header = kwargs.get('header', True)
        json1 = self.json2names(jsonf=json1, surnames=False)
        json2 = self.json2names(jsonf=json2, surnames=False)
        i = 0
        maxi_json1 = len(json1) - 1
        maxi_json2 = len(json2) - 1
        while ((i < maxi_json1) and
               (i < maxi_json2) and
               (json1[i].lower() == json2[i].lower())):
            i = i + 1
        ret = json1[i].lower()
        if ((i > maxi_json1) and (i > maxi_json2)):
            ret = ""
        elif (i > maxi_json1):
            ret = json2[i].lower()
        elif (i > maxi_json2):
            ret = json1[i].lower()
        elif (json1[i].lower() == json2[i].lower()):
            ret = ""
        return [ret, i]

    def first_uneq_csv_and_csv_in_names(self, csv1="", csv2="",
                                        *args, **kwargs):
        # it compares two CSV files and returns the first
        # non-equal name between the two.
        header = kwargs.get('header', True)
        csv1 = self.csv2names(path=csv1, header=header)
        csv2 = self.csv2names(path=csv2, header=header)
        i = 0
        maxi_csv1 = len(csv1) - 1
        maxi_csv2 = len(csv2) - 1
        while ((i < maxi_csv1) and
               (i < maxi_csv2) and
               (csv1[i].lower() == csv2[i].lower())):
            i = i + 1
        ret = csv1[i].lower()
        if ((i > maxi_csv1) and (i > maxi_csv2)):
            ret = ""
        elif (i > maxi_csv1):
            ret = csv1[i].lower()
        elif (i > maxi_csv2):
            ret = csv2[i].lower()
        elif (csv1[i].lower() == csv2[i].lower()):
            ret = ""
        return [ret, i]

    def confusion_matrix_gender(self, path='', jsonf=''):
        # this method is an interfaz to confusion_matrix_table
        # allowing introduce a json file in dame_sexmachine
        # we must rewrite it to allow machine learning algorithm
        truevector = self.csv2gender_list(path)
        if (os.path.isfile(jsonf)):
            guessvector = self.json2gender_list(jsonf=jsonf, gender_encoded=True)
        else:
            guessvector = self.guess_list(path, gender_encoded=True)
        res = dst.confusion_matrix_table(truevector, guessvector)
        return res

    def print_confusion_matrix_gender(self, path='', dimensions='',
                                      *args, **kwargs):
        # prints a gender confusion matrix. The confusion matrix
        # is a tool used to evaluate the performance of a machine
        # learning model.
        reverse = kwargs.get('reverse', False)
        jsonf = kwargs.get('jsonf', '')
        jf = os.getcwd() + "/" + jsonf
        if (os.path.isfile(jf)):
            cmd = self.confusion_matrix_gender(path, jsonf=jf)
        else:
            cmd = self.confusion_matrix_gender(path)

        if (dimensions == "1x1"):
            if not (reverse):
                print("      M    ")
                print("M  [[ %s ]]" % (cmd[1][1]))
            elif reverse:
                print("      F    ")
                print("F  [[ %s ]]" % (cmd[0][0]))
        elif (dimensions == "1x2"):
            if not (reverse):
                print("      M    F   ")
                print("M  [[ %s,   %s ]]" %
                      (cmd[1][1], cmd[1][0]))
            elif reverse:
                print("      F    M   ")
                print("F  [[ %s,   %s ]]" %
                      (cmd[0][0], cmd[0][1]))
        elif (dimensions == "1x3"):
            if not (reverse):
                print("      M    F   U   ")
                print("M  [[ %s, %s, %s ]]" %
                      (cmd[1][1], cmd[1][0], cmd[1][2]))
            elif reverse:
                print("     F  M  U   ")
                print("F [[ %s, %s, %s ]]" %
                      (cmd[0][0], cmd[0][1], cmd[0][2]))
        elif (dimensions == "2x1"):
            if not (reverse):
                print("      M  ")
                print("M  [[ %s ]" %
                      (cmd[1][1]))
                print("F   [ %s ]]" %
                      (cmd[1][0]))
            elif reverse:
                print("      F   ")
                print("F  [[ %s ] " % (cmd[0][0]))
                print("M   [ %s ]]" % (cmd[0][1]))
        elif (dimensions == "2x2"):
            if not (reverse):
                print("      M    F  ")
                print("M  [[ %s , %s ]" %
                      (cmd[1][1], cmd[1][0]))
                print("F   [ %s , %s ]]" %
                      (cmd[0][1], cmd[0][0]))
            if reverse:
                print("      F   M  ")
                print("F  [[ %s , %s ]" %
                      (cmd[0][0], cmd[0][1]))
                print("M   [ %s , %s ]]" %
                      (cmd[1][0], cmd[1][1]))
        elif (dimensions == "2x3"):
            if not (reverse):
                print("      M   F   U  ")
                print("M  [[ %s,  %s,  %s ]" %
                      (cmd[1][1], cmd[1][0], cmd[1][2]))
                print("F   [ %s,  %s,  %s ]]" %
                      (cmd[0][1], cmd[0][0], cmd[0][2]))
            if reverse:
                print("      F   M   U  ")
                print("F  [[ %s,  %s,  %s ]" %
                      (cmd[0][0], cmd[0][1], cmd[0][2]))
                print("M   [ %s,  %s,  %s ]]" %
                      (cmd[1][0], cmd[1][1], cmd[1][2]))
        elif (dimensions == "3x1"):
            if not (reverse):
                print("       M   ")
                print("M  [[ %s ]" % (cmd[1][1]))
                print("F   [ %s ]" % (cmd[0][1]))
                print("U   [ %s ]]" % (cmd[2][1]))
            elif reverse:
                print("       F   ")
                print("F   [[ %s ]" % (cmd[0][0]))
                print("M    [ %s ]" % (cmd[1][0]))
                print("U    [ %s ]]" % (cmd[2][0]))
        elif (dimensions == "3x2"):
            if not (reverse):
                print("      M    F  ")
                print("M  [[ %s ,  %s ]" %
                      (cmd[1][1], cmd[1][0]))
                print("F   [ %s ,  %s ]" %
                      (cmd[0][1], cmd[0][0]))
                print("U   [ %s ,  %s ]]" %
                      (cmd[2][1], cmd[2][0]))
            if reverse:
                print("      F   M  ")
                print("F  [[ %s,  %s ]" %
                      (cmd[0][0], cmd[0][1]))
                print("M   [ %s,  %s ]" %
                      (cmd[1][0], cmd[1][1]))
                print("U   [ %s,  %s ]]" %
                      (cmd[2][0], cmd[2][1]))
        elif (dimensions == "3x3"):
            if not (reverse):
                print("      M  F  U   ")
                print("M  [[ %s, %s, %s ]" %
                      (cmd[1][1], cmd[1][0], cmd[1][2]))
                print("F   [ %s, %s, %s ]" %
                      (cmd[0][1], cmd[0][0], cmd[0][2]))
                print("U   [ %s, %s, %s ]]" %
                      (cmd[2][1], cmd[2][0], cmd[2][2]))
            if reverse:
                print("      F   M   U   ")
                print("F  [[ %s, %s, %s ]" %
                      (cmd[0][0], cmd[0][1], cmd[0][2]))
                print("M   [ %s, %s, %s ]" %
                      (cmd[1][0], cmd[1][1], cmd[1][2]))
                print("U   [ %s, %s, %s ]]" %
                      (cmd[2][0], cmd[2][1], cmd[2][2]))
        return ""
