#include <iostream> 
#include <thread> 
#include <mutex> 
#include <stdlib.h> 
#include <sys/time.h> 
#include <time.h> 
#include <sys/mman.h> 
#include <sys/types.h>
#include <string.h>
//#include "mops.h"

using namespace std;
int threadCnt = 0;
pthread_mutex_t mutex_sync;
pthread_cond_t cond_sync;


static unsigned int count[16];
unsigned long long SIZE;
//uint32_t A[2];
uint cpus = 0;
struct timeval proc_start;
unsigned long time_start = 0;


void array_add(int *a, int *b, int *c, int tid, int threads, int num_values)
{
    for (int i = tid; i < num_values; i += threads) {
        c[i] = a[i] + b[i];
    }
}

unsigned long usec_diff(struct timeval *a, struct timeval *b)
{
    unsigned long usec;

    usec = (b->tv_sec - a->tv_sec) *1000000;
    usec += b->tv_usec - a->tv_usec;
    return usec;
}

void print_test(unsigned int thread_id)
{
    cout << "byebye world["<<thread_id<<"]"<<endl;
}

void wait_time_start()
{
    if (time_start != 0) {
        struct timeval cur_time;
        unsigned long diff;
        do {
            gettimeofday(&cur_time, NULL);
            diff = usec_diff(&proc_start, &cur_time);
        } while (diff < time_start);
        unsigned long usec = cur_time.tv_sec * 1000000 + cur_time.tv_usec;
        cout <<" cur time:"<< usec <<";end diff: "<<diff<<endl;
    }
}

void threadplus(uint32_t *buffer, uint thread_id)
{
    wait_time_start();

    pthread_mutex_lock(&mutex_sync);
    threadCnt--;

    if (threadCnt <= 0) {
        pthread_mutex_unlock(&mutex_sync);
        pthread_cond_broadcast(&cond_sync);
        //m5_reset_stats(0, 0);
    } else {
        pthread_cond_wait(&cond_sync, &mutex_sync);
        pthread_mutex_unlock(&mutex_sync);
    }
    //gettimeofday(&start, NULL);

    while(buffer[thread_id] < SIZE) {
        //cout << buffer << endl;
        buffer[thread_id] ++;
    }

    //gettimeofday(&end, NULL);
    pthread_mutex_lock(&mutex_sync);
    threadCnt++;
    if (threadCnt == 1) {
        pthread_mutex_unlock(&mutex_sync);
        //m5_dump_reset_stats(0, 0);
    } else {
        pthread_mutex_unlock(&mutex_sync);
    }

}

int main(int argc, char *argv[])
{
    pthread_mutex_init(&mutex_sync, NULL);
    pthread_cond_init(&cond_sync, NULL);

    SIZE = 1000;

    cout << "SIZE: " << SIZE << endl;

    cpus = 2;
    cout << "Thread: " << cpus << endl;

    //cout << "Op: " << op_str << endl;
    if (!cpus) {
        cpus = thread::hardware_concurrency();
    }
    cout << "Running on " << cpus << " cores." << endl;

    thread *threads = new thread[cpus];
    uint32_t *A = new uint32_t[cpus];
    //A[0] = new uint32_t;
    //A[1] = new uint32_t; 

    threadCnt = cpus;

    for (int i = 1; i < cpus ; i++) {
        threads[i] = thread(threadplus, A, i);
    }

    cout << "start test" << endl;
    threadplus(A, 0);

    cout << "Waiting for other threads to complete" << endl;
    cout << A[0] << endl;
    cout << A[1] << endl;

    for(int i=1; i< cpus; i++){
        if (threads[i].joinable()) {
            try {
                threads[i].join();
            } catch (const std::exception& ex) {
                cout <<"exc!!!!!"<<&ex<<endl;
            }
        }
        cout <<"join thread " << i <<endl;
    }

    

    //delete[] threads;
    //delete [] buffer;
    cout << "Validating..." << flush;
    return 0;
}