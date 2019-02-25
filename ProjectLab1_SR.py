
from pyo import *
s = Server(sr=44100, nchnls=2, buffersize=512, duplex=1).boot()

class InstSoprano:
    #Constructeur pour InstSoprano
    def __init__(self, feedback=0.08):
        self.feedback = feedback
        self.envelope = Fader(fadein=0.005, fadeout=0.05)
        self.soprano = SineLoop(100, feedback, mul=self.envelope)

    # Cette fonction est appelee pour jouer une note.
    def play(self, freq, dur, amp):
        self.soprano.freq = freq
        self.envelope.dur = dur
        self.envelope.mul = amp
        self.envelope.play()
    
    def sig(self):
        return self.soprano

class SR:
    #Phrases from Salve Regina
    def __init__(self):
    
        pit1 = midiToHz([60, 64, 67, 69, 67])
        pit2 = midiToHz([67, 69, 71, 72, 67])
        pit3 = midiToHz([72, 67, 69, 65, 62, 64])
        pit4 = midiToHz([67, 69, 71, 72])
        pit5 = midiToHz([67, 69, 72, 71, 69, 67])
        pit6 = midiToHz([72, 67, 69, 65, 62])
        pit7 = midiToHz([64, 60, 65, 64, 64, 62, 60])

# frequence, duree, amplitude
    #Salve Regina 2 fois
        self.notes1 = [(pit1[0], 0.5, 0.05), (pit1[1], 0.5, 0.08), (pit1[2], 0.5, 0.10), (pit1[3], 1.0, 0.15), (pit1[4], 1.5, 0.13)]
    #ad te clamamus
        self.notes2 = [(pit2[0], 0.5, 0.08), (pit2[1], 0.5, 0.10), (pit2[2], 0.5, 0.12), (pit2[3], 1.0, 0.17), (pit2[4], 1.5, 0.15)] 
    #ad te suspiramus
        self.notes3 = [(pit3[0], 0.5, 0.08), (pit3[1], 0.5, 0.07), (pit3[2], 1.5, 0.20), (pit3[3], 0.5, 0.15), (pit3[4], 0.7, 0.13), (pit3[5], 1.5, 0.15)] 
    #Eia ergo
        self.notes4 = [(pit4[0], 0.5, 0.08), (pit4[1], 0.5, 0.10), (pit4[2], 0.5, 0.15), (pit4[3], 1.5, 0.20)]
    #advocata nostra 
        self.notes5 = [(pit5[0], 0.5, 0.08), (pit5[1], 0.5, 0.08), (pit5[2], 0.5, 0.09), (pit5[3], 0.5, 0.08), (pit5[4], 0.7, 0.07), (pit5[5], 1.0, 0.06)]
    #vita dulcedo
        self.notes6 = [(pit6[0], 0.5, 0.08), (pit6[1], 0.5, 0.06), (pit6[2], 0.5, 0.07), (pit6[3], 0.5, 0.06), (pit6[4], 1.0, 0.05)]
    #et spes nostra salve
        self.notes7 = [(pit7[0], 1.5, 0.08), (pit7[1], 1.5, 0.06), (pit7[2], 2.0, 0.15), (pit7[3], 1.0, 0.10), (pit7[4], 1.0, 0.10), (pit7[5], 1.5, 0.08), (pit7[6], 2.0, 0.05)] 
        

    def chooseMelody(self, mel):
        if mel ==1:
            phrase = self.notes1
        elif mel ==2:
            phrase = self.notes2
        elif mel ==3:
            phrase = self.notes3
        elif mel ==4:
            phrase = self.notes4
        elif mel ==5:
            phrase = self.notes5
        elif mel ==6:
            phrase = self.notes6
        elif mel ==7:
            phrase = self.notes7
                        
        return phrase

# Partition pour la voix de soprano
class PartitionSoprano:
    def __init__(self):
        # melodies
        self.sr =SR()
        # instruments
        self.soprano = InstSoprano()

        # Le numero de la melodie
        self.melody = 1
        # Le compte des notes dans la melodie
        self.count = 0

        print("Playing soprano melody # %d" % self.melody)

        # La liste de notes a jouer
        self.notes = self.sr.chooseMelody(self.melody)

        # self.newNote est appelee a chaque nouvelle note.
        self.player = Pattern(self.newNote, time=0.5)

    def newNote(self):
        # On recupere la note dans la liste et on active une note a l'instrument alto.
        note = self.notes[self.count]
        freq = note[0]
        dur = note[1]
        amp = note[2]
        self.soprano.play(freq, dur, amp)
        # On ajuste le "time" du Pattern pour suivre la sequence rythmique des durees
        self.player.time = dur

        # On incremente le compte
        self.count += 1
        # Si au bout de la liste...
        if self.count == len(self.notes):
            # On remet le compte a zero
            self.count = 0
            # On incremente le compte des melodies
            self.melody += 1
            # Si au bout du compte des melodies...
            if self.melody > 7:
                # On revient a 1.
                self.melody = 1
            print("Playing soprano melody # %d" % self.melody)

            # On met a jour self.notes avec la nouvelle melodie
            self.notes = self.sr.chooseMelody(self.melody)

    # Methode pour activer la partition de la voix soprano.
    def play(self):
        self.player.play()

    # Methode pour recuperer le son de la voix soprano.
    def getSound(self):
        return self.soprano.sig()

# Classe pour la partition globale (toutes les voix)
class Partition:
    def __init__(self):
        # Voix soprano
        self.pSoprano = PartitionSoprano()
        # Activation de la voix alto
        self.pSoprano.play()

    # La methode getSound() devrait faire la somme des signaux de toutes les voix
    def getSound(self):
        return self.pSoprano.getSound()

# On cree la partition globale
partition = Partition()

# On passe le son dans une petite reverberation!
reverb = STRev(partition.getSound(), inpos=0.50, revtime=1, cutoff=5000, bal=0.25).out()

s.gui(locals())
