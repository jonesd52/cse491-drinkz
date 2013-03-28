#! /usr/bin/env python
"""
Using the cse491-linkz example to create html files
"""

import os
from drinkz import db
from drinkz import recipes

try:
    os.mkdir('html')
except OSError:
    # already exists
    pass

###

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

db._reset_db()

def Index():
    return """<p><a href='inventory'>Inventory</a></p><p><a href='recipes'>Recipes</a></p><p><a href='liquor_types'>Liquor Types</a></p><p><a href='input_amount'>Convert an Amount</a></p>"""


###

def Recipes():

    
    fp =  """<table border="1"><tr><th>Cocktail</th><th>Can We Make It?</th></tr>"""

    for r in db.get_all_recipes():
        a = r.need_ingredients()
        if( a != [] ):
            fp += "<tr><td>%s</td><td align=center>&#x2717;</td></tr>" % (r.name,)
        else:
            fp += "<tr><td>%s</td><td align=center>&#x2713;</td></tr>" % (r.name,)

    fp += "</table>" 

    fp += """<p><a href='/'>Index</a></p><p><a href='inventory'>Inventory</a></p><p><a href='liquor_types'>Liquor Types</a></p>"""

    return fp

###

def Inventory():

    fp =  """<table border="1"><tr><th>Liquor</th><th>Amount (in mL)</th></tr>"""

    for mfg, liquor in db.get_liquor_inventory():
        x = db.get_liquor_amount( mfg, liquor)
        fp +=  "<tr><td>%s</td><td align=center>%s</td></tr>" % (mfg, x)


    fp += "</table>" 

    fp += "<p><a href='/'>Index</a></p><p><a href='recipes'>Recipes</a></p><p><a href='liquor_types'>Liquor Types</a></p>"

    return fp


###

def Liquor_Types():

    fp = """<table border="1"><tr><th>Maker</th><th>Liqour</th><th>Type</th><th>Is It Delicious?</th></tr>"""

    for (m, l, t) in db._bottle_types_db:
        if(t == "blended scotch"):
            fp += "<tr><td>%s</td><td>%s</td><td>%s</td><td align=center>Indeed!</td></tr>" % (m, l, t)
        else:
            fp += "<tr><td>%s</td><td>%s</td><td>%s</td><td align=center>NOPE!</td></tr>" % (m, l, t)


    fp += "</table>" 

    fp += "<p><a href='/'>Index</a></p><p><a href='inventory'>Inventory</a></p><p><a href='recipes'>Recipes</a></p>"

    return fp

# a checkmark   &#x2713;
# an x mark   &#x2717;









