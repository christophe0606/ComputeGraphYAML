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
static unsigned int schedule[452]=
{ 
10,11,2,9,3,5,8,1,10,11,2,9,3,5,8,1,4,6,10,11,2,9,3,5,8,1,10,11,2,9,3,5,8,1,4,6,10,11,2,9,
3,5,8,1,10,11,2,9,3,5,8,1,4,6,10,11,2,9,3,5,8,1,10,11,2,9,3,5,8,1,4,6,10,11,2,9,3,5,8,1,
10,11,2,9,3,5,8,1,4,6,10,11,2,9,3,5,8,1,10,11,2,9,3,5,8,1,4,6,10,11,2,9,3,5,8,1,10,11,2,9,
3,5,8,1,4,6,10,11,2,9,3,5,8,1,10,11,2,9,3,5,8,1,4,6,10,11,2,9,3,5,8,1,10,11,2,9,3,5,8,1,
4,6,10,11,2,9,3,5,8,1,10,11,2,9,3,5,8,1,4,6,10,11,2,9,3,5,8,1,10,11,2,9,3,5,8,1,4,6,10,11,
2,9,3,5,8,1,10,11,2,9,3,5,8,1,4,6,10,11,2,9,3,5,8,1,10,11,2,9,3,5,8,1,4,6,10,11,2,9,3,5,
8,1,10,11,2,9,3,5,8,1,4,6,10,11,2,9,3,5,8,1,10,11,2,9,3,5,8,1,4,6,10,11,2,9,3,5,8,1,10,11,
2,9,3,5,8,1,4,6,10,11,2,9,3,5,8,1,10,11,2,9,3,5,8,1,4,6,10,11,2,9,3,5,8,1,10,11,2,9,3,5,
8,1,4,6,10,11,2,9,3,5,8,1,10,11,2,9,3,5,8,1,4,6,10,11,2,9,3,5,8,1,10,11,2,9,3,5,8,1,4,6,
10,11,2,9,3,5,8,1,10,11,2,9,3,5,8,1,4,6,10,11,2,9,3,5,8,1,10,11,2,9,3,5,8,1,4,6,10,11,2,9,
3,5,8,1,10,11,2,9,3,5,8,1,4,6,10,11,2,9,3,5,8,1,10,11,2,9,3,5,8,1,4,6,10,11,2,9,3,5,8,1,
10,11,2,9,3,5,8,1,4,6,7,0,
};

CG_BEFORE_FIFO_BUFFERS
/***********

FIFO buffers

************/
#define FIFOSIZE0 330
#define FIFOSIZE1 160
#define FIFOSIZE2 160
#define FIFOSIZE3 160
#define FIFOSIZE4 160
#define FIFOSIZE5 160
#define FIFOSIZE6 320
#define FIFOSIZE7 640
#define FIFOSIZE8 250
#define FIFOSIZE9 500
#define FIFOSIZE10 160
#define FIFOSIZE11 160
#define FIFOSIZE12 160

#define BUFFERSIZE1 330
CG_BEFORE_BUFFER
float32_t buf1[BUFFERSIZE1]={0};

#define BUFFERSIZE2 160
CG_BEFORE_BUFFER
float32_t buf2[BUFFERSIZE2]={0};

#define BUFFERSIZE3 160
CG_BEFORE_BUFFER
float32_t buf3[BUFFERSIZE3]={0};

#define BUFFERSIZE4 160
CG_BEFORE_BUFFER
float32_t buf4[BUFFERSIZE4]={0};

#define BUFFERSIZE5 160
CG_BEFORE_BUFFER
float32_t buf5[BUFFERSIZE5]={0};

#define BUFFERSIZE6 160
CG_BEFORE_BUFFER
float32_t buf6[BUFFERSIZE6]={0};

#define BUFFERSIZE7 320
CG_BEFORE_BUFFER
float32_t buf7[BUFFERSIZE7]={0};

#define BUFFERSIZE8 640
CG_BEFORE_BUFFER
float32_t buf8[BUFFERSIZE8]={0};

#define BUFFERSIZE9 250
CG_BEFORE_BUFFER
float32_t buf9[BUFFERSIZE9]={0};

#define BUFFERSIZE10 500
CG_BEFORE_BUFFER
float32_t buf10[BUFFERSIZE10]={0};

#define BUFFERSIZE11 160
CG_BEFORE_BUFFER
float32_t buf11[BUFFERSIZE11]={0};

#define BUFFERSIZE12 160
CG_BEFORE_BUFFER
float32_t buf12[BUFFERSIZE12]={0};

#define BUFFERSIZE13 160
CG_BEFORE_BUFFER
float32_t buf13[BUFFERSIZE13]={0};


CG_BEFORE_SCHEDULER_FUNCTION
uint32_t scheduler(int *error)
{
    int cgStaticError=0;
    uint32_t nbSchedule=0;

    CG_BEFORE_FIFO_INIT;
    /*
    Create FIFOs objects
    */
    FIFO<float32_t,FIFOSIZE0,0,0> fifo0(buf1,10);
    FIFO<float32_t,FIFOSIZE1,1,0> fifo1(buf2);
    FIFO<float32_t,FIFOSIZE2,1,0> fifo2(buf3);
    FIFO<float32_t,FIFOSIZE3,1,0> fifo3(buf4);
    FIFO<float32_t,FIFOSIZE4,1,0> fifo4(buf5);
    FIFO<float32_t,FIFOSIZE5,1,0> fifo5(buf6);
    FIFO<float32_t,FIFOSIZE6,0,0> fifo6(buf7);
    FIFO<float32_t,FIFOSIZE7,1,0> fifo7(buf8);
    FIFO<float32_t,FIFOSIZE8,0,0> fifo8(buf9);
    FIFO<float32_t,FIFOSIZE9,1,0> fifo9(buf10);
    FIFO<float32_t,FIFOSIZE10,1,0> fifo10(buf11);
    FIFO<float32_t,FIFOSIZE11,1,0> fifo11(buf12);
    FIFO<float32_t,FIFOSIZE12,1,0> fifo12(buf13);

    CG_BEFORE_NODE_INIT;
    /* 
    Create node objects
    */
    TFLite<float32_t,500> TFLite(fifo9);
    SlidingBuffer<float32_t,640,320> audioWin(fifo6,fifo7);
    Duplicate2<float32_t,160,float32_t,160,float32_t,160> dup0(fifo10,fifo11,fifo12);
    MFCC<float32_t,640,float32_t,10> mfcc(fifo7,fifo8);
    SlidingBuffer<float32_t,500,250> mfccWind(fifo8,fifo9);
    StereoSource<float32_t,320> src(fifo0);
    Unzip<float32_t,320,float32_t,160,float32_t,160> toMono(fifo0,fifo1,fifo2);

    /* Run several schedule iterations */
    CG_BEFORE_SCHEDULE;
    while(cgStaticError==0)
    {
        /* Run a schedule iteration */
        CG_BEFORE_ITERATION;
        for(unsigned long id=0 ; id < 452; id++)
        {
            CG_BEFORE_NODE_EXECUTION;

            switch(schedule[id])
            {
                case 0:
                {
                   cgStaticError = TFLite.run();
                }
                break;

                case 1:
                {
                   
                  {

                   float32_t* i0;
                   float32_t* i1;
                   float32_t* o2;
                   i0=fifo5.getReadBuffer(160);
                   i1=fifo12.getReadBuffer(160);
                   o2=fifo6.getWriteBuffer(160);
                   arm_add_f32(i0,i1,o2,160);
                   cgStaticError = 0;
                  }
                }
                break;

                case 2:
                {
                   
                  {

                   float32_t* i0;
                   float32_t* o2;
                   i0=fifo1.getReadBuffer(160);
                   o2=fifo3.getWriteBuffer(160);
                   arm_scale_f32(i0,HALF,o2,160);
                   cgStaticError = 0;
                  }
                }
                break;

                case 3:
                {
                   
                  {

                   float32_t* i0;
                   float32_t* o2;
                   i0=fifo2.getReadBuffer(160);
                   o2=fifo10.getWriteBuffer(160);
                   arm_scale_f32(i0,HALF,o2,160);
                   cgStaticError = 0;
                  }
                }
                break;

                case 4:
                {
                   cgStaticError = audioWin.run();
                }
                break;

                case 5:
                {
                   cgStaticError = dup0.run();
                }
                break;

                case 6:
                {
                   cgStaticError = mfcc.run();
                }
                break;

                case 7:
                {
                   cgStaticError = mfccWind.run();
                }
                break;

                case 8:
                {
                   
                  {

                   float32_t* i0;
                   float32_t* i1;
                   float32_t* o2;
                   i0=fifo4.getReadBuffer(160);
                   i1=fifo11.getReadBuffer(160);
                   o2=fifo5.getWriteBuffer(160);
                   my_binary(i0,i1,o2,160);
                   cgStaticError = 0;
                  }
                }
                break;

                case 9:
                {
                   
                  {

                   float32_t* i0;
                   float32_t* o1;
                   i0=fifo3.getReadBuffer(160);
                   o1=fifo4.getWriteBuffer(160);
                   my_scale(i0,o1,160);
                   cgStaticError = 0;
                  }
                }
                break;

                case 10:
                {
                   cgStaticError = src.run();
                }
                break;

                case 11:
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
