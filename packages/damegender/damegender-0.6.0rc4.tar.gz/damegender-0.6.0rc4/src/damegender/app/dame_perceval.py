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


import requests
import json
import re
import datetime
from datetime import timedelta
from app.dame_utils import DameUtils
from app.dame_gender import Gender
try:
    from perceval.backends.core.mbox import MBox
    from perceval.backends.core.git import Git
    from perceval.backends.core.launchpad import Launchpad
except ModuleNotFoundError:
    print("module 'perceval' is not installed")
    print("try:")
    print("$ pip3 install 'perceval'")
    exit()


class DamePerceval(object):

    def numCommits(self, url, directory):
        # create a git object with the specified url and directory
        repo = Git(uri=url, gitpath=directory)
        count = 0
        for commit in repo.fetch():
            count += 1
        return count

    def numMails(self, url, directory="files/mbox"):
        # Counts the number of emails at a specific URL
        repo = MBox(uri=url, dirpath=directory)
        count = 0
        for message in repo.fetch():
            count += 1
        return count

    def removeMail(self, s):
        # removes an email address from a given string
        result = ""
        if re.search(r' ?<.*@.*>', s):
            result = re.sub(r' ?<.*@.*>', '', s)
        return result

    def firstName(self, s):
        # It uses the regular expression (re) library
        # to extract the first name from the string.
        result = ""
        m = re.match("(\\w+)", s)
        if m:
            first = m.group(1)
        else:
            first = ""
        return first

    def secondName(self, s):
        # If there is a match, it returns the second word.
        # If there is no match, it returns an empty string.
        result = ""
        m = re.match("(\\w+) (\\w+)", s)
        if m:
            second = m.group(2)
        else:
            second = ""
        return second

    def dicc_authors_and_commits(self, url, directory, *args, **kwargs):
        # creates a dictionary containing the authors and the number of
        # commits made by each one.
        repo = Git(uri=url, gitpath=directory)
        authors = {}
        for user in repo.fetch():
            if not (user['data']['Author'] in authors):
                authors[user['data']['Author']] = 1
            tmp = authors[user['data']['Author']]
            authors[user['data']['Author']] = tmp + 1
        return authors

    def dicc_authors_and_mails(self, url, directory="files/mbox"):
        # creates an MBox object from the specified url and directory.
        # Then, create an empty dictionary called authors.
        # Finally, it walks through the messages in the MBox repository
        # and adds the senders to authors as keys with
        # the number of messages sent as values.
        repo = MBox(uri=url, dirpath=directory)
        authors = {}
        for message in repo.fetch():
            if not (message['data']['From'] in authors.keys()):
                authors[message['data']['From']] = 1
            tmp = authors[message['data']['From']]
            authors[message['data']['From']] = tmp + 1
        return authors

    def list_committers(self, url, directory, *args, **kwargs):
        # make a list from a csv file
        mail = kwargs.get('mail', False)
        du = DameUtils()
        repo = Git(uri=url, gitpath=directory)
        list_committers = []
        for r in repo.fetch():
            if mail:
                committer = r['data']['Author']
            else:
                committer = self.removeMail(r['data']['Author'])
            list_committers.append(committer)
        list_committers = du.delete_duplicated(list_committers)
        return list_committers

    def list_mailers(self, url, directory="files/mbox"):
        # uses the MBox class to read email
        # messages in a specific URL and directory,
        # loop through each message, and add the sender to a list.
        # Finally, it returns the list of senders.
        repo = MBox(uri=url, dirpath=directory)
        count = 0
        list_mailers = []
        for message in repo.fetch():
            list_mailers.append(message['data']['From'])
        return list_mailers

    def list_launchpad(self, name, from_date=""):
        l1 = []
        if (from_date == ""):
            from_date = datetime.datetime.now() - timedelta(days=1)
        # name = "ubuntu"
        # retrieve only reviews changed since one day ago
        repo = Launchpad(name)
        for r in repo.fetch(from_date=from_date):
            x = r['data']['activity_data'][0]['person_data']['display_name']
            l1.append(x)
        return l1

    def count_gender_in_list(self, l1):
        # Count the number of men and women on a list.
        g = Gender()
        males = 0
        females = 0
        for elem in l1:
            x = int(g.name_frec(str(elem.upper()), 'us')['females'])
            y = int(g.name_frec(str(elem.upper()), 'us')['males'])
            if (x > y):
                females = females + 1
            else:
                males = males + 1
        return [females, males]

    def get_github_json_user(self, nick):
        # Returns a dictionary with the user's data in JSON format
        string = 'https://api.github.com/users/'
        string = string + nick
        r = requests.get(string)
        d = json.loads(r.text)
        return d
