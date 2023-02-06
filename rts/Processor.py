import numpy


class Processor:
    """
    Implementation of Single- or Multi-Core Processor
    
    Parameters:
    
        core_count: int -> number of cores (1 by default, Single-Core Processor)
    """
    def __init__(self, core_count: int = 1):
        self.core_count = core_count
        self.prepare(self.core_count)
        
    def prepare(self, cc):
        """
        Creates empty partitioning table for Processor
        
        Parameters:
        
            cc: int -> core_count of Processor
        """
        self.core_dict = dict()
        
        for i in range(cc):
            self.core_dict[f"C{i+1}"] = dict()
            self.core_dict[f"C{i+1}"]["u"] = 0
            self.core_dict[f"C{i+1}"]["u_max"] = 1
            self.core_dict[f"C{i+1}"]["u_rel"] = 0
            self.core_dict[f"C{i+1}"]["Tasks"] = list()
            
    def reset(self):
        """
        Empties partitioning table
        """
        self.prepare(self.core_count)
        
    def get_partitioning(self):
        """
        Returns current partitioning table for processor
        """
        return self.core_dict
    
    # Partitioning procedures    
    def rmnf(self, T) -> bool:
        """
        Rate Monotonous Next Fit Scheduling using Liu-Layland-Test.
        
        Parameters:
        
            T: TaskSet -> task set that should be scheduled
            
        Returns:
        
            bool -> True if scheduling was successful
        """
        self.reset()
        
        i = 0  # Taskindex
        j = 1  # Processorindex
        T = T.sort('p')
        n = len(T)
        T = T.taskset
        
        while i < n:
            if j > self.core_count:
                return False
            
            t_urm = (len(self.core_dict[f"C{j}"]["Tasks"])+1) * (numpy.power(2, 1/(len(self.core_dict[f"C{j}"]["Tasks"])+1)) - 1) 
            
            try: 
                if self.core_dict[f"C{j}"]['u'] + (T[i].u) < t_urm:
                    self.core_dict[f"C{j}"]["Tasks"].append(T[i])
                    self.core_dict[f"C{j}"]['u'] += T[i].u
                    self.core_dict[f"C{j}"]["u_max"] = len(self.core_dict[f"C{j}"]["Tasks"]) * (numpy.power(2, 1/len(self.core_dict[f"C{j}"]["Tasks"])) - 1)
                    self.core_dict[f"C{j}"]["u_rel"] = self.core_dict[f"C{j}"]["u"] / self.core_dict[f"C{j}"]['u_max']
                else:
                    if j + 1 > self.core_count:
                        return False
                    self.core_dict[f"C{j+1}"]["Tasks"].append(T[i])
                    self.core_dict[f"C{j+1}"]['u'] += T[i].u
                    self.core_dict[f"C{j+1}"]["u_max"] = len(self.core_dict[f"C{j}"]["Tasks"]) * (numpy.power(2, 1/len(self.core_dict[f"C{j}"]["Tasks"])) - 1)
                    self.core_dict[f"C{j}"]["u_rel"] = self.core_dict[f"C{j}"]["u"] / self.core_dict[f"C{j}"]['u_max']
                    j += 1
                
                i += 1
            except ZeroDivisionError:
                return False
            
        return True
    
    def rmff(self, T) -> bool:
        """
        Rate Monotonous First Fit Scheduling using Liu-Layland-Test.
        
        Parameters:
        
            T: TaskSet -> task set that should be scheduled
            
        Returns:
        
            bool -> True if scheduling was successful
        """
        self.reset()
        
        N = 1
        i = 0
        T = T.sort('p')
        n = len(T)
        T = T.taskset
        
        while i < n:
            j = 1

            t_urm = (len(self.core_dict[f"C{j}"]["Tasks"])+1) * (numpy.power(2, 1/(len(self.core_dict[f"C{j}"]["Tasks"])+1)) - 1) 
            
            while self.core_dict[f"C{j}"]['u'] + (T[i].u) > t_urm:
                j += 1
                
                if j > self.core_count:
                    return False 
                
            self.core_dict[f"C{j}"]["Tasks"].append(T[i])
            self.core_dict[f"C{j}"]['u'] += T[i].u
            self.core_dict[f"C{j}"]["u_max"] = len(self.core_dict[f"C{j}"]["Tasks"]) * (numpy.power(2, 1/len(self.core_dict[f"C{j}"]["Tasks"])) - 1)
            self.core_dict[f"C{j}"]["u_rel"] = self.core_dict[f"C{j}"]["u"] / self.core_dict[f"C{j}"]['u_max']
            
            if j > N:
                N = j
            
            i += 1 
            
        return True
    
    def rmffdu(self, T) -> bool:
        """
        Rate Monotonous First Fit with Decreasing Utilizations Scheduling using Hyperbolic Bound.
        
        Parameters:
        
            T: TaskSet -> task set that should be scheduled
            
        Returns:
        
            bool -> True if scheduling was successful
        """
        self.reset()
        
        i = 0  # Taskindex
        N = 1  # Processor count
        T = T.sort(key='u', desc=True)
        n = len(T)
        T = T.taskset
        
        while i < n:
            j = 1  # Processorindex
        
            while True:
                m_hb = 1
                for task in self.core_dict[f"C{j}"]["Tasks"]:
                    m_hb *= (task.u + 1)
                
                if T[i].u < 2/m_hb - 1:
                    break
                j += 1
                
                if j > self.core_count:
                    return False
                
            self.core_dict[f"C{j}"]["Tasks"].append(T[i])
            self.core_dict[f"C{j}"]['u'] += T[i].u
            self.core_dict[f"C{j}"]["u_max"] = len(self.core_dict[f"C{j}"]["Tasks"]) * (numpy.power(2, 1/len(self.core_dict[f"C{j}"]["Tasks"])) - 1)
            self.core_dict[f"C{j}"]["u_rel"] = self.core_dict[f"C{j}"]["u"] / self.core_dict[f"C{j}"]['u_max']
            
            if j > N:
                N = j
                
            i += 1 
        
        return True
    
    def rmst(self, T) -> bool:
        """
        Rate Monotonous Small Task Scheduling
        
        Parameters:
        
            T: TaskSet -> task set that should be scheduled
            
        Returns:
        
            bool -> True if scheduling was successful
        """
        self.reset()
        
        i = 0  # Taskindex
        j = 0  # Processorindex
        T = T.sort(key="xi")
        n = len(T)
        T = T.taskset
        tasks_planned = 0
        
        while i+1 < n:
            j += 1
            
            if j > self.core_count:
                return False
            
            self.core_dict[f"C{j}"]["Tasks"].append(T[i])
            self.core_dict[f"C{j}"]['u'] += T[i].u
            tasks_planned += 1
            zeta = 0
            xmin = T[0].xi
            ex = 0
            
            while ex != 1:
                i += 1
                
                if i >= n:
                    break
                
                zeta = T[i].xi - xmin
                
                if T[i].u + self.core_dict[f"C{j}"]['u'] <= numpy.max([numpy.log(2), 1 - zeta*numpy.log(2)]):
                    self.core_dict[f"C{j}"]["Tasks"].append(T[i])
                    self.core_dict[f"C{j}"]['u'] += T[i].u
                    self.core_dict[f"C{j}"]["u_max"] = len(self.core_dict[f"C{j}"]["Tasks"]) * (numpy.power(2, 1/len(self.core_dict[f"C{j}"]["Tasks"])) - 1)
                    self.core_dict[f"C{j}"]["u_rel"] = self.core_dict[f"C{j}"]["u"] / self.core_dict[f"C{j}"]['u_max']
                    tasks_planned += 1
                    continue

                ex = 1
        
        if tasks_planned != n:
            return False
        
        return True
    
    def rmgt(self, T) -> bool:
        """
        Rate Monotonous General Task Scheduling
        Using RMST for u <= 1/3
        Using RMFF for u > 1/3
        
        Parameters:
        
            T: TaskSet -> task set that should be scheduled
            
        Returns:
        
            bool -> True if scheduling was successful
        """
        # TODO
        self.reset()
        return True
    
    def rmbf(self, T) -> bool:
        """
        Rate Monotonous Best Fit Scheduling
        
        Parameters:
        
            T: TaskSet -> task set that should be scheduled
            
        Returns:
        
            bool -> True if scheduling was successful
        """
        # TODO
        self.reset()
        return True
    
    def rmwf(self, T) -> bool:
        """
        Rate Monotonous Worst Fit Scheduling
        
        Parameters:
        
            T: TaskSet -> task set that should be scheduled
            
        Returns:
        
            bool -> True if scheduling was successful
        """
        # TODO
        self.reset()
        return True
    
    def edfnf(self, T) -> bool:
        """
        Earliest Deadline First Next Fit Scheduling
        
        Parameters:
        
            T: TaskSet -> task set that should be scheduled
            
        Returns:
        
            bool -> True if scheduling was successful
        """
        self.reset()
        
        i = 0  # Taskindex
        j = 1  # Processorindex
        n = len(T)
        T = T.taskset
        
        while i < n:
            if j > self.core_count:
                return False
            
            if self.core_dict[f"C{j}"]['u'] + (T[i].u) < 1:
                self.core_dict[f"C{j}"]["Tasks"].append(T[i])
                self.core_dict[f"C{j}"]['u'] += T[i].u
                self.core_dict[f"C{j}"]["u_max"] = 1
                self.core_dict[f"C{j}"]["u_rel"] = self.core_dict[f"C{j}"]["u"] / self.core_dict[f"C{j}"]['u_max']
            else:
                if j + 1  > self.core_count:
                    return False
                self.core_dict[f"C{j+1}"]["Tasks"].append(T[i])
                self.core_dict[f"C{j+1}"]['u'] += T[i].u
                self.core_dict[f"C{j+1}"]["u_max"] = 1
                self.core_dict[f"C{j}"]["u_rel"] = self.core_dict[f"C{j}"]["u"] / self.core_dict[f"C{j}"]['u_max']
                j += 1
            
            i += 1
            
        return True
    
    def edfff(self, T) -> bool:
        """
        Earliest Deadline First First Fit Scheduling
        
        Parameters:
        
            T: TaskSet -> task set that should be scheduled
            
        Returns:
        
            bool -> True if scheduling was successful
        """
        self.reset()

        N = 1
        i = 0
        n = len(T)
        T = T.taskset

        while i < n:
            j = 1

            while self.core_dict[f"C{j}"]['u'] + (T[i].u) > 1:
                j += 1

                if j > self.core_count:
                    return False

            self.core_dict[f"C{j}"]["Tasks"].append(T[i])
            self.core_dict[f"C{j}"]['u'] += T[i].u
            self.core_dict[f"C{j}"]["u_max"] = len(self.core_dict[f"C{j}"]["Tasks"]) * (numpy.power(2, 1/len(self.core_dict[f"C{j}"]["Tasks"])) - 1)
            self.core_dict[f"C{j}"]["u_rel"] = self.core_dict[f"C{j}"]["u"] / self.core_dict[f"C{j}"]['u_max']

            if j > N:
                N = j

            i += 1

        return True
    
    def edfbf(self, T) -> bool:
        """
        Earliest Deadline First Best Fit Scheduling
        
        Parameters:
        
            T: TaskSet -> task set that should be scheduled
            
        Returns:
        
            bool -> True if scheduling was successful
        """
        # TODO
        self.reset()
        return True

    # Global procedures
    def adaptive_tkc(self, T) -> bool:
        """
        Adaptive TkC
        
        Parameters:
        
            T: TaskSet -> task set that should be scheduled
            
        Returns:
        
            bool -> True if scheduling was successful
        """
        self.reset()
        
        m = self.core_count
        
        for task in T.taskset:
            task.pke = task.p - (m-1*numpy.sqrt(5*m**2-6*m+1)/(2*m)) * task.e
            
        T = T.sort('pke')
        
        Us = ((2*m)/(3*m-1+numpy.sqrt(5*m**2-6*m+1)))
        
        print(f"Task set ordered by k = {T}")
        print(f"Us = {Us}")
        
        return T.u < Us
    
    def rmus(self, T) -> bool:
        """
        Rate Monotonic Utilization Separation
        
        Parameters:
        
            T: TaskSet -> task set that should be scheduled
            
        Returns:
        
            bool -> True if scheduling was successful
        """
        self.reset()
        
        m = self.core_count
        umax = (numpy.power(m, 2))/(3*m - 2)
        us = m/(3*m-2)
        
        T = T.sort('p')
        
        print(f"Task set ordered by p: {T}")
        
        high_prio = [task for task in T.taskset if task.u > us]
        low_prio = [task for task in T.taskset if task.u <= us]
        
        print(f"High Priority Tasks: {high_prio}")
        print(f"Low Priority Tasks: {low_prio}")

        print(f"Max. schedulable utilization = {umax}")
        print(f"Task set utilization = {T.u}")
        
        return T.u < umax
    
    def global_edf(self, T) -> bool:
        """
        Global Earliest Deadline First
        
        Parameters:
        
            T: TaskSet -> task set that should be scheduled
            
        Returns:
        
            bool -> True if scheduling was successful
        """
        self.reset()
        
        m = self.core_count
        T = T.sort('u')
        
        umax = T.taskset[-1].u

        u = umax + m * (1 - umax)
        
        print(f"u = {u}, Tu = {T.u}")
        
        return T.u < u
    
    def edfus(self, T) -> bool:
        """
        Earliest Deadline First Utilization Separation
        
        Parameters:
        
            T: TaskSet -> task set that should be scheduled
            
        Returns:
        
            bool -> True if scheduling was successful
        """
        self.reset()

        m = self.core_count
        umax = (m**2)/(2*m-1)
        us = m/(2*m-1)
        
        T = T.sort('p')
        
        high_prio = [task for task in T.taskset if task.u > us]
        low_prio = [task for task in T.taskset if task.u <= us]
        
        print(f"High Priority Tasks: {high_prio}")
        print(f"Low Priority Tasks: {low_prio}")
        
        return T.u < umax
    
    def fpedf(self, T) -> bool:
        """
        First Priority Earliest Deadline First
        
        Parameters:
        
            T: TaskSet -> task set that should be scheduled
            
        Returns:
        
            bool -> True if scheduling was successful
        """
        self.reset()
        
        m = self.core_count
        umax = (m - 1)/2
        
        T = T.sort('u')
        alpha = T.taskset[-1].u

        high_prio = [task for task in T.taskset if task.u > 0.5]
        low_prio = [task for task in T.taskset if task.u <= 0.5]

        print(f"High Priority Tasks: {high_prio}")
        print(f"Low Priority Tasks: {low_prio}")
        
        return alpha <= 0.5 or T.u <= umax