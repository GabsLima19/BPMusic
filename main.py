import os
import time
import threading
import subprocess 
import librosa
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from pytube import YouTube

from kivy.clock import Clock
from kivy.properties import NumericProperty

Window.size = (320, 600)

class GerenciarTelas(ScreenManager):
    pass

class ContentNavigationDrawer(MDBoxLayout):
    pass

class TelaCarregamento(Screen):

    #verificar se na pasta possui um audio.wav, se tiver, apaga.
    def verificaraudio(self):
        if os.path.exists('audio.wav'):
            os.remove('audio.wav') 
    pass

class TelaInicial(Screen):

    #verificar se na pasta possui um audio.wav, se tiver, apaga.
    def verificaraudio(self):
        if os.path.exists('audio.wav'):
            os.remove('audio.wav')
        else:
            pass 

    #baixa audio do youtube e converte para wav
    def importarvideo (self):
    
        linkvideo = str(self.ids.link.text)
        yt = YouTube(linkvideo)

        titulo = yt.title
        self.ids.titulo_video.text = titulo
        
        video = yt.streams.filter(only_audio=True)[0]
        out_file = video.download()
        
        os.path.splitext(out_file)
        new_file = 'audio.mp3'
        os.rename(out_file, new_file)

        subprocess.call(['ffmpeg', '-i', 'audio.mp3', 'audio.wav'])

        os.remove('audio.mp3')

    #analisa o bpm do audio wav
    def analisarbpm(self):
        if os.path.exists('audio.wav'):
            y, sr = librosa.load('audio.wav')
            tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
            
            self.ids.selection_path.title = "{:.0f}".format(tempo) 

    #reprodução música
    #def play_music(self):
        #self.wav = SoundLoader.load('audio.wav')
        #self.wav.play()

    #playermusic
    length = NumericProperty(0.0)
    progress = NumericProperty(0.0)

    def play_music(self):
        self.sound = SoundLoader.load("audio.wav")
        if self.sound:
            self.length = self.sound.length
            self.sound.play()
            # Now schedule and start updating after every 1.0 sec.
            # Use 'Clock.create_trigger' for more control.
            self.prog_ev = Clock.schedule_interval(self.update_progress, 1.0)

    def update_progress(self, dt):
        if self.progress < self.length:
            self.progress += 1 # Update value.
        else: # End case.
            self.progress = 0 # Reset value.
            self.prog_ev.cancel() # Stop updating.

    def stop_music(self):
        if os.path.exists('audio.wav'):
            self.wav.stop()
    
    #descarrega audio da memoria
    def des_audio(self): 
        self.sound.unload()
        self.progress = 0
        self.prog_ev.cancel()

    #apagar o audio na pasta
    def apagaraudio(self):
        if os.path.exists('audio.wav'):
            os.remove('audio.wav')  

    pass

class TelaMetronomo(Screen):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.pause = True

    def play_metronome(self, *args):
        if self.pause:
            self.pause = False
            thread = threading.Thread(target=self._play, daemon=True)
            thread.start()

    def close(self, *args):
        self.pause = False

    def _play(self):
        bpm = int(self.ids.bpm.text)
        wav = SoundLoader.load('Woodblock.wav')
        sleep = 60 / bpm

        while not self.pause:
            wav.play()
            time.sleep(sleep)

    def stop_metronome(self):
        if not self.pause:
            self.pause = True

    #apagar o audio na pasta
    def apagaraudio(self):
        if os.path.exists('audio.wav'):
            os.remove('audio.wav')   
       
    pass

class TelaConfig(Screen):
    pass

class TelaAjuda(Screen):
    pass

class TelaSobre(Screen):
    pass


class BPMusic(MDApp):
    def build(self):
        return Builder.load_file("main.kv")


BPMusic().run()









