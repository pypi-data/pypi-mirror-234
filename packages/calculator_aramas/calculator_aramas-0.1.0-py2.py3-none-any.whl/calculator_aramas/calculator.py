class Calculator:
    def __init__(self, memory=0.0):
        self.memory = memory
    
    def add(self, addend: float) -> float:
        """Performs addition on the value in memory
            >>> result = Calculator(memory=9.0).add(addend=3.0)
            >>> result
            12.0
        """
        self.memory += addend
        return self.memory
    
    def substract(self, subtrahend: float) -> float:
        """Performs substraction on the value in memory
            >>> result = Calculator(memory=9.0).substract(subtrahend=3.0)
            >>> result
            6.0
        """
        self.memory -= subtrahend
        return self.memory
    
    def multiply(self, multiplier: float) -> float:
        """Performs multiplication on the value in memory
            >>> result = Calculator(memory=9.0).multiply(multiplier=3.0)
            >>> result
            27.0
        """
        self.memory = self.memory*multiplier
        return self.memory
    
    def divide(self, divisor: float) -> float:
        """Performs division on the value in memory
            >>> result = Calculator(memory=9.0).divide(divisor=2.0)
            >>> result
            4.5
        """
        if divisor == 0:
            raise ValueError("Divisor cannot be zero.")
        
        self.memory = self.memory/divisor
        return self.memory
    
    def root(self, degree_of_root:float) -> float:
        """Takes (n) root of a value in memory
            >>> result = Calculator(memory=9).root(degree_of_root=2)
            >>> result
            3.0
        """
        if degree_of_root == 0:
            raise ValueError("Root degree cannot be zero.")
        
        # Handle case where memory is zero
        if self.memory == 0:
            if degree_of_root < 0:
                raise ValueError("Cannot raise 0 to a negative power")
            return 0

        # Handle negative numbers with even roots
        if self.memory < 0 and degree_of_root % 2 == 0:
            raise ValueError("Cannot compute even root for negative number")
        
        self.memory = self.memory**(1/degree_of_root)
        return self.memory
    
    def reset(self) -> None:
        """Resets the calculator's memory to 0."""
        self.memory = 0.0
    
if __name__=='__main__':
    import doctest
    print(doctest.testmod())