#!/usr/bin/env python
import pandas as pd
from rts.Helpers import *
from rts.Processor import *
from rts.Task import *
from rts.TaskSet import *


def main():
    T = TaskSet(PTask(7, 2), PTask(21, 3), PTask(29, 9), PTask(49,15), PTask(64, 20), PTask(66, 16), PTask(160, 32), PTask(235, 72), PTask(260, 25), PTask(450, 120))
    CPU = Processor(4)

    line = '\n' + '-' * 50 + '\n'
    sline = '-' * 50

    def test(r): return f"Test success: {r}"
    def stest(r, proc="pessimistic"): return ("Result: Task set is schedulable" if r else "Result: Task set is not schedulable") + " (" + proc + ")"

    print(sline)
    print("UP Scheduling Tests")
    print(sline)
    print('\n')
    print(f"Task Set is simple periodic: {T.is_simple_periodic()}")
    print(line)
    if T.is_simple_periodic():
        print("[RMS] u < 1 Test")
        ult1t = T.ult1_test()
        print(stest(ult1t, "optimistic"))
        print(line)
    print("[RMS] Liu-Layland-Test")
    llt = T.ll_test()
    print(stest(llt))
    print(line)
    print("[RMS] RMA Test")
    rmat = T.rma_test()
    print(stest(rmat, "optimistic"))
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
    success = len(np.where(srt_df["u < 1"].isin(["True", True]))) > 0
    print(srt_df)
    print(stest(success))
    print(line)
    print("[EDF] u < 1 Test")
    ult1t = T.ult1_test()
    print(stest(ult1t, "optimistic"))
    print('\n')
    
    print(sline)
    print("MP Partitioning Procedures")
    print(sline)
    print('\n')
    print("RM Next Fit")
    rmnft = CPU.rmnf(T)
    rmnf_df = pd.DataFrame(CPU.get_partitioning()).T
    print(rmnf_df)
    print(f"Average Core Utilization: {round(np.mean(rmnf_df['u_rel']), 4) * 100}%")
    print(test(rmnft))
    print(line)
    print("RM First Fit")
    rmfft = CPU.rmff(T)
    rmff_df = pd.DataFrame(CPU.get_partitioning()).T
    print(rmff_df)
    print(f"Average Core Utilization: {round(np.mean(rmff_df['u_rel']), 4) * 100}%")
    print(test(rmfft))
    print(line)
    print("RM First Fit with Decreasing Utilization")
    rmffdut = CPU.rmffdu(T)
    rmffdu_df = pd.DataFrame(CPU.get_partitioning()).T
    print(rmffdu_df)
    print(f"Average Core Utilization: {round(np.mean(rmffdu_df['u_rel']), 4) * 100}%")
    print(test(rmffdut))
    print(line)
    print("RM Small Task")
    rmstt = CPU.rmst(T)
    rmst_df = pd.DataFrame(CPU.get_partitioning()).T
    print(rmst_df)
    print(f"Average Core Utilization: {round(np.mean(rmst_df['u_rel']), 4) * 100}%")
    print(test(rmstt))
    print(line)
    # print("RM General Task")
    # rmgtt = CPU.rmgt(T)
    # rmgt_df = pd.DataFrame(CPU.get_partitioning()).T
    # print(rmgt_df)
    # print(test(rmgtt))
    # print(line)
    # print("RM Best Fit")
    # rmbft = CPU.rmbf(T)
    # rmbf_df = pd.DataFrame(CPU.get_partitioning()).T
    # print(rmbf_df)
    # print(test(rmbft))
    # print(line)
    # print("RM Worst Fit")
    # rmwft = CPU.rmwf(T)
    # rmwf_df = pd.DataFrame(CPU.get_partitioning()).T
    # print(rmwf_df)
    # print(test(rmwft))
    # print(line)
    print("EDF Next Fit")
    edfnft = CPU.edfnf(T)
    edfnf_df = pd.DataFrame(CPU.get_partitioning()).T
    print(edfnf_df)
    print(f"Average Core Utilization: {round(np.mean(edfnf_df['u_rel']), 4) * 100}%")
    print(test(edfnft))
    # print(line)
    # print("EDF First Fit")
    # edffft = CPU.edfff(T)
    # edfff_df = pd.DataFrame(CPU.get_partitioning()).T
    # print(edfff_df)
    # print(test(edffft))
    # print(line)
    # print("EDF Best Fit")
    # edfbft = CPU.edfbf(T)
    # edfbf_df = pd.DataFrame(CPU.get_partitioning()).T
    # print(edfbf_df)
    # print(test(edfbft))
    print('\n')

    print(sline)
    print("MP Global Procedures")
    print(sline)
    print('\n')
    print("Adaptive TkC")
    atkct = CPU.adaptive_tkc(T)
    print(test(atkct))
    print(line)
    print("RM Utilization Separation")
    rmust = CPU.rmus(T)
    print(test(rmust))
    print(line)
    print("Global EDF")
    gedft = CPU.global_edf(T)
    print(test(gedft))
    print(line)
    print("EDF Utilization Separation")
    edfust = CPU.edfus(T)
    print(test(edfust))
    print(line)
    print("fpEDF")
    fpedft = CPU.fpedf(T)
    print(test(fpedft))
    print('\n')


if __name__ == "__main__":
    main()
