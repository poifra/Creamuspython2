from __future__ import division
def snap(random, scale, maxSize = 0):
	"""
	Snaps given random data to a specified MIDI scale
	arguments: 
		random : list of random data
		scale : scale to use, MIDI list of notes
		maxSize : limits number of notes to return

	returns:
		snapped scale, with length maxSize or len(random) if maxSize was not specified
	"""
	scaleSize = len(scale)
	randomRange = max(random) + abs(min(random))
	bucketSize = randomRange/scaleSize
	snappedScale = []
	print bucketSize
	for x,d in enumerate(random):
		if maxSize > 0 and x > maxSize:
			break
		i = 1
		while abs(d) > i*bucketSize and i < len(scale):
			i += 1
		matchingNote = scale[i-1]
		snappedScale.append(matchingNote)
	return snappedScale
