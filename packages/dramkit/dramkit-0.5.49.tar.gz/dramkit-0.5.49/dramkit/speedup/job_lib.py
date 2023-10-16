# -*- coding: utf-8 -*-

import time
from joblib import Parallel, delayed
import platform

_WINDOWS_SYSTEM = 'windows' in platform.system().lower()


def joblib_parl(func, args_list, n_jobs, backend='threading',
                **kw_jb):
    jb = Parallel(n_jobs=n_jobs, backend=backend, **kw_jb)
    res = jb(delayed(func)(*args) for args in args_list)
    return res


def joblib_parl_mp(func, args_list, n_jobs, backend='threading',
                   **kw_jb):
    jb = Parallel(n_jobs=n_jobs, backend=backend, **kw_jb)
    res = jb(delayed(func)(args) for args in args_list)
    return res


def test_add_win(a, b):
    time.sleep(1)
    return a+b, (a, b)

def test_add_win_mp(args):
    return test_add_win(*args)


if __name__ == '__main__':
    import numpy as np
    from dramkit import TimeRecoder
    tr = TimeRecoder(monotonic=False)
    
    def test_add(a, b):
        time.sleep(1)
        return a+b, (a, b)
    
    def test_add_mp(args):
        return test_add(*args)
    
    n = 10
    args_list = list(zip(np.random.randint(n, size=n),
                         np.random.randint(n, size=n)))
    
    # 若用multiprocessing，windows下被调用的函数不能定义在__main__之下
    backend = 'threading'
    # backend = 'loky'
    # backend = 'multiprocessing'
    if backend in ['multiprocessing'] and _WINDOWS_SYSTEM:
        res1 = joblib_parl(test_add_win, args_list,
                          n_jobs=5,
                          backend=backend
                          )
        res2 = joblib_parl_mp(test_add_win_mp, args_list,
                             n_jobs=5,
                             backend=backend
                             )
    else:
        res1 = joblib_parl(test_add, args_list,
                          n_jobs=5,
                          backend=backend
                          )
        res2 = joblib_parl_mp(test_add_mp, args_list,
                             n_jobs=5,
                             backend=backend
                             )
    print(res1)
    print(res2)
    
    
    tr.used()