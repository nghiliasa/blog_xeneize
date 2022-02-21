from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.generic import View
from django.http import Http404
from bs4 import BeautifulSoup
from collections import OrderedDict
import xml.etree.ElementTree as ET
import requests
import cfscrape
import random
import urllib
import json
from .models import Visit


def get_user_public_ip(request):
    """  Getting client Ip  """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def youtube(origin, id):
    urlvideo = 'https://www.youtube.com/feeds/videos.xml?{}={}'.format(origin, id)
    query = requests.get(urlvideo, headers={ "User-Agent": "Chrome/50.0.2661.94" })
    data = query.content
    root = ET.fromstring(data.decode())
    channel_title = root.find('.//{http://www.w3.org/2005/Atom}title').text
    channel_link = root.findall('.//{http://www.w3.org/2005/Atom}link')[1].get('href')
    videos_content = root.findall('.//{http://www.w3.org/2005/Atom}entry')
    videos = []
    for item in videos_content:
        video = {
            'title': item.find('.//{http://www.w3.org/2005/Atom}title').text,
            'embed': 'https://www.youtube.com/embed/' + item.find('.//{http://www.w3.org/2005/Atom}link').get('href').split('watch?v=')[1],
            'link': item.find('.//{http://www.w3.org/2005/Atom}link').get('href'),
            'thumb': item.find('.//{http://search.yahoo.com/mrss/}thumbnail').get('url'),
            'views': item.find('.//{http://search.yahoo.com/mrss/}statistics').get('views'),
            'likes': item.find('.//{http://search.yahoo.com/mrss/}starRating').get('count'),
            'channel_title': channel_title,
            'channel_link': channel_link,
        }
        videos.append(video)
    return videos

# Create your views here.

def prueba(request):

    tyc_news = []
    tyc_title = 'TyC Sports'
    tyc_web = 'https://www.tycsports.com/'
    ole_news = []
    ole_title = 'Diario Deportivo Olé'
    ole_web = 'https://www.ole.com.ar/'
    as_news = []
    as_title = 'AS Argentina'
    as_web = 'https://argentina.as.com/'
    infobae_news = []
    infobae_title = 'Infobae'
    infobae_web = 'https://www.infobae.com/'
    ln_news = []
    ln_title = 'La Nación'
    ln_web = 'https://www.lanacion.com.ar/'
    bv_news = []
    bv_title = 'Bola Vip'
    bv_web = 'https://bolavip.com/ar'

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

    # ----------------Fuente MundoBocaTV------------------

    mbtv_title = 'MundoBocaTV' 
    mbtv_channel = 'https://www.youtube.com/channel/UCtFanqiLodEW0ZQEshO1gyw'
    mbtv_videos = youtube('channel_id', 'UCtFanqiLodEW0ZQEshO1gyw')
    
    # ----------------Fuente Alma Xeneize------------------

    ax_title = 'Alma Xeneize' 
    ax_channel = 'https://www.youtube.com/c/ALMAXENEIZEradio'
    ax_videos = youtube('channel_id', 'UCx7rTQEwFDvSBxYjo7rmdPA')
    
    # ----------------Fuente Club Atlético Boca Juniors------------------

    cabj_title = 'Club Atlético Boca Juniors' 
    cabj_channel = 'https://www.youtube.com/c/bocajuniors'
    cabj_videos = youtube('channel_id', 'UCRtB_RAtKH72CgVAKHFgdIw')
    
    # ----------------Fuente AX------------------

    ax2_title = 'AX' 
    ax2_channel = 'https://www.youtube.com/channel/UCZFhYCVsAzEXdmJRPiKdMaA'
    ax2_videos = youtube('channel_id', 'UCZFhYCVsAzEXdmJRPiKdMaA')
    
    # ----------------Fuente El Show de Boca (con Roberto Leto)------------------

    esdb_title = 'El Show de Boca (con Roberto Leto)' 
    esdb_channel = 'https://www.youtube.com/channel/UCigMtQPA1eB3pAa1ri78syg'
    esdb_videos_list = youtube('channel_id', 'UCigMtQPA1eB3pAa1ri78syg')
    esdb_videos = []
    for video in esdb_videos_list:
        string = video['title']
        if "EL SHOW DE #BOCA CON ROBERTO LETO" in string:
            esdb_videos.append(video)
        else:
            pass
    
    # ----------------Fuente Tato Aguilera------------------

    ta_title = 'Tato Aguilera' 
    ta_channel = 'https://www.youtube.com/c/TatoAguileraPeriodistaDeportivo'
    ta_videos = youtube('channel_id', 'UCAcqM8y1nSTdAtIPYhX-Sgw')
    
    # ----------------------- Últimos Videos ----------------------------
    
    last_videos = []
    
    try:
        last_videos.append(mbtv_videos[0])
        last_videos.append(ax_videos[0])
        last_videos.append(cabj_videos[0])
        last_videos.append(ax2_videos[0])
        last_videos.append(esdb_videos[0])
        last_videos.append(ta_videos[0])
        last_videos.append(mbtv_videos[1])
        last_videos.append(ax_videos[1])
        last_videos.append(cabj_videos[1])
        last_videos.append(ax2_videos[1])
        last_videos.append(esdb_videos[1])
        last_videos.append(ta_videos[1])
        last_videos.append(mbtv_videos[2])
        last_videos.append(ax_videos[2])
        last_videos.append(cabj_videos[2])
        last_videos.append(ax2_videos[2])
        last_videos.append(esdb_videos[2])
        last_videos.append(ta_videos[2])
        last_videos.append(mbtv_videos[3])
        last_videos.append(ax_videos[3])
        last_videos.append(cabj_videos[3])
        last_videos.append(ax2_videos[3])
        last_videos.append(esdb_videos[3])
        last_videos.append(ta_videos[3])
        last_videos.append(mbtv_videos[4])
        last_videos.append(ax_videos[4])
        last_videos.append(cabj_videos[4])
        last_videos.append(ax2_videos[4])
        last_videos.append(ta_videos[4])
        last_videos.append(mbtv_videos[5])
        last_videos.append(ax_videos[5])
        last_videos.append(cabj_videos[5])
    except:
        pass

    contenido = {
        "nombre_sitio": "Blog Xeneize", 
        "tyc_news": tyc_news,
        "tyc_title": tyc_title,
        "tyc_web": tyc_web,
        "ole_news": ole_news,
        "ole_title": ole_title,
        "ole_web": ole_web,
        "as_news": as_news,
        "as_title": as_title,
        "as_web": as_web,
        "infobae_news": infobae_news,
        "infobae_title": infobae_title,
        "infobae_web": infobae_web,
        "ln_news": ln_news,
        "ln_title": ln_title,
        "ln_web": ln_web,
        "bv_news": bv_news,
        "bv_title": bv_title,
        "bv_web": bv_web,
        "last_tyc_news": last_tyc_news,
        "last_ole_news": last_ole_news,
        "last_as_news": last_as_news,
        "last_infobae_news": last_infobae_news,
        "last_ln_news": last_ln_news,
        "last_bv_news": last_bv_news,
        "mbtv_title": mbtv_title,
        "mbtv_channel": mbtv_channel,
        "mbtv_videos": mbtv_videos,
        "ax_title": ax_title,
        "ax_channel": ax_channel,
        "ax_videos": ax_videos,
        "cabj_title": cabj_title,
        "cabj_channel": cabj_channel,
        "cabj_videos": cabj_videos,
        "ax2_title": ax2_title,
        "ax2_channel": ax2_channel,
        "ax2_videos": ax2_videos,
        "esdb_title": esdb_title,
        "esdb_channel": esdb_channel,
        "esdb_videos": esdb_videos,
        "ta_title": ta_title,
        "ta_channel": ta_channel,
        "ta_videos": ta_videos,
        "last_videos": last_videos,
        }
    return render(request, "blog/index.html", contenido)

def index(request):

    tyc_news = []
    tyc_title = 'TyC Sports'
    tyc_web = 'https://www.tycsports.com/'
    ole_news = []
    ole_title = 'Diario Deportivo Olé'
    ole_web = 'https://www.ole.com.ar/'
    as_news = []
    as_title = 'AS Argentina'
    as_web = 'https://argentina.as.com/'
    infobae_news = []
    infobae_title = 'Infobae'
    infobae_web = 'https://www.infobae.com/'
    ln_news = []
    ln_title = 'La Nación'
    ln_web = 'https://www.lanacion.com.ar/'
    bv_news = []
    bv_title = 'Bola Vip'
    bv_web = 'https://bolavip.com/ar'

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

    # ----------------Fuente MundoBocaTV------------------

    mbtv_title = 'MundoBocaTV' 
    mbtv_channel = 'https://www.youtube.com/channel/UCtFanqiLodEW0ZQEshO1gyw'
    mbtv_videos = youtube('channel_id', 'UCtFanqiLodEW0ZQEshO1gyw')
    
    # ----------------Fuente Alma Xeneize------------------

    ax_title = 'Alma Xeneize' 
    ax_channel = 'https://www.youtube.com/c/ALMAXENEIZEradio'
    ax_videos = youtube('channel_id', 'UCx7rTQEwFDvSBxYjo7rmdPA')
    
    # ----------------Fuente Club Atlético Boca Juniors------------------

    cabj_title = 'Club Atlético Boca Juniors' 
    cabj_channel = 'https://www.youtube.com/c/bocajuniors'
    cabj_videos = youtube('channel_id', 'UCRtB_RAtKH72CgVAKHFgdIw')
    
    # ----------------Fuente AX------------------

    ax2_title = 'AX' 
    ax2_channel = 'https://www.youtube.com/channel/UCZFhYCVsAzEXdmJRPiKdMaA'
    ax2_videos = youtube('channel_id', 'UCZFhYCVsAzEXdmJRPiKdMaA')
    
    # ----------------Fuente El Show de Boca (con Roberto Leto)------------------

    esdb_title = 'El Show de Boca (con Roberto Leto)' 
    esdb_channel = 'https://www.youtube.com/channel/UCigMtQPA1eB3pAa1ri78syg'
    esdb_videos_list = youtube('channel_id', 'UCigMtQPA1eB3pAa1ri78syg')
    esdb_videos = []
    for video in esdb_videos_list:
        string = video['title']
        if "EL SHOW DE #BOCA CON ROBERTO LETO" in string:
            esdb_videos.append(video)
        else:
            pass
    
    # ----------------Fuente Tato Aguilera------------------

    ta_title = 'Tato Aguilera' 
    ta_channel = 'https://www.youtube.com/c/TatoAguileraPeriodistaDeportivo'
    ta_videos = youtube('channel_id', 'UCAcqM8y1nSTdAtIPYhX-Sgw')
    
    # ----------------------- Últimos Videos ----------------------------
    
    last_videos = []
    
    try:
        last_videos.append(mbtv_videos[0])
        last_videos.append(ax_videos[0])
        last_videos.append(cabj_videos[0])
        last_videos.append(ax2_videos[0])
        last_videos.append(esdb_videos[0])
        last_videos.append(ta_videos[0])
        last_videos.append(mbtv_videos[1])
        last_videos.append(ax_videos[1])
        last_videos.append(cabj_videos[1])
        last_videos.append(ax2_videos[1])
        last_videos.append(esdb_videos[1])
        last_videos.append(ta_videos[1])
        last_videos.append(mbtv_videos[2])
        last_videos.append(ax_videos[2])
        last_videos.append(cabj_videos[2])
        last_videos.append(ax2_videos[2])
        last_videos.append(esdb_videos[2])
        last_videos.append(ta_videos[2])
        last_videos.append(mbtv_videos[3])
        last_videos.append(ax_videos[3])
        last_videos.append(cabj_videos[3])
        last_videos.append(ax2_videos[3])
        last_videos.append(esdb_videos[3])
        last_videos.append(ta_videos[3])
        last_videos.append(mbtv_videos[4])
        last_videos.append(ax_videos[4])
        last_videos.append(cabj_videos[4])
        last_videos.append(ax2_videos[4])
        last_videos.append(ta_videos[4])
        last_videos.append(mbtv_videos[5])
        last_videos.append(ax_videos[5])
        last_videos.append(cabj_videos[5])
    except:
        pass
    
    try:
        #------------------------Visitor data------------------------------
        
        user_ip = get_user_public_ip(request)
        user_ip_data = requests.get('http://ip-api.com/json/{}'.format(user_ip)).json()
        user_country = user_ip_data['country']
        user_city = user_ip_data['regionName']
        user_location = user_ip_data['city']
        user_zip = user_ip_data['zip']
        user_lat = user_ip_data['lat']
        user_lon = user_ip_data['lon']
        
        #------------------------New visit------------------------------
        
        new_visit = Visit(
            ip=user_ip,
            country=user_country,
            city=user_city,
            location=user_location,
            zip=user_zip,
            lat=user_lat,
            lon=user_lon
        )
        new_visit.save()

    except:
        pass

    contenido = {
        "nombre_sitio": "Blog Xeneize", 
        "tyc_news": tyc_news,
        "tyc_title": tyc_title,
        "tyc_web": tyc_web,
        "ole_news": ole_news,
        "ole_title": ole_title,
        "ole_web": ole_web,
        "as_news": as_news,
        "as_title": as_title,
        "as_web": as_web,
        "infobae_news": infobae_news,
        "infobae_title": infobae_title,
        "infobae_web": infobae_web,
        "ln_news": ln_news,
        "ln_title": ln_title,
        "ln_web": ln_web,
        "bv_news": bv_news,
        "bv_title": bv_title,
        "bv_web": bv_web,
        "last_tyc_news": last_tyc_news,
        "last_ole_news": last_ole_news,
        "last_as_news": last_as_news,
        "last_infobae_news": last_infobae_news,
        "last_ln_news": last_ln_news,
        "last_bv_news": last_bv_news,
        "mbtv_title": mbtv_title,
        "mbtv_channel": mbtv_channel,
        "mbtv_videos": mbtv_videos,
        "ax_title": ax_title,
        "ax_channel": ax_channel,
        "ax_videos": ax_videos,
        "cabj_title": cabj_title,
        "cabj_channel": cabj_channel,
        "cabj_videos": cabj_videos,
        "ax2_title": ax2_title,
        "ax2_channel": ax2_channel,
        "ax2_videos": ax2_videos,
        "esdb_title": esdb_title,
        "esdb_channel": esdb_channel,
        "esdb_videos": esdb_videos,
        "ta_title": ta_title,
        "ta_channel": ta_channel,
        "ta_videos": ta_videos,
        "last_videos": last_videos,
        }
    return render(request, "blog/prueba.html", contenido)