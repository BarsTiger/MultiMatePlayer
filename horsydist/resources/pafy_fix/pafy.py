# -*- coding: utf-8 -*-

Pafy = None

def new(url, basic=True, gdata=False, size=False,
        callback=None, ydl_opts=None):
    global Pafy
    if Pafy is None:
       from .backend_youtube_dl import YtdlPafy as Pafy

    return Pafy(url, basic, gdata, size, callback, ydl_opts=ydl_opts)
