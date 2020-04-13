
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

LOCALE = "United Kingdom"

ADD = ADDRESSES = hierarchy = {'United Kingdom':
                            {'Exeter, Devon':
                                {'Topsham':
                                    ['Hamilton Road',
                                     'Strand',
                                     'Wendover Way',
                                     'Western Avenue',
                                     'Ashford Road',
                                     'Tollards Road',
                                     'Tresilian Gardens',
                                     'Ludwell Lane',
                                     'Rydon Lane',
                                     'Altamira',
                                     'Old Rydon Close',
                                     'Bishop Westall Road',
                                     'Monmouth Hill',
                                     'Victoria Road',
                                     'North Street',
                                     'Elm Grove Avenue',
                                     'Bowling Green Road',
                                     'Moonridge',
                                     'Topsham Road',
                                     'Pynes Hill',
                                     'River Plate Road',
                                     'Rivers Walk',
                                     'Station Road',
                                     'Bridge Hill',
                                     'The Copse',
                                     'Liberty Way',
                                     'Pound Lane',
                                     'Globe Lane',
                                     'High Street',
                                     'Underhill Terrace',
                                     'Resolution Road',
                                     'Strand View',
                                     'Lower Shapter Street',
                                     'Gordon Road',
                                     'Denver Close',
                                     'Southbrook Road',
                                     'Highfield',
                                     'Orchard Way',
                                     'Newcourt Road',
                                     'Exe Street',
                                     'Balmoral Gardens',
                                     'Ferry Road',
                                     'Globefield',
                                     'Exeter Road',
                                     'The Mede',
                                     'Monmouth Avenue',
                                     'Elm Grove Gardens',
                                     'Caroline Avenue',
                                     'Holman Way',
                                     'Old Rydon Lane',
                                     'Swallowfield Road',
                                     'Wessex Close',
                                     'Omaha Drive',
                                     'Denver Road',
                                     'Higher Shapter Close',
                                     'Greatwood Terrace',
                                     'Haldon Close',
                                     'Tappers Close',
                                     'Eastern Avenue',
                                     'Fore Street',
                                     'Rhode Island Drive',
                                     'Sidmouth Road',
                                     'Robert Davey Road',
                                     'Clyst Road',
                                     'Sir Alex Walk',
                                     'Towerfield',
                                     'Grove Hill',
                                     'Nurseries Close',
                                     'Parkfield Road',
                                     'Sunhill Avenue',
                                     'Retreat Road',
                                     'Batavia Drive',
                                     'Russell Way',
                                     'Nelson Close',
                                     'Jutland Way',
                                     'Central Avenue',
                                     'Monmouth Street',
                                     'Second Avenue',
                                     'White Street',
                                     'Follett Road',
                                     'Riverside Road',
                                     'Belvedere Close',
                                     'Pound Close',
                                     'Powderham Close',
                                     'Bridgehill Garth',
                                     'Elm Grove Road',
                                     'First Avenue',
                                     'Higher Shapter Street',
                                     'Old Rydon Ley',
                                     'The Retreat Drive',
                                     'Third Avenue']},
                             'Hammersmith & Fulham, London':
                                {'Fulham': ['Munster Road',
                                              'Fulham Palace '
                                              'Road',
                                              "New King's "
                                              'Road'],
                                 'Hammersmith': ['Talgarth '
                                                   'Road',
                                                   'Hammersmith '
                                                   'Road']},
                              'Kingston-upon-Thames, London':
                                 {'':
                                      ['Richmond Road',
                                      'London Road',
                                      'Kingston Hill'],
                                  'New Malden':
                                      ['Salisbury '
                                       'Road',
                                       'Coombe '
                                       'Road']},
                               'Lambeth, London':
                                  {'Brixton':
                                       ['Acre Lane',
                                        'Town Hall Parade'],
                               'Clapham Town':
                                       ['The Pavement',
                                        'Venn Street',
                                        'Clapham High '
                                        'Street']},
                              'Merton, London':
                                    {'Mitcham':
                                     ['Croydon Road',
                                      'Madeira Road'],
                              'Morden':
                                     ['St Helier Avenue',
                                      'Central Road',
                                      'London Road']},
                              'Wandsworth, London':
                                 {'Balham':
                                   ['Royal Duchess Mews',
                                    'Harberson Road',
                                    'Beira Street',
                                    'Gaskarth Road',
                                    'Amner Road',
                                    'Wroughton Road',
                                    'Caistor Road',
                                    'Martindale Road',
                                    'Earlsthorpe Mews',
                                    'Lammermoor Road',
                                    'Cathles Road',
                                    'Caister Mews',
                                    'Old Devonshire Road',
                                    'Walsingham Place',
                                    'Alderbrook Road',
                                    'Grove Place',
                                    'Hillier Road',
                                    'Malwood Road',
                                    'Ranmere Street',
                                    'Bedford Hill',
                                    'Lysias Road',
                                    'Shipka Road',
                                    'Windmill Drive',
                                    'Bellamy Street',
                                    'Morella Road',
                                    'Broomwood Road',
                                    'Balham High Road',
                                    'Granard Road',
                                    'Ravenswood Road',
                                    'Hanson Close',
                                    'Rinaldo Road',
                                    'Rusham Road',
                                    'Pickets Street',
                                    'Yukon Road',
                                    'Kenilford Road',
                                    'Blandfield Road',
                                    'Ormeley Road',
                                    'Fernlea Road',
                                    'Roseneath Road',
                                    'Balham New Road',
                                    'Badminton Road',
                                    'Devereux Road',
                                    'Clarence Mews',
                                    'Hendrick Avenue',
                                    'Manchuria Road',
                                    'Verran Road',
                                    'Lochinvar Street',
                                    'Kyrle Road',
                                    'Clapham Common West '
                                    'Side',
                                    'Laitwood Road',
                                    'Cavendish Road',
                                    'Nightingale Lane',
                                    'Temperley Road',
                                    'Denning Mews',
                                    'Ramsden Road',
                                    'Penny Mews',
                                    'Sumburgh Road',
                                    'Bracken Avenue',
                                    'Broxash Road',
                                    'Oldridge Road',
                                    'Thurleigh Avenue',
                                    'Hildreth Street',
                                    'The Avenue',
                                    'Bolingbroke Grove',
                                    'Nightingale Walk',
                                    'Ethelbert Street',
                                    'Dinsmore Road',
                                    'Thurleigh Road',
                                    'Balham Grove',
                                    'Lynn Road',
                                    'Ballingdon Road',
                                    'Holmside Road',
                                    'Sudbrooke Road',
                                    'Rossiter Road',
                                    'Balham Hill',
                                    'Westlands Terrace',
                                    'Baldwin Road',
                                    'Balham Station Road',
                                    'Old Park Avenue',
                                    'Clavering Place',
                                    'Hillgate Place',
                                    'Sistova Road',
                                    'Dagnan Road'],
                         'Battersea':
                                  ['Fowler Close',
                                   'Brynmaer Road',
                                   'Ingrave Street',
                                   'Brougham Street',
                                   'Millgrove Street',
                                   'Candahar Road',
                                   'Wolftencroft Close',
                                   'Trinity Road',
                                   'Mantua Street',
                                   'Fairchild Close',
                                   'Usk Road',
                                   'Kennet Close',
                                   'Mcdermott Close',
                                   'Abercrombie Street',
                                   'Este Road',
                                   'Batten Street',
                                   'Nepaul Road',
                                   'Shellwood Road',
                                   'Plough Road',
                                   'Musjid Road',
                                   'Bramlands Close',
                                   'Great Chart Street',
                                   'Weekley Square',
                                   'Odger Street',
                                   'Wye Street',
                                   'Wallis Close',
                                   'Benham Close',
                                   'Wynter Street',
                                   'Falcon Road',
                                   'Parkside Street',
                                   'Dagnall Street',
                                   'Cabul Road',
                                   'Poyntz Road',
                                   'Grant Road',
                                   'Kambala Road',
                                   'Lavender Road',
                                   'Patience Road',
                                   'Henley Street',
                                   'Knowsley Road',
                                   'Beechmore Road',
                                   'Frere Street',
                                   'Matthews Street',
                                   'Cranleigh Mews',
                                   'Longhedge Street',
                                   'Burns Road',
                                   'Kersley Street',
                                   'Kennard Street',
                                   'Chesney Street',
                                   'Reform Street',
                                   'Rowena Crescent',
                                   'Sullivan Close',
                                   'Heaver Road',
                                   'Blondel Street',
                                   'Sheepcote Lane',
                                   'Fawcett Close',
                                   'Hope Street',
                                   'Wayford Street',
                                   'Afghan Road',
                                   'Crombie Mews',
                                   'Winstanley Road',
                                   'Hicks Close',
                                   'Battersea Park Road',
                                   'Albert Bridge Road',
                                   'Chillington Drive',
                                   'Thomas Baines Road',
                                   'Freedom Street',
                                   'Holgate Avenue',
                                   'Maysoule Road',
                                   'Fownes Street',
                                   'Coppock Close',
                                   'Eltringham Street',
                                   'Atherton Street',
                                   'Darien Road',
                                   'Astle Street',
                                   'Falcon Terrace',
                                   'Harpsden Street',
                                   "St James's Grove",
                                   'Petergate',
                                   'Livingstone Road',
                                   'Hibbert Street',
                                   'York Road',
                                   'Lavender Terrace',
                                   'Joubert Street',
                                   'Culvert Road',
                                   'Battersea Bridge '
                                   'Road',
                                   'Falcon Grove',
                                   'Khyber Road',
                                   'Rowditch Lane',
                                   'Lombard Road',
                                   'Orkney Street',
                                   'Meyrick Road',
                                   'Windrush Close',
                                   'Latchmere Road',
                                   'Beverley Close',
                                   'Latchmere Street',
                                   'Newcomen Road',
                                   'Kerrison Road'],
                         'Putney':
                                   ['Greenstead Gardens',
                                    'Woodborough Road',
                                    'Chartfield Avenue',
                                    'Swinburne Road',
                                    'Pettiward Close',
                                    'Cortis Road',
                                    'Holroyd Road',
                                    'Luttrell Avenue',
                                    'Dover House Road',
                                    'Elmshaw Road',
                                    'Queensgate Gardens',
                                    'Torwood Road',
                                    'Montolieu Gardens',
                                    'Lysons Walk',
                                    'Aubyn Square',
                                    'Campion Road',
                                    'Isis Close',
                                    'Marrick Close',
                                    'Mendez Way',
                                    'Cotman Close',
                                    'Larpent Avenue',
                                    'Enmore Road',
                                    'Hobbes Walk',
                                    'Cortis Terrace',
                                    'Hawkesbury Road',
                                    'Bramcote Road',
                                    'Gibbon Walk',
                                    'Balfour Place',
                                    'Dungarvan Avenue',
                                    'Westmead',
                                    'Tideswell Road',
                                    'Akehurst Street',
                                    'Colinette Road',
                                    'Eliot Gardens',
                                    'Briar Walk',
                                    'Coalecroft Road',
                                    'Putney Park Avenue',
                                    'Holford Way',
                                    'Huntingfield Road',
                                    'Parkstead Road',
                                    'Toland Square',
                                    'Granard Avenue',
                                    'Malbrook Road',
                                    'Kingslawn Close',
                                    'Castello Avenue',
                                    'Coppice Drive',
                                    'Fairdale Gardens',
                                    'The Footpath',
                                    'Roehampton Close',
                                    'Fairfax Mews',
                                    "Howard's Lane",
                                    'Telegraph Road',
                                    'Dryburgh Road',
                                    'Roehampton Lane',
                                    'Tildesley Road',
                                    'Breasley Close',
                                    'Putney Heath',
                                    'Daylesford Avenue',
                                    'Sunnymead Road',
                                    'Pullman Gardens',
                                    'Henty Walk',
                                    'Langside Avenue',
                                    'Carslake Road',
                                    'Genoa Avenue',
                                    'William Gardens',
                                    'Solna Avenue',
                                    'Vanneck Square',
                                    'Woodthorpe Road',
                                    'Grosse Way',
                                    'Balmuir Gardens',
                                    'The Pleasance',
                                    "St Margaret's Crescent",
                                    'Parkmead',
                                    'Highdown Road',
                                    'Ellenborough Place',
                                    'Upper Richmond Road',
                                    'Dover Park Drive',
                                    'Innes Gardens',
                                    'Hayward Gardens',
                                    'Hazlewell Road',
                                    'Parkfields',
                                    'Putney Hill',
                                    'Carmalt Gardens',
                                    'Wildcroft Road',
                                    'Lantern Close',
                                    'Dealtry Road',
                                    'Westleigh Avenue',
                                    'Laneway',
                                    'Pleasance Road',
                                    'Crestway',
                                    'Putney Park Lane',
                                    'Wandsworth High Street',
                                    'East Hill'],
                         'Wandsworth':
                                   ['Acris Street',
                                    'Allfarthing Lane',
                                    'Alma Terrace',
                                    'Aslett Street',
                                    'Barmouth Road',
                                    'Baskerville Road',
                                    'Bassingham Road',
                                    'Battersea Rise',
                                    'Beechcroft Road',
                                    'Bevin Square',
                                    'Brightman Road',
                                    'Broadgates Road',
                                    'Brocklebank Road',
                                    'Brodrick Road',
                                    'Bucharest Road',
                                    'Burcote Road',
                                    'Burntwood Close',
                                    'Burntwood Grange '
                                    'Road',
                                    'Burntwood Lane',
                                    'Cader Road',
                                    'Carmichael Mews',
                                    'Chancery Mews',
                                    'Cicada Road',
                                    'Coates Avenue',
                                    'Collamore Avenue',
                                    'College Gardens',
                                    'Crealock Street',
                                    'Crieff Road',
                                    'Daphne Street',
                                    'Dingwall Road',
                                    'Dorlcote Road',
                                    'Earlsfield Road',
                                    'East Hill',
                                    'Ellerton Road',
                                    'Fieldview',
                                    'Fitzhugh Grove',
                                    'Frewin Road',
                                    'Galesbury Road',
                                    'Geraldine Road',
                                    'Glenburnie Road',
                                    'Godley Road',
                                    'Groom Crescent',
                                    'Gunners Road',
                                    'Heathfield Avenue',
                                    'Heathfield Gardens',
                                    'Heathfield Road',
                                    'Heathfield Square',
                                    'Henderson Road',
                                    'Herondale Avenue',
                                    'Huguenot Place',
                                    'Inman Road',
                                    'Jessica Road',
                                    'Jeypore Road',
                                    'John Archer Way',
                                    'Kershaw Close',
                                    'Killarney Road',
                                    'Loxley Road',
                                    'Lyford Road',
                                    'Lyminge Gardens',
                                    'Magdalen Road',
                                    'Marcilly Road',
                                    'Marham Gardens',
                                    'Melody Road',
                                    'Muir Drive',
                                    'Multon Road',
                                    'Nevinson Close',
                                    'Nicosia Road',
                                    'North Side '
                                    'Wandsworth Common',
                                    'Openview',
                                    'Patten Road',
                                    'Quarry Road',
                                    'Routh Road',
                                    'Sandgate Lane',
                                    'Spencer Park',
                                    "St Ann's Hill",
                                    "St Ann's Park Road",
                                    'St Anthonys Close',
                                    'St Benets Close',
                                    'St Catherines Close',
                                    'St Edmunds Close',
                                    'St Hildas Close',
                                    'St Hughes Close',
                                    'St Peters Close',
                                    'Stott Close',
                                    'Strickland Row',
                                    'Swaffield Road',
                                    'Swanage Road',
                                    'Tilehurst Road',
                                    'Titchwell Road',
                                    'Trefoil Road',
                                    'Trinity Road',
                                    'Wandle Road',
                                    'Wandsworth Common '
                                    'West Side',
                                    'Westover Road',
                                    'Wilde Place',
                                    'Wilna Road',
                                    'Windmill Road',
                                    'Winfrith Road']}}}

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

uk = Address()
