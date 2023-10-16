#!/bin/bash
# Copyright (C) 2020  David Arroyo Menéndez (davidam@gmail.com)
# This file is part of Damegender.

# Author: David Arroyo Menéndez <davidam@gmail.com>
# Maintainer: David Arroyo Menéndez <davidam@gmail.com>

# This file is Free Software; you can redistribute it and/or modify
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

cd ../..

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

cp config.cfg config.cfg.backup

echo "We need enable apis to execute this script, we are trying to do it for you..."

cp config.enabled.cfg config.cfg

echo "Checking Internet connection"
wget -q --spider http://google.com

if [ $? -eq 0 ]; then
    echo "Online"

    python3 api2gender.py David --api="wikidata" > files/tests/api2genderwikidata-$(date "+%Y-%m-%d-%H").txt

    if ! diff files/tests/api2genderwikidata.txt files/tests/api2genderwikidata-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
    then
	echo -e "api2genderiwikidata test is ${RED}failing${NC}"
    else
	echo -e "api2genderwikidata test is ${GREEN}ok${NC}"
    fi

    python3 downloadjson.py --api=brazilapi --csv=files/names/min.csv --outjson=files/tmp/brazilapimin.json

    if [ -f files/tmp/brazilapimin.json ]; then
	echo -e "download brazilapi json files names min is ${GREEN}ok${NC}"
    else
	echo -e "download brazilapi json files names min is ${RED}failing${NC}"
    fi

    python3 downloadcsv.py --api=brazilapi --csv=files/names/min.csv --outcsv=files/tmp/brazilapimin.csv

    if [ -f files/tmp/brazilapimin.csv ]; then
	echo -e "download brazilapi csv files names min is ${GREEN}ok${NC}"
    else
	echo -e "download brazilapi csv files names min is ${RED}failing${NC}"
    fi

    python3 downloadcsv.py --api=genderapi --csv=files/names/min.csv --outcsv=files/tmp/genderapimin.csv

    if [ -f files/tmp/genderapimin.csv ]; then
	echo -e "download genderapi csv files names min is ${GREEN}ok${NC}"
    else
	echo -e "download genderapi csv files names min is ${RED}failing${NC}"
    fi

    python3 downloadcsv.py --api=genderapi --csv=files/names/min.csv --outcsv=files/tmp/genderapiminfemales.csv --outformat="females"

    if [ -f files/tmp/genderapiminfemales.csv ]; then
	echo -e "download genderapi csv files names min is ${GREEN}ok${NC}"
    else
	echo -e "download genderapi csv files names min is ${RED}failing${NC}"
    fi

    python3 downloadcsv.py --api=genderapi --csv=files/names/min.csv --outcsv=files/tmp/genderapiminmales.csv --outformat="males"

    if [ -f files/tmp/genderapiminmales.csv ]; then
	echo -e "download genderapi csv files names min is ${GREEN}ok${NC}"
    else
	echo -e "download genderapi csv files names min is ${RED}failing${NC}"
    fi

    python3 downloadcsv.py --api=genderapi --csv=files/names/min.csv --outcsv=files/tmp/genderapiminall.csv --outformat="all"

    if [ -f files/tmp/genderapiminall.csv ]; then
	echo -e "download genderapi csv files names min is ${GREEN}ok${NC}"
    else
	echo -e "download genderapi csv files names min is ${RED}failing${NC}"
    fi


    python3 downloadcsv.py --api=genderize --csv=files/names/min.csv --outcsv=files/tmp/genderizeminfemales.csv --outformat="females"

    if [ -f files/tmp/genderizeminfemales.csv ]; then
	echo -e "download genderize csv files names min is ${GREEN}ok${NC}"
    else
	echo -e "download genderize csv files names min is ${RED}failing${NC}"
    fi

    python3 downloadcsv.py --api=genderize --csv=files/names/min.csv --outcsv=files/tmp/genderizeminmales.csv --outformat='males'

    if [ -f files/tmp/genderizeminmales.csv ]; then
	echo -e "download genderize csv files names min is ${GREEN}ok${NC}"
    else
	echo -e "download genderize csv files names min is ${RED}failing${NC}"
    fi

    python3 downloadcsv.py --api=genderize --csv=files/names/min.csv --outcsv=files/tmp/genderizeminall.csv --outformat='all'

    if [ -f files/tmp/genderizeminall.csv ]; then
	echo -e "download genderize csv files names min is ${GREEN}ok${NC}"
    else
	echo -e "download genderize csv files names min is ${RED}failing${NC}"
    fi


    if [ -f files/apikeys/genderizepass.txt ]; then

	python3 api2gender.py David --api="genderize" > files/tests/api2genderDavidgenderize-$(date "+%Y-%m-%d-%H").txt

	if ! diff files/tests/api2genderDavidgenderize.txt files/tests/api2genderDavidgenderize-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
	then
	    echo -e "api2genderDavidgenderize test is ${RED}failing${NC}"
	else
	    echo -e "api2genderDavidgenderize test is ${GREEN}ok${NC}"
	fi

	python3 downloadjson.py --api=genderize --csv=files/names/min.csv

	if [ -f files/names/genderizefiles_names_min.csv.json ]; then
	    echo -e "download genderize files names min is ${GREEN}ok${NC}"
	else
	    echo -e "download genderize files names min is ${RED}failing${NC}"
	fi
    else
	echo -e "Doesn't exist files/apikeys/genderizepass.txt. You must introduce the api key in this file"
    fi

    if [ -f files/apikeys/namsorpass.txt ]; then
	python3 api2gender.py Leticia --surname="Martin" --api="namsor" > files/tests/api2genderLeticianamsor-$(date "+%Y-%m-%d-%H").txt

	if ! diff files/tests/api2genderLeticianamsor.txt files/tests/api2genderLeticianamsor-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
	then
	    echo -e "api2genderLeticianamsor test is ${RED}failing${NC}"
	else
	    echo -e "api2genderLeticianamsor test is ${GREEN}ok${NC}"
	fi

	python3 downloadjson.py --api=namsor --csv=files/names/min.csv

	if [ -f files/names/namsorfiles_names_min.csv.json ]; then
	    echo -e "download namsor files names min is ${GREEN}ok${NC}"
	else
	    echo -e "download namsor files names min is ${RED}failing${NC}"
	fi
    else
	echo -e "Doesn't exist files/apikeys/namsorpass.txt. You must introduce the api key in this file"

    fi

    if [ -f files/apikeys/genderapipass.txt ]; then

	python3 downloadjson.py --api=genderapi --csv=files/names/min.csv

	if [ -f files/names/genderapifiles_names_min.csv.json ]; then
	    echo -e "download genderapi files names min is ${GREEN}ok${NC}"
	else
	    echo -e "download genderapi files names min is ${RED}failing${NC}"
	fi

	python3 downloadjson.py --api=genderapi --csv=files/names/names_tests/gender_JMLA.min.dta.csv --name_position=1

	if [ -f files/names/genderapifiles_names_min.csv.json ]; then
	    echo -e "download genderapi files names min is ${GREEN}ok${NC}"
	else
	    echo -e "download genderapi files names min is ${RED}failing${NC}"
	fi

	
	python3 api2gender.py Inés --api="genderapi" > files/tests/api2genderInésgenderapi-$(date "+%Y-%m-%d-%H").txt

	if ! diff files/tests/api2genderInésgenderapi.txt files/tests/api2genderInésgenderapi-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
	then
	    echo -e "api2genderInésgenderapi test is ${RED}failing${NC}"
	else
	    echo -e "api2genderInésgenderapi test is ${GREEN}ok${NC}"
	fi

    else
	echo "Doesn't exist files/apikeys/genderapipass.txt. You must introduce the api key in this file"

    fi

    
else
    echo "Offline"
fi

echo "cleaning temporary files"
rm files/tests/*$(date "+%Y")*.txt

echo "restoring config.cfg"
cp config.cfg.backup config.cfg
