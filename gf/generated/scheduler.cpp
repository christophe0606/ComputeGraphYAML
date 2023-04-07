/*

Generated with CMSIS-DSP Compute Graph Scripts.
The generated code is not covered by CMSIS-DSP license.

The support classes and code is covered by CMSIS-DSP license.

*/


#include "arm_math.h"
#include "custom.h"
#include "GenericNodes.h"
#include "AppNodes.h"
#include "scheduler.h"

#if !defined(CHECKERROR)
#define CHECKERROR       if (cgStaticError < 0) \
       {\
         goto errorHandling;\
       }

#endif

#if !defined(CG_BEFORE_ITERATION)
#define CG_BEFORE_ITERATION
#endif 

#if !defined(CG_AFTER_ITERATION)
#define CG_AFTER_ITERATION
#endif 

#if !defined(CG_BEFORE_SCHEDULE)
#define CG_BEFORE_SCHEDULE
#endif

#if !defined(CG_AFTER_SCHEDULE)
#define CG_AFTER_SCHEDULE
#endif

#if !defined(CG_BEFORE_BUFFER)
#define CG_BEFORE_BUFFER
#endif

#if !defined(CG_BEFORE_FIFO_BUFFERS)
#define CG_BEFORE_FIFO_BUFFERS
#endif

#if !defined(CG_BEFORE_FIFO_INIT)
#define CG_BEFORE_FIFO_INIT
#endif

#if !defined(CG_BEFORE_NODE_INIT)
#define CG_BEFORE_NODE_INIT
#endif

#if !defined(CG_AFTER_INCLUDES)
#define CG_AFTER_INCLUDES
#endif

#if !defined(CG_BEFORE_SCHEDULER_FUNCTION)
#define CG_BEFORE_SCHEDULER_FUNCTION
#endif

#if !defined(CG_BEFORE_NODE_EXECUTION)
#define CG_BEFORE_NODE_EXECUTION
#endif

#if !defined(CG_AFTER_NODE_EXECUTION)
#define CG_AFTER_NODE_EXECUTION
#endif

CG_AFTER_INCLUDES


/*

Description of the scheduling. 

*/
static unsigned int schedule[292]=
{ 
4,5,4,5,4,5,4,5,0,1,4,5,4,5,4,5,4,5,0,1,4,5,4,5,4,5,4,5,0,1,4,5,4,5,4,5,4,5,0,1,
4,5,4,5,4,5,4,5,0,1,4,5,4,5,4,5,4,5,0,1,4,5,4,5,4,5,4,5,0,1,4,5,4,5,4,5,4,5,0,1,
4,5,4,5,4,5,4,5,0,1,4,5,4,5,4,5,4,5,0,1,4,5,4,5,4,5,4,5,0,1,4,5,4,5,4,5,4,5,0,1,
4,5,4,5,4,5,4,5,0,1,4,5,4,5,4,5,4,5,0,1,4,5,4,5,4,5,4,5,0,1,4,5,4,5,4,5,4,5,0,1,
4,5,4,5,4,5,4,5,0,1,4,5,4,5,4,5,4,5,0,1,4,5,4,5,4,5,4,5,0,1,4,5,4,5,4,5,4,5,0,1,
4,5,4,5,4,5,4,5,0,1,4,5,4,5,4,5,4,5,0,1,4,5,4,5,4,5,4,5,0,1,4,5,4,5,4,5,4,5,0,1,
4,5,4,5,4,5,4,5,0,1,4,5,4,5,4,5,4,5,0,1,4,5,4,5,4,5,4,5,0,1,4,5,4,5,4,5,4,5,0,1,
4,5,4,5,4,5,4,5,0,1,2,3,
};

CG_BEFORE_FIFO_BUFFERS
/***********

FIFO buffers

************/
#define FIFOSIZE0 384
#define FIFOSIZE1 768
#define FIFOSIZE2 1024
#define FIFOSIZE3 377
#define FIFOSIZE4 754

#define BUFFERSIZE1 384
CG_BEFORE_BUFFER
q15_t buf1[BUFFERSIZE1]={0};

#define BUFFERSIZE2 768
CG_BEFORE_BUFFER
q15_t buf2[BUFFERSIZE2]={0};

#define BUFFERSIZE3 1024
CG_BEFORE_BUFFER
q15_t buf3[BUFFERSIZE3]={0};

#define BUFFERSIZE4 377
CG_BEFORE_BUFFER
q15_t buf4[BUFFERSIZE4]={0};

#define BUFFERSIZE5 754
CG_BEFORE_BUFFER
q15_t buf5[BUFFERSIZE5]={0};


CG_BEFORE_SCHEDULER_FUNCTION
uint32_t scheduler(int *error)
{
    int cgStaticError=0;
    uint32_t nbSchedule=0;

    CG_BEFORE_FIFO_INIT;
    /*
    Create FIFOs objects
    */
    FIFO<q15_t,FIFOSIZE0,1,0> fifo0(buf1);
    FIFO<q15_t,FIFOSIZE1,0,0> fifo1(buf2);
    FIFO<q15_t,FIFOSIZE2,1,0> fifo2(buf3);
    FIFO<q15_t,FIFOSIZE3,0,0> fifo3(buf4);
    FIFO<q15_t,FIFOSIZE4,1,0> fifo4(buf5);

    CG_BEFORE_NODE_INIT;
    /* 
    Create node objects
    */
    SlidingBuffer<q15_t,1024,256> audioWin(fifo1,fifo2);
    MFCC<q15_t,1024,q15_t,13> mfcc(fifo2,fifo3,mfccConfig);
    SlidingBuffer<q15_t,754,377> mfccWin(fifo3,fifo4);
    NumpySink<q15_t,754> sink(fifo4,dispbuf);
    WavSource<q15_t,384> src(fifo0,True,"test_stereo.wav");
    InterleavedStereoToMono<q15_t,384,q15_t,192> toMono(fifo0,fifo1);

    /* Run several schedule iterations */
    CG_BEFORE_SCHEDULE;
    while(cgStaticError==0)
    {
        /* Run a schedule iteration */
        CG_BEFORE_ITERATION;
        for(unsigned long id=0 ; id < 292; id++)
        {
            CG_BEFORE_NODE_EXECUTION;

            switch(schedule[id])
            {
                case 0:
                {
                   cgStaticError = audioWin.run();
                }
                break;

                case 1:
                {
                   cgStaticError = mfcc.run();
                }
                break;

                case 2:
                {
                   cgStaticError = mfccWin.run();
                }
                break;

                case 3:
                {
                   cgStaticError = sink.run();
                }
                break;

                case 4:
                {
                   cgStaticError = src.run();
                }
                break;

                case 5:
                {
                   cgStaticError = toMono.run();
                }
                break;

                default:
                break;
            }
            CG_AFTER_NODE_EXECUTION;
            CHECKERROR;
        }
       CG_AFTER_ITERATION;
       nbSchedule++;
    }

errorHandling:
    CG_AFTER_SCHEDULE;
    *error=cgStaticError;
    return(nbSchedule);
}
