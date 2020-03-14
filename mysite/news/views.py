from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import os
import json
from newspaper import Article
# Create your views here.

import re
import nltk

from newspaper import Article
nltk.download('stopwords')
nltk.download('punkt')

from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


from nltk.sentiment.vader import SentimentIntensityAnalyzer
from newspaper import Article
from textblob import TextBlob
from nltk.stem import PorterStemmer 
from rake_nltk import Rake
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import string
def index(request):
    return render(request,'index.html')

def preprocessing(line):
    if(len(line) != 0):
        line = line.lower()
        line = re.sub(r"[{}]".format(string.punctuation), " ", line)
        
        return line
    else:
        return "Error"


def result(request):
    headline = request.GET['headline']
    querystring = {"q":headline,"apiKey":"f4165a93afb24b4285b4c49e41925e2b","pageSize":"15", "language": "en"}
    url = "http://newsapi.org/v2/everything"
    headers = {
        'authorization': "Basic Ymx1ZW1vb24tbnVnZXQtdXNlcjpleUoyWlhJaU9pSXlJaXdpZEhsd0lqb2lTbGRVSWl3aVlXeG5Jam9pVWxNeU5UWWlMQ0pyYVdRaU9pSmZSRzAyVFdGUldVMVBibnBFTVdRMmFubGhPRzlSVVVvdFFqYzVZbU4xY0Y4Mk5tdzJXRVYyZGtobkluMC5leUp6ZFdJaU9pSnFabkowUURBeFpHTXlOMjB5YldGcmQySm5NVEZoT0dzMWMzSXdOWG95WEM5MWMyVnljMXd2WW14MVpXMXZiMjR0Ym5WblpYUXRkWE5sY2lJc0luTmpjQ0k2SW0xbGJXSmxjaTF2WmkxbmNtOTFjSE02S2lCaGNHazZLaUlzSW1GMVpDSTZJbXBtY25SQU1ERmtZekkzYlRKdFlXdDNZbWN4TVdFNGF6VnpjakExZWpJaUxDSnBjM01pT2lKcVpuSjBRREF4WkdNeU4yMHliV0ZyZDJKbk1URmhPR3MxYzNJd05Yb3lYQzkxYzJWeWMxd3ZZV1J0YVc0aUxDSmxlSEFpT2pFMU9UQXpNemt5TWpRc0ltbGhkQ0k2TVRVNE1qVTJNekl5TkN3aWFuUnBJam9pWlRNMk1UY3lZbUV0TjJVeVlpMDBZVEV4TFRsbE1tTXRNRGRsTURKa09ETmlPVFU0SW4wLlpHOTFhYkhWSFd6ZkdoVnZHMEVkSzdObUhibDBkRWxCcFAwZHBZSmZQTUMtSDkxbDF4QVdEX0FJa2dtYmpta3NwOUVOMlE2OWplOGxCWVBMQ3A3WjFrbGhBbTBHQnYyd0J5enZReWoyVmRGYXh5aFdNME1pekpvTktSVkJwRWRkYWVndjVpejhZZjcwMm11U3RWdnJmc3hlZkEzQjhRYldPMVlWelZqZXRkMndVRFRzbjgyYVdkX205Nm1DUy1xSC1UcDF4ZC1Ydm5VMVI3aXFoMnljM3Y5XzFETTVYNWNaWHkxbWhZdTZpb3JxYWgxWTZVRHhHTC1fd1M2a1l2M3lqSE1BVjQwWnpNUU9td2dLN3JUOWlza0lYTzlFMkYxeFNLLWpVaWpHVWNwNThfSkVkRFdOa19TbHYyMHVnZEI4UUpYZXcxVWtKMGVPaGpuLVI1N1RMdw==",
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "33239ded-a675-5d3e-79ff-6032cfa29b4e"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    #print(response.text)
    news_dict = json.loads(response.text)
    length = len(news_dict['articles'])
    author = []
    title = []
    content = []
    source = []
    description = []
    all_url = []
    counter=0
    for i in news_dict['articles']:
        print(counter)
        counter+=1
        try:
            author.append(i['author'])
            title.append(i['title'])
            source.append(i['source'])
            description.append(i['description'])
            all_url.append(i['url'])
            r1 = requests.get(i['url'])
            text = r1.content
            soup = BeautifulSoup(text, 'html.parser')
            paragraph_list = soup.find_all('p')
            whole_content = ""
            for item in range(len(paragraph_list)):
                whole_content = whole_content + " " + paragraph_list[item].get_text()
            content.append(whole_content)
        except:
            continue
        
    keyword = headline
    stop_words = set(stopwords.words('english')).union(keyword)
    symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n,"
    stemmer = PorterStemmer()
    filtered = []
    for i in range(len(content)):
        word_tokens = word_tokenize(content[i]) 
        filtered_sentence = [w for w in word_tokens if not w in stop_words] 
        filtered_sentence = [] 
        filtered_string = ""

        for w in word_tokens: 
            if w not in stop_words: 
                filtered_sentence.append(w)
                for i in symbols:
                    w = np.char.replace(w, i, ' ')
                w = np.char.replace(w, "'", "")
                w = stemmer.stem(str(w).lower())
                filtered_string = filtered_string + " " + w

        filtered_string = " ".join(filtered_string.split())
        filtered.append(filtered_string)


    tfidf_vectorizer = TfidfVectorizer(preprocessor=preprocessing)
    tfidf = tfidf_vectorizer.fit_transform(filtered)

    kmeans = KMeans(n_clusters=2).fit(tfidf)

    lines_for_predicting = filtered
    results = list(kmeans.predict(tfidf_vectorizer.transform(lines_for_predicting)))
    
    first = []
    second = []
    
    for i,j in zip(results, title):
        if(i == 0):
            first.append(j)
        elif (i == 1):
            second.append(j)

    return render(request,'result.html',{"headline":headline,"first":first,"second":second})