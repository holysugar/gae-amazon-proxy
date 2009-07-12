# vim: set fileencoding=utf-8


from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch

import re
import time
import urllib
import ConfigParser

import paapi as am

# hashlib.sha256(message).hexdigest()

def config():
    c = ConfigParser.ConfigParser()
    c.read('amazon-proxy.ini')
    c.access_key = lambda: c.get('amazon-proxy', 'access_key')
    c.secret_key = lambda: c.get('amazon-proxy', 'secret_key')
    c.entry_point = lambda: c.get('amazon-proxy', 'entry_point')
    c.default_aid = lambda: c.get('amazon-proxy', 'default_aid')
    return c

class MainPage(webapp.RequestHandler):
    def get(self):
        params = self.request.GET
        newparams = []

        conf = config()

        for (key, value) in params.iteritems():
            if key in ("AWSAccessKeyId","SubscriptionId"):
                newparams.append((key, conf.access_key()))
            elif key in ('Timestamp', 'Signature'):
                # ignore this key
                pass
            else:
                newparams.append((key, value))
        
        if not params.has_key('AssociateTag'):
            newparams.append(('AssociateTag', conf.default_aid()))

        newparams.append(('Timestamp',
            time.strftime('%Y-%m-%dT%XZ', time.gmtime())))

        url = am.encode(newparams, conf.secret_key())
        
        self.response.headers['Content-Type'] = 'text/xml; charset=utf-8'

        result = urlfetch.fetch(url)

        if result.status_code == 200:
            self.response.out.write(result.content)
        else:
            self.response.set_status(result.status_code)
            self.response.out.write(result.content)

application = webapp.WSGIApplication(
                                     [('/.*', MainPage)],
                                     debug=False)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()

