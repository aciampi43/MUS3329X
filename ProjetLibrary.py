
"""
#Classes du Projet#
#Sauf PArtition globale#

"""




from pyo import *
s = Server(sr=44100, nchnls=2, buffersize=512, duplex=1).boot()
"""
_________________________________________________________________
##Classes pour Ave MAris STella: InstAlto, AMS, PartitionAlto ##
_________________________________________________________________
"""
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



"""
__________________________________________________________________
##Classes pour Salve Regina: InstSoprano, SR, PartitionSoprano ##
___________________________________________________________________
"""

#Chant d'extrait de la Salve Regina pour soprano voice
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
        
#Choice of phrase among the 7 of the Salve Regina
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


"""
______________________________________________________________________
##Classes pour Ave Maria Procidana: InstCloche, AVMP, PartitionAVMP ##
______________________________________________________________________
"""

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



"""
______________________________________________________________________
##Classes pour mantra OmTare: InstChor, OmTare, PartitionChor ##
______________________________________________________________________
"""


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

""""
___________________
Fin pour le moment
___________________
"""
