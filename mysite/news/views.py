from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import os
import json
from newspaper import Article
# Create your views here.

def index(request):
    return render(request,'index.html')

def result(request):
    headline = request.GET['headline']
    querystring = {"q":headline,"apiKey":"f4165a93afb24b4285b4c49e41925e2b","pageSize":"100", "language": "en"}
    url = "http://newsapi.org/v2/everything"
    headers = {
        'authorization': "Basic Ymx1ZW1vb24tbnVnZXQtdXNlcjpleUoyWlhJaU9pSXlJaXdpZEhsd0lqb2lTbGRVSWl3aVlXeG5Jam9pVWxNeU5UWWlMQ0pyYVdRaU9pSmZSRzAyVFdGUldVMVBibnBFTVdRMmFubGhPRzlSVVVvdFFqYzVZbU4xY0Y4Mk5tdzJXRVYyZGtobkluMC5leUp6ZFdJaU9pSnFabkowUURBeFpHTXlOMjB5YldGcmQySm5NVEZoT0dzMWMzSXdOWG95WEM5MWMyVnljMXd2WW14MVpXMXZiMjR0Ym5WblpYUXRkWE5sY2lJc0luTmpjQ0k2SW0xbGJXSmxjaTF2WmkxbmNtOTFjSE02S2lCaGNHazZLaUlzSW1GMVpDSTZJbXBtY25SQU1ERmtZekkzYlRKdFlXdDNZbWN4TVdFNGF6VnpjakExZWpJaUxDSnBjM01pT2lKcVpuSjBRREF4WkdNeU4yMHliV0ZyZDJKbk1URmhPR3MxYzNJd05Yb3lYQzkxYzJWeWMxd3ZZV1J0YVc0aUxDSmxlSEFpT2pFMU9UQXpNemt5TWpRc0ltbGhkQ0k2TVRVNE1qVTJNekl5TkN3aWFuUnBJam9pWlRNMk1UY3lZbUV0TjJVeVlpMDBZVEV4TFRsbE1tTXRNRGRsTURKa09ETmlPVFU0SW4wLlpHOTFhYkhWSFd6ZkdoVnZHMEVkSzdObUhibDBkRWxCcFAwZHBZSmZQTUMtSDkxbDF4QVdEX0FJa2dtYmpta3NwOUVOMlE2OWplOGxCWVBMQ3A3WjFrbGhBbTBHQnYyd0J5enZReWoyVmRGYXh5aFdNME1pekpvTktSVkJwRWRkYWVndjVpejhZZjcwMm11U3RWdnJmc3hlZkEzQjhRYldPMVlWelZqZXRkMndVRFRzbjgyYVdkX205Nm1DUy1xSC1UcDF4ZC1Ydm5VMVI3aXFoMnljM3Y5XzFETTVYNWNaWHkxbWhZdTZpb3JxYWgxWTZVRHhHTC1fd1M2a1l2M3lqSE1BVjQwWnpNUU9td2dLN3JUOWlza0lYTzlFMkYxeFNLLWpVaWpHVWNwNThfSkVkRFdOa19TbHYyMHVnZEI4UUpYZXcxVWtKMGVPaGpuLVI1N1RMdw==",
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "33239ded-a675-5d3e-79ff-6032cfa29b4e"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)
    news_dict = json.loads(response.text)
    length = len(news_dict['articles'])
    author = []
    title = []
    content = []
    source = []
    description = []
    all_url = []
    for i in range(length):
        author.append(news_dict['articles'][i]['author'])
        title.append(news_dict['articles'][i]['title'])
        source.append(news_dict['articles'][i]['source'])
        description.append(news_dict['articles'][i]['description'])
        all_url.append(news_dict['articles'][i]['url'])
        r1 = requests.get(news_dict['articles'][i]['url'])
        text = r1.content
        soup = BeautifulSoup(text, 'html.parser')
        paragraph_list = soup.find_all('p')
        whole_content = ""
        for item in range(len(paragraph_list)):
            whole_content = whole_content + " " + paragraph_list[item].get_text()
        
        content.append(whole_content)
    return render(request,'result.html',{"headline":headline,"headlines": title})