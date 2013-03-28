#Builds a database to test on

import os
import db
from . import recipes

def Build_Database():

    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')

    db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
    db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')
        
    db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
    db.add_to_inventory('Gray Goose', 'vodka', '1 liter')

    db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
    db.add_to_inventory('Rossi', 'extra dry vermouth', '24 oz')

    r = recipes.Recipe('scotch on the rocks', [('blended scotch','4 oz')])
    s = recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'),('vermouth', '1.5 oz')])
    t = recipes.Recipe('vomit inducing martini', [('orange juice','6 oz'),('vermouth','1.5 oz')])

    db.add_recipe(r)
    db.add_recipe(s)
    db.add_recipe(t)
    
    print r