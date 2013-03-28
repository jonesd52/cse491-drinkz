#! /usr/bin/env python

from wsgiref.simple_server import make_server
import dynamic_html

import urlparse
import db
import simplejson

import os.path

sample_db = os.path.dirname(__file__) + '/../SAMPLE-DATABASE-FOR-3C'

dispatch = {
    '/' : 'index',
    '/error' : 'error',
    '/recipes' : 'recipes',
    '/inventory' : 'inventory',
    '/liquor_types' : 'liquor_type',
    '/input_amount' : 'input_amount',
    '/output_ml' : 'ml_output',
    
}

html_headers = [('Content-type', 'text/html')]

db.load_db(sample_db)

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
        data = dynamic_html.Index()
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
        data = dynamic_html.Recipes()
        
        start_response('200 OK', list(html_headers))
        return [data]

    def inventory(self, environ, start_response):
        content_type = 'text/html'
        data = dynamic_html.Inventory()
        
        start_response('200 OK', list(html_headers))
        return [data]
        
    def liquor_type(self, environ, start_response):
        content_type = 'text/html'
        data = dynamic_html.Liquor_Types()
        
        start_response('200 OK', list(html_headers))
        return [data]
        
    def input_amount(self, environ, start_response):
        data = form()
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

