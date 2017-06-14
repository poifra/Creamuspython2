from __future__ import division #python2 pls
#encoding:utf-8

'''
Because i'm lazy, midi helper to find chord recipes

0 C 
1 C#/Db
2 D
3 D#/Eb
4 E
5 F
6 F#/Gb
7 G
8 G#/Ab
9 A
10 A#/Bb
11 B
12 C
'''

#assuming 4/4 time, no dotted notes :(
durations = {
    "whole":1,
    "half":1/2,
    "quarter":1/4,
    "eigth":1/8,
    "triple":1/12,
    "sixteenth":1/16,
}

scales = {
    "minor": [0, 2, 3, 5, 7, 8, 10],
    "chromatic": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    "major": [0, 2, 4, 5, 7, 9, 11],
    "blues": [0, 2, 3, 4, 5, 7, 9, 10, 11],
    "diatonic minor": [0, 2, 3, 5, 7, 8, 10],
    "pentatonic": [0, 2, 4, 7, 9],
    "harmonic minor": [0, 2, 3, 5, 7, 8, 11],
    "aeolian": [0, 2, 3, 5, 7, 8, 10],
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "turkish": [0, 1, 3, 5, 7, 10, 11],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "lydian": [0, 2, 4, 6, 7, 9, 10],
    "locrian": [0, 1, 3, 5, 6, 8, 10],
    "indian": [0, 1, 1, 4, 5, 8, 10],
    "phrygian": [0, 1, 3, 5, 7, 8, 10]
}

chords = {
#todo : decent voice leading
    "maj": [0, 4, 7],#major
    "maj7": [0, 4, 7, 11],
    "maj9": [0, 4, 7, 11, 14],
    "maj11": [0, 4, 7, 11, 14, 17],
    "maj13": [0, 4, 7, 11, 14, 17, 21],
    "maj9#11": [0, 4, 7, 11, 14, 18],
    "maj13#11": [0, 4, 7, 11, 14, 18, 21],
    "6": [0, 4, 7, 9],
    "add9": [0, 4, 7, 14],
    "6add9": [0, 4, 7, 9, 14],
    "maj7b5": [0, 4, 6, 11],
    "maj7#5": [0, 4, 8, 11],
    "7": [0, 4, 7, 10],
    "9": [0, 4, 7, 10, 14],
    "11": [0, 4, 7, 10, 14, 17],
    "13": [0, 4, 7, 10, 14, 17, 21],
    "7sus4": [0, 5, 7, 10],
    "7b5": [0, 4, 6, 10],
    "7#5": [0, 4, 8, 10],
    "7b9": [0, 4, 7, 10, 13],
    "7#9": [0, 4, 7, 10, 15],
    "7(b5, b9)": [0, 4, 6, 10, 13],
    "7(b5, #9)": [0, 4, 6, 10, 15],
    "7(#5, b9)": [0, 4, 8, 10, 13],
    "7(#5, #9)": [0, 4, 8, 10, 15],
    "9b5": [0, 4, 6, 10, 14],
    "9#5": [0, 4, 8, 10, 14],
    "13#11": [0, 4, 7, 10, 14, 18, 21],
    "13b9": [0, 4, 7, 10, 13, 17, 21],
    "11b9": [0, 4, 7, 10, 13, 17],
    "aug": [0, 3, 8],
    "dim": [0, 3, 6],
    "dim7": [0, 3, 6, 9],
    "5": [0, 6, 12],
    "sus4": [0, 5, 7],
    "sus2": [0, 2, 7],
    "sus2sus4": [0, 2, 5, 7],
    "-5": [0, 4, 6],
}

#adds all minor chords. Python one-liners FTW
for k, v in chords.items(): 4 in v and chords.update({'m'+k: [3 if i == 1 else v[i] for i, _ in enumerate(v)]}) 

#old version, has a useless condition in it, i kept it because it's beautiful
#for k,v in chords.items():4 in v and 'm'+k not in chords.keys() and chords.update({'m'+k: [3 if i==1 else v[i] for i,_ in enumerate(v)]})

#remove random dimished chord and fix minor triad
del chords['m-5'] 
del chords['mmaj']
chords['m'] = [0,3,7]

shiftFactors = {
    "G": -5,
    "Ab": -4,
    "G#": -4,
    "A": -3,
    "Bb": -2,
    "A#": -2,
    "B": -1,
    "C": 0,
    "C#": 1,
    "Db": 1,
    "D": 2,
    "D#": 3,
    "Eb": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "Gb": 6
}

def transpose(target='', octave=3, key='C', inversion=None):
    #change l'octave et transpose une gamme ou un accord
    if target not in scales and target not in chords:
        raise ValueError("Unknown chord or scale")
    
    if target in scales:
        target = scales[target]
    else:
        target = chords[target]

    if key in shiftFactors:
        notes = [(i+12*octave)+shiftFactors[key] for i in target]
        if inversion:
            if inversion in notes:
                print "chord tone inversion"
                notes.remove(inversion)
                notes = [inversion] + notes
            else:
                print "other inversion"
    else:
        raise ValueError("Unknown key!")

    return notes

def changeOctave(chord, amount):
    return [max(0,(i+12*amount)) for i in chord] #max prevents going to negative midi notes
