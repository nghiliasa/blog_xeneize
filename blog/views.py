from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.generic import View
from django.http import Http404
from bs4 import BeautifulSoup
from collections import OrderedDict
import requests
import cfscrape
import random
import urllib
import json

# Create your views here.

def index(request):
    tyc_news = []
    tyc_title = 'TyC Sports'
    ole_news = []
    ole_title = 'Diario Deportivo Olé'
    as_news = []
    as_title = 'AS Argentina'
    infobae_news = []
    infobae_title = 'Infobae'
    ln_news = []
    ln_title = 'La Nación'
    bv_news = []
    bv_title = 'Bola Vip'

    # ----------------------- Fuente Tyc Sports ----------------------------
    try:
        tyc = 'https://www.tycsports.com/boca-juniors.html'
        tyc_page = requests.get(tyc)
        tyc_soup = BeautifulSoup(tyc_page.content, 'html.parser')
        tyc_section = tyc_soup.find_all('section', 'p20')
        tyc_a_labels = tyc_section[0].find_all('a', 'card-thumbnail rat16x9')
        tyc_clock = 1
        for label in tyc_a_labels:
            news = {}
            news_link = 'https://www.tycsports.com' + label.attrs.get('href')
            if tyc_clock == 1:
                image = label.find('img', attrs={'class': None}).attrs.get('src')
            else:
                image = label.find('img', attrs={'class': None}).attrs.get('data-src')
            title = label.find('img', attrs={'class': None}).attrs.get('title')
            news['id'] = tyc_clock
            news['news_link'] = news_link
            news['image'] = image
            news['title'] = title
            news['source'] = tyc_title
            tyc_news.append(news)
            tyc_clock += 1

    except:
        pass

    # ----------------------- Fuente Olé ----------------------------
    try:
        ole = 'https://www.ole.com.ar/boca-juniors/'
        ole_page = requests.get(ole)
        ole_soup = BeautifulSoup(ole_page.content, 'html.parser')
        ole_articles_base_1 = ole_soup.find_all('div', 'bb-tu first-t col col_4')
        ole_articles_base_2 = ole_soup.find_all('div', 'bb-tu col col_4')
        ole_articles_base_3 = ole_soup.find_all('div', 'bb-tu first-t col col_8')[0].find_all('article')
        ole_articles_1 = []
        ole_articles_2 = []
        ole_articles_3 = []
        for i in ole_articles_base_1:
            articles = i.find_all('article', 'entry entry-box modNot-33')
            for x in articles:
                ole_articles_1.append(x)
        for i in ole_articles_base_2:
            articles = i.find_all('article', 'entry entry-box modNot-33')
            for x in articles:
                ole_articles_2.append(x)
        
        ole_articles = ole_articles_1 + ole_articles_2 + ole_articles_base_3
        ole_clock = 1
        for article in ole_articles:
            news = {}
            news_link = 'https://www.ole.com.ar' + article.find_all('a')[0].attrs.get('href')
            image = article.find_all('a')[0].find_next('img').attrs.get('src')
            title = article.find_next('div', 'entry-data').find_next('h2', 'entry-title').find_next('a').get_text()
            news['id'] = ole_clock
            news['news_link'] = news_link
            news['image'] = image
            news['title'] = title
            news['source'] = ole_title
            ole_news.append(news)
            ole_clock += 1

    except:
        pass

    # ----------------------- Fuente AS Argentina ----------------------------
    try:
        as_link = 'https://argentina.as.com/tag/boca_juniors/a/'
        as_page = requests.get(as_link)
        as_soup = BeautifulSoup(as_page.content, 'html.parser')
        as_articles = as_soup.find_all('article', 's s--v')
        as_clock = 1
        for article in as_articles:
            news = {}
            news_link = 'https://argentina.as.com' + article.find_next('figure', 'mm s__mm').find_next('a').attrs.get('href')
            image = article.find_next('figure', 'mm s__mm').find_next('img').attrs.get('src')
            if image == 'https://as01.epimg.net/t.gif':
                image = article.find_next('figure', 'mm s__mm').find_next('img').attrs.get('srcset')
            title = article.find_next('h2', 's__tl').find_next('a').get_text()
            news['id'] = as_clock
            news['news_link'] = news_link
            news['image'] = image
            news['title'] = title
            news['source'] = as_title
            as_news.append(news)
            as_clock += 1

    except:
        pass

    # ----------------------- Fuente Infobae ----------------------------
    try:
        infobae_link = 'https://www.infobae.com/tag/boca-juniors/'
        infobae_page = requests.get(infobae_link)
        infobae_soup = BeautifulSoup(infobae_page.content, 'html.parser')
        infobae_articles = infobae_soup.find_all('a', 'nd-feed-list-card')
        infobae_clock = 1
        for article in infobae_articles:
            news = {}
            news_link = 'https://www.infobae.com' + article.attrs.get('href')
            image = 'https://' + article.find_next('img').attrs.get('src').split('quality(85)/')[1].split(' ')[0]
            title = article.find_next('h2').get_text()
            news['id'] = infobae_clock
            news['news_link'] = news_link
            news['image'] = image
            news['title'] = title
            news['source'] = infobae_title
            infobae_news.append(news)
            infobae_clock += 1

    except:
        pass

    # ----------------------- Fuente La Nación ----------------------------
    try:
        ln_link = 'https://www.lanacion.com.ar/deportes/futbol/boca-juniors/'
        ln_page = requests.get(ln_link)
        ln_soup = BeautifulSoup(ln_page.content, 'html.parser')
        ln_articles = ln_soup.find_all('article', 'mod-article')
        ln_clock = 1
        for article in ln_articles:
            try:
                news = {}
                news_link = 'https://www.lanacion.com.ar' + article.find_next('figure').find_next('a').attrs.get('href')
                image = article.find_next('figure').find_next('picture').find_next('img').attrs.get('src')
                title = article.find_next('section', 'mod-description').find_next('h2', 'com-title').get_text()
                news['id'] = ln_clock
                news['news_link'] = news_link
                news['image'] = image
                news['title'] = title
                news['source'] = ln_title
                ln_news.append(news)
                ln_clock += 1
            except:
                pass

    except:
        pass

    # ----------------------- Fuente Bola Vip ----------------------------
    try:
        bv_link = 'https://bolavip.com/ar/boca'
        bv_page = requests.get(bv_link)
        bv_soup = BeautifulSoup(bv_page.content, 'html.parser')
        bv_articles1 = bv_soup.find_all('article')
        bv_clock = 1
        for article in bv_articles1:
            try:
                news = {}
                news_link = article.find_next('figure').find_next('a').attrs.get('href')
                if news_link.startswith('https://bolavip.com') == False:
                    news_link = 'https://bolavip.com' + news_link
                image = article.find_next('img').attrs.get('src')
                title = article.find_next('a').attrs.get('title')
                news['id'] = bv_clock
                news['news_link'] = news_link
                news['image'] = image
                news['title'] = title
                news['source'] = bv_title
                bv_news.append(news)
                bv_clock += 1
            except:
                pass

    except:
        pass

    # ----------------------- Últimas noticias ----------------------------
    last_tyc_news = []
    
    try:
        last_tyc_news.append(tyc_news[0])
        last_tyc_news.append(tyc_news[1])
        last_tyc_news.append(tyc_news[2])
        last_tyc_news.append(tyc_news[3])
        last_tyc_news.append(tyc_news[4])
    except:
        pass

    last_ole_news = []
    
    try:
        last_ole_news.append(ole_news[0])
        last_ole_news.append(ole_news[1])
        last_ole_news.append(ole_news[2])
        last_ole_news.append(ole_news[3])
        last_ole_news.append(ole_news[4])
    except:
        pass

    last_as_news = []
    
    try:
        last_as_news.append(as_news[0])
        last_as_news.append(as_news[1])
        last_as_news.append(as_news[2])
        last_as_news.append(as_news[3])
        last_as_news.append(as_news[4])
    except:
        pass

    last_infobae_news = []
    
    try:
        last_infobae_news.append(infobae_news[0])
        last_infobae_news.append(infobae_news[1])
        last_infobae_news.append(infobae_news[2])
        last_infobae_news.append(infobae_news[3])
        last_infobae_news.append(infobae_news[4])
    except:
        pass

    last_ln_news = []
    
    try:
        last_ln_news.append(ln_news[0])
        last_ln_news.append(ln_news[1])
        last_ln_news.append(ln_news[2])
        last_ln_news.append(ln_news[3])
        last_ln_news.append(ln_news[4])
    except:
        pass

    last_bv_news = []
    
    try:
        last_bv_news.append(bv_news[0])
        last_bv_news.append(bv_news[1])
        last_bv_news.append(bv_news[2])
        last_bv_news.append(bv_news[3])
        last_bv_news.append(bv_news[4])
    except:
        pass

    contenido = {
        "nombre_sitio": "Blog Xeneize", 
        "tyc_news": tyc_news,
        "tyc_title": tyc_title,
        "ole_news": ole_news,
        "ole_title": ole_title,
        "as_news": as_news,
        "as_title": as_title,
        "infobae_news": infobae_news,
        "infobae_title": infobae_title,
        "ln_news": ln_news,
        "ln_title": ln_title,
        "bv_news": bv_news,
        "bv_title": bv_title,
        "last_tyc_news": last_tyc_news,
        "last_ole_news": last_ole_news,
        "last_as_news": last_as_news,
        "last_infobae_news": last_infobae_news,
        "last_ln_news": last_ln_news,
        "last_bv_news": last_bv_news,
        }
    return render(request, "blog/index.html", contenido)