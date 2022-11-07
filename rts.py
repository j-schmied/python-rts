#!/usr/bin/env python
import pandas as pd
from rts.Helpers import *
from rts.Processor import *
from rts.Task import *
from rts.TaskSet import *


def main():
    T = TaskSet(PTask(4, 1), PTask(8, 3), PTask(32, 4), PTask(16, 3))
    CPU = Processor(8)

    line = '\n' + '-' * 50 + '\n'
    sline = '-' * 50

    def test(r): return f"Test success: {r}"
    def stest(r): return "Result: Task set is schedulable" if r else "Result: Task set is not schedulable"

    print(sline)
    print("UP Scheduling Tests")
    print(sline)
    print('\n')
    print(f"Task Set is simple periodic: {T.is_simple_periodic()}")
    print(line)
    if T.is_simple_periodic():
        print("[RMS] u < 1 Test")
        ult1t = T.ult1_test()
        print(stest(ult1t))
        print(line)
    print("[RMS] Liu-Layland-Test")
    llt = T.ll_test()
    print(stest(llt))
    print(line)
    print("[RMS] RMA Test")
    rmat = T.rma_test()
    print(stest(rmat))
    print(line)
    print("[RMS] Hyperbolic Bound")
    hb = T.hyperbolic_bound()
    print(stest(hb))
    print(line)
    print("[RMS] Burchard Test")
    bt = T.burchard_test()
    print(stest(bt))
    print(line)
    print("[RMS] SR-Test")
    srt_df = pd.DataFrame(T.sr_test()).T
    print(srt_df)
    print(line)
    print("[EDF] u < 1 Test")
    ult1t = T.ult1_test()
    print(stest(ult1t))
    print('\n')
    
    print(sline)
    print("MP Partitioning Procedures")
    print(sline)
    print('\n')
    print("RM Next Fit")
    rmnft = CPU.rmnf(T)
    rmnf_df = pd.DataFrame(CPU.get_partitioning()).T
    print(rmnf_df)
    print(test(rmnft))
    print(line)
    print("RM First Fit")
    rmfft = CPU.rmff(T)
    rmff_df = pd.DataFrame(CPU.get_partitioning()).T
    print(rmff_df)
    print(test(rmfft))
    print(line)
    print("RM First Fit with Decreasing Utilization")
    rmffdut = CPU.rmffdu(T)
    rmffdu_df = pd.DataFrame(CPU.get_partitioning()).T
    print(rmffdu_df)
    print(test(rmffdut))
    print(line)
    print("RM Small Task")
    rmstt = CPU.rmst(T)
    rmst_df = pd.DataFrame(CPU.get_partitioning()).T
    print(rmst_df)
    print(test(rmstt))
    print('\n')


if __name__ == "__main__":
    main()
