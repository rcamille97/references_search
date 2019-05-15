#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 19:06:12 2019

@author: camillemac
"""

class Publication:
    
    """
    TODO:: Faire une fonction qui permet d'ajouter une publication à une recherche sans qu'elle soit en double
    """
    
    
    def __init__(self, _title= None, _authors = None, _publication_type = None, 
                 _publication_info = None, _year = None, _keywords = None, _pdf_access = None,
                 _doi = None, _source = None, _abstract = None):
        
        self._title = _title
        self._authors = _authors
        self._publication_type = _publication_type
        if type(_publication_info) == dict or type(_publication_info) == None:
            self._publication_info = _publication_info
        self._year = _year
        self._keywords = _keywords
        self._pdf_access = _pdf_access
        self._doi = _doi
        self._source = _source
        self._abstract = _abstract
        self._mySearch = []
        
    @property
    def title(self):
        return self._title
    
    @title.setter 
    def title(self,title):
        self._title = title
    
    @property
    def authors(self):
        return self._authors
    
    @authors.setter 
    def authors(self,authors):
        self._authors = authors
    
    @property
    def publication_type(self):
        return self._publication_type
    
    @publication_type.setter 
    def publication_type(self,publication_type):
        self._publication_type = publication_type
        
    @property
    def publication_info(self):
        return self._publication_info
    
    @publication_info.setter 
    def publication_info(self,publication_info):
        self._publication_info = publication_info
    
    @property
    def year(self):
        return self._year
    
    @year.setter 
    def year(self,year):
        self._year = year
    
    @property
    def keywords(self):
        return self._keywords
    
    @keywords.setter 
    def keywords(self,keywords):
        self._keywords = keywords
        
    @property
    def pdf_access(self):
        return self._pdf_access
    
    @pdf_access.setter 
    def pdf_access(self,pdf_access):
        self._pdf_access = pdf_access
    
    @property
    def doi(self):
        return self._doi
    
    @doi.setter 
    def doi(self,doi):
        self._doi = doi
        
    @property
    def source(self):
        return self._source
    
    @source.setter 
    def source(self,source):
        self._source = source
        
    @property
    def abstract(self):
        return self._abstract
    
    @abstract.setter 
    def abstract(self,abstract):
        self._abstract = abstract

    @property
    def mySearch(self):
        return self._mySearch
    
    @mySearch.setter 
    def mySearch(self,mySearch):
        self._mySearch = mySearch
    
    def displayData(self):
        print("\nTitre : {}".format(str(self.title)))
        print("Auteurs : ")
        if self.authors != None or self.authors:
            for a in self.authors:
                a.displayData()
        print("Type of publication : {} ".format(self.publication_type))
        print("info: {}".format(self.publication_info))
        print("Year: {} ".format(self.year))
        print("Keywords: {} ".format(self.keywords))
        print("pdf: {} ".format(self.pdf_access))
        print("doi: {} ".format(self.doi))
        print("source: {} ".format(self.source))
        print("Abstract: {} \n".format(self.abstract))
    
                
        
        
    
class Author:
    
    def __init__(self, _name = None , _location = None):
        self._name = _name
        self._location = _location 
    
    @property
    def name(self):
        return self._name
    
    @name.setter 
    def title(self,name):
        self._name = name
    
    @property
    def location(self):
        return self._location
    
    @location.setter 
    def location(self,location):
        self._location = location
    
    def displayData(self):
        print("    Name: {}\n    Location: {}\n".format(self.name, self.location))
        
        
        
    