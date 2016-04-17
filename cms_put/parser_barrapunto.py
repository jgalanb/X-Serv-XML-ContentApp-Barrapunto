#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Simple XML parser for the RSS channel from BarraPunto
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Just prints the news (and urls) in BarraPunto.com,
#  after reading the corresponding RSS channel.

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""
        self.respuesta = "<h2><font color='green'>Titulares de " +\
                            "Barrapunto.com</font></h2>"

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement (self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                line = "Title: " + self.theContent + "."
                # To avoid Unicode trouble
                self.respuesta += line + "<br/>"
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                self.respuesta +=  " Link: <a href='" + self.theContent + "'>" + \
                            self.theContent + "</a>" + "." + "<br>" + "<hr/>" + \
                            "<br/>"
                self.inContent = False
                self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

# --- Main prog

def obtener_titulares():

    # Load parser and driver

    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)

    # Ready, set, go!

    xmlURL = "http://barrapunto.com/index.rss"
    theParser.parse(xmlURL)
    return theHandler.respuesta
