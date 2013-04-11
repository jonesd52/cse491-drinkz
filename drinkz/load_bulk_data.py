"""
Module to load in bulk data from text files.
"""

# ^^ the above is a module-level docstring.  Try:
#
#   import drinkz.load_bulk_data
#   help(drinkz.load_bulk_data)
#

import csv                              # Python csv package

from . import db, recipes                        # import from local package

def read_data(i_file):
  
    reader = csv.reader(i_file)
    
    x = []
    
    for line in reader:
        if not line or not line[0].strip() or line[0].startswith('#'):
            continue
        yield line

def read_recipe_data(i_file):
    
    for line in i_file:
        if not line or not line[0].strip() or line[0].startswith('#'):
             continue
        yield line
    

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
    
    for line in new_reader:
        try:
            (mfg, name, typ) = line
        except ValueError:
            print 'Badly formatted line: %s' % line
	    continue

        
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
    
    for line in new_reader:
        try:
            (mfg, name, amount) = line
        except ValueError:
	    print 'Badly formatted line: %s' % line
	    continue
    
        n += 1
        db.add_to_inventory(mfg, name, amount)

    return n


def load_recipes(fp):
    "Load bulk number of recipes"

    new_reader = read_recipe_data(fp)

    n = 0
    
    for line in new_reader:
        x = []
        line = line.split('|')
        name = line[0]
        ingredients = line[1]
        ingredients = ingredients.split('/')
        while (ingredients != []):
             r = ingredients[0].split(',')
	     ingredients.pop(0)
             t = (r[0], r[1])
	     x.append(t)

        recipe = recipes.Recipe(name, x)
        db.add_recipe(recipe)
	n += 1
    
    return n


        



