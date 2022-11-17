# python-rts

This library provides various functions for real time systems related calculations.

NOTE: currently under development. Not all functions are implemented yet. PR's/improvements welcome! Also, this library is limited to periodic tasks and is not planned to be extended furthermore in the future. Feel free to fork and extend on your own!

## Content

### Types

* PTask - Periodic Task with parameters: Period p, Execution Time e, Phase fi and (relative) Deadline d
* TaskSet - Set of periodic Tasks, takes list of PTask‘s
* Processor - CPU with parameter core count, returns Single-Core Processor by default

### Procedures

For Rate Monotonic Scheduling (RMS):

* Scheduling Tests:
  * Liu-Layland Test
  * Rate Monotonous Analysis
  * Hyperbolic Bound
  * Burchard Test
  * SR Test
* Partitioning Procedures:
  * RM Next Fit
  * RM First Fit
  * RM First Fit with Decreasing Utilization
  * RM Small Task
  * RM General Task (TbA)
  * RM Best Fit (TbA)
  * RM Worst Fit (TbA)
* Global Procedures:
  * Adaptive TkC
  * RM Utilization Separation

For Earliest Deadline First Scheduling (EDF):

* Scheduling Tests:
  * u < 1 Test
* Partitioning Procedures:
  * EDF Next Fit
  * EDF First Fit (TbA)
  * EDF Best Fit (TbA)
* Global Procedures:
  * Global EDF
  * EDF Utilization Separation
  * fpEDF

### Comparison

| Procedure | Test | Complexity | N/N0 |
|:----------|:-----|-----------:|-----:|
|RMNF|LL|O(n)|2.67|
|RMFF|LL|O(nlogn)|2.23|
|RMBF|LL|O(nlogn)|2.23|
|RMFFDU|Hyp. Bd.|O(nlogn)|1.66|
|RMST|Burch.|O(nlogn)|1/(1-max ui)|
|EDFNF|u<1|O(n)|?|
|EDFFF|u<1|O(nlogn)|1.7|
|EDFBF|u<1|O(nlogn)|1.7|

## Usage

* Install: `pip install git+https://github.com/j-schmied/python-rts.git`
* Usage:
  * `rts.ipynb` (Note: Notebook also uses `pandas` and `plotly`)
  * `rts.py` -> adapt task set on top and run script

## Sources

* Jane W. S. Liu. “Real-Time Systems“
* Sudarshan K. Dhall und C. L. Liu. “On a Real-Time Scheduling Problem”
* Ching-Chih Han und Hung-ying Tyan. “A Better Polynomial-Time Schedulability Test for Real-Time Fixed-Priority Scheduling Algorithms”
* Almut Burchard u. a. “Assigning Real-Time Tasks to Homogeneous Multiprocessor Systems”
* Tei-Wei Kuo und Aloysius K. Mok. “Load Adjustment in Adaptive Real-Time Systems”
* C. L. Liu und James W. Layland. “Scheduling Algorithms for Multiprogramming in a Hard-Real-Time Environment”
