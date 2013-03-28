"""
Functionality for a Recipe class
"""

import db

class Recipe:
    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = []
        self.ingredients = ingredients
        
    def need_ingredients(self):
        missing = []
        for (typ,need) in self.ingredients:
	    database_liquors = db.check_for_type(typ)
	    amt = db.convert_to_ml(need)
	    liq_max = 0.0
	    for (m,l) in database_liquors:
	        liq_amt = db.get_liquor_amount(m,l)
	        if(liq_amt > liq_max):
	            liq_max = liq_amt
	    if(liq_max < amt):
	        necesito = amt - liq_max
	        missing.append((typ,necesito))
	return missing
    
