import numpy as np 

from cmsisdsp.cg.scheduler import *


from sharedconfig import *



q15Type = CType(Q15)

### The feature computed by the graph is one second of MFCCs.
### So the nbMFCCOutputs is computed from this and with the additional
### assumption that it must be even.
### Because the MFCC slising window is sliding by half a second
### each time (half number of MFCCs)
src=WavSource("src",NBCHANNELS*AUDIO_INTERRUPT_LENGTH)
src.addLiteralArg(True)
src.addLiteralArg("test_stereo.wav")

toMono=InterleavedStereoToMono("toMono",q15Type,AUDIO_INTERRUPT_LENGTH)

slidingAudio=SlidingBuffer("audioWin",q15Type,FFTSize,AudioOverlap)
slidingMFCC=SlidingBuffer("mfccWin",q15Type,numOfDctOutputs*nbMFCCOutputs,numOfDctOutputs*nbMFCCOutputs>>1)

mfcc=MFCC("mfcc",q15Type,FFTSize,numOfDctOutputs)
mfcc.addVariableArg("mfccConfig")

sink=NumpySink("sink",q15Type,nbMFCCOutputs * numOfDctOutputs)
sink.addVariableArg("dispbuf")

g = Graph()

g.connect(src.o, toMono.i)

g.connect(toMono.o, slidingAudio.i)

g.connect(slidingAudio.o, mfcc.i)

g.connect(mfcc.o,slidingMFCC.i)
g.connect(slidingMFCC.o,sink.i)

the_graph = g

conf=Configuration()
conf.debugLimit=40