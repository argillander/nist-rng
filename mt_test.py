from multiprocessing import Process, Manager
import os


def f(results):
    import time, random
    t = random.randint(0,5)
    print(os.getpid(), " sleeping ", t)
    time.sleep(t)

    results.append(t)
    print("hello from ", os.getpid())

if __name__ == '__main__':
    #info('main line')
    procs = []
    m = Manager()
        
    results = m.list()
    for i in range(5):
        p = Process(target=f, args=(results,))
        procs.append(p)
        p.start()
    
    for p in procs:
        p.join()

    print("Results from MT test was ")
    print(results)