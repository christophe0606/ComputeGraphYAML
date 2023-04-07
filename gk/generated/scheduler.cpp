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
static unsigned int schedule[9]=
{ 
7,8,2,1,4,0,3,5,6,
};

CG_BEFORE_FIFO_BUFFERS
/***********

FIFO buffers

************/
#define FIFOSIZE0 1
#define FIFOSIZE1 1
#define FIFOSIZE2 1
#define FIFOSIZE3 1
#define FIFOSIZE4 1
#define FIFOSIZE5 1
#define FIFOSIZE6 1
#define FIFOSIZE7 1

#define BUFFERSIZE1 1
CG_BEFORE_BUFFER
int16_t buf1[BUFFERSIZE1]={0};

#define BUFFERSIZE2 1
CG_BEFORE_BUFFER
int16_t buf2[BUFFERSIZE2]={0};

#define BUFFERSIZE3 1
CG_BEFORE_BUFFER
int16_t buf3[BUFFERSIZE3]={0};

#define BUFFERSIZE4 1
CG_BEFORE_BUFFER
int16_t buf4[BUFFERSIZE4]={0};

#define BUFFERSIZE5 1
CG_BEFORE_BUFFER
int16_t buf5[BUFFERSIZE5]={0};

#define BUFFERSIZE6 1
CG_BEFORE_BUFFER
int16_t buf6[BUFFERSIZE6]={0};

#define BUFFERSIZE7 1
CG_BEFORE_BUFFER
int16_t buf7[BUFFERSIZE7]={0};

#define BUFFERSIZE8 1
CG_BEFORE_BUFFER
int16_t buf8[BUFFERSIZE8]={0};


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
    MyFIFO<int16_t,FIFOSIZE4,1,0> fifo4(buf5);
    FIFO<int16_t,FIFOSIZE5,1,0> fifo5(buf6);
    FIFO<int16_t,FIFOSIZE6,1,0> fifo6(buf7);
    FIFO<int16_t,FIFOSIZE7,1,0> fifo7(buf8);

    CG_BEFORE_NODE_INIT;
    /* 
    Create node objects
    */
    NullSink<int16_t,1> debug(fifo4);
    Duplicate2<int16_t,1,int16_t,1,int16_t,1> dup0(fifo2,fifo3,fifo4);
    Duplicate2<int16_t,1,int16_t,1,int16_t,1> dup1(fifo5,fifo6,fifo7);
    ProcessingOddEven<int16_t,1,int16_t,1,int16_t,1> proc(fifo3,fifo0,fifo1);
    SinkAsync<int16_t,1> sinka(fifo6);
    SinkAsync<int16_t,1> sinkb(fifo7);
    SourceEven<int16_t,1> sourceEven(fifo0);
    SourceOdd<int16_t,1> sourceOdd(fifo2);

    /* Run several schedule iterations */
    CG_BEFORE_SCHEDULE;
    while(cgStaticError==0)
    {
        /* Run a schedule iteration */
        CG_BEFORE_ITERATION;
        for(unsigned long id=0 ; id < 9; id++)
        {
            CG_BEFORE_NODE_EXECUTION;

            switch(schedule[id])
            {
                case 0:
                {
                   
                  {

                   int16_t* i0;
                   int16_t* o1;
                   i0=fifo1.getReadBuffer(1);
                   o1=fifo5.getWriteBuffer(1);
                   compute(i0,o1,1);
                   cgStaticError = 0;
                  }
                }
                break;

                case 1:
                {
                   cgStaticError = debug.run();
                }
                break;

                case 2:
                {
                   cgStaticError = dup0.run();
                }
                break;

                case 3:
                {
                   cgStaticError = dup1.run();
                }
                break;

                case 4:
                {
                   cgStaticError = proc.run();
                }
                break;

                case 5:
                {
                   cgStaticError = sinka.run();
                }
                break;

                case 6:
                {
                   cgStaticError = sinkb.run();
                }
                break;

                case 7:
                {
                   cgStaticError = sourceEven.run();
                }
                break;

                case 8:
                {
                   cgStaticError = sourceOdd.run();
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
