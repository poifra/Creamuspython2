#encoding: utf-8
from __future__ import division
from pyo import *

class BaseSynth:
    def __init__(self, sequence, amp=1, pan=0.5):
        self.sequence = sequence
        self.trig = self.sequence.trigger
        self.dur = self.sequence.time
        self.freq = self.sequence.signal
        self.amp = Sig(amp)
        self.master_amp = Port(self.amp, init=amp, risetime=0, falltime=0)
        self.pan = Sig(pan)
        self.master_pan = Port(self.pan, init=pan, risetime=0, falltime=0)

    def out(self):
        self.stream = self.last_audio_object.out()

    def get_out(self):
        return self.last_audio_object

    def set_amp(self, value, time):
        self.master_amp.setRiseTime(time)
        self.master_amp.setFallTime(time)
        self.amp.setValue(value)
        return self

    def set_pan(self, value, time):
        self.master_pan.setRiseTime(time)
        self.master_pan.setFallTime(time)
        self.pan.setValue(value)
        return self 

    def set_sequence(self, sequence):
        self.sequence = sequence
        self.trig = self.sequence.trigger
        self.dur = self.sequence.time
        self.freq = self.sequence.signal

    def set_notes(self, notes, tempo=96):
        self.sequence.set_notes(notes)

class ClassicSynth(BaseSynth):
    def __init__(self, sequence, amp=1, pan=0.5):
        BaseSynth.__init__(self, sequence, amp, pan)
        self.env = CosTable([(0,0.0000),(353,1.0000),(4166,0.6528),(8000,0.0000)])
        self.env_reader = TrigEnv(self.trig, self.env, dur=Max(self.dur, comp=0.3125))
        self.sine_freqs = []
        for i in range(-1,1):
            self.sine_freqs.extend([self.freq*(1+0.001*i), self.freq*2*(1+0.002*i), self.freq*3*(1+0.002*i),self.freq*5*(1+0.002*i)]) 
            
        self.osc = Sine(freq=self.sine_freqs, mul=[self.env_reader, self.env_reader*0.2, self.env_reader*0.2, self.env_reader*0.1]*3)
         
        self.trans_env = CosTable([(0,0.0000),(123,0.0777),(812,0.0570),(2083,0.0052),(8000,0.0000)])
        self.trans_env_reader = TrigEnv(self.trig, self.trans_env, dur=0.25)
        self.trans = Noise(mul=self.trans_env_reader)
        self.trans_filter = Biquad(self.trans, freq=1690)
        self.trans_resonator = Biquad(self.trans_filter, q=30, freq=self.freq*4)
        self.panner = Pan((self.trans_resonator+self.osc).mix(0), mul=(0.5)*self.master_amp, pan=self.master_pan)
        self.last_audio_object = self.panner

    def set_notes(self, notes, tempo=96):
        BaseSynth.set_notes(self,notes)
        self.trans_env_reader.input=self.trig
        self.env_reader.input=self.trig
        sine_freqs = []
        sine_freqs.extend([self.freq*(1+0.001*i), self.freq*2*(1+0.002*i), self.freq*3*(1+0.002*i),self.freq*5*(1+0.002*i)])
        
        self.osc.freq = sine_freqs
        self.trans_resonator.freq = self.freq*4
        self.env_reader.dur = Max(self.dur, comp=0.3125)

class PianoSynth(BaseSynth): 
    #Not very strong approximation but it works
    def __init__(self, sequence, amp = 1, pan = 0.5):
        BaseSynth.__init__(self, sequence, amp, pan)
        self.env = ExpTable(list=[(0,0),(20,1),(8191,0)], exp=2)
        self.env_reader = TrigEnv(self.trig, self.env, dur=Max(self.dur, comp=0.3125), interp=1)
        self.f = SumOsc(freq=self.freq, ratio=1.01, index=.7, mul=self.env_reader)
        self.chorus = Chorus(self.f, depth=.5, feedback=0, bal=.25, mul=1)
        self.rev = Freeverb(self.chorus, size=.4, damp=.9, bal=.83, mul=1)
        self.ret = Mix(self.chorus+self.rev,2)
        self.panner  = Pan(self.ret, mul=0.1*self.master_amp, pan=self.master_pan)
        self.last_audio_object = self.panner

    def set_notes(self, notes, tempo=96):
        BaseSynth.set_notes(self,notes)
        self.ex.input=self.trig
        self.f.freq = MToF(self.freq)

class ChorusSynth(BaseSynth):
    #Work in progress
    def __init__(self, sequence, amp = 1, pan = 0.5):
        self.SIZE = 5
        BaseSynth.__init__(self, sequence, amp, pan)
        self.vibrato = Sine(freq=1, mul=0.5)
        #self.sig = SineLoop(freq=[self.freq*(random.uniform(0.990,1.01)) for _ in range(self.SIZE)],feedback=0.1,mul=1.0/(5*self.SIZE)-self.vibrato)
        self.sig = SineLoop(freq=self.freq)
        self.chorus = Chorus(self.sig)
        self.rev = Freeverb(self.chorus)
        self.panner = Pan(self.rev, mul=0.5*self.master_amp, pan=self.master_pan)
        self.last_audio_object = self.panner

    def set_notes(self, notes, tempo = 96):
        BaseSynth.set_notes(self,notes)
        self.sig.freq = [self.freq*(random.uniform(0.990,1.01)) for _ in range(self.SIZE)]