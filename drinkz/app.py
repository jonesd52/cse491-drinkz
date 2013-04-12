#! /usr/bin/env python

from wsgiref.simple_server import make_server
import dynamic_html

import urlparse
import simplejson

import sys

import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from drinkz import db

dispatch = {
    '/' : 'index',
    '/error' : 'error',
    '/recipes' : 'recipes',
    '/inventory' : 'inventory',
    '/liquor_types' : 'liquor_type',
    '/input_amount' : 'input_amount',
    '/output_ml' : 'ml_output',
    '/add_liquor_type' : 'add_liquortype',
    '/added_liquor': 'addedliquor',
    '/add_inventory' : 'add_to_inventory',
    '/added_inventory' : 'addedinventory',
}

html_headers = [('Content-type', 'text/html')]

#sample_db = os.path.dirname(__file__) + '/../SAMPLE-DATABASE-FOR-3C'
#db.load_db(sample_db)

def load_test_file():
    print "Loaded DB"
    sample_db = os.path.dirname(__file__) + '/../SAMPLE-DATABASE-FOR-3C'
    db.load_db(sample_db)

load_test_file()

class SimpleApp(object):
    def __call__(self, environ, start_response):

        path = environ['PATH_INFO']
        fn_name = dispatch.get(path, 'error')

        # retrieve 'self.fn_name' where 'fn_name' is the
        # value in the 'dispatch' dictionary corresponding to
        # the 'path'.
        fn = getattr(self, fn_name, None)

        if fn is None:
            start_response("404 Not Found", html_headers)
            return ["No path %s found" % path]

        return fn(environ, start_response)
            
    def index(self, environ, start_response):
      
        data = """<p><a href='inventory'>Inventory</a></p>
<p><a href='recipes'>Recipes</a></p>
<p><a href='liquor_types'>Liquor Types</a></p>
<p><a href='input_amount'>Convert an Amount</a></p>
<p><a href='add_liquor_type'>Add A Liquor Type</a></p>
<p><a href='add_inventory'>Add To Inventory</a></p>
"""
        start_response('200 OK', list(html_headers))
        return [data]
        
    def error(self, environ, start_response):
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]
        
    def recipes(self, environ, start_response):
        content_type = 'text/html'
    
        fp =  """<table border="1"><tr><th>Cocktail</th><th>Can We Make It?</th></tr>"""

        for r in db.get_all_recipes():
            a = r.need_ingredients()
            if( a != [] ):
                fp += "<tr><td>%s</td><td align=center>&#x2717;</td></tr>" % (r.name,)
            else:
                fp += "<tr><td>%s</td><td align=center>&#x2713;</td></tr>" % (r.name,)

        fp += "</table>" 

        fp += """<p><a href='/'>Index</a></p><p><a href='inventory'>Inventory</a></p><p><a href='liquor_types'>Liquor Types</a></p>"""

        data = fp
        
        start_response('200 OK', list(html_headers))
        return [data]

    def inventory(self, environ, start_response):
        content_type = 'text/html'
        
        fp =  """<table border="1"><tr><th>Liquor</th><th>Amount (in mL)</th></tr>"""
    
        for mfg, liquor in db.get_liquor_inventory():
            x = db.get_liquor_amount( mfg, liquor)
            fp +=  "<tr><td>%s</td><td align=center>%s</td></tr>" % (mfg, x)


        fp += "</table>" 

        fp += "<p><a href='/'>Index</a></p><p><a href='recipes'>Recipes</a></p><p><a href='liquor_types'>Liquor Types</a></p>"

        data = fp 
        
        start_response('200 OK', list(html_headers))
        return [data]
        
    def liquor_type(self, environ, start_response):
        content_type = 'text/html'
        
        fp = """<table border="1"><tr><th>Maker</th><th>Liqour</th><th>Type</th><th>Is It Delicious?</th></tr>"""

        for (m, l, t) in db._bottle_types_db:
            if(t == "blended scotch"):
                fp += "<tr><td>%s</td><td>%s</td><td>%s</td><td align=center>Indeed!</td></tr>" % (m, l, t)
            else:
                fp += "<tr><td>%s</td><td>%s</td><td>%s</td><td align=center>NOPE!</td></tr>" % (m, l, t)


        fp += "</table>" 

        fp += "<p><a href='/'>Index</a></p><p><a href='inventory'>Inventory</a></p><p><a href='recipes'>Recipes</a></p>"

        data = fp
        
        start_response('200 OK', list(html_headers))
        return [data]
        
    def input_amount(self, environ, start_response):
        data = form()
        start_response('200 OK', list(html_headers))
        return [data]

    def add_liquortype(self, environ, start_response):
        data = add_liquor_form()
        start_response('200 OK', list(html_headers))
        return [data]

    def add_to_inventory(self, environ, start_response):
        data = add_to_inventory_form()
        start_response('200 OK', list(html_headers))
        return [data]
    
    def addedliquor(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        mfg = results['manu'][0]
        liq = results['liquor'][0]
        ltype = results['typ'][0]

        db.add_bottle_type(mfg,liq,ltype)
        
        print db._bottle_types_db

        data = "Added liquor type to database"
        data += "<p><a href = '/'>Index</a></p>"

        start_response('200 OK', list(html_headers))
        return [data]

    def addedinventory(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        mfg = results['manu'][0]
        liq = results['liquor'][0]
        amt = results['amount'][0]
        
        print amt
    
        try:
	    db.add_to_inventory(mfg, liq, amt)
	    data = "Added bottle to the inventory"
	except db.LiquorMissing:
	    data = "Could not add bottle to inventory, liquor type muse be added first"

        data += "<p><a href='/'>Index</a></p>"
        
        start_response('200 OK', list(html_headers))
        return [data]
 
    def ml_output(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        number = results['number'][0]
        unit = results['unit'][0]
        
        show = conversion(number, unit)
        data = "Converted Amount: %s ml" % show
        data += "<p><a href='/'>Index</a></p>"
      
        start_response('200 OK', list(html_headers))
        return [data]

    
def form():
    return """
<form action='output_ml'>
Amount to convert: <input type='text' name='number' size'20'> <select name="unit">
<option value="ml">Milliliters</option>
<option value="liter">Liters</option>
<option value="oz">Ounces</option>
<option value="gallon">Gallons</option>
</select>
<input type='submit'>
</form>
<p><a href='/'>Index</a></p>
"""

def add_liquor_form():
    return """
<form action='added_liquor'>
Manufacturer: <input type='text' name='manu'>
Liquor: <input type='text' name='liquor'>
Type: <input type='text' name='typ'>
<input type='submit'>
</form>
<p><a href='/'>Index</a></p>

"""

def add_to_inventory_form():
    return """
<form action='added_inventory'>
Manufacturer: <input type='text' name='manu'>
Liquor: <input type='text' name='liquor'>
Amount: <input type='text' name='amount'>
<input type='submit'>
</form>
<p><a href='/'>Index</a></p>
"""


def conversion(number, unit):
    amount = '%s %s' % (number,unit)
    amount = db.convert_to_ml(amount)
    return amount
    

if __name__ == '__main__':
    import random, socket
    port = random.randint(8000, 9999)
    
    app = SimpleApp()
    
    httpd = make_server('', port, app)
    print "Serving on port %d..." % port
    print "Try using a Web browser to go to http://%s:%d/" % \
          (socket.getfqdn(), port)
    httpd.serve_forever()
    
def __init__():
    pass

