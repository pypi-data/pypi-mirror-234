class Calculator:
    """
    A simple calculator class that allows performing basic arithmetic operations
    and maintains a memory value that can be accessed after each operation.

    Attributes:
        memory (float): The current value stored in the calculator's memory.

    Methods:
        add(num: float) -> float:
            Add a number to the current memory value and return the updated memory.

        subtract(num: float) -> float:
            Subtract a number from the current memory value and return the updated memory.

        multiply(num: float) -> float:
            Multiply the current memory value by a number and return the updated memory.

        divide(num: float) -> float:
            Divide the current memory value by a number and return the updated memory.
            Raises a ValueError if 'num' is zero.

        nth_root(n: float) -> float:
            Compute the nth root of the current memory value and return the result.
            Raises a ValueError if 'n' is even and the memory value is negative.

        reset() -> float:
            Reset the calculator's memory to zero and return the new memory value.
    """

    def __init__(self):
        """
        Initialize a new Calculator object with memory set to zero.
        """
        self.memory: float = 0

    def add(self, num: float) -> float:
        """
        Add 'num' to the current memory value and return the updated memory.

        Args:
            num (float): The number to add to the memory.

        Returns:
            float: The updated memory value after addition.
        """
        self.memory += num
        return self.memory

    def subtract(self, num: float) -> float:
        """
        Subtract 'num' from the current memory value and return the updated memory.

        Args:
            num (float): The number to subtract from the memory.

        Returns:
            float: The updated memory value after subtraction.
        """
        self.memory -= num
        return self.memory

    def multiply(self, num: float) -> float:
        """
        Multiply the current memory value by 'num' and return the updated memory.

        Args:
            num (float): The number to multiply with the memory.

        Returns:
            float: The updated memory value after multiplication.
        """
        self.memory *= num
        return self.memory

    def divide(self, num: float) -> float:
        """
        Divide the current memory value by 'num' and return the updated memory.

        Args:
            num (float): The number to divide the memory by.

        Returns:
            float: The updated memory value after division.

        Raises:
            ValueError: If 'num' is zero.
        """
        if num == 0:
            raise ValueError("Division by zero is not allowed")
        self.memory /= num
        return self.memory

    def nth_root(self, n: float) -> float:
        """
        Compute the nth root of the current memory value and return the result.

        Args:
            n (float): The degree of the root to compute.

        Returns:
            float: The result of computing the nth root of the memory.

        Raises:
            ValueError: If 'n' is even and the memory value is negative.
        """
        if self.memory < 0 and n % 2 == 0:
            raise ValueError("Cannot take an even root of a negative number")
        self.memory = self.memory ** (1 / n)
        return self.memory

    def reset(self) -> float:
        """
        Reset the calculator's memory to zero and return the new memory value.

        Returns:
            float: The memory value after resetting, which is always zero.
        """
        self.memory = 0
        return self.memory
