from django.utils import simplejson as json
from google.appengine.api import urlfetch


class MyFlickr(object):
    """A simple class for dealing with flickr via the API"""
    def __init__(self, api_key):
        super(MyFlickr, self).__init__()
        self.api_key = api_key
        self.api_host = "http://api.flickr.com/services/rest/"
    
    def default_args(self, method):
        return {
                    "method": method,
                    "api_key": self.api_key,
                    "format": "json",
                    "nojsoncallback": 1,
                }
    
    def dict_to_query_string(self, the_dict):
        qs = ""
        for key in the_dict:
            qs += "%s=%s&" % (key, str(the_dict[key]))
        return qs
        
    def url_for_method(self, method, **kwargs):
        qs = ""
        url_args = self.default_args(method)
        url_args.update(kwargs)
        return self.api_host + "?" + self.dict_to_query_string(url_args)
    
    def call(self, method, **kwargs):
        result = urlfetch.fetch(self.url_for_method(method, **kwargs))
        return json.loads(result.content)
    
    def get_photos(self, resp):
        if resp["stat"] == "fail":
            return "Error: " + resp["message"]
        else:
            return resp["photos"]["photo"]
    
    def interesting(self, **kwargs):
        photos = self.call("flickr.interestingness.getList", **kwargs)
        return self.get_photos(photos)
    
