#!/usr/bin/env python3

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty
from kivy.lang import Builder
from search import Search
from kivymd.uix.list import OneLineAvatarListItem, ImageLeftWidget
import yt_dlp
from kivy.core.audio import SoundLoader
import tempfile
import threading
from time import sleep
import os


class HomeScreen(MDScreen):
    pass

class SettingsScreen(MDScreen):
    pass

class SearchScreen(MDScreen):
    pass

class SpotifyApp(MDApp):
    current_s = StringProperty()
    
    temp_file = tempfile.NamedTemporaryFile(delete=True, suffix=".webm") 
    out_path= temp_file.name
    temp_file.close()
    flag=1
    global sound

    ydl_opts = {
            'quiet': True,
            'verbose': False,
            'outtmpl' : out_path,
            'format': 'bestaudio[ext=webm]/bestaudio/best',
            # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
            'no_warnings': True,
            'cachedir' : False
        }
    ydl = yt_dlp.YoutubeDL(ydl_opts)


    def on_stop(self):
        print("Deleting wav files..")
        os.remove(self.out_path)

    def build(self):
        self.title = "OpenFy"
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file("config.kv")

    def navigate(self, destination):
        self.root.current = destination

    def perform_search(self, query):

        def setSong(link, title):
            psong = threading.Thread(target=self.PlaySong, args=(link,))
            psong.start()
            self.current_s=title

        data = Search.dataParsing(query)
        titles = data[0]
        links = data[1]
        images = data[2]
        results_list = self.root.get_screen("search").ids.search_results
        results_list.clear_widgets()
        for title, image, link in zip(titles, images, links):
            item = OneLineAvatarListItem(text=title)

            image = ImageLeftWidget(source=image)

            item.add_widget(image)

            item.on_release = lambda title=title, link=link: setSong(link, title)
            results_list.add_widget(item)

    def PlaySong(self, link):
        try:
            self.sound.stop()
            os.remove(self.out_path)
        except (IOError,AttributeError) as e:
            print("OS error:", e)

        self.ydl.download([link])
        self.sound = SoundLoader.load(self.out_path)
        if self.sound:
            print("Sound found at %s" % self.sound)
            print("Sound is %.3f seconds" % self.sound.length)
            self.sound.play()

    def play_or_stop(self):
        if self.flag == 1:
            self.sound.stop()
            self.flag=0
            print ("stopping song")
        else:
            self.sound.play()
            self.flag=1
            print ("play song")

if __name__ == '__main__':
    SpotifyApp().run()

