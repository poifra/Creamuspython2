from pyo import midiToHz
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
	"power": [0, 7, 12],
	"major triad": [0, 4, 7],
	"minor triad": [0, 3, 7],
	"dominant seventh": [0, 4, 7, 10],
	"major seventh": [0, 4, 7, 11],
	"minor seventh": [0, 3, 7, 10],
	"minor major seventh": [0, 3, 7, 11]
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