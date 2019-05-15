#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 19:10:51 2019

@author: camillemac
"""

#import time
from random import choice
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
from http import cookiejar
from modules.Publication import Publication, Author
#import json

"""
TODO:: pour comparer les titrers: les mettre en majuscule et retirer les espaces"
"""
class Search:
    
    #Putting a max research rate, as too much requests involves being banned
    #TODO:: implement max research rate verification
    MAXRESULTS=100
    
    listOfResults = []
    
    desktop_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']

    def __init__(self, _keyword, _numberOfResults, _results = []):
        self._keyword = _keyword
        self._numberOfResults = _numberOfResults
        self._results = _results
        
    @property
    def keyword(self):
        return self._keyword
    
    @keyword.setter 
    def keyword(self,keyword):
        self._keyword = keyword
    
    @property
    def numberOfResults(self):
        return self._numberOfResults
    
    @numberOfResults.setter 
    def numberOfResults(self,numberOfResults):
        self._numberOfResults = numberOfResults
    
    @property
    def results(self):
        return self._results
    
    @results.setter 
    def results(self,results):
        self._results = results
 
    #Prevents the same User-Agent to do all the requests
    def get_random_headers(self):
        return {'User-Agent': choice(self.desktop_agents),'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
    
    def getListOfResults(self):
        if not self.results:
            raise ValueError("La liste des résultats est vide")
        else:
            return self.results
    
    #TODO:: add verification to duplication
    def addResult(self, publication):
        if not publication.mySearch:
            self.results.append(publication)
            publication.mySearch.append(self)
        else:
            print("already existant")
    

#Blocks all cookies for a given request.
class BlockAll(cookiejar.CookiePolicy):
        return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
        netscape = True
        rfc2965 = hide_cookie2 = False
   

     
#DIFFERENT CLASSES FOR EVERY WEBSITE TO SEARCH
#CLASS NEED TO BE ADDED IF OTHER WEBSITES ADDED
class Microsoft(Search): 
    def search(self):
        
        keywords = self.keyword
        numberOfResults = self.numberOfResults
        
        #TODO:: CONVERT DATE TO YEAR

        url = 'https://academic.microsoft.com/api/search'
        data = {"query": keywords,
                "queryExpression": "",
                "filters": [],
                "orderBy": None,
                "skip": 0,
                "sortAscending": True,
                "take": numberOfResults}
        
        r = requests.post(url=url, json=data, headers = self.get_random_headers())

        
        #print(json.dumps(r.json()))
        for result in r.json()['paperResults']:
            
            p = None
            r = result['paperResult']
            
            
            p = Publication()
            
            p.source = "Microsoft"
            
            p.title = r["displayName"]
            
            #authors
            authors = []
            for i in r['authors']:
                if 'displayName' in i["institutions"][0]:
                    institution = i["institutions"][0]['displayName']
                    author = Author(i["displayName"], institution)
                else:
                    author = Author(i["displayName"])
                authors.append(author)
            p.authors = authors
            
            #description 
            p.abstract = r["description"]
            
            #keywords
            tabKeywords = []
            for k in r["fieldsOfStudy"]:
                tabKeywords.append(k["displayName"])               
            p.keywords = tabKeywords

            
            #source PDF
            p.pdf_access = r["sources"][0]['link']
            
            if int(r["publicationType"]) == 0:
                info = { 
                        'type' : 'Paper',
                        'publication_date' : r["venueInfo"]["publishedDate"]
                        }
            elif int(r["publicationType"]) == 1:
                info = { 
                        'type' : 'Author',
                        'publication_date' : r["venueInfo"]["publishedDate"],
                        'name' :  r["venueInfo"]["displayName"],
                        'volume' : r["venueInfo"]["volume"],
                        'issue' : r["venueInfo"]["issue"],
                        'pages' : r["venueInfo"]["firstPage"] + " - " + r["venueInfo"]["lastPage"]
                        }
            elif int(r["publicationType"]) == 2:
                info = { 
                        'type' : 'Journal',
                        'publication_date' : r["venueInfo"]["publishedDate"]
                        }
            elif int(r["publicationType"]) == 3:
                info = { 
                        'type' : 'Conference Series',
                        'name' : r["venueInfo"]["displayName"],
                        'publication_date' : r["venueInfo"]["publishedDate"]
                        }
                p.year = info['publication_date']
            elif int(r["publicationType"]) == 4:
                info = { 
                        'type' : 'Conference Instance',
                        'publication_date' : r["venueInfo"]["publishedDate"]
                        }
            elif int(r["publicationType"]) == 5:
                info = { 
                        'type' : 'Affiliation',
                        'publication_date' : r["venueInfo"]["publishedDate"]
                        }
            else:
                info = { 
                        'type' : 'Field Of Study',
                        'publication_date' : r["venueInfo"]["publishedDate"]
                        }
            if info != None:
                p.publication_type = info['type']
                p.publication_info = info
                p.year = r["venueInfo"]["publishedDate"]
                
            else: 
                raise ValueError("Null info")
                
            self.addResult(p)
            #self.addResult(p) #To check duplication verification
            

class SagePub(Search):
    def search(self):
        
        keywords = self.keyword
        numberOfResults = self.numberOfResults

        url ='https://journals.sagepub.com/action/doSearch?AllField=' + str(keywords) + '&pageSize=' + str(numberOfResults) + '&startPage=0'
        session = requests.Session()
        session.cookies.set_policy(BlockAll())
        response = session.request('GET', url, headers=self.get_random_headers())
        response = response.text 
        soup = BeautifulSoup(response, "html.parser")
        for results in soup.find_all('article'):
            title = results.find('span', attrs={'class': 'art_title'})
            if title != None :
                p = Publication()
                
                title = results.find('span', attrs={'class': 'art_title'})
                p.title = title.get_text()
                
                typeArticle = results.find('span', attrs={'class': 'ArticleType'})
                if typeArticle != None :
                    p.publication_type = typeArticle.get_text()
                    
                
                authors = results.find('span', attrs={'class': 'articleEntryAuthorsLinks'})
                
                #TODO:: get name of authors, location.
                '''if authors != None:
                    author = authors.find_all('a', attrs={'class': 'entryAuthor'})
                    for a in author:
                        #print(a.get('href'))
                        if a.get('href') != None :
                            print(a.get_text())
                '''    
                
                info = { 
                            'type' : ' ',
                            'publication_date' : ' ',
                            'name' :  ' ',
                            'volume' : ' ',
                            'issue' : ' ',
                            'pages' : ' '
                        }
                
                journalTitle = results.find('span', attrs={'class': 'journal-title'})
                if journalTitle != None :
                    info['name'] = journalTitle.get_text()

                publishedDate = results.find('span', attrs={'class': 'maintextleft'})
                if publishedDate != None :
                    info['publication_date'] = publishedDate.get_text()
                    p.year = publishedDate.get_text()
                
                p.publication_info = info
                
                
                doi = results.find('span', attrs={'class': 'publication-meta-doi'})
                if doi != None :
                    p.doi = doi.get_text()
                
                self.addResult(p)


class GoogleScholar(Search):
    def search(self):
        keywords = self.keyword
        numberOfResults = self.numberOfResults
        print("La recherche: " + keywords + "\n")
        for i in range(0,numberOfResults,10):
            url ='https://scholar.google.fr/scholar?start=' + str(i) + '&q=' +keywords
            req = Request(url, headers=self.get_random_headers())
            response = urlopen(req).read()
            soup = BeautifulSoup(response, "html.parser")
            for results in soup.find_all("div", {"class" : 'gs_r gs_or gs_scl'}):
                for r in results:
                    if r.a.get('id') != None:
                        print("Titre: " + r.a.get_text() + '\n') 
                    if str(r.div.get('class'))== "['gs_a']":
                        authors= ""
                        for ra in r.div.find_all('a'):
                            authors= authors + ra.get_text() + " "
                            print(ra.get_text())
                    if r.a.get('id') == None:
                        if r.a == None:
                            print("null")
                        else:
                            print("Editeur: " + r.a.get_text() + "\n")
            #time.sleep(5)

        
class ScienceDirect(Search):
    def search(keywords, numberOfResults):
        url ='https://www.sciencedirect.com/search?qs=' + keywords + '&show=' + str(numberOfResults) + '&sortBy=relevance'
        req = Request(url, headers=Search.get_random_headers())
        response = urlopen(req).read()
        soup = BeautifulSoup(response, "html.parser")
        for result in soup.find_all('a'):
            print(result.get_text())
class Springer(Search):
    def search(keywords, numberOfResults):
        url ='https://link.springer.com/search?query=machine+learning'
        req = Request(url, headers=Search.get_random_headers())
        response = urlopen(req).read()
        soup = BeautifulSoup(response, "html.parser")
        for result in soup.find_all('a'):
            print(result.get_text())
class IEEE(Search):
    def search(keywords, numberOfResults):
        url ='https://link.springer.com/search?query=machine+learning'
        req = Request(url, headers=Search.get_random_headers())
        response = urlopen(req).read()
        soup = BeautifulSoup(response, "html.parser")
        for result in soup.find_all("a", {'class': 'title'}):
            print(result.get_text())
        
class ACM(Search): 
    def search(keywords, numberOfResults):
        url ='https://dl.acm.org/results.cfm?query=machine%20learning&start=0'
        req = Request(url, headers=Search.get_random_headers())
        response = urlopen(req).read()
        soup = BeautifulSoup(response, "html.parser")
        for result in soup.find_all('a'):
            print(result.get_text())
