#!/usr/bin/python

import sys
sys.path.append("google_appengine")
sys.path.append("google_appengine/lib/django")
sys.path.append("google_appengine/lib/webob")
sys.path.append("google_appengine/lib/yaml/lib")

import unittest
import re
from myflickr import MyFlickr


class TestMyFlickr(unittest.TestCase):
    def setUp(self):
        self.flickr = MyFlickr("abc")
        
    def test_url_for_method_should_have_method(self):
        url = self.flickr.url_for_method("bob")
        assert re.search("method=bob", url)
    
    def test_url_for_method_should_have_api_key(self):
        url = self.flickr.url_for_method("test")
        assert re.search("api_key=abc", url)

    def test_dict_to_query_string(self):
        dict = {"a":1, "b":"water"}
        assert "a=1&b=water&" == self.flickr.dict_to_query_string(dict)
    
    def test_generic_query_with_call(self):
        url = self.flickr.url_for_method("erik", page=1, per_page=50)
        assert re.search("method=erik", url)
        assert re.search("page=1", url)
        assert re.search("per_page=50", url)
        
        
if __name__ == "__main__":
    unittest.main()