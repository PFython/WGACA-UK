# ETL utilitilies (Extract, Transform, Load) for taking Ordnance Survey
# address spreadsheets and extracting basic Named Street information.

from pathlib import Path
import pandas as pd
import datetime
import os
import json
import pyperclip

import anvil.server
from anvil.tables import app_tables
from streetdata_config import UK_DEV_TEST, UK_PROD
anvil.server.connect(UK_DEV_TEST)
# anvil.server.connect(UK_PROD)

# Shortcuts and aliases
if __name__ == "__main__":
    try:
        data_path = Path(__file__).parent / "OS data"
    except NameError:
        data_path = Path.cwd().parent / "OS data"
else:
    data_path = Path.cwd().parent / "OS data"
header_path = data_path / "OS_Open_Names_Header.csv"
header = pd.read_csv(header_path)
fields = "NAME1 TYPE LOCAL_TYPE POSTCODE_DISTRICT POPULATED_PLACE DISTRICT_BOROUGH COUNTY_UNITARY".split()
final_fields = "NAME1 POPULATED_PLACE COUNTY_UNITARY address_line".split()
sheet_options = {'1': ("Single spreadsheet HP40.csv",[data_path /(x+".csv") for x in "HP40".split()]),
              '2': ("Two spreadsheets TQ00.csv and SU20.csv", [data_path /(x+".csv") for x in "TQ00 SU20".split()]),
              '3': ("All 800+ Ordnance Survey Spreadsheets", [x for x in data_path.glob('*.csv') if x != header_path]),}
separator = "; "

def upload_txt():
    """ Send as file to Anvil for onward emailing"""
    file_path = data_path / "OS.txt"
    with open(file_path,"r", encoding='utf-8') as file:
        print(F"Uploading: {file_path}")
        blob = anvil.BlobMedia("text/plain",file.read(), file_path.name)
        row = app_tables.uploads.add_row(name = "Address_Data_UK", media = blob, datetime = datetime.datetime.now())

def safe_filepath(filepath):
    """
    Checks to see if file already exists.
    If so,adds a timestamp to the base filepath thereby returning
    "safe" filepath which will not over-write an existing file.

    Returns a pathlib.Path object.

    Safe to within 1 second.
    """
    if filepath.is_file():
        return Path(f'{filepath.parent / filepath.stem} [{datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}]{filepath.suffix}')
    else:
        return Path(filepath)

def load_OS():
    """ Load OS.json from file"""
    global OS
    path = data_path / "OS.json"
    with open(path,"r", encoding='utf-8') as file:
        OS = json.loads(file.read())

def save(sheet, filepath, echo = True):
    """ Classic save to file """
    filepath = safe_filepath(safe_filepath(filepath))
    with open(filepath,"a",encoding='utf-8') as file:
        file.writelines(sheet)
    if echo:
        print("Saved as:",filepath.absolute())

def save_py():
    """ Save data as a .py file to import from: from OS import address_list"""
    mega_set = set()
    for sheet, lines in OS.items():
        for line in lines:
            mega_set.add(line)
    mega_set_py = f"address_list = {repr(mega_set)}"
    with open(safe_filepath(data_path / "OS.py"), "w", encoding = 'utf-8') as file:
        file.write(mega_set_py)

def save_json():
    with open(safe_filepath(data_path / "OS.json"),"w") as file:
        file.write(json.dumps(OS, indent=4, sort_keys=True))

def save_txt():
    """ Saves a list to file using .writelines """
    mega_set = set()
    for sheet, lines in OS.items():
        for line in lines:
            mega_set.add(line)
    mega_set = sorted([x for x in list(mega_set) if x != ""])
    with open(safe_filepath(data_path / "OS.txt"), "a", encoding = 'utf-8') as file:
        file.writelines(mega_set)

def sheet(search):
    """
    Returns any sheet names containing the search string.
    """
    results = []
    search = search.lower()
    global OS
    for sheet in OS:
        for line in OS[sheet]:
            if search.lower() in line.lower():
                results += [sheet]
                break
    return results

def index(echo=True):
    """
    Creates a global variable INDEX containing an index of sheet numbers and
    counties within each sheet.
    """
    sheet_index = {}
    for sheet, lines in OS.items():
        counties = set()
        for line in lines:
            *_, county = line.split(separator)
            counties.add(county)
        sheet_index[sheet] = counties
        if echo:
            print(sheet, ":",counties)
    global INDEX
    INDEX = sheet_index

def search(string):
    """ Searches for a keyword within each line of OS """
    matches = {}
    global OS
    for sheet in OS:
        for line in OS[sheet]:
            if string.lower() in line.lower():
                if matches.get(sheet):
                    matches[sheet] += [line]
                else:
                    matches[sheet] = [line]
    return matches

def cleanup():
    """Deletes ALL .txt files in parent"""
    all_text = list(data_path.glob('*.txt'))
    print(len(all_text),".txt files identified for deletion...")
    if len(all_text) > 10:
        print("\n".join([x.name for x in all_text[:5]]))
        print(".....")
        print("\n".join([x.name for x in all_text[-5:]]))
    else:
        print("\n".join([x.name for x in all_text]))
    i = input("Press ENTER to cancel or (X) to delete: ")
    if i.lower() == "x":
        for file in all_text:
            if file.name != "OS.txt":
                os.remove(file)
                print(file.name,"removed.")

def adjust_miscellaneous(data):
    """ Various corrections/replacements spotten in source data """
    changes = {"'Tween Woods Lane": "Tween Woods Lane",
               "'b' Station Road": "Station Road",
               "(Old) Middlewich": "Old Middlewich",
               "Àite Bhaile à Bhlàir": "Aite Bhaile a Bhlair",
               "Queen 'S Arms Yard": "Queen's Arms Yard",}
    for line in data.copy():
        for original, new in changes.items():
            if line.startswith(original):
                data += [line.replace(original, new)]
                data.remove(line)
    return data

def adjust_london(data):
    """
    Transforms mystreet; London; Brent, Greater London i.e.
    where no town is given for a London address.
    """
    new_data = []
    for line in data:
        street, town, county = line.split(separator)
        if town == "London":
            town = county.split(", ")[0]
        line = separator.join([street, town, county])
        new_data += [line]
    return new_data

def select_sheets(import_option=""):
    """ Uses sheet_options to select between 1, 2, or 817 sheets to process """
    global sheet_options
    if import_option == "":
        for key, value in sheet_options.items():
            print(key, ":", value[0])
        import_option = input("Please select an input source from the list above: ")
    if import_option not in sheet_options.keys():
        return
    else:
        return sheet_options[import_option][1]

def count_rows():
    """
    Returns the number of rows in in all selected spreadsheets, for interest!
    """
    all_sheets = select_sheets()
    if not all_sheets:
        return
    row_count = 0
    for sheet in all_sheets:
        print(sheet)
        data = pd.read_csv(sheet, low_memory=False)
        row_count += len(data)
    return row_count

def handle_data_gaps(address_string):
    street, town, county = address_string.split(separator)
    if "london" not in county.lower():
        county = county.replace(", _","") # missing COUNTY_UNITARY
        county = county.replace("_, ","") # missing DISTRICT_BOROUGH
        county = county if county else town # both missing
        town = town if town != "_" else county.rstrip()
        # except AttributeError:
        #         OS_fail.add(sheet)
        #     except ValueError:
        #         print ("ValueError:",x)
        # print("Empty/problem sheets saved to  global variable OS_fail.")
    return separator.join([street, town, county])

# Main Loop
def importOS(import_option="", echo = False):
    """
    Imports one or more Ordnance Survey spreadsheets
    and converts to Street; Town; County format.

    Saves as global variable OS: a dictionary with sheet names as keys and
    Street; Town; County lines as values.
    """
    all_sheets = select_sheets(import_option)
    if not all_sheets:
        return
    total = len(all_sheets)
    data_dict = {}
    global OS, OS_fail, OS_empty
    OS_fail = OS_empty = set()
    for n, spreadsheet in enumerate(all_sheets):
        if echo:
            print(spreadsheet.name)
        else:
            percent = round((n+1)*100/total)
            print(F"Progress: {n+1} out of {total} ({percent}%)", end="\r")
        data = pd.read_csv(spreadsheet, low_memory=False)
        data.columns = header.columns
        data = data[fields]
        data_nr = data[data['LOCAL_TYPE'].isin(["Named Road"])]
        data_snr = data[data['LOCAL_TYPE'].isin(["Section Of Named Road"])]
        data = pd.concat([data_nr,data_snr])
        data['POPULATED_PLACE'] = data['POPULATED_PLACE'].fillna("_")
        data['DISTRICT_BOROUGH'] = data['DISTRICT_BOROUGH'].fillna("_")
        data['COUNTY_UNITARY'] = data['COUNTY_UNITARY'].fillna("_")
        data['address_line'] = data['NAME1']+separator+data['POPULATED_PLACE']+separator+data['DISTRICT_BOROUGH']+", "+data['COUNTY_UNITARY']+"\n"
        data = data[final_fields]
        data['final_address'] = data['address_line'].apply(handle_data_gaps)
        data = pd.unique(data['final_address']).tolist()
        data = adjust_london(data)
        data = adjust_miscellaneous(data)
        data_dict[spreadsheet.stem] = data
        save(data, data_path / (str(spreadsheet.stem) + ".txt"), False)
    print(end="\n")
    OS_empty = {spreadsheet:lines for spreadsheet,lines in data_dict.items() if lines ==[]}
    OS = {spreadsheet:lines for spreadsheet,lines in data_dict.items() if lines !=[]}

importOS()

# OTHER PANDAS COMMANDS I'VE BEEN PLAYING WITH

# tq, su = [pd.read_csv(x) for x in all_sheets]
# tq.columns = su.columns = header.columns
# su = su[fields]
#Look for value in column
# so16 = su[su['POSTCODE_DISTRICT'] == "SO16"]
# sux = su[su['LOCAL_TYPE'].isin(["Named Road"])]
# addr = sux['address_line'].tolist()
# is_NaN = suxx.isnull()
# row_has_NaN = is_NaN.any(axis=1)
# suxx[row_has_NaN]
# # Get single row
# sux.loc[ 2651 , : ]
# # Get a single value
# postcode = su.at[1001,"POSTCODE_DISTRICT"]
# # Extract rows as dictionary
# tq_dict = tq[0:3].to_dict()
