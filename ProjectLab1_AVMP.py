
from pyo import *
s = Server(sr=44100, nchnls=2, buffersize=512, duplex=1).boot()

class InstCloche:
    #Constructeur pour InstCloche
    def __init__(self, feedback=0.08):
        self.feedback = feedback
        self.envelope = Fader(fadein=0.005, fadeout=0.05)
        self.cloche = SineLoop(100, feedback, mul=self.envelope)

    # Cette fonction est appelee pour jouer une note.
    def play(self, freq, dur, amp):
        self.cloche.freq = freq
        self.envelope.dur = dur
        self.envelope.mul = amp
        self.envelope.play()
    
    def sig(self):
        return self.cloche

class AVMP:
    #Phrases de l'Ave Maria Procidana
    def __init__(self):
    
        pit1 = midiToHz([67, 67, 67, 67, 69, 69, 67, 69, 69, 67, 71, 69, 67, 65, 69, 69, 69, 69, 69, 69, 67, 67, 
                            67, 67, 67, 65, 64])
        pit2 = midiToHz([67, 67, 69, 69, 67, 67, 67, 69, 69, 67, 69, 71, 69, 67, 65, 69, 
                            69, 69, 69, 69, 69, 69, 67, 71, 69, 67, 67, 65, 64])

# frequence, duree, amplitude
    #Madonna delle Grazie...
        self.notes1 = [(pit1[0], 0.6, 0.04), (pit1[1], 0.6, 0.08), (pit1[2], 0.6, 0.05), (pit1[3], 0.6, 0.05), (pit1[4], 0.6, 0.05), 
            (pit1[5], 1.2, 0.08), (pit1[6], 0.6, 0.05), (pit1[7], 0.6, 0.05,), (pit1[8], 0.6, 0.08), (pit1[9], 0.6, 0.05),
            (pit1[10], 0.6, 0.05), (pit1[11], 0.6, 0.05), (pit1[12], 1.2, 0.08), (pit1[13], 0.6, 0.05,), (pit1[14], 0.6, 0.05),
            (pit1[15], 0.6, 0.08), (pit1[16], 0.6, 0.05), (pit1[17], 0.6, 0.05), (pit1[18], 0.6, 0.05,), (pit1[19], 1.2, 0.08),
            (pit1[20], 0.6, 0.05), (pit1[21], 0.6, 0.05), (pit1[22], 0.6, 0.08), (pit1[23], 0.6, 0.05,), (pit1[24], 0.6, 0.05),
            (pit1[25], 0.6, 0.05), (pit1[26], 2.4, 0.08)]
    #Santa Maria
        self.notes2 = [(pit2[0], 0.6, 0.10), (pit2[1], 0.4, 0.10), (pit2[2], 0.2, 0.05), (pit2[3], 0.4, 0.10), (pit2[4], 0.2, 0.05), 
            (pit2[5], 0.2, 0.10), (pit2[6], 0.2, 0.05), (pit2[7], 0.2, 0.05), (pit2[8], 0.2, 0.10), (pit2[9],0.2, 0.05), 
            (pit2[10], 0.2, 0.05), (pit2[11], 0.4, 0.10), (pit2[12], 0.2, 0.05), (pit2[13], 0.6, 0.10), (pit2[14], 0.4, 0.10), (pit2[15], 0.2 ,0.05), 
            (pit2[16], 0.2, 0.10), (pit2[17], 0.2, 0.05), (pit2[18], 0.2, 0.05), (pit2[19], 0.4, 0.10), (pit2[20],0.2 ,0.05), (pit2[21], 0.4, 0.10), 
            (pit2[22], 0.2, 0.05), (pit2[23], 0.4, 0.10), (pit2[24], 0.2, 0.05), (pit2[25], 0.6, 0.10), (pit2[26], 0.4, 0.10), (pit2[27],  0.2, 0.05), 
            (pit2[28], 0.6, 0.10)]

    def chooseMelody(self, mel):
        if mel ==1:
            phrase = self.notes1
        elif mel ==2:
            phrase = self.notes2
        
        return phrase

# Partition pour cloche
class PartitionCloche:
    def __init__(self):
        # melodies
        self.avmp =AVMP()
        # instruments
        self.cloche = InstCloche()

        # Le numero de la melodie
        self.melody = 1
        # Le compte des notes dans la melodie
        self.count = 0

        print("Playing cloche melody # %d" % self.melody)

        # La liste de notes a jouer
        self.notes = self.avmp.chooseMelody(self.melody)

        # self.newNote est appelee a chaque nouvelle note.
        self.player = Pattern(self.newNote, time=0.5)

    def newNote(self):
        # On recupere la note dans la liste et on active une note a l'instrument alto.
        note = self.notes[self.count]
        freq = note[0]
        dur = note[1]
        amp = note[2]
        self.cloche.play(freq, dur, amp)
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
            if self.melody > 2:
                # On revient a 1.
                self.melody = 1
            print("Playing cloche melody # %d" % self.melody)

            # On met a jour self.notes avec la nouvelle melodie
            self.notes = self.avmp.chooseMelody(self.melody)

    # Methode pour activer la partition de cloche.
    def play(self):
        self.player.play()

    # Methode pour recuperer le son de cloche.
    def getSound(self):
        return self.cloche.sig()




# Classe pour la partition globale (toutes les voix)
class Partition:
    def __init__(self):
        # Cloche
        self.pCloche = PartitionCloche()
        # Activation de la voix alto
        self.pCloche.play()

    # La methode getSound() devrait faire la somme des signaux de toutes les voix
    def getSound(self):
        return self.pCloche.getSound()

# On cree la partition globale
partition = Partition()

# On passe le son dans une petite reverberation!
reverb = STRev(partition.getSound(), inpos=0.50, revtime=1, cutoff=5000, bal=0.25).out()

s.gui(locals())
