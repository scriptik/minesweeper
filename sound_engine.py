import pygame
import data

if pygame.mixer: pygame.mixer.init()

class dummysound:
    def play(self): pass

class SoundPlayer:
    def __init__(self, sounds):
        self.sounds = {}
        for s in sounds:
            self.load(*s)

    def play(self,sound):
        self.sounds[sound].play()

    def load(self,key,filename):
        self.sounds[key] = self.load_sound(filename)

    def load_sound(self,filename):
        if not pygame.mixer: return dummysound()
        filepath = data.filepath("sfx",filename)
        if filepath:
            sound = pygame.mixer.Sound(filepath)
            return sound
        else:
            return dummysound()

class MusicPlayer:
    def __init__(self, filename=None):
        if filename is not None:
            pygame.mixer.music.load(data.filepath(".",filename))

    def load(self, filename):
        pygame.mixer.music.load(data.filepath(".",filename))

    def play(self):
        pygame.mixer.music.play(-1)

    def once(self):
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()
