#encoding:utf-8
'''
Because i'm lazy, midi helper to find chord recipes

0 C 
1 C#
2 D
3 D#
4 E
5 F
6 F#
7 G
8 G#
9 A
10 A#
11 B
12 C
'''
#assuming 4/4 time
durations = {
	"whole":1,
	"half":1/2,
	"quarter":1/4,
	"eigth":1/8,
	"triple":1/12,
	"sixteenth":1/16,
}

scales = {
	"minor":[0, 2, 3, 5, 7, 8, 10],
	"chromatic": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
	"major":[0, 2, 4, 5, 7, 9, 11],
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
	"fifth": [0, 7, 12],
	"major triad": [0, 4, 7],
	"minor triad": [0, 3, 7],
	"augmented triad": [0, 4, 8],
	"diminished triad": [0, 3, 6],
	"dominant seventh": [0, 4, 7, 10],
	"major seventh": [0, 4, 7, 11],
	"minor seventh": [0, 3, 7, 10],
	"minor major seventh": [0, 3, 7, 11],
	"major ninth" : [0, 4, 7, 11, 14],
	"dominant ninth" : [0, 4, 7, 10, 13],
	"sus2" : [0, 2, 7],
	"sus4" : [0, 5, 7],
	"major add9" : [0, 4, 7, 14],
	"minor add9" : [0, 3, 7, 14],
}

chordSymbols = {
	"fifth": "5",
	"major triad": "",
	"minor triad": "m",
	"augmented triad": "+",
	"diminished triad": 'dim',
	"dominant seventh": "7",
	"major seventh": "M7",
	"minor seventh": "m7",
	"minor major seventh": "mMaj7",
	"major ninth" : "maj9",
	"dominant ninth" : "9",
	"sus2" : "sus2",
	"sus4" : "sus4",
	"major add9" : "add9",
	"minor add9" : "mAdd9",
}


shiftFactors = {
	"G":-5,
	"Ab":-4,
	"G#":-4,
	"A":-3,
	"Bb":-2,
	"A#":-2,
	"B":-1,
	"C":0,
	"C#":1,
	"Db":1,
	"D":2,
	"D#":3,
	"Eb":3,
	"E":4,
	"F":5,
	"F#":6,
	"Gb":6
}

def transpose(target='major', octave=3, key='C'):
	#change l'octave et transpose une gamme ou un accord
	if target not in scales and target not in chords:
		raise ValueError("Unknown chord or scale")
	
	if target in scales:
		target = scales[target]
	else:
		target = chords[target]

	if key in shiftFactors:
		return [(i+12*octave)+shiftFactors[key] for i in target]
	else:
		raise ValueError("Unknown key!")

def changeOctave(chord, amount):
	return [max(0,(i+12*amount)) for i in chord] #max prevents going to negative midi notes