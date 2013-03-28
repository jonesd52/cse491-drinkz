"""
Database functionality for drinkz information.

Saved the recipes in a dictionary.  Allows me to save the name as the key to the dictionary, with the recipe as the value.
Cannot have two different recipes with the same name.
"""

from cPickle import dump, load
import recipes  

# private singleton variables at module level
_bottle_types_db = set()
_inventory_db = dict()
_recipes_db = dict()

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db, _recipes_db
    _bottle_types_db = set()
    _inventory_db = dict()
    _recipes_db = dict()

def save_db(filename):
    fp = open(filename, 'wb')

    tosave = (_bottle_types_db, _inventory_db,_recipes_db)
    dump(tosave, fp)

    fp.close()

def load_db(filename):
    global _bottle_types_db, _inventory_db,_recipes_db
    fp = open(filename, 'rb')

    loaded = load(fp)
    (_bottle_types_db, _inventory_db,_recipes_db) = loaded

    fp.close()

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
    pass

class DuplicateRecipeName(Exception):
    pass

def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."
    _bottle_types_db.add((mfg, liquor, typ))

def _check_bottle_type_exists(mfg, liquor):
    for (m, l, _) in _bottle_types_db:
        if mfg == m and liquor == l:
            return True

    return False

def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."
    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)

    if check_inventory(mfg, liquor):
        new_amt = convert_to_ml(amount)
        old = convert_to_ml(_inventory_db[(mfg,liquor)])
        totes = new_amt + old
        _inventory_db[(mfg,liquor)] = "%s ml" % (totes,)

    else:
        _inventory_db[(mfg, liquor)] = amount

def check_inventory(mfg, liquor):
    for key in _inventory_db:
        if key == (mfg, liquor):
            return True
        
    return False

def convert_to_ml(amount):
    """This function returns the amount of a liquor in
    milliliters.
    """

    num, units = amount.split()
    num = float(num)
    units = units.lower()
   
    total = 0.0
    if units == 'ml':
        total += num
    elif units == 'oz':
        total += 29.5735 * num
    elif units == 'gallon':
        total += 3785.41 * num
    elif units == 'liter':
        total += 1000 * num
    else:
        raise Exception("unknown unit %s" % units)

    return total

def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    amounts = []
    for key in _inventory_db:
        if key == (mfg, liquor):
            amounts.append(_inventory_db[key])

    total = 0.0
    for amount in amounts:
         amount = convert_to_ml(amount)
         total += amount

    return float(total)

def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for key in _inventory_db:
        yield key

def add_recipe(r):
    "Add a recipe to the dictionary of recipes"
    err = "Recipe %s already in database " % (r.name,)
    
    if (r.name in _recipes_db):
        raise DuplicateRecipeName()
    else:
        _recipes_db[r.name]=r

def get_recipe(name):
    "Get a recipe name"
    for x in _recipes_db:
        if(x == name):
            return _recipes_db[x]
    return False

def get_all_recipes():
    "Retrieve all recipes"
    recipes = set()
    for x in _recipes_db:
        recipes.add(_recipes_db[x])
    return recipes

def check_for_type(typ):
    "Check for liquor types"
    liquor_types = set()
    for (m, l, t) in _bottle_types_db:
        if t == typ:
            liquor_types.add((m,l))
    return liquor_types




