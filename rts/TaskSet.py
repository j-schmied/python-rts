import numpy 


class TaskSet:
    """
    Set of periodic tasks
    
    Parameters:
    
        *Tasks -> (PTask(...), ...)
    """
    def __init__(self, *Tasks):
        self.taskset = Tasks
        self.urm = len(self.taskset) * (numpy.power(2, 1/len(self.taskset)) - 1)
        self.u = numpy.sum([task.u for task in self.taskset])
        self.zeta = numpy.max([task.xi for task in self.taskset]) - numpy.min([task.xi for task in self.taskset])
        
    def __len__(self) -> int:
        return len(self.taskset)
    
    def __str__(self) -> str:
        return f"{[task for task in self.taskset]}"

    def __repr__(self) -> str:
        return f"{[task for task in self.taskset]}"
    
    def get_min_priority_task(self):
        """
        Returns task with the least priority (task with maximum period)
        """
        t_pmin = None
        
        for task in self.taskset:
            if t_pmin is None or task.p > t_pmin.p:
                t_pmin = task
                
        return t_pmin
        
    def is_simple_periodic(self) -> bool:
    	T = self
    	T = T.sort(key="p")
    	T = T.taskset
    	
    	factor = T[1].p / T[0].p
    	
    	for i in range(1, len(T)):
    		f = T[i-1].p * factor
    		if f != T[i].p:
    			return False
    	
    	return True
        
    def sort(self, key: str, desc: bool = False):
        """
        Sort task set by key
        
        Parameters:
        
            key: str    -> key that should be used for sorting
            desc: bool  -> sort descending, False by default
            
        Returns:
        
            TaskSet: with self.taskset sorted by key
        """
        Ttemp = self
        Ttemp.taskset = sorted(self.taskset, key=lambda i: getattr(i, key), reverse=desc)
        return Ttemp
    
    def add_task(self, T):
        """
        Add task to task set
        
        Parameters:
        
            T: PTask -> task to add
        """
        self.taskset.append(T)
    
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
                tl2 += (numpy.ceil(tls[k-1]/task.p) * task.e)
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
        
        print(f"Hyp. Bd. = {hb}")
        return hb <= 2
    
    def burchard_test(self):
        """
        Burchard Test
        """
        n = len(self)
        U = (n - 1) * (numpy.power(2, self.zeta/(n-1)) - 1) + numpy.power(2, 1-self.zeta) - 1
        
        print(f"U(n, zeta) = {U}")
        
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
            tbi = tpi / 2 ** numpy.ceil(numpy.log2(tpi/tpmin))
            res[f"T{i}"]["tbi"] = tbi
            j = 0
            tpjs = list()
            
            while j < n:
                tpj = T[j].p
                tpj = tbi * 2 ** numpy.floor(numpy.log2(tpj/tbi))
                tpjs.append(tpj)
                j += 1    
                
            # Calculate usage
            res[f"T{i}"]["p_mod"] = tpjs
            u = numpy.sum([task.e / tpjs[j] for j, task in enumerate(T)])
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
