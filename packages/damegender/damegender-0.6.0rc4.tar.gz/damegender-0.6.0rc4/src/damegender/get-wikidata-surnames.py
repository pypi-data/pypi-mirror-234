#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2022  David Arroyo Menéndez

# Author: David Arroyo Menéndez <davidam@gnu.org>
# Maintainer: David Arroyo Menéndez <davidam@gnu.org>

# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.

# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Damegender; see the file GPL.txt.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA,

import argparse
import re
from app.dame_wikidata import DameWikidata
from app.dame_utils import DameUtils
try:
    import requests
except:
    print("module 'requests' is not installed")
    print("try:")
    print("$ pip3 install 'requests'")
    exit()    

du = DameUtils()
dw = DameWikidata()
dicc = dw.dicc_countries()

parser = argparse.ArgumentParser()
parser.add_argument('--total', default="us",
                    choices=dicc.keys())
parser.add_argument('--outcsv',
                    default="surnames.csv")
args = parser.parse_args()

url = 'https://query.wikidata.org/sparql'
if du.check_connection(url,timeout=25):
    query2 = """
SELECT ?surname ?surnameLabel ?count
WITH {
  SELECT ?surname (count(?person) AS ?count) WHERE {
    ?person wdt:P734 ?surname .
    ?person wdt:P27 wd:""" + dicc[args.total] + """ .
  }
  GROUP BY ?surname
  ORDER BY DESC(?count)
} AS %results
WHERE {
  INCLUDE %results
  SERVICE wikibase:label
  { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
ORDER BY DESC(?count)
"""

    try:
        r = requests.get(url, params={'format': 'json', 'query': query2})
        data = r.json()
        print("Dumping to %s" % args.outcsv)
        fo = open(args.outcsv, "w")
        dicc = {}
        for d in data["results"]["bindings"]:
            # surnames as Q010234 is a wikidata identifier not a name
            match1 = re.search(r'(Q[0-9]*)', d['surnameLabel']['value'])
            # url is not a surname
            match2 = re.search(r'(^http*)', d['surnameLabel']['value'])
            if not(match2) and not(match1):
                dicc[d['surnameLabel']['value']] = d['count']['value']

        l = sorted(dicc.items(), reverse=False)
        dicc2 = {}
        str0 = ""
        for name, count in l:
            str0 = str0 + name + "," + count + "\n"
            
        fo.writelines(str0)
        fo.close()
        
    except ValueError:
        print("Please, check the Internet connection")
