# -*- coding: utf-8 -*-
import xml.dom.minidom

def lsMap(xmlFile):
    
    myMap = xml.dom.minidom.parse(xmlFile)
    
    for e in myMap.childNodes:
        if e.nodeType == e.ELEMENT_NODE:
            mapName = e.getAttribute("name")
            mapEnv = e.getAttribute("envset")
            mapSize = e.getAttribute("size")
            #printout basic map infos
            print "loaded map ", xmlFile
            print "Name:", mapName
            print "Environment:", mapEnv
            print "Size:", mapSize
            
            #treating envinronment and customized
            for e in e.childNodes:
                if e.nodeType == e.ELEMENT_NODE:
                    #treating rows
                    for e in e.childNodes:
                        if e.nodeType == e.ELEMENT_NODE:
                            #trating squares
                            for e in e.childNodes:
                                if e.nodeType == e.ELEMENT_NODE:
                                    for e in e.childNodes:
                                        if e.nodeType == e.ELEMENT_NODE:
                                            print "building square with", e.getAttribute("type")
                            
    
    
lsMap("experimental.swm")