import numpy


class PTask:
    """
    Periodic Task
    
    Parameters:
    
        p:  Period
        e:  Execution Time
        fi: Phase (0 by default)
        d:  (relative) Deadline (p by default)
        
    Attributes:
    
        u:   Utilization (e/p)
        xi:  ld(p) - floor(ld(p)) for Burchard Test
        pke: (m-1 + sqrt(5m^2 - 6m + 1)/2m) for Adaptive TkC
    """
    def __init__(self, p: float, e: float, fi: float = 0.0, d: float = None):
        self.p = p
        self.e = e
        self.fi = fi
        self.d = d if d is not None else p
        self.u = self.e / self.p
        self.xi = numpy.log2(self.p) - numpy.floor(numpy.log2(self.p))
        self.pke = 0

    def __eq__(self, __o: object) -> bool:
        if self.p == __o.p and self.e == __o.e and self.fi == __o.fi and self.d == __o.d:
            return True
        return False
        
    def __str__(self) -> str:
        return f"T({self.p},{self.e})"
    
    def __repr__(self) -> str:
        return f"T({self.p},{self.e})"