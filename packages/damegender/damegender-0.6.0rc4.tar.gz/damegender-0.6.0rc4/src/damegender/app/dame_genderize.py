#!/usr/bin/python
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
import json
import configparser
from app.dame_gender import Gender
from app.dame_utils import DameUtils
try:
    import requests
except:
    print("module 'requests' is not installed")
    print("try:")
    print("$ pip3 install 'requests'")
    exit()    

class DameGenderize(Gender):

    def get(self, name, *args, **kwargs):
        # obtaining data from genderize
        string = 'https://api.genderize.io/?name='
        string = string + name
        if ('country_id' in kwargs):
            string = string + "&country_id=" + kwargs.get('country_id')
        if ('surname' in kwargs):
            string = string + "&surname=" + kwargs.get('surname')
        r = requests.get(string)
        d = json.loads(r.text)
        return d

    def get2to10(self, l1):
        # It constructs a URL with a number of names between
        # 2 and 10 and makes an HTTP GET request
        # to the constructed URL.
        # After, loads the returned data in JSON
        # format into a dictionary called d
        string = 'https://api.genderize.io/'

        if ((len(l1) > 1) and (len(l1) <= 10)):
            string = string + '?name[]=' + l1[0]
            for i in l1[1:10]:
                string = string + '&name[]=' + i
            r = requests.get(string)
            d = json.loads(r.text)
        elif (len(l) == 1):
            d = [self.get(l1[0])]
        else:
            d = ""
        return d

    def samples(self, name):
        # returns the number of people using a name
        v = self.get(name)
        return v["count"]
    
    def guess(self, name, gender_encoded=False, *args, **kwargs):
        # guess a name using the method get
        # and taking gender_encoded as argument
        # and country as optional argument
        # TODO: ISO/IEC 5218 proposes a norm about coding gender:
        # ``0 as not know'',``1 as male'', ``2 as female''
        # and ``9 as not applicable''
        country_id = kwargs.get('dataset', 'us')
        d = self.get(name, country_id)
        if (gender_encoded is True):
            if (d['gender'] == 'female'):
                gender = 0
            elif (d['gender'] == 'male'):
                gender = 1
            else:
                gender = 2
        else:
            gender = d['gender']
        return gender

    def prob(self, name):
        # Retrieves the dictionary associated with the
        # specified name and returns the value of the
        # "probability" key of the dictionary.
        d = self.get(name)
        return d['probability']

    def download(self, path='files/names/partial.csv', surnames=False):
        # It is used to download the data from a
        # CSV file specified in the path to a json file
        du = DameUtils()
        new = []
        d = ""
        lresult = []
        res = ""
        if (surnames is True):
            l1 = self.csv2names(path, surnames=True)
            for i in range(0, len(l1)):
                d = self.get(l1[i][0], surname=l1[i][1])
                d["surname"] = l1[i][1]
                lresult.append(d)
            res = str(lresult)
        else:
            l1 = self.csv2names(path)
            # We must split the list in different lists with size 10
            for i in range(0, len(l1), 10):
                new.append(l1[i:i+10])
            for j in new:
                lresult.append(self.get2to10(j))
            for k in lresult:
                res = res + str(k)
        res = str(res).replace("\'", "\"")
        res = str(res).replace('None', '"unknown"')
        path = "files/names/genderize" + du.path2file(path) + ".json"
        backup = open(path, "w+")
        backup.write(res)
        backup.close()
        return res

    def download_csv(self, path='files/names/partial.csv',
                     surnames=False, *args, **kwargs):
        # It is used to download the data from a
        # CSV file specified in the path to a csv file.
        outpath = kwargs.get('outpath', 'files/tmp/downloadgenderize.csv')
        outformat = kwargs.get('outformat', 'all')
        du = DameUtils()
        new = []
        d = ""
        lresult = []
        res = ""
        if (surnames is True):
            l1 = self.csv2names(path, surnames=True)
            fo = open(outpath, "w")
            for i in range(0, len(l1)):
                d = self.get(l1[i][0], surname=l1[i][1])
                d["surname"] = l1[i][1]
                res = res + d["name"]+","+d["count"]+"\n"
        else:
            l1 = self.csv2names(path)
            # We must split the list in different lists with size 10
            for i in range(0, len(l1), 10):
                new.append(l1[i:i+10])
            for j in new:
                lresult.append(self.get2to10(j))
            for k in lresult[0]:
                if ((k['gender'] == "female") and (outformat == "females")):
                    res = res + str(k["name"])+","+str(k["count"])+"\n"
                elif ((k['gender'] == "male") and (outformat == "males")):
                    res = res + str(k["name"])+","+str(k["count"])+"\n"
                elif (((k['gender'] == "male") or (k["gender"] == "female"))
                      and (outformat == "all")):
                    res = res + str(k["name"])+","+str(k["count"])+"\n"
        res = str(res).replace("\'", "\"")
        res = str(res).replace('None', '"unknown"')
        backup = open(outpath, "w+")
        backup.write(res)
        backup.close()
        return res

    def json2gender_list(self, jsonf="", gender_encoded=False):
        # from a json file, it generates a list
        # of 0, 1, 2 as females, males and unknows
        # TODO: ISO/IEC 5218 proposes a norm about coding gender:
        # ``0 as not know'',``1 as male'', ``2 as female''
        # and ``9 as not applicable''
        jsondata = open(jsonf).read()
        json_object = json.loads(jsondata)
        guesslist = []
        for i in json_object:
            if gender_encoded:
                if (i["gender"] == 'female'):
                    guesslist.append(0)
                elif (i["gender"] == 'male'):
                    guesslist.append(1)
                else:
                    guesslist.append(2)
            else:
                guesslist.append(i["gender"])
        return guesslist

    def apikey_limit_exceeded_p(self):
        # Checks if the API limit has been exceeded.
        j = ""
        baseurl = 'https://api.genderize.io/'
        if (self.config['DEFAULT']['genderize'] == 'yes'):
            fichero = open("files/apikeys/genderizepass.txt", "r+")
            key = fichero.readline()
            key = contenido.replace('\n', '')
            content = '?name[]=peter&name[]=lois&name[]=stevie?apikey='
            str1 = baseurl + content + key
        else:
            content = '?name[]=peter&name[]=lois&name[]=stevie'
            str1 = baseurl + content
        r = requests.get(string)
        j = json.loads(r.text)
        if (j["error"] is not None):
            p = True
        else:
            p = False
        return p

    # def guess(self, name, gender_encoded=False):
    #     # guess method to check names dictionary
    #     if (self.config['DEFAULT']['genderize'] == 'no'):
    #         v = Genderize().get([name])
    #     elif (self.config['DEFAULT']['genderize'] == 'yes'):
    #         fichero = open(self.config['FILES']['genderize'], "r+")
    #         apikey = fichero.readline().rstrip()
    #         v = Genderize(
    #             user_agent='GenderizeDocs/0.0',
    #             api_key=apikey).get([name])
    #     g = v[0]['gender']
    #     if ((g == 'female') and gender_encoded):
    #         guess = 0
    #     elif ((g == 'male') and gender_encoded):
    #         guess = 1
    #     elif (not(gender_encoded)):
    #         guess = g
    #     return guess

    # def prob(self, name, gender_encoded=False):
    #     # guess method to check names dictionary
    #     if (self.config['DEFAULT']['genderize'] == 'no'):
    #         v = Genderize().get([name])
    #     elif (self.config['DEFAULT']['genderize'] == 'yes'):
    #         fichero = open(self.config['DEFAULT']['genderizefile'], "r+")
    #         apikey = fichero.readline().rstrip()
    #         v = Genderize(
    #             user_agent='GenderizeDocs/0.0',
    #             api_key=apikey).get([name])
    #     prob = v[0]['probability']
    #     return prob

    # def guess_list(self, path='files/names/partial.csv', gender_encoded=False):
    #     # guess list method
    #     slist = []
    #     with open(path) as csvfile:
    #         sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    #         next(sexreader, None)
    #         i = 0
    #         genderlist = list()
    #         for row in sexreader:
    #             name = row[0].title()
    #             name = name.replace('\"', '')
    #             genderlist.append(name)
    #     new = []
    #     # We must split the list in different lists with size 10
    #     for i in range(0, len(genderlist), 10):
    #         new.append(genderlist[i:i+10])
    #     for i in new:
    #         if (self.config['DEFAULT']['genderize'] == 'no'):
    #             jsonlist = Genderize().get(i)
    #         elif (self.config['DEFAULT']['genderize'] == 'yes'):
    #             fichero = open("files/apikeys/genderizepass.txt", "r+")
    #             apikey = fichero.readline().rstrip()
    #             jsonlist = Genderize(user_agent='GenderizeDocs/0.0',
    #                                  api_key=apikey).get(i)
    #         for item in jsonlist:
    #             if ((item['gender'] is None) & gender_encoded):
    #                 slist.append(2)
    #             elif ((item['gender'] is None) & (not gender_encoded)):
    #                 slist.append("unknown")
    #             elif ((item['gender'] == "male") & gender_encoded):
    #                 slist.append(1)
    #             elif ((item['gender'] == "male") & (not gender_encoded)):
    #                 slist.append("male")
    #             elif ((item['gender'] == "female") & gender_encoded):
    #                 slist.append(0)
    #             elif ((item['gender'] == "female") & (not gender_encoded)):
    #                 slist.append("female")
    #     return slist
