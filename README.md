# python-rts

This library provides various functions for real time systems related calculations.

NOTE: currently under development. Not all functions are implemented yet. PR's/improvements welcome!

## Content

### Types

* PTask - Periodic Task with parameters: Period p, Execution Time e, Phase fi and (relative) Deadline d
* TaskSet - Set of periodic Tasks, takes list of PTask‘s
* Processor - CPU with parameter core count, returns Single-Core Processor by default

### Procedures

For Rate Monotonus Scheduling (RMS):

* Scheduling Tests:
    * Liu-Layland Test
    * Rate Monotonous Analysis
    * Hyperbolic Bound
    * Burchard Test
    * SR Test
* Partitioning Procedures:
    * Rate Monotonous Next Fit
    * Rate Monotonous First Fit
    * Rate Monotonous First Fit with Decreasing Utilization
    * Rate Monotonous Small Task
    * Rate Monotonous General Task
    * Rate Monotonous Best Fit
    * Rate Monotonous Worst Fit

For Earliest Deadline First Scheduling (EDF):

* Scheduling Tests:
    * u < 1 Test 
* Partitioning Procedures:
    * Earliest Deadline First Next Fit
    * Earliest Deadline First First Fit
    * Earliest Deadline First Best Fit

## Usage

* Install: `pip install git+https://github.com/j-schmied/python-rts.git`
* Usage: see `rts.ipynb` (Note: Notebook also uses `pandas` and `plotly`)

## Sources

* Jane W. S. Liu. “Real-Time Systems“
* Sudarshan K. Dhall und C. L. Liu. “On a Real-Time Scheduling Problem”     
* Ching-Chih Han und Hung-ying Tyan. “A Better Polynomial-Time Schedulability Test for Real-Time Fixed-Priority Scheduling Algorithms”
* Almut Burchard u. a. “Assigning Real-Time Tasks to Homogeneous Multiprocessor Systems”
* Tei-Wei Kuo und Aloysius K. Mok. “Load Adjustment in Adaptive Real-Time Systems”
* C. L. Liu und James W. Layland. “Scheduling Algorithms for Multiprogramming in a Hard-Real-Time Environment”
 