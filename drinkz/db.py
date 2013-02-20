"""
Database functionality for drinkz information.
"""

# private singleton variables at module level
_bottle_types_db = set()
_inventory_db = dict()
_recipes_db = dict()

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db
    _bottle_types_db = set()
    _inventory_db = dict()

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
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
        new_amt = _add_liquors_amount(amount, _inventory_db[(mfg,liquor)])
        _inventory_db[(mfg,liquor)] = new_amt

    else:
        _inventory_db[(mfg, liquor)] = amount

def check_inventory(mfg, liquor):
    for key in _inventory_db:
        if key == (mfg, liquor):
            return True
        
    return False

def convert_to_ml(amount):
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

def _add_liquors_amount(amount_1, amount_2):
    # Adds the amounts of the same liquor together
    total = 0.0
    amount = []
    amount.append(amount_1)
    amount.append(amount_2)
    
    for amt in amount:
        num, units = amt.split()
        num = float(num)
        units = units.lower()

        if units == 'ml':
	    total += num
	elif units == 'oz':
	    total += 29.5735 * num
	else:
	    raise Exception("unknown unit %s" %units)

    return "%s ml" % (total,)
    
    
def add_recipe(r):
    "Add a recipe to the dictionary of recipes"
    
    
    pass
