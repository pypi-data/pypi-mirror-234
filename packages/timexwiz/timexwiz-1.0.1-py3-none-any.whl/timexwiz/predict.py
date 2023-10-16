from typing import Callable, Tuple, List, Dict, TypeAlias, Any

from .measure_timer import *

Arguments: TypeAlias = Tuple[List, Dict[str, Any]]
MS_THRESHOLD = 250


def measure_funcs_on_args(total_sec: float, funcs: List[Callable], all_arguments: List[Arguments]):
    one_func_ms = total_sec * 1000.0 / len(funcs)
    res = []
    for func in funcs:
        measures = []
        rep_counts = predict_repeat_counts(one_func_ms, func, all_arguments)
        arg_with_repeats = list(zip(all_arguments, rep_counts))
        for arg, rep_count in arg_with_repeats:
            with Timer() as t:
                for _ in range(rep_count):
                    func(*arg[0], **arg[1])
            measures.append(t.result_ms / rep_count)
        res.append(measures)


def predict_repeat_counts(target_ms: float, func: Callable, all_arguments: List[Arguments]):
    res = []
    one_measure_ms = target_ms / len(all_arguments)
    for args in all_arguments:
        avg = mean_time(func, args)
        need_runs = int(one_measure_ms / avg) + 1
        res.append(need_runs)
    return res


def mean_time(func: Callable, arguments: Arguments):
    runs = 0
    ms_total = 0
    while ms_total <= ms_total:
        runs += 1
        with Timer() as t:
            func(*arguments[0], **arguments[1])
        ms_total += t.result_ms
    return ms_total / runs
