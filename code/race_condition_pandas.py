import pandas as pd

from threading import Thread



def func(df: pd.DataFrame):    
    for _ in range(10000):       
        df.iat[0, 0] += 1 # type: ignore


if __name__ == '__main__':
    df = pd.DataFrame({"col_1": range(1000)})

    t1 = Thread(target=func, args=(df, ))
    t2 = Thread(target=func, args=(df, ))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print(df.iat[0, 0])