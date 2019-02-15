

from pyo import *
#Tentative de construction de class à partire d'une fonction
#L'Instrument est RCOsc, ligne 45
s = Server(sr=44100, nchnls=2, buffersize=512, duplex=1).boot()

class AMS:
    #Phrases from Ave Maris Stella
  def __init__(self, mel):
        pit1 = midiToHz([62, 69, 71, 67, 69, 71, 74, 72, 71, 69, 67, 69])
        pit2 = midiToHz([69, 69, 62, 64, 67, 65, 64, 62])
        pit3 = midiToHz([65, 64, 67, 69, 69, 62, 64, 65, 62, 60])
        pit4 = midiToHz([64, 67, 64, 65, 64, 62])
    
 # frequence, duree, amplitude, velocity
    # Ave Maris Stella
        self.notes1 = [(pit1[0], 0.5, 0.05), (pit1[1], 0.5, 0.07), (pit1[2], 0.5, 0.05), (pit1[3], 0.5, 0.05), (pit1[4], 0.5, 0.07), (pit1[5], 0.5, 0.05), (pit1[6], 0.5, 0.08), (pit1[7], 0.5, 0.07), (pit1[8], 0.5, 0.06), (pit1[9], 0.5, 0.05), (pit1[10], 0.5, 0.04), (pit1[11], 0.8, 0.05)]
    #Dei Mater Alma
        self.notes2 = [(pit2[0], 0.5, 0.05), (pit2[1], 0.5, 0.05), (pit2[2], 0.5, 0.06), (pit2[3], 0.5, 0.05), (pit2[4], 0.5, 0.05), (pit2[5], 0.5, 0.06), (pit2[6], 0.5, 0.07),(pit2[7], 0.7, 0.06)] 
    #Atque semper Virgo
        self.notes3 = [(pit3[0], 0.5, 0.08), (pit3[1], 0.5, 0.07), (pit3[2], 0.5, 0.05), (pit3[3], 0.5, 0.05), (pit3[4], 0.5, 0.05), (pit3[5], 0.5, 0.09), (pit3[6], 0.5, 0.08), (pit3[7], 0.5, 0.07), (pit3[8], 0.5, 0.06), (pit3[9],0.7, 0.05)] 
    #Felix coeli porta
        self.notes4 = [(pit4[0], 0.5, 0.05), (pit4[1], 0.5, 0.05), (pit4[2], 0.5, 0.05), (pit4[3], 0.5, 0.05), (pit4[4], 0.8, 0.07), (pit4[5], 1.2, 0.06)] 
        
        if mel ==1:
            phrase = self.notes1
        elif mel ==2:
                phrase = self.notes2
        elif mel ==3:
                    phrase = self.notes3
        elif mel ==4:
                    phrase = self.notes4
                        
        return phrase
                
#Partition                
starttime=0
oscs = []
def chant():
        global starttime
        mel = phrase
        for note in mel:
            f = Fader(fadein=0.005, fadeout=0.25, mul=note[2]).play(dur=note[1], delay=starttime)
            o = Harmonizer(RCOsc(freq=note[0], mul=f).out(dur=note[1], delay=starttime))
        oscs.append(o)
    # le depart de la note tout de suite apres la note precedente.
        starttime += note[1]
        return chant()

    #Partition
def joue():
        second = 0
        def timeline():
            global second
            chant()
        second += 1 
        pat = Pattern(timeline, time=1).play()
        return joue



s.gui(locals())


"""
#J'ajoute la classe Instrument Soprano. Comment les mettre ensemble?
#Ça suffit de remplacer ROsc avec InstAlto...en ligne 45?

#!/usr/bin/env python3
# encoding: utf-8
from pyo import *

class InstAlto:

    #Constructeur pour InstAlto
    def __init__(self, freq, feedback, mul):
        self.freq = freq
        self.feedback = feedback
        self.Alto = SineLoop(freq, feedback, mul)
    def sig(self):
        return self.Alto
s.gui(locals())
"""