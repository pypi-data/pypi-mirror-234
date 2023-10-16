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

# DESCRIPTION: This script allows to download a list of names in a
# json files from a csv file with an api system


from app.dame_gender import Gender
from app.dame_namsor import DameNamsor
from app.dame_genderize import DameGenderize
from app.dame_genderapi import DameGenderApi
from app.dame_nameapi import DameNameapi
from app.dame_brazilapi import DameBrazilApi
from app.dame_utils import DameUtils

import argparse
import os
parser = argparse.ArgumentParser()
parser.add_argument('--csv', type=str, required=True,
                    default="files/names/min.csv", help='input file for names')
parser.add_argument('--name_position', type=int, required=False,
                    default=0, help='input file for names')
parser.add_argument('--api', required=True,
                    choices=['brazilapi', 'genderapi',
                             'genderize', 'namsor', 'nameapi'])
parser.add_argument("--surnames", default=False,
                    action="store_true", help="Flag to surnames")
parser.add_argument('--outjson', type=str, required=False,
                    default="names.json", help='output file for names')
args = parser.parse_args()

du = DameUtils()

if not(du.check_connection("https://www.google.com")):
    print("You can't to use this script without Internet")
    exit()

if (args.api == 'genderize'):
    dg = DameGenderize()
    text1 = dg.download(path=args.csv,
                        surnames=args.surnames,
                        name_position=args.name_position,
                        backup=args.outjson)
elif (args.api == 'genderapi'):
    dga = DameGenderApi()
    if (dga.config['DEFAULT']['genderapi'] == 'yes'):
        num = len(dga.csv2names(args.csv, name_position=args.name_position))
        if (dga.apikey_limit_exceeded_p() is False):
            text1 = dga.download(path=args.csv,
                                 name_position=args.name_position,
                                 backup=args.outjson)
        elif (dga.apikey_count_requests() < num):
            print("You don't have enough requests with this api key")
        elif (dga.apikey_count_requests() >= num):
            text1 = dga.download(path=args.csv,
                                 name_position=args.name_position,
                                 backup=args.outjson)
        else:
            print("You have not money with this api key")
    else:
        print("You must enable genderapi in config.cfg")
elif (args.api == 'namsor'):
    dn = DameNamsor()
    if (dn.config['DEFAULT']['namsor'] == 'yes'):
        text1 = dn.download(path=args.csv,
                            name_position=args.name_position,
                            backup=args.outjson)
    else:
        print("You must enable namsor in config.cfg")
elif (args.api == 'nameapi'):
    dna = DameNameapi()
    if (dna.config['DEFAULT']['nameapi'] == 'yes'):
        text1 = dna.download(path=args.csv,
                             name_position=args.name_position,
                             backup=args.outjson)
    else:
        print("You must enable nameapi in config.cfg")

elif (args.api == 'brazilapi'):
    dba = DameBrazilApi()
    text1 = dba.download(path=args.csv,
                         name_position=args.name_position,
                         backup=args.outjson)
