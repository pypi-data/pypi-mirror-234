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
import os
from app.dame_gender import Gender
from app.dame_utils import DameUtils
try:
    import requests
except:
    print("module 'requests' is not installed")
    print("try:")
    print("$ pip3 install 'requests'")
    exit()    


class DameNameapi(Gender):

    def get(self, name, surname="", gender_encoded=False):
        # from name, surname and gender_encoded arguments
        # calls an API request and returns
        # gender and probability
        nameapilist = []
        guess = ""
        confidence = ""
        if (self.config['DEFAULT']['nameapi'] == 'yes'):
            fichero = open(self.config['FILES']['nameapi'], "r+")
            content = fichero.readline().rstrip()
            host = "http://rc50-api.nameapi.org/"
            path = "rest/v5.0/parser/personnameparser?"
            var = "apiKey="
            # url of the NameAPI.org endpoint:
            url = (
                host + path + var + content
            )

            # Dict of data to be sent to NameAPI.org:
            payload = {
                "inputPerson": {
                    "type": "NaturalInputPerson",
                    "personName": {
                        "nameFields": [
                            {
                                "string": name,
                                "fieldType": "GIVENNAME"
                            }, {
                                "string": surname,
                                "fieldType": "SURNAME"
                            }
                        ]
                    },
                    "gender": "UNKNOWN",
                    "confidence": "UNKNOW"
                }
            }

            # Proceed, only if no error:
            try:
                # Send request to NameAPI.org by doing the following:
                # - make a POST HTTP request
                # - encode the Python payload dict to JSON
                # - pass the JSON to request body
                # - set header's 'Content-Type' to
                #   'application/json' instead of
                #   default 'multipart/form-data'
                resp = requests.post(url, json=payload)
                resp.raise_for_status()
                # Decode JSON response into a Python dict:
                respd = resp.json()
                g = respd['matches'][0]['parsedPerson']['gender']['gender']
                g = g.lower()
                c = respd['matches'][0]['parsedPerson']['gender']['confidence']
                if (gender_encoded is True):
                    if (g == 'female'):
                        g = 0
                    elif (g == 'male'):
                        g = 1
                    else:
                        g = 2
            except requests.exceptions.HTTPError as e:
                print("Bad HTTP status code:", e)
            except requests.exceptions.RequestException as e:
                print("Network error:", e)
        else:
            if (gender_encoded is True):
                g = 2
            else:
                g = "unknown"
        return [g, c]

    def download(self, path="files/names/partial.csv"):
        # Create a JSON file from a CSV file.
        # And to read the CSV file and to dump
        # first name, last name, confidence and
        # gender of the users.
        du = DameUtils()
        path1 = "files/names/nameapi" + du.path2file(path) + ".json"
        nameapijson = open(path1, "w+")
        names = self.csv2names(path, surnames=True)
        nameapijson.write("[")
        length = len(names)
        i = 0
        while (i < length):
            nameapijson.write('{"name":"'+names[i][0]+'",\n')
            g = self.get(names[i][0], names[i][1], gender_encoded=True)
            nameapijson.write('"surname":"'+names[i][1]+'",\n')
            nameapijson.write('"gender":'+str(g[0])+',\n')
            nameapijson.write('"confidence":'+str(g[1])+'\n')
            if ((length - 1) == i):
                nameapijson.write('} \n')
            else:
                nameapijson.write('}, \n')
            i = i + 1
        nameapijson.write("]")
        nameapijson.close()
        return 0

    def guess(self, name, surname, gender_encoded=False):
        # guess a name using name, surname and gender_encoded as arguments
        # returning the gender
        # TODO: ISO/IEC 5218 proposes a norm about coding gender:
        # ``0 as not know'',``1 as male'', ``2 as female''
        # and ``9 as not applicable''
        v = self.get(name, surname, gender_encoded)
        return v[0]

    def confidence(self, name, surname, gender_encoded=False):
        # guess a name using name, surname and gender_encoded as arguments
        # returning the confidence
        v = self.get(name, surname, gender_encoded)
        return v[1]

    def guess_list(self, path='files/names/partial.csv', gender_encoded=False):
        # giving a csv file as input returns
        # a guess list as output
        slist = []
        with open(path) as csvfile:
            sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            next(sexreader, None)
            for row in sexreader:
                name = row[0].title()
                name = name.replace('\"', '')
                surname = row[2].title()
                surname = surname.replace('\"', '')
                slist.append(self.guess(name, surname, gender_encoded))
        return slist
