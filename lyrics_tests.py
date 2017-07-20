#!/usr/bin/python3

import io
import unittest

import lyrics

class YoutubeLyricsTestCase(unittest.TestCase):

    def test_makerequest(self):
        # given
        music_title = "Metallica - Nothing else matters"
        # then
        result = "https://www.musixmatch.com/search/Metallica%20-%20Nothing%20else%20matters"
        self.assertEqual(lyrics.makerequest(music_title), result)

    def test_bestresult(self):
        # given
        with open('musixmatch_results_new.html', 'rb') as html_file:
            # then
            self.assertEqual(lyrics.bestresult(html_file), "https://www.musixmatch.com/lyrics/Metallica/Nothing-Else-Matters")
        # given
        html_file = io.BytesIO(b'invalid content')
        with self.assertRaises(ValueError):
            lyrics.bestresult(html_file)

    def test_getlyrics(self):
        # given
        with open('nirvana-smells_like_teen_spirit_lyrics_musixmatch.html', 'r', encoding='utf-8') as html_file, \
             open('nirvana-smells_like_teen_spirit.lyrics', 'r', encoding='utf-8') as lyrics_file:
            # then
            self.assertEqual(lyrics.getlyrics(html_file), lyrics_file.read())

if __name__ == "__main__":
    unittest.main()
