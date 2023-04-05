from cmsisdsp.cg.scheduler import *
import math
from gl.SpeexNodes import *
from gl.ApplicationNodes import *
from gl.GraphCommon import *

import colorama
from colorama import Fore, Back, Style

colorama.init()

class UnknownBoardConfig(Exception):
    pass


class Empty:
    pass 

args=Empty()

args.stereo = True 
args.avh = False
args.fake = False 
args.ho = False

# Sampling frequency
IO_FREQ = 48000 
SPEEX_FREQ = 44100

WITH_RESAMPLING = SPEEX_FREQ != IO_FREQ

DELAY_MS = 30 

DELAY_SAMPLES = round(DELAY_MS / 1000.0 * IO_FREQ)

#print(Fore.GREEN + "DELAY SAMPLES" + Style.RESET_ALL + (" = %d" % DELAY_SAMPLES))

HOST = args.ho
FAKE = args.fake
AVH = args.avh

#if HOST:
#   print(Fore.GREEN + "Host mode selected")
#else:
#   print(Fore.GREEN + "AVH / MPS3 mode selected")

#if FAKE:
#   print(Fore.GREEN + "Fake audio driver for MPS3")

#if WITH_RESAMPLING:
#   print(Fore.GREEN + "Resampling nodes added")

#if args.stereo:
#    print(Fore.GREEN + "Stereo input / outputs")

#if not HOST and (IO_FREQ != 48000):
#    print("Sampling freq different from 48 kHz not yet supported for MPS3 real HW")
#    exit(1)

# Create the graph configuration and generate
# the C include file containing the configuration
# for use by the C code
# (sampling frequency and packet size are
# generated in this include file)
config=GraphConfig(IO_FREQ, SPEEX_FREQ)



# Create the source node.
# There are 2 version : a version for host reading
# wave files. And a version for board using
# the audio queues.
# For host, we need to provide the path
# to the sound file
def mkSource():
    if HOST:
        source = WavSource("src",sampleType,config.AUDIOPACKET_INPUT_NB_SAMPLES)
        if args.stereo:
            source.addLiteralArg("../sounds/stereo_%dkHz.wav" % fileSampling(IO_FREQ))
        else:
           source.addLiteralArg("../sounds/background_%dkHz.wav" % fileSampling(IO_FREQ))
        return(source)
    else:
        source = Source("src",sampleType,config.AUDIOPACKET_INPUT_NB_SAMPLES)
        source.addVariableArg("queues->inputQueue")
        return(source)
    
    raise UnknownBoardConfig()

# Create the sink node. There are two versions.
# A version for host, writing a .wav file
# and a version for board using the audio queues
def mkSink():
    if HOST:
        sink=WavSink("sink",sampleType,config.AUDIOPACKET_OUTPUT_NB_SAMPLES)
        sink.addLiteralArg("output_%dkHz.wav" % fileSampling(IO_FREQ),IO_FREQ)
        return(sink)
    else:
        sink=Sink("sink",sampleType,config.AUDIOPACKET_OUTPUT_NB_SAMPLES)
        sink.addVariableArg("queues->outputQueue")

        # How many buffer are already pending and to be
        # read by output DMA.
        # So it is the next ID to be computed and pushed
        # by the sink.
        # In case there is more latency generated by
        # the compute graph, this value may need to be
        # increased and the audio_init.c files
        # would need to be modified to push a few
        # buffer in advance.
        sink.addLiteralArg(2)

        return(sink)
    raise UnknownBoardConfig()

# Where to generate the comoute graph scheduler
def schedulerFolder():
    if HOST:
        return("host")
    else:
        return(".")
    raise UnknownBoardConfig()


# Description of the compute graph.
nearEndSource = mkSource()
sink = mkSink()

farEndSource = BackgroundSource("far",sampleType,config.AUDIOPACKET_INPUT_NB_SAMPLES)
mixFar = SeparateStereoToMono("mixFar",sampleType,config.AUDIOPACKET_INPUT_NB_SAMPLES)


mixNear = SeparateStereoToMono("mixNear",sampleType,config.AUDIOPACKET_INPUT_NB_SAMPLES)

echo = EchoModel("echo",sampleType,config.AUDIOPACKET_INPUT_NB_SAMPLES)

if WITH_RESAMPLING:
   downsamplerNear = Resampler("downNear",sampleType,config.AUDIOPACKET_INPUT_NB_SAMPLES,[185,185,185,180])
   downsamplerNear.addVariableArg("desc_480_16")
   
   downsamplerFar = Resampler("downFar",sampleType,config.AUDIOPACKET_INPUT_NB_SAMPLES,[185,185,185,180])
   downsamplerFar.addVariableArg("desc_480_16")

   upsampler = Resampler("up",sampleType,[185,185,185,180],config.AUDIOPACKET_OUTPUT_NB_SAMPLES)
   upsampler.addVariableArg("desc_16_480")


aec = EchoCanceller("aec",sampleType,config.AUDIOPACKET_SPEEX_NB_SAMPLES)
aec.addVariableArg("echoState")
aec.addLiteralArg(SPEEX_FREQ)

denoise = Denoise("denoise",sampleType,config.AUDIOPACKET_SPEEX_NB_SAMPLES)
denoise.addVariableArg("echoState")

noiseReductionLevel = 20
agcEnable = 0
agcLevel = 8000
dereverbEnable = 0
dereverbDecay = 0.0
dereverbLevel = 0.0
denoise.addLiteralArg( SPEEX_FREQ
                      ,noiseReductionLevel
                      ,agcEnable
                      ,agcLevel
                      ,dereverbEnable
                      ,dereverbDecay
                      ,dereverbLevel)

g = Graph()

g.connect(farEndSource.oleft,mixFar.ileft)
g.connect(farEndSource.oright,mixFar.iright)

g.connect(nearEndSource.oleft,mixNear.ileft)
g.connect(nearEndSource.oright,mixNear.iright)

g.connect(mixNear.o,echo.n)
g.connectWithDelay(mixFar.o,echo.f,DELAY_SAMPLES)

if WITH_RESAMPLING:
   g.connect(mixFar.o,downsamplerFar.i)
   g.connect(downsamplerFar.o,aec.r)
   
   g.connect(echo.o,downsamplerNear.i)
   g.connect(downsamplerNear.o,aec.i)
else:
   g.connect(mixFar.o,aec.r)
   g.connect(echo.o,aec.i)

g.connect(aec.o,denoise.i)

#mixer= Mixer2("mix2",sampleType,config.AUDIOPACKET_SPEEX_NB_SAMPLES)
#mixer.addLiteralArg(0.5,0.5)
#g.connect(downsamplerNear.o,mixer.ia)
#g.connect(downsamplerFar.o,mixer.ib)
#g.connect(mixer.o,denoise.i)

if WITH_RESAMPLING:
   g.connect(denoise.o,upsampler.i)
   g.connect(upsampler.o,sink.ileft)
   g.connect(upsampler.o,sink.iright)
else:
   g.connect(denoise.o,sink.ileft)
   g.connect(denoise.o,sink.iright)


the_graph = g