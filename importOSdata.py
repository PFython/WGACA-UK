from pathlib import Path
import pandas as pd
import datetime
import os
import json
import pyperclip

# Shortcuts and aliases
parent = Path("""D:\Pete's Data\OneDrive\Python Scripts\WGACA_UK_DEV_TEST\OS data""")
server_code = Path("""D:\Pete's Data\OneDrive\Python Scripts\WGACA_UK_DEV_TEST\server_code""")
header_path = parent / "OS_Open_Names_Header.csv"
header = pd.read_csv(header_path)
fields = "NAME1 TYPE LOCAL_TYPE POSTCODE_DISTRICT POPULATED_PLACE DISTRICT_BOROUGH COUNTY_UNITARY".split()
sheet_options = {'1': ("Single spreadsheet TQ00.csv",[parent /(x+".csv") for x in "TQ00".split()]),
              '2': ("Two spreadsheets TQ00.csv and SU20.csv", [parent /(x+".csv") for x in "TQ00 SU20".split()]),
              '3': ("All 800+ Ordnance Survey Spreadsheets", [x for x in parent.glob('*.csv') if x != header_path]),}

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
    global OS
    with open("OS.json","r") as file:
        OS = json.loads(file.read())

def save(sheet, filename):
    filepath = safe_filepath(parent / f"{filename}")
    with open(filepath,"a",encoding='utf-8') as file:
        file.writelines(sheet)
    print("Saved as:",filepath.absolute())


def save_OS_as_py():
    mega_sheet = ['address_lines="""',]
    for sheet, lines in OS.items():
        mega_sheet.extend(lines)
    mega_sheet += ['"""']
    save(mega_sheet, "OS.py")
    # Deal with error:
    # 'utf-8' codec can't decode byte 0xe8 in position 8095968
    # with open(parent / "OS.py","r") as file:
    #     pyperclip.copy(file.read())
    # mega_sheet = pyperclip.paste()
    # save(mega_sheet, "OS.py")
    os.rename(parent / "OS.py", safe_filepath(server_code / "OS.py"))

def sheet(search):
        """
        Returns any sheet names containing the search string.
        """
        results = []
        search = search.lower()
        global OS
        for sheet in OS:
            for line in OS[sheet]:
                if search in line.lower():
                    results += [sheet]
                    break
        return results

def index(echo=True):
    """
    Creates a global variable OS containing an index of sheet numbers and
    counties within each sheet.
    """
    sheet_index = {}
    for sheet, lines in data_dict.items():
        counties = set()
        for line in lines:
            *_, county = line.split(" | ")
            counties.add(county)
        sheet_index[sheet] = counties
        if echo:
            print(sheet, ":",counties)
    global INDEX
    INDEX = sheet_index

def search(string):
    matches = {}
    global OS
    for sheet in OS:
        for line in OS[sheet]:
            if string in line:
                if matches.get(sheet):
                    matches[sheet] += [line]
                else:
                    matches[sheet] = [line]
    return matches

def cleanup():
    """Deletes ALL .txt files in parent"""
    all_text = list(parent.glob('*.txt'))
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
            os.remove(file)
            print(file.name,"removed.")

def adjust_london(data):
    """
    Transforms mystreet | London | Brent, Greater London i.e.
    where no town is given for a London address.
    """
    new_data = []
    for line in data:
        street, town, county = line.split(" | ")
        if town == "London":
            town = county.split(", ")[0]
        line = " | ".join([street, town, county])
        new_data += [line]
    return new_data


# Main Loop
def importOS(import_option=""):
    """
    Imports one or more Ordnance Survey spreadsheets
    and converts to Street | Town | County format.

    Returns a dictionary with sheet names as keys and
    Street | Town | County lines as values.
    """
    global sheet_options
    if import_option == "":
        for key, value in sheet_options.items():
            print(key, ":", value[0])
        import_option = input("Please select an input source from the list above: ")
    if import_option not in sheet_options.keys():
        return
    else:
        all_sheets = sheet_options[import_option][1]
    data_dict = {}
    for sheet in all_sheets:
        data = pd.read_csv(sheet)
        data.columns = header.columns
        data = data[fields]
        data_nr = data[data['LOCAL_TYPE'].isin(["Named Road"])]
        data_snr = data[data['LOCAL_TYPE'].isin(["Section Of Named Road"])]
        data = pd.concat([data_nr,data_snr])
        data['address_line'] = data['NAME1']+" | "+data['POPULATED_PLACE']+" | "+data['DISTRICT_BOROUGH']+", "+data['COUNTY_UNITARY']+"\n"
        data = pd.unique(data['address_line']).tolist()
        data = [x for x in data if type(x) != float]
        data = adjust_london(data)
        data_dict[sheet.stem] = data
        # counties(data, sheet.stem)
        # i = input("Press ENTER to cancel, or (S) to Save: ")
        # if i.lower() == 's':
        save(data, sheet.name)
    return {sheet:lines for sheet,lines in data_dict.items() if lines !=[]}

OS = importOS()
with open("OS.json","w") as file:
    file.write(json.dumps(OS, indent=4, sort_keys=True))



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
