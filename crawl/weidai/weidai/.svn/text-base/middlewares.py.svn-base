# -*- coding: utf-8 -*-

#import random

#class ProxyMiddleware(object):
 #   def process_request(self, request, spider):
  #      proxy_ip = "http://183.207.228.122:80"
   #     request.meta['proxy'] = proxy_ip
    #    print proxy_ip



# Importing base64 library because we'll need it ONLY in case if the proxy we are going to use requires authentication
import base64, random
# Start your middleware class
class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        request.meta['proxy'] = "http://59.78.160.244:8080"
        #print proxy_ip
        # Use the following lines if your proxy requires authentication
        #proxy_user_pass = "USERNAME:PASSWORD"
        # setup basic authentication for the proxy
       # encoded_user_pass = base64.encodestring(proxy_user_pass)
        #request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass