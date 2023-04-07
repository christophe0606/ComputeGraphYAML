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
static unsigned int schedule[46]=
{ 
11,9,6,3,11,9,11,7,8,4,2,6,3,9,11,7,8,4,2,6,3,9,7,8,4,2,6,3,7,8,4,2,0,1,12,5,10,12,5,10,
12,5,10,12,5,10,
};

CG_BEFORE_FIFO_BUFFERS
/***********

FIFO buffers

************/
#define FIFOSIZE0 800
#define FIFOSIZE1 800
#define FIFOSIZE2 800
#define FIFOSIZE3 800
#define FIFOSIZE4 800
#define FIFOSIZE5 735
#define FIFOSIZE6 800
#define FIFOSIZE7 735
#define FIFOSIZE8 735
#define FIFOSIZE9 735
#define FIFOSIZE10 800
#define FIFOSIZE11 1440
#define FIFOSIZE12 800
#define FIFOSIZE13 800
#define FIFOSIZE14 800
#define FIFOSIZE15 800

#define BUFFERSIZE1 800
CG_BEFORE_BUFFER
int16_t buf1[BUFFERSIZE1]={0};

#define BUFFERSIZE2 800
CG_BEFORE_BUFFER
int16_t buf2[BUFFERSIZE2]={0};

#define BUFFERSIZE3 800
CG_BEFORE_BUFFER
int16_t buf3[BUFFERSIZE3]={0};

#define BUFFERSIZE4 800
CG_BEFORE_BUFFER
int16_t buf4[BUFFERSIZE4]={0};

#define BUFFERSIZE5 800
CG_BEFORE_BUFFER
int16_t buf5[BUFFERSIZE5]={0};

#define BUFFERSIZE6 735
CG_BEFORE_BUFFER
int16_t buf6[BUFFERSIZE6]={0};

#define BUFFERSIZE7 800
CG_BEFORE_BUFFER
int16_t buf7[BUFFERSIZE7]={0};

#define BUFFERSIZE8 735
CG_BEFORE_BUFFER
int16_t buf8[BUFFERSIZE8]={0};

#define BUFFERSIZE9 735
CG_BEFORE_BUFFER
int16_t buf9[BUFFERSIZE9]={0};

#define BUFFERSIZE10 735
CG_BEFORE_BUFFER
int16_t buf10[BUFFERSIZE10]={0};

#define BUFFERSIZE11 800
CG_BEFORE_BUFFER
int16_t buf11[BUFFERSIZE11]={0};

#define BUFFERSIZE12 1440
CG_BEFORE_BUFFER
int16_t buf12[BUFFERSIZE12]={0};

#define BUFFERSIZE13 800
CG_BEFORE_BUFFER
int16_t buf13[BUFFERSIZE13]={0};

#define BUFFERSIZE14 800
CG_BEFORE_BUFFER
int16_t buf14[BUFFERSIZE14]={0};

#define BUFFERSIZE15 800
CG_BEFORE_BUFFER
int16_t buf15[BUFFERSIZE15]={0};

#define BUFFERSIZE16 800
CG_BEFORE_BUFFER
int16_t buf16[BUFFERSIZE16]={0};


CG_BEFORE_SCHEDULER_FUNCTION
uint32_t scheduler(int *error)
{
    int cgStaticError=0;
    uint32_t nbSchedule=0;

    CG_BEFORE_FIFO_INIT;
    /*
    Create FIFOs objects
    */
    FIFO<int16_t,FIFOSIZE0,1,0> fifo0(buf1);
    FIFO<int16_t,FIFOSIZE1,1,0> fifo1(buf2);
    FIFO<int16_t,FIFOSIZE2,1,0> fifo2(buf3);
    FIFO<int16_t,FIFOSIZE3,1,0> fifo3(buf4);
    FIFO<int16_t,FIFOSIZE4,1,0> fifo4(buf5);
    FIFO<int16_t,FIFOSIZE5,0,0> fifo5(buf6);
    FIFO<int16_t,FIFOSIZE6,1,0> fifo6(buf7);
    FIFO<int16_t,FIFOSIZE7,0,0> fifo7(buf8);
    FIFO<int16_t,FIFOSIZE8,1,0> fifo8(buf9);
    FIFO<int16_t,FIFOSIZE9,0,0> fifo9(buf10);
    FIFO<int16_t,FIFOSIZE10,1,0> fifo10(buf11);
    FIFO<int16_t,FIFOSIZE11,0,0> fifo11(buf12,1440);
    FIFO<int16_t,FIFOSIZE12,1,0> fifo12(buf13);
    FIFO<int16_t,FIFOSIZE13,1,0> fifo13(buf14);
    FIFO<int16_t,FIFOSIZE14,1,0> fifo14(buf15);
    FIFO<int16_t,FIFOSIZE15,1,0> fifo15(buf16);

    CG_BEFORE_NODE_INIT;
    /* 
    Create node objects
    */
    EchoCanceller<int16_t,735,int16_t,735,int16_t,735> aec(fifo7,fifo5,fifo8,echoState,44100);
    Denoise<int16_t,735,int16_t,735> denoise(fifo8,fifo9,echoState,44100,20,0,8000,0,0.0,0.0);
    Resampler<int16_t,800,int16_t,185> downFar(fifo12,fifo5,desc_480_16);
    Resampler<int16_t,800,int16_t,185> downNear(fifo6,fifo7,desc_480_16);
    Duplicate2<int16_t,800,int16_t,800,int16_t,800> dup0(fifo10,fifo11,fifo12);
    Duplicate2<int16_t,800,int16_t,800,int16_t,800> dup1(fifo13,fifo14,fifo15);
    EchoModel<int16_t,800,int16_t,800,int16_t,800> echo(fifo11,fifo4,fifo6);
    BackgroundSource<int16_t,800,int16_t,800> far(fifo0,fifo1);
    SeparateStereoToMono<int16_t,800,int16_t,800,int16_t,800> mixFar(fifo0,fifo1,fifo10);
    SeparateStereoToMono<int16_t,800,int16_t,800,int16_t,800> mixNear(fifo2,fifo3,fifo4);
    Sink<int16_t,800,int16_t,800> sink(fifo14,fifo15,queues->outputQueue,2);
    Source<int16_t,800,int16_t,800> src(fifo2,fifo3,queues->inputQueue);
    Resampler<int16_t,185,int16_t,800> up(fifo9,fifo13,desc_16_480);

    /* Run several schedule iterations */
    CG_BEFORE_SCHEDULE;
    while(cgStaticError==0)
    {
        /* Run a schedule iteration */
        CG_BEFORE_ITERATION;
        for(unsigned long id=0 ; id < 46; id++)
        {
            CG_BEFORE_NODE_EXECUTION;

            switch(schedule[id])
            {
                case 0:
                {
                   cgStaticError = aec.run();
                }
                break;

                case 1:
                {
                   cgStaticError = denoise.run();
                }
                break;

                case 2:
                {
                   cgStaticError = downFar.run();
                }
                break;

                case 3:
                {
                   cgStaticError = downNear.run();
                }
                break;

                case 4:
                {
                   cgStaticError = dup0.run();
                }
                break;

                case 5:
                {
                   cgStaticError = dup1.run();
                }
                break;

                case 6:
                {
                   cgStaticError = echo.run();
                }
                break;

                case 7:
                {
                   cgStaticError = far.run();
                }
                break;

                case 8:
                {
                   cgStaticError = mixFar.run();
                }
                break;

                case 9:
                {
                   cgStaticError = mixNear.run();
                }
                break;

                case 10:
                {
                   cgStaticError = sink.run();
                }
                break;

                case 11:
                {
                   cgStaticError = src.run();
                }
                break;

                case 12:
                {
                   cgStaticError = up.run();
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
