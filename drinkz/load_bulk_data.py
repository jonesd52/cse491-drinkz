"""
Module to load in bulk data from text files.
"""

# ^^ the above is a module-level docstring.  Try:
#
#   import drinkz.load_bulk_data
#   help(drinkz.load_bulk_data)
#

import csv                              # Python csv package

from . import db                        # import from local package

def read_data(i_file):
  
    reader = csv.reader(i_file)
    
    x = []
    
    for line in reader:
        print line
        if not line:
	    continue
        if not line[0].strip():
	    continue
        if line[0].startswith('#'):
	    continue
	  
	x.append(line)

    print x
    return x
    
    

def load_bottle_types(fp):
    """
    Loads in data of the form manufacturer/liquor name/type from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of bottle types loaded
    """
    #reader = csv.reader(fp)
    new_reader = read_data(fp)

    x = []
    n = 0
    
    
    for (mfg, name, typ) in new_reader:
        n += 1
        db.add_bottle_type(mfg, name, typ)

    return n

def load_inventory(fp):
    """
    Loads in data of the form manufacturer/liquor name/amount from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of records loaded.

    Note that a LiquorMissing exception is raised if bottle_types_db does
    not contain the manufacturer and liquor name already.
    """
    #reader = csv.reader(fp)
    new_reader = read_data(fp)

    x = []
    n = 0
    
    
    for (mfg,name,amount) in new_reader:
	n += 1
        db.add_to_inventory(mfg, name, amount)

    return n
