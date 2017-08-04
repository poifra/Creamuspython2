#encoding:utf-8

from Chordbook import transpose, shiftFactors
from random import choice
import MyRandoms

class AudioEngine:
    def __init__(self, chordProgression, key):
        self.chordProgression = chordProgression
        self.size = len(self.chordProgression)*4
        self.counter = 0
        self.validateKey(key)

    def validateKey(self, key):
        '''
        Validates that key given as argument is actually a Key. For the key
        to be valid, It needs to start with either one of A,B,C,D,E,F,G
        and have a # or b after and can be minor eg. F#m

        I might redo this with a regex ¯\_(ツ)_/¯
        '''
        if len(key) == 0:
            raise ValueError("No key specified!")
        if len(key) == 3:
            if key[:1] in shiftFactors.keys() and key[2] == 'm':
                self.mode = 'minor'
                self.key = key[:1]
            else:
                raise ValueError("Invalid key name (got "+key+").")
        elif len(key) == 2:
            if key[0] in shiftFactors.keys() and key[1] == 'm':
                self.mode = 'minor'
                self.key = key[0]
            elif key[0] in shiftFactors.keys() and key[1] in ('#','b'):
                self.mode = 'major'
                self.key = key[0]
            else:
                raise ValueError("Invalid key name (got "+key+").")
        elif len(key) == 1:
            if key in shiftFactors.keys():
                self.mode = 'major'
                self.key = key

class WalkingBass(AudioEngine):
    def __init__(self, chordProgression, key):
        AudioEngine.__init__(self, chordProgression, key)

    def buildWalkingBass(self):
        chordTones = self.chordProgression
        self.bassLine = list()
        if self.mode == 'major':
            scale = transpose(key=self.key, target='minor', octave=3)
        else:
            scale = transpose(key=self.key, target='major', octave=3)

        for i in range(self.size):
            pos = i % 4
            if pos == 0: #first note of bar, play tonic
                self.bassLine.append(chordTones[i%len(chordTones)][0])
            elif pos == 1: #second note of bar, play random scale note that is not a chord tone
                self.bassLine.append(choice(scale))
            elif pos == 2: #third beat, play chord tone
                self.bassLine.append(choice(chordTones[i%len(chordTones)]))
            elif pos == 3: #fourth beat, play approaching tone
                self.bassLine.append(chordTones[(i+1)%len(chordTones)][0]-1)

    def getNextNote(self):
        currentNote = self.bassLine[self.counter % self.size]
        self.counter += 1
        return currentNote

    def getBassline(self):
        return self.bassLine

class Melody(AudioEngine):
    def __init__(self, chordProgression, key):
        AudioEngine.__init__(self, chordProgression, key)

        self.rngInstance = MyRandoms.MyRandoms()
        
    def buildMelody(self, randomFunction, maxSize=0, **kwargs):
        random = [self.rngInstance.call(randomFunction, **kwargs) for _ in range(100)] 
        scale = transpose(target='major',key=self.key, octave=5)
        scaleSize = len(scale)
        randomRange = max(random) + abs(min(random))
        bucketSize = randomRange/scaleSize

        self.snappedScale = []
        for x,d in enumerate(random):
            if maxSize > 0 and x > maxSize:
                break
            i = 1
            while abs(d) > i*bucketSize and i < len(scale):
                i += 1
            matchingNote = scale[i-1]
            self.snappedScale.append(matchingNote)

    def getNextNote(self):
        currentNote = self.snappedScale[self.counter % len(self.snappedScale)]
        self.counter += 1
        return currentNote

    def getMelody(self):
        return self.snappedScale

