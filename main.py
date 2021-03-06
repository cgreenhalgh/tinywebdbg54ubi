#!/usr/bin/env python
###
### This is a web service for use with App
### Inventor for Android (<http://appinventor.googlelabs.com>)
### This particular service stores and retrieves tag-value pairs 
### using the protocol necessary to communicate with the TinyWebDB
### component of an App Inventor app.
### 

### Author: David Wolber (wolber@usfca.edu), using sample of Hal Abelson

### Modified by Chris Greenhalgh

import webapp2
import logging
from cgi import escape
from google.appengine.ext import ndb as db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.db import Key
import json

class StoredData(db.Model):
  user = db.StringProperty()
  tag = db.StringProperty()
  value = db.StringProperty(multiline=True)
  ## defining value as a string property limits individual values to 500
  ## characters.   To remove this limit, define value to be a text
  ## property instead, by commnenting out the previous line
  ## and replacing it by this one:
  ## value db.TextProperty()
  date = db.DateTimeProperty(required=True, auto_now=True)


MainMessage = '''
<p>Please use a URL with an additional path element (user id) to access this 
variant of the TinyWebDB service, for example
<a href="test/">test/</a></p>
<p>There is also a simple Javascript client example: <a href="jsclient/index.html">jsclient/index.html</a></p>
'''


class MainPage(webapp2.RequestHandler):

  def get(self):
    write_page_header(self, None);
    self.response.out.write(MainMessage)
#    write_available_operations(self)
#    show_stored_data(self)
    self.response.out.write('</body></html>')

IntroMessage = '''
<table border=0>
<tr valign="top">
<td><image src="/images/customLogo.gif" width="200" hspace="10"></td>
<td>
<p>
This web service is designed to work with <a
href="http://appinventor.googlelabs.com">App Inventor
for Android</a> and the TinyWebDB component. The end-goal of this service is
to communicate with a mobile app created with App Inventor.
</p>
The page your are looking at is 
a web page interface to the web service to help programmers with debugging. You
can invoke the get and store operations by hand, view the existing entries, and also delete individual entries.</p>

</td> </tr> </table>'''


class List(webapp2.RequestHandler):

  def get(self, user):
    write_page_header(self, user);
    self.response.out.write(IntroMessage)
    write_available_operations(self, user)
    show_stored_data(self, user)
    self.response.out.write('</body></html>')

########################################
### Implementing the operations
### Each operation is design to respond to the JSON request
### or to the Web form, depending on whether the fmt input to the post
### is json or html.

### Each operation is a class.  The class includes the method that
### actually, manipualtes the DB, followed by the methods that respond
### to post and to get.


class StoreAValue(webapp2.RequestHandler):

  def store_a_value(self, tag, value, user):
    # There's a potential readers/writers error here :(
    entry = db.GqlQuery("SELECT * FROM StoredData where tag = :1 AND user = :2", tag, user).get()
    if entry:
      entry.value = value
    else: entry = StoredData(tag = tag, value = value, user = user)
    entry.put()
    ## Send back a confirmation message.  The TinyWebDB component ignores
    ## the message (other than to note that it was received), but other
    ## components might use this.
    result = ["STORED", tag, value]
    WritePhoneOrWeb(self, lambda : json.dump(result, self.response.out), user)

  def post(self, user):
    tag = self.request.get('tag')
    value = self.request.get('value')
    self.store_a_value(tag, value, user)

  def get(self, user):
    self.response.out.write('''
    <html><body>
    <form action="/%s/storeavalue" method="post"
          enctype=application/x-www-form-urlencoded>
       <p>Tag<input type="text" name="tag" /></p>
       <p>Value<input type="text" name="value" /></p>
       <input type="hidden" name="fmt" value="html">
       <input type="submit" value="Store a value">
    </form></body></html>\n''' % (user))

class GetValue(webapp2.RequestHandler):

  def get_value(self, tag, user):
    entry = db.GqlQuery("SELECT * FROM StoredData where tag = :1 AND user = :2", tag, user).get()
    if entry:
      value = entry.value
    else: value = ""
    ## We tag the returned result with "VALUE".  The TinyWebDB
    ## component makes no use of this, but other programs might.
    ## check if it is a html request and if so clean the tag and value variables
    if self.request.get('fmt') == "html":
      value = escape(value)
      tag = escape(tag)
    WritePhoneOrWeb(self, lambda : json.dump(["VALUE", tag, value], self.response.out), user)

  def post(self, user):
    tag = self.request.get('tag')
    self.get_value(tag, user)

  def get(self, user):
    self.response.out.write('''
    <html><body>
    <form action="/%s/getvalue" method="post"
          enctype=application/x-www-form-urlencoded>
       <p>Tag<input type="text" name="tag" /></p>
       <input type="hidden" name="fmt" value="html">
       <input type="submit" value="Get value">
    </form></body></html>\n''' % (user))


### The DeleteEntry is called from the Web only, by pressing one of the
### buttons on the main page.  So there's no get method, only a post.

class DeleteEntry(webapp2.RequestHandler):

  def post(self, user):
    logging.debug('/deleteentry?%s\n|%s|' %
                  (self.request.query_string, self.request.body))
    entry_key_string = self.request.get('entry_key_string')
    key = db.Key(entry_key_string)
    tag = self.request.get('tag')
    db.run_in_transaction(dbSafeDelete,key)
    self.redirect('/%s/' % (user))


########################################
#### Procedures used in displaying the main page

### Show the API
def write_available_operations(self, user):
  self.response.out.write('''
    <p>Available calls:\n
    <ul>
    <li><a href="/%s/storeavalue">/storeavalue</a>: Stores a value, given a tag and a value</li>
    <li><a href="/%s/getvalue">/getvalue</a>: Retrieves the value stored under a given tag.  Returns the empty string if no value is stored</li>
    <li><form action="/%s/clean" method="post"
            enctype=application/x-www-form-urlencoded>
            <input type="hidden" name="fmt" value="html">
            <input type="submit" style="background-color: red" value="Delete All"></form></li>\n
    </ul>''' % (user, user, user))

### Generate the page header
def write_page_header(self, user):
  self.response.headers['Content-Type'] = 'text/html'
  self.response.out.write('''
     <html>
     <head>
     <style type="text/css">
        body {margin-left: 5% ; margin-right: 5%; margin-top: 0.5in;
             font-family: verdana, arial,"trebuchet ms", helvetica, sans-serif;}
        ul {list-style: disc;}
     </style>
     <title>Tiny WebDB</title>
     </head>
     <body>''')
  self.response.out.write('<h2>App Inventor for Android: Custom Tiny WebDB Service</h2>')
  if user != None:
    self.response.out.write('<p>User &quot;%s&quot;</p>' % (user))

### Show the tags and values as a table.
def show_stored_data(self, user):
  self.response.out.write('''
    <p><table border=1>
      <tr>
         <th>Key</th>
         <th>Value</th>
         <th>Created (GMT)</th>
      </tr>''')
  # This next line is replaced by the one under it, in order to help
  # protect against SQL injection attacks.  Does it help enough?
  #entries = db.GqlQuery("SELECT * FROM StoredData ORDER BY tag")
  entries = db.GqlQuery("SELECT * FROM StoredData where user = :1 ORDER BY tag", user)
  for e in entries:
    entry_key_string = str(e.key())
    self.response.out.write('<tr>')
    self.response.out.write('<td>%s</td>' % escape(e.tag))
    self.response.out.write('<td>%s</td>' % escape(e.value))      
    self.response.out.write('<td><font size="-1">%s</font></td>\n' % e.date.ctime())
    self.response.out.write('''
      <td><form action="/%s/deleteentry" method="post"
            enctype=application/x-www-form-urlencoded>
	    <input type="hidden" name="entry_key_string" value="%s">
	    <input type="hidden" name="tag" value="%s">
            <input type="hidden" name="fmt" value="html">
	    <input type="submit" style="background-color: red" value="Delete"></form></td>\n''' %
                            (user, entry_key_string, escape(e.tag)))
    self.response.out.write('</tr>')
  self.response.out.write('</table>')





#### Utilty procedures for generating the output

#### Write response to the phone or to the Web depending on fmt
#### Handler is an appengine request handler.  writer is a thunk
#### (i.e. a procedure of no arguments) that does the write when invoked.
def WritePhoneOrWeb(handler, writer, user):
  if handler.request.get('fmt') == "html":
    WritePhoneOrWebToWeb(handler, writer, user)
  elif handler.request.get('jsonp') == '':
    handler.response.headers['Content-Type'] = 'application/jsonrequest'
    writer()
  else:
    handler.response.headers['Content-Type'] = 'text/javascript'
    handler.response.out.write(handler.request.get('jsonp'))
    handler.response.out.write('(')
    writer()
    handler.response.out.write(')')
    

#### Result when writing to the Web
def WritePhoneOrWebToWeb(handler, writer, user):
  handler.response.headers['Content-Type'] = 'text/html'
  handler.response.out.write('<html><body>')
  handler.response.out.write('''
  <em>The server will send this to the component:</em>
  <p />''')
  writer()
  WriteWebFooter(handler, writer, user)


#### Write to the Web (without checking fmt)
def WriteToWeb(handler, writer, user):
  handler.response.headers['Content-Type'] = 'text/html'
  handler.response.out.write('<html><body>')
  writer()
  WriteWebFooter(handler, writer, user)

def WriteWebFooter(handler, writer, user):
  handler.response.out.write('''
  <p><a href="/%s/">
  <i>Return to Game Server Main Page</i>
  </a>''' % (user))
  handler.response.out.write('</body></html>')

### A utility that guards against attempts to delete a non-existent object
def dbSafeDelete(key):
  if db.get(key) :  db.delete(key)

class CleanUser(webapp2.RequestHandler):

  def post(self, user):
    if user == None:  
        keys = db.GqlQuery("SELECT __key__ FROM StoredData", user)
    else:
        keys = db.GqlQuery("SELECT __key__ FROM StoredData where user = :1", user)
    for key in keys:
        db.run_in_transaction(dbSafeDelete,key)
    self.redirect('/%s/' % (user))


### Assign the classes to the URL's

application =     \
   webapp2.WSGIApplication([('/', MainPage),
                           (r'/([^/]+)/', List),
                           (r'/([^/]+)/storeavalue', StoreAValue),
                           (r'/([^/]+)/deleteentry', DeleteEntry),
                           (r'/([^/]+)/getvalue', GetValue),
                           (r'/([^/]+)/clean', CleanUser)
                           ],
                          debug=True)

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()

### Copyright 2009 Google Inc.
###
### Licensed under the Apache License, Version 2.0 (the "License");
### you may not use this file except in compliance with the License.
### You may obtain a copy of the License at
###
###     http://www.apache.org/licenses/LICENSE-2.0
###
### Unless required by applicable law or agreed to in writing, software
### distributed under the License is distributed on an "AS IS" BASIS,
### WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
### See the License for the specific language governing permissions and
### limitations under the License.
###
