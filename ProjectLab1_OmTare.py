
from pyo import *
s = Server(sr=44100, nchnls=2, buffersize=512, duplex=1).boot()

class InstChor:
    #Constructeur pour InstCloche
    def __init__(self, feedback=0.08):
        self.feedback = feedback
        self.envelope = Fader(fadein=0.005, fadeout=0.05)
        self.chor = SineLoop(100, feedback, mul=self.envelope)

    # Cette fonction est appelee pour jouer une note.
    def play(self, freq, dur, amp):
        self.chor.freq = freq
        self.envelope.dur = dur
        self.envelope.mul = amp
        self.envelope.play()
    
    def sig(self):
        return self.chor

class OmTare:
    #Mantra PmTare
    def __init__(self):
        pit1 = midiToHz([36, 43, 43, 43, 43, 43, 47, 43, 43, 43, 36])


# frequence, duree, amplitude

        self.notes1 = [(pit1[0], 0.5, 0.04), (pit1[1], 0.5, 0.08), (pit1[2], 0.5, 0.05), (pit1[3], 0.5, 0.05), (pit1[4], 1.0, 0.08), 
            (pit1[5], 0.5, 0.05), (pit1[6], 0.5, 0.08), (pit1[7], 0.5, 0.05,), (pit1[8], 0.5, 0.08), (pit1[9], 0.5, 0.08),
            (pit1[10], 0.6, 0.05)]
        
        self.notes2 = [(pit1[0], 0.5, 0.04), (pit1[1], 0.5, 0.08), (pit1[2], 0.5, 0.05), (pit1[3], 0.5, 0.05), (pit1[4], 1.0, 0.08), 
            (pit1[5], 0.5, 0.05), (pit1[6], 0.5, 0.08), (pit1[7], 0.5, 0.05,), (pit1[8], 0.5, 0.08), (pit1[9], 0.5, 0.08),
            (pit1[10], 0.6, 0.05)]    

    def chooseMelody(self, mel):
        if mel ==1:
            phrase = self.notes1
        elif mel ==2:
            phrase = self.notes2
        
        return phrase

# Partition pour chor
class PartitionChor:
    def __init__(self):
        # melodies
        self.omtare =OmTare()
        # instruments
        self.chor = InstChor()

        # Le numero de la melodie
        self.melody = 1
        # Le compte des notes dans la melodie
        self.count = 0

        print("Playing chor melody # %d" % self.melody)

        # La liste de notes a jouer
        self.notes = self.omtare.chooseMelody(self.melody)


        # self.newNote est appelee a chaque nouvelle note.
        self.player = Pattern(self.newNote, time=0.5)

    def newNote(self):
        # On recupere la note dans la liste et on active une note a l'instrument alto.
        note = self.notes[self.count]
        freq = note[0]
        dur = note[1]
        amp = note[2]
        self.chor.play(freq, dur, amp)
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
            print("Playing chor melody # %d" % self.melody)

            # On met a jour self.notes avec la nouvelle melodie
            self.notes = self.omtare.chooseMelody(self.melody)

    # Methode pour activer la partition de cloche.
    def play(self):
        self.player.play()


    # Methode pour recuperer le son de cloche.
    def getSound(self):
        return self.chor.sig()



# Classe pour la partition globale (toutes les voix)
class Partition:
    def __init__(self):
        # Chor
        self.pChor = PartitionChor()
        # Activation de la voix alto
        self.pChor.play()

    # La methode getSound() devrait faire la somme des signaux de toutes les voix
    def getSound(self):
        return self.pChor.getSound()

# On cree la partition globale
partition = Partition()

# On passe le son dans une petite reverberation!
reverb = STRev(partition.getSound(), inpos=0.50, revtime=1, cutoff=5000, bal=0.25).out()



s.gui(locals())
