import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.media

# Version 0.1 created 2020-04-09
#
# This script is intended to:
#
# Assist in WGACA development and localisation tasks
# e.g. importing address data
#
# Author: peter@southwestlondon.tv
# © MMXX, South West London TV Ltd.

# AUTHOR SPECIFIC MODULES
# Spreadsheet and data tools
# import pfsheets

# STANDARD PYTHON MODULES
import time
import os
import pprint
import copy
import datetime
# MODULES INSTALLED USING PIP
# import pyperclip

from .Address_Data_UK import ADDRESSES
LOCALE = "United Kingdom"

class AutoHistory():
    """ This object has an in-built version history and the attributes .history and .modified are reserved for this purpose.  Please don't use them! """
    def __init__(self):
        self.__dict__["history"] = []
        self.__dict__['modified'] = datetime.datetime.now()
    def __setattr__(self, name, value):
        if name in "history modified".split():
            raise Exception(self.__doc__.strip())
        else:
        # Create backup of self & remove .history from copy to avoid recursion
            self_copy = AutoHistory()
            for key_copy, value_copy in self.__dict__.items():
                if key_copy != "history":
                    self_copy.__dict__[key_copy] = value_copy
            del self_copy.__dict__["history"]
            self.__dict__["history"] += [self_copy]
            self.__dict__[name] = value
            self.__dict__['modified'] = datetime.datetime.now()

    @staticmethod
    def format_date(datetime_object):
        return datetime_object.strftime("%Y-%m-%d at %H:%M:%S")

    def get_attr_history_tuples(self, attribute):
        """Returns the history of a particular attribute over time"""
        results = []
        for version in self.history:
            value = version.__dict__.get(attribute)
            results += [(version.modified, attribute, value)]
        return results

    def get_attr_history_string(self, attribute):
        return "\n".join([f"{AutoHistory.format_date(x)}: {y} = {z}" for x, y, z in self.get_attr_history_tuples(attribute)])

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        count = self.__dict__.get("history")
        count = f"{len(count)}" if count else "no"
        date = AutoHistory.format_date(self.modified)
        return f"This {type(self).__name__} object was modified on {date}."

class Address(AutoHistory):
    def __init__(self):
        super().__init__()
        self.data = ADDRESSES

    def add_street(self, address_string, country = LOCALE):
        """
        If required, creates a street list under Town key under County keyself.
        e.g. {'Exeter, Devon': {'Topsham': []}

        Input string separated by pipes e.g. 'Exeter, Devon | Topsham | Altamira'
        """
        try:
            county, town, street = address_string.replace("\r","").split(" | ")
        except ValueError:
            print(f"! badly formatted line: {address_string}")
            return
        if not self.data.get(country).get(county):
            self.data[country][county] = {}
            print(f"Added {county} to counties in {country}.  ")
        if not self.data.get(country).get(county).get(town):
            self.data[country][county][town]= []
            print(f"Added {town} to towns in {county}.  ")
        if street not in self.data[country][county][town]:
            self.data[country][county][town] += [street]
            print(f"Added {street} to streets in {town}.  ")

    def add_addresses(self, new_address_list):
        """
        Loops through a plain text list of addresses and adds to them to the
        global ADDRESSES dictionary.

        Format of each input line is e.g. 'Exeter, Devon | Topsham | Altamira'
        """
        for line in new_address_list.split("\n"):
            self.add_street(line, country = LOCALE)

    def remove_duplicate_streets(self, country = LOCALE):
        for county in self.data[country]:
            for town in self.data[country][county]:
                self.data[country][county][town] = list(set(self.data[country][county][town]))
                
    def save_all_as_dict(self):
        blob = anvil.BlobMedia("text/plain",self.__str__().encode('utf-8'), "addresses.txt")

uk = Address()
