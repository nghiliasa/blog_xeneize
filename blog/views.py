from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.generic import View
from django.http import Http404
from bs4 import BeautifulSoup
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
        ole_articles = ole_soup.find_all('article')
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

    # ----------------------- Fuente Goal ----------------------------

    last_tyc_news = [
        tyc_news[0],
        tyc_news[1],
        tyc_news[2],
        tyc_news[3],
        tyc_news[4],
    ]
    last_ole_news = [
        ole_news[0],
        ole_news[1],
        ole_news[2],
        ole_news[3],
        ole_news[4],
    ]
    last_as_news = [
        as_news[0],
        as_news[1],
        as_news[2],
        as_news[3],
        as_news[4],
    ]
    last_infobae_news = [
        infobae_news[0],
        infobae_news[1],
        infobae_news[2],
        infobae_news[3],
        infobae_news[4],
    ]
    last_ln_news = [
        ln_news[0],
        ln_news[1],
        ln_news[2],
        ln_news[3],
        ln_news[4],
    ]
    last_bv_news = [
        bv_news[0],
        bv_news[1],
        bv_news[2],
        bv_news[3],
        bv_news[4],
    ]

    # ----------------------- Fuente Fútbol Libre ----------------------------

    pr_link = 'https://www.promiedos.com.ar/primera'
    pr_page = requests.get(pr_link)
    pr_soup = BeautifulSoup(pr_page.content, 'html.parser')
    pr_table = pr_soup.find_all('table', 'tablesorter1')[0]
    filas = pr_table.find_next('img')['src'] = 'https://www.promiedos.com.ar/' + pr_table.find('img')['src']
    print(filas)
    pr_clock = 1
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
        "pr_table": str(pr_table),
        }
    return render(request, "blog/index.html", contenido)