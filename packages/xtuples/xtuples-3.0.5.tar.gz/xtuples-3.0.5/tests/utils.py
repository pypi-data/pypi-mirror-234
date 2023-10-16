
import inspect
import itertools
import datetime

from pympler.asizeof import asizeof  # type: ignore

# ---------------------------------------------------------------

def lineno(n_back = 0):
    frame = inspect.currentframe()
    for _ in range(n_back + 1):
        assert frame is not None
        frame = frame.f_back
    assert frame is not None
    return frame.f_lineno

def outer_func_name(n_back = 0):
    frame = inspect.currentframe()
    for _ in range(n_back + 1):
        assert frame is not None
        frame = frame.f_back
    assert frame is not None
    return frame.f_code.co_name

# ---------------------------------------------------------------

def log_time(start, times):
    end = datetime.datetime.now()
    t = (end - start).microseconds
    times.append(t)
    return end, t

def time_funcs(*fs, iters = 10e4, max_time = 10e6):
    
    n = len(fs)
    f_times_mems = itertools.cycle(zip(
        range(n), fs, [[] for _ in fs], [[] for _ in fs]
    )) # type: ignore

    runs = int(iters / 100)
    start = datetime.datetime.now()

    total = 0

    incr = 0

    for _ in range(100):
        for _ in range(n):

            i, f, times, mems = next(f_times_mems)

            res = [f() for _ in range(runs)]
            r = res[0]

            start, t = log_time(start, times)
            mems.append(asizeof(r))
            
            total += t

        if total > max_time:
                break
        
        # discard one instance
        # so each time we start with a different func
        i, _, _, _ = next(f_times_mems)
        incr += 1
    
    while i < n - 1:
        i, _, _, _ = next(f_times_mems)

    return (incr,) + tuple(
        (sum(times) / len(times)) / 1000
        for _, (_, _, times, _) in zip(range(n), f_times_mems)
    ) + tuple(
        (sum(mems) / len(mems)) / 1000
        for _, (_, _, _, mems) in zip(range(n), f_times_mems)
    )

    # in milliseconds

# ---------------------------------------------------------------

def within_multiple(m, fastest=1):
    def f_compare(v1, v2, m1, m2):
        v1, v2 = ((v1, v2,) if fastest == 1 else (v2, v1,))
        if v2 < v1:
            return True
        return (v1 * m) >= v2
    return f_compare

def within_percent(pct, fastest=1):
    def f_compare(v1, v2, m1, m2):
        v1, v2 = ((v1, v2,) if fastest == 1 else (v2, v1,))
        if v2 < v1:
            return True
        return (v2 - v1) < (v1 * (pct / 100))
    return f_compare

def compare(
    f1,
    f2,
    fastest = 1,
    f_compare = None,
    **kwargs,
):

    print("--")

    loops, millis_1, millis_2, mem_1, mem_2 = time_funcs(f1, f2, **kwargs)

    passed = (
        round(millis_2, 1) <= round(millis_1, 1)
        if fastest == 1
        else round(millis_1, 1) <= round(millis_2, 1)
        if fastest == 0
        else True
    ) if f_compare is None else f_compare(
        millis_1, 
        millis_2,
        mem_1,
        mem_2,
    )

    result = {
        **{
            "iters": "{}%".format(loops),
            "pass": passed,
            "line": lineno(n_back=1),
        },
        **({} if fastest is None else {
            "fastest": fastest,
        }),
        **{
            "memory": {
                f1.__name__: mem_1,
                f2.__name__: mem_2,
            },
            "milliseconds": {
                f1.__name__: round(millis_1, 2),
                f2.__name__: round(millis_2, 2),
            },
        },
    }
    for k, v in result.items():
        print(k, v)

    assert passed, result

# ---------------------------------------------------------------
