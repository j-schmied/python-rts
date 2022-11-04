import numpy as np


class TaskSet:
    """
    Set of periodic tasks
    
    Parameters:
    
        *Tasks -> (PTask(...), ...)
    """
    def __init__(self, *Tasks):
        self.taskset = Tasks
        self.urm = len(self.taskset) * (np.power(2, 1/len(self.taskset)) - 1)
        self.u = np.sum([task.u for task in self.taskset])
        self.zeta = np.max([task.xi for task in self.taskset]) - np.min([task.xi for task in self.taskset])
        
    def __len__(self) -> int:
        return len(self.taskset)
    
    def __str__(self) -> str:
        return f"{[task for task in self.taskset]}"

    def __repr__(self) -> str:
        return f"{[task for task in self.taskset]}"
    
    def get_min_priority_task(self):
        t_pmin = None
        
        for task in self.taskset:
            if t_pmin is None or task.p > t_pmin.p:
                t_pmin = task
                
        return t_pmin
        
    def sort_by_xi(self):
        Ttemp = self
        
        sorted = False
        
        while not sorted:
            i = 0
            n = len(self)
            
            for i in range(n):
                if Ttemp[i].xi > Ttemp[i+1].xi and i+1 < n:
                    Ttemp[i], Ttemp[i+1] = Ttemp[i+1], Ttemp[i]
                    continue
                
                sorted = True 
                    
        return Ttemp 
    
    ### RMS Tests
    def ll_test(self) -> bool:
        """
        Liu-Layland-Test
        
        Parameters:
        
            T: TaskSet -> task set [Task(p: float, e: float), ...]
            
        Returns:
        
            bool -> True if test (u <= uRM) succeeds
        """
        n = len(self)
        
        u = 0
        for task in self.taskset:
            u += (task.e/task.p)
                
        print(f"u\t= {round(u, 4)}")
        print(f"uRM\t= {round(self.urm, 4)}")
        
        return True if u <= self.urm else False
    
    def rma_test(self) -> bool:
        """
        Rate Monotonous Analysis Test for a given task set.
        
        Parameters:
        
            T: TaskSet -> task set [Task(p: float, e: float), ...]
            
        Returns:
        
            bool: True if twcrt < t_pmin
        """
        
        t_pmin = self.get_min_priority_task()
        
        print(f"Least prioritized task: {t_pmin}")
        
        tls = list()
        
        t0 = t_pmin.e
        tls.append(t0)
        
        print(f"t0\t= {t0}")
        
        k = 1
        while True:
            tl1 = t_pmin.e
            tl2 = 0
            for task in self.taskset:
                if task == t_pmin:
                    continue
                tl2 += (np.ceil(tls[k-1]/task.p) * task.e)
            tl_ges = tl1 + tl2
            tls.append(tl_ges)
            
            print(f"t{k}\t= {tl_ges}")
        
            if tls[k] == tls[k-1]:
                break
            
            k += 1
            
        print(f"=> converges after {len(tls)} iterations")
                
        twcrt = tls[-1]
        
        print(f"t_wcrt\t= {twcrt}")
                
        return True if twcrt < t_pmin.p else False

    def hyperbolic_bound(self) -> bool:
        """
        Hyperbolic Bound
        
        Returns:
        
            bool: True if hyperbolic bound of task set < 2
        """
        hb = 1
        for task in self.taskset:
            hb *= (task.u + 1)
        
        return hb <= 2
    
    def burchard_test(self):
        """
        Burchard Test
        """
        
        U = (n - 1) * (np.power(2, self.zeta/(n-1)) - 1) + np.power(2, 1-self.zeta) - 1
        return self.u <= U
    
    def sr_test(self, stop: bool = False):
        """
        Test for Distant-Constrained Tasks.
        
        Goal:
        
            From a set of n tasks, n simple periodic task sets result.
        
        Parameters:
        
            T: TaskSet -> task set [Task(p: float, e: float), ...]
            stop: bool -> stop after first modified T that passes u < 1 test
            
        Returns:
        
            dict: {T0: {tbi: float, p_mod: list}, ...} -> for every iteration (every element in the passed task set T)
        """
        tpmin = self.pmin
        n = len(self)
        i = 0
        
        T = self.taskset
        res = dict()
        
        while i < n:
            res[f"T{i}"] = dict()
            tpi = T[i].p
            tbi = tpi / 2 ** np.ceil(np.log2(tpi/tpmin))
            res[f"T{i}"]["tbi"] = tbi
            j = 0
            tpjs = list()
            
            while j < n:
                tpj = T[j].p
                tpj = tbi * 2 ** np.floor(np.log2(tpj/tbi))
                tpjs.append(tpj)
                j += 1    
                
            # Calculate usage
            res[f"T{i}"]["p_mod"] = tpjs
            u = np.sum([task.e / tpjs[j] for j, task in enumerate(T)])
            res[f"T{i}"]["u"] = u
            res[f"T{i}"]["u < 1"] = u < 1
            
            if stop and u < 1:
                break
            
            i += 1
            
        return res
    
    ### EDF Tests
    def ult1_test(self) -> bool:
        """
        u < 1 Test for EDF Scheduling
        
        Returns:
        
            bool: True if u < 1
        """
        return self.u < 1
    
    @property
    def pmin(self):
        """
        Returns minimum period of all tasks of the set
        """
        pmin = None
        for task in self.taskset:
            if pmin is None:
                pmin = task.p
            if task.p < pmin:
                pmin = task.p
        return pmin
