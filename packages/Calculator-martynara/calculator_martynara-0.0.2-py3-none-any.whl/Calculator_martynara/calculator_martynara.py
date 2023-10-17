# Calculator project

'''
A Calculator class capable of performing five arithmetic operations and storing a memory value.
'''
class Calculator:

    def __init__(self, memory = 0):
        '''
        Initializes the Calculator instance.
        Args:
            memory (float, optional): The initial memory value. Defaults to 0.
        '''
        self.memory = memory
        
    def insert(self, number) -> float:
        '''
        Inserts the first number and updates the memory value.

        Args:
            number (float): The number to update the memory with.

        Returns:
            float: The updated memory value.
        '''
        self.memory = number  
        return self.memory
    
    def add(self, number) -> float:
        '''
        Performs addition by adding the provided number to the memory value.

        Args:
            number (float): The number to be added.

        Returns:
            float: The updated memory value.
        '''
        self.memory += number
        return self.memory
    
    def subtract(self, number) -> float:
        '''
        Performs subtraction by subtracting the provided number from the memory value.

        Args:
            number (float): The number to be subtracted.

        Returns:
            float: The updated memory value.
        '''
        self.memory -= number
        return self.memory
    
    def multiply(self, number) -> float:
        '''
        Performs multiplication by multiplying the memory value by the provided number.

        Args:
            number (float): The number to multiply by.

        Returns:
            float: The updated memory value.
        '''
        self.memory *= number
        return self.memory

    def divide(self, number) -> float:
        '''
        Performs division by dividing the memory value by the provided number.

        Args:
            number (float): The number to divide by. Non-zero.

        Returns:
            float: The updated memory value.

        '''
        if number == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        
        result = self.memory / number
        self.memory = result
        return self.memory
    
    def root(self, power) -> float:
        '''
        Calculates the root of the memory value with the specified power.

        Args:
            power (float): The power to use for the root operation. Non-zero.

        Returns:
            float: The updated memory value, rounded up to 4 digits.

        '''
        if power == 0:
            print("Error: Cannot calculate the root with a power of 0.")
            return self.memory  
        try:
            result = round((self.memory ** (1 / power)),4)
        except ZeroDivisionError:
            # Handle division by zero
            print("Error: Division by zero is not allowed.")
            return self.memory

        self.memory = result
        return self.memory

    def reset(self) -> float:
        '''
        Resets the memory value to 0.

        Returns:
            float: The updated memory value (0).
        '''
        self.memory = 0
        return self.memory
