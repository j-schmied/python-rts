import numpy as np


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
            self.core_dict[f"C{i+1}"]["urm"] = 1
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
        
    def rmnf(self, T) -> bool:
        """
        Rate Monotonous Next Fit Scheduling.
        
        Parameters:
        
            T: TaskSet -> task set that should be scheduled
            
        Returns:
        
            bool -> True if scheduling was successful
        """
        self.reset()
        
        i = 0  # Taskindex
        j = 0  # Processorindex
        n = len(T)
        T = T.taskset
        
        while i < n:
            if j+1 > self.core_count:
                return False
            
            t_urm = (len(self.core_dict[f"C{j+1}"]["Tasks"])+1) * (np.power(2, 1/(len(self.core_dict[f"C{j+1}"]["Tasks"])+1)) - 1) 
            
            if self.core_dict[f"C{j+1}"]['u'] + (T[i].u) < t_urm:
                self.core_dict[f"C{j+1}"]["Tasks"].append(T[i])
                self.core_dict[f"C{j+1}"]['u'] += T[i].u
                self.core_dict[f"C{j+1}"]["urm"] = len(self.core_dict[f"C{j+1}"]["Tasks"]) * (np.power(2, 1/len(self.core_dict[f"C{j+1}"]["Tasks"])) - 1)
            else:
                self.core_dict[f"C{j+2}"]["Tasks"].append(T[i])
                j += 1
            
            i += 1
            
        return True
    
    def rmff(self, T) -> bool:
        """
        Rate Monotonous First Fit Scheduling.
        
        Parameters:
        
            T: TaskSet -> task set that should be scheduled
            
        Returns:
        
            bool -> True if scheduling was successful
        """
        self.reset()
        
        N = 1
        i = 0
        n = len(T)
        urm = T.urm
        T = T.taskset
        
        while i < n:
            j = 0
            
            if j+1 > self.core_count:
                return False

            t_urm = (len(self.core_dict[f"C{j+1}"]["Tasks"])+1) * (np.power(2, 1/(len(self.core_dict[f"C{j+1}"]["Tasks"])+1)) - 1) 
            
            while self.core_dict[f"C{j+1}"]['u'] + (T[i].u) > t_urm:
                j += 1
                
            self.core_dict[f"C{j+1}"]["Tasks"].append(T[i])
            self.core_dict[f"C{j+1}"]['u'] += T[i].u
            self.core_dict[f"C{j+1}"]["urm"] = len(self.core_dict[f"C{j+1}"]["Tasks"]) * (np.power(2, 1/len(self.core_dict[f"C{j+1}"]["Tasks"])) - 1)
            
            if j+1 > N:
                N = j+1
            
            i += 1 
            
        return True
    
    def rmffdu(self, T) -> bool:
        """
        Rate Monotonous First Fit with Decreasing Utilizations Scheduling
        
        Parameters:
        
            T: TaskSet -> task set that should be scheduled
            
        Returns:
        
            bool -> True if scheduling was successful
        """
        self.reset()
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
        return True
    
    def rmgt(self, T) -> bool:
        """
        Rate Monotonous General Task Scheduling
        
        Parameters:
        
            T: TaskSet -> task set that should be scheduled
            
        Returns:
        
            bool -> True if scheduling was successful
        """
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
        return True
    
    def edfbf(self, T) -> bool:
        """
        Earliest Deadline First Best Fit Scheduling
        
        Parameters:
        
            T: TaskSet -> task set that should be scheduled
            
        Returns:
        
            bool -> True if scheduling was successful
        """
        self.reset()
        return True
