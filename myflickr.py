from django.utils import simplejson as json
from google.appengine.api import urlfetch
import md5


class MyFlickr(object):
    """A simple class for dealing with flickr via the API"""
    def __init__(self, api_key, secret=""):
        super(MyFlickr, self).__init__()
        self.api_key = api_key
        self.secret = secret
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
    
    def signature(self, the_dict):
        string = ""
        for key in sorted(the_dict):
            string += key + str(the_dict[key])
        return md5.new(string).hexdigest()
    
    def login_link(self, perms="read"):
        dict = {
            "api_key": self.api_key,
            "perms": perms
        }
        signature = self.signature(dict)
        dict.update({"api_sig": signature})
        return "http://flickr.com/services/auth/?" + self.dict_to_query_string(dict)
