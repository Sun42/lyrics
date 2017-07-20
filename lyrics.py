#!/usr/bin/python3
"""
Print lyrics of a song.

Usage:
    lyrics.py <song_title>
"""
import pdb
import re
import sys
from urllib.parse import quote
import urllib.request

from lxml import html

def makerequest(search):
    """
    Construct a musixmatch search request
    Parameter: string:search
    Returns: string
    """
    uri = "https://www.musixmatch.com/search/" + quote(search)
    return uri

def bestresult(musixmatch_searchresult_page):
    """Take a musixmatch result page and extract the best result link.

    Args:
        musixmatch_searchresult_page (stream_object): The html  musixmatch searchresult page

    Returns:
        str: the 'best result' link

    Raises:
        ValueError: If the regex didnt match anything
    """
    html = musixmatch_searchresult_page.read()
    pattern = re.compile(b'"track_share_url":"(\S+?)",')
    ret = pattern.findall(html)
    if ret:
        return str(ret[0], 'unicode_escape')
    raise ValueError('No result found')

def getlyrics(musixmatch_lyrics_page):
   """Take a musixmatch lyrics page and extract the lyrics content.

    Args:
        musixmatch_lyrics_page (stream_object): The html musixmatch lyrics page

    Returns:
        str: lyrics content

    Raises:
        ValueError: If no lyrics to be found
    """
   doc = html.fromstring(musixmatch_lyrics_page.read())
   ret = [e.text_content() for e in doc.find_class('mxm-lyrics__content')]
   ret = "\n".join(ret)
   return ret

if __name__ == "__main__":
    if len(sys.argv) == 2:
        try:
            search_uri = makerequest(sys.argv[1])
            print(search_uri)
            search_req = urllib.request.Request(search_uri, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(search_req) as search_page:
                lyrics_uri = bestresult(search_page)
                print(bytes(lyrics_uri, "utf-8").decode("unicode_escape"))
            lyrics_req = urllib.request.Request(lyrics_uri, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(lyrics_req) as lyrics_page:
                text = getlyrics(lyrics_page)
            print(text)
        except Exception as e:
            print(str(e))
            sys.exit(1)
    else:
        print(__doc__)
