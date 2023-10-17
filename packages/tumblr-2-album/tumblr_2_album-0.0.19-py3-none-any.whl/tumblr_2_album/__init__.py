#!/usr/bin/env python3

# -*- coding: utf-8 -*-

name = 'tumblr_2_album'

from telegram_util import AlbumResult as Result
from bs4 import BeautifulSoup
from tumdlr import downloader
import cached_url
from contextlib import contextmanager
import sys, os

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout

def getImgs(post):
    soup = BeautifulSoup(post, 'html.parser')
    has_video = False
    for item in soup.find_all('source'):
        if item.get('type') != 'video/mp4':
            continue
        if not item.get('src'):
            continue
        has_video = True
        yield item['src']
    if not has_video:
        for item in soup.find_all('img'):
            yield item['src']

def getImgsJson(post):
    for photo in post:
        yield photo['original_size']['url']

def preDownload(img):
    filename = cached_url.getFilePath(img)
    if os.path.exists(filename):
        return
    # seems this is not silent
    with suppress_stdout():
        downloader.download(img, filename, silent=True)

def getText(post):
    soup = BeautifulSoup(post, 'html.parser')
    for item in soup.find_all('a', class_='tumblr_blog'):
        item.decompose()
    for tag in ['img']:
        for item in soup.find_all(tag):
            item.decompose()
    lines = []
    for item in soup.find_all():
        if item.name not in ['p', 'li', 'h1', 'h2', 'h3', 'h4', 'blockquote', 'figure']:
            continue
        if item.name == 'blockquote' and item.find('p'):
            continue
        if item.name == 'figure':
            if 'tmblr-embed' in (item.attrs.get('class') or []):
                url = item.get('data-url')
                iframe = item.find('iframe')
                if url:
                    iframe.replace_with(url)
        if item.find('a'):
            sub_item = item.find('a')
            if 'href' not in sub_item:
                print('tumblr_2_album no href', sub_item)
            else:
                link = sub_item['href'].split('https://href.li/?')[-1]
                sub_text = sub_item.text.strip('\u200b').strip()
                sub_item.replace_with(sub_text + ' ' + link + ' ')
        line = item.text.strip('\u200b').strip()
        if len(line) > 2:
            lines.append(line)
        item.decompose()
    return '\n\n'.join(lines)

def getBlogNameAndPostId(url):
    blog_name = url.split('/')[2].split('.')[0]
    if blog_name == 'www':
        blog_name = url.split('/')[3]
    for index in range(-1, -4, -1):
        try:
            post_id = int(url.strip('/').split('/')[index])
            break
        except:
            ...
    return blog_name, post_id

def getFromPost(post, pre_download=True):
    result = Result()
    result.url = post['post_url']
    result.video = post.get('video_url')
    post_body = post.get('caption', '') or post.get('body', '') or post.get('question', '') + post.get('answer', '')
    result.cap_html_v2 = getText(post_body) or post['summary']
    post_body_all = post.get('caption', '') + (post.get('body', '') or post.get('question', '') + post.get('answer', ''))
    if post.get('caption'):
        result.imgs = list(getImgsJson(post.get('photos', []))) 
    result.imgs += list(getImgs(post_body_all))
    if pre_download:
        for img in result.imgs:
            preDownload(img)
    return result

def getCanonical(post):
    result = getFromPost(post, pre_download=False)
    if result.video or len(result.cap_html_v2) < 900 or (not result.imgs):
        for img in result.imgs:
            preDownload(img)
        return result
    result.imgs = []
    return result

def get(client, url):
    blog_name, post_id = getBlogNameAndPostId(url)
    post = client.posts(blog_name, id=post_id)['posts'][0]
    return getFromPost(post)
    