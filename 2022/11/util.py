import cProfile, pstats, io
from pstats import SortKey

def profile_func(func):
    pr = cProfile.Profile()
    pr.enable()

    result = func()

    pr.disable()
    s = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())

    return result
