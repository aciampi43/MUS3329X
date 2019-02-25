
from pyo import *
s = Server(sr=44100, nchnls=2, buffersize=512, duplex=1).boot()

class InstAlto:
    #Constructeur pour InstAlto
    def __init__(self, feedback=0.08):
        self.feedback = feedback
        self.envelope = Fader(fadein=0.005, fadeout=0.05)
        self.alto = SineLoop(100, feedback, mul=self.envelope)

    # Cette fonction est appelee pour jouer une note.
    def play(self, freq, dur, amp):
        self.alto.freq = freq
        self.envelope.dur = dur
        self.envelope.mul = amp
        self.envelope.play()
    
    def sig(self):
        return self.alto

class AMS:
    #Phrases from Ave Maris Stella
    def __init__(self):
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
       
    def chooseMelody(self, mel):
        if mel ==1:
            phrase = self.notes1
        elif mel ==2:
            phrase = self.notes2
        elif mel ==3:
            phrase = self.notes3
        elif mel ==4:
            phrase = self.notes4
                        
        return phrase

# Partition pour la voix d'alto
class PartitionAlto:
    def __init__(self):
        # melodies
        self.ams = AMS()
        # instruments
        self.alto = InstAlto()

        # Le numero de la melodie
        self.melody = 1
        # Le compte des notes dans la melodie
        self.count = 0

        print("Playing alto melody # %d" % self.melody)

        # La liste de notes a jouer
        self.notes = self.ams.chooseMelody(self.melody)

        # self.newNote est appelee a chaque nouvelle note.
        self.player = Pattern(self.newNote, time=0.5)

    def newNote(self):
        # On recupere la note dans la liste et on active une note a l'instrument alto.
        note = self.notes[self.count]
        freq = note[0]
        dur = note[1]
        amp = note[2]
        self.alto.play(freq, dur, amp)
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
            if self.melody > 4:
                # On revient a 1.
                self.melody = 1
            print("Playing alto melody # %d" % self.melody)

            # On met a jour self.notes avec la nouvelle melodie
            self.notes = self.ams.chooseMelody(self.melody)

    # Methode pour activer la partition de la voix alto.
    def play(self):
        self.player.play()

    # Methode pour recuperer le son de la voix alto.
    def getSound(self):
        return self.alto.sig()

# Classe pour la partition globale (toutes les voix)
class Partition:
    def __init__(self):
        # Voix alto
        self.pAlto = PartitionAlto()
        # Activation de la voix alto
        self.pAlto.play()

    # La methode getSound() devrait faire la somme des signaux de toutes les voix
    def getSound(self):
        return self.pAlto.getSound()

# On cree la partition globale
partition = Partition()

# On passe le son dans une petite reverberation!
reverb = STRev(partition.getSound(), inpos=0.50, revtime=1, cutoff=5000, bal=0.25).out()

s.gui(locals())
