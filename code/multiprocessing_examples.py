import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import Manager, Pool, Process
from multiprocessing.sharedctypes import Array, Synchronized, SynchronizedArray, Value
from typing import Dict, List

import numpy as np
from joblib import Parallel, delayed

GLOBAL_VAR = 0

## Запуск процесса
def func(name: str):
    print(f"name: {name}, var: {GLOBAL_VAR}")

def ex_1():
    p = Process(target=func, args=("val",))
    p.start()
    p.join()


## Использование различных механизмов запуска и влияние на глобальные переменные
def ex_2():
    global GLOBAL_VAR
    GLOBAL_VAR = 5
   
    ctx = mp.get_context("spawn")
    p = ctx.Process(target=func, args=("spawn",))
    p.start()
    p.join()

    ctx = mp.get_context("fork")
    p = ctx.Process(target=func, args=("fork",))
    p.start()
    p.join()  


## Использование общих областей данных
def func_mul(val: Synchronized, arr: SynchronizedArray):
    val.value *= 2
    arr[0] += 1.0

def ex_3():
    # val = 7
    val = Value('i', 7)
    # arr = [0.0 for _ range(10)]
    arr = Array('d', 10)

    p = Process(target=func_mul, args=(val, arr))
    p.start()
    p.join()

    print(f"val: {val.value}, arr: {list(arr)}") # type: ignore


## Использование структур данных через прокси
def func_shared_dict(d: Dict[str, int], lst: List[int]):
    d["hello"] = 5
    lst[0] = 10

def ex_4():
    with Manager() as manager:
        d = manager.dict()
        lst = manager.list(range(10))

        p = Process(target=func_shared_dict, args=(d, lst))
        p.start()
        p.join()
    
        print(f"dict: {d}, list: {lst}")


## Использование пулов процессов
def func_worker(val: int) -> int:
    return val * 2

def ex_5():
    with Pool(5) as pool:
        fut1 = pool.apply_async(func_worker, (20,))
        fut2 = pool.apply_async(func_worker, (30,))

        print(f"val: {fut1.get()}, val: {fut2.get()}")   

        lst = pool.map(func_worker, [1, 2, 3, 4, 5]) 
        print(f"mapped list: {lst}")

        for v in pool.imap(func_worker, [1, 2, 3, 4, 5]):
            print(f"{v}")


## Использование concurrent.futures и as_completed
def ex_6():
    with ProcessPoolExecutor(max_workers=4) as pool:
        fut1 = pool.submit(func_worker, 20)
        fut2 = pool.submit(func_worker, 30)

        print(f"val: {fut1.result()}, val: {fut2.result()}")

        futures = [pool.submit(func_worker, x) for x in range(1000)]
        for res in as_completed(futures):
            pass
       

## Общий numpy массив
def func_numpy(shared_arr: SynchronizedArray):
    arr = np.frombuffer(
        shared_arr.get_obj(), 
        count=len(shared_arr), 
        dtype=np.double
    ).reshape((100, 100))

    arr[0, :] = 100

def ex_7():
    count = 100 * 100
    shared_arr = mp.Array('d', count)

    arr = np.frombuffer(
        shared_arr.get_obj(), 
        count=len(shared_arr), 
        dtype=np.double
    ).reshape((100, 100))

    p = Process(target=func_numpy, args=(shared_arr, ))
    p.start()
    p.join()

    print(arr)
    

def ex_10():
    count = 100 *1000
    shared_arr = mp.Array('d', count)

    arr = np.frombuffer(
        shared_arr.get_obj(), 
        count=len(shared_arr), 
        dtype=np.double
    ).reshape((100, 100))

    p = Process(target=func_numpy, args=(shared_arr, ))
    p.start()
    p.join()

    print(arr)    

## joblib
def func_joblib(val: int) -> int:
    return val ** 2

def ex_8():
    with Parallel(n_jobs=4) as pool:
        res = pool(delayed(func_joblib)(i) for i in range(10))
        print(res)
        

if __name__ == '__main__':
    GLOBAL_VAR = 5
    
    # ex_1()
    ex_2()
    # ex_3()
    # ex_4()
    # ex_5()
    # ex_6()
    # ex_7()
    # ex_8()
