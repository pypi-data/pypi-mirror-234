from typing import Union

Value = Union[int, float]


class Calculator:
    """
    A simple calculator that can do basic math operations.

    Calculator includes methods for addition, subtraction, multiplication,
    division, and nth root calculation. Calculator saves the returned values
    from each opperation in memory value. If not reset, memory value is used
    in the following operation.

    Attributes:
        memory_value (Value): Current calculator's memory value.
    """    

    def __init__(self) -> None:
        """
        Initializing a Calculator object with memory value of 0.
        
        Example:
        >>> calc = Calculator()
        >>> calc.memory_value
        0
        """
        self.memory_value = 0

    @staticmethod
    def validate_value(value: Value) -> None:
        """
        Validate that input value is numeric.
        
        Args:
            value: Value to be validated.
            
        Raises:
            TypeError: If input is not numeric.
        """
        if not isinstance(value, (int, float) or isinstance(value, bool)):
            raise TypeError("Input must be numeric!")

    def add(self, value: Value) -> Value:
        """
        Add input value to the memory.

        Args:
            value (Value): The value to be added.
        
        Returns:
            Value: Returns memory value after addition.
        
        Example:
        >>> calc = Calculator()
        >>> calc.add(5)
        5
        >>> calc.add(1.5)
        6.5
        >>> calc.reset_memory()
        """
        self.validate_value(value)
        self.memory_value += value
        return self.memory_value

    def subtract(self, value: Value) -> Value:
        """
        Subtract input value from the memory.

        Args:
            value (Value): Value to be subtracted from memory.
        
        Returns:
            Value: Updated memory value after subtraction.

        Example:
        >>> calc = Calculator()
        >>> calc.subtract(5)
        -5
        >>> calc.subtract(1.5)
        -6.5
        >>> calc.reset_memory()
        """
        self.validate_value(value)
        self.memory_value -= value
        return self.memory_value

    def multiply(self, value: Value) -> Value:
        """
        Multiply memory value by input value.

        Args:
            value (Value): Value by which to multiply memory value.

        Returns:
            Value: Updated memory value after multiplying.

        Example:
        >>> calc = Calculator()
        >>> calc.add(5)
        5
        >>> calc.multiply(5)
        25
        >>> calc.multiply(-0.5)
        -12.5
        >>> calc.reset_memory()
        """
        self.validate_value(value)
        self.memory_value *= value
        return self.memory_value

    def divide(self, value: Value) -> Value:
        """
        Divide memory value by given value.

        Args:
            value (Value): Value by which memory value is divided.
        
        Returns:
            Value: Updated memory value after division.

        Raises:
            ValueError: If value is 0.

        Example:
        >>> calc = Calculator()
        >>> calc.add(5)
        5
        >>> calc.divide(5)
        1.0
        >>> calc.divide(-0.5)
        -2.0
        >>> calc.reset_memory()
        """

        self.validate_value(value)
        if value != 0.0:
            self.memory_value /= value
            return self.memory_value
        else:
            raise ValueError("Cannot divide by zero!")

    def n_root(self, value: Value, n_root: Value) -> Value:
        """
        Calculate the nth root of the input value.

        Args:
            value (Value): Value for which nth root is calculated.
            n_root (Value): Degree by which root is calculated.
        
        Returns:
            Value: Calculated nth root of given value.

        Raises:
            ValueError: If n_root is 0 or if value (Value) is negative
                when n_root is even.

        Example:
        >>> calc = Calculator()
        >>> calc.n_root(25, 2)
        5.0
        >>> calc.n_root(0.125, 3)
        0.5
        >>> calc.reset_memory()
        """
        self.validate_value(value)
        self.validate_value(n_root)
        if n_root == 0:
            raise ValueError("Root by 0 is undefined!")
        if value >= 0.0:
            self.memory_value = value ** (1.0 / n_root)
            return self.memory_value
        elif n_root % 2 == 0 and value < 0.0:
            raise ValueError("Cannot calculate even root"
                             " of a negative number")
        else:
            value *= -1
            self.memory_value = -1 * value ** (1.0 / n_root)
            return self.memory_value



    def reset_memory(self) -> None:
        """
        Reset the memory value to 0.
        
        Example:
        >>> calc = Calculator()
        >>> calc.add(5)
        5
        >>> calc.reset_memory()
        >>> calc.memory_value
        0
        """
        self.memory_value = 0



