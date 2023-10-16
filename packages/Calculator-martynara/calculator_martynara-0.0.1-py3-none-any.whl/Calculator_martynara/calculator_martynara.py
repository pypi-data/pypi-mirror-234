# Calculator project

'''
A Calculator class capable of performing five arithmetic operations and store a memory value.
'''
class Calculator:

    def __init__(self, memory = 0, number = 0):
        '''
        Initializes the Calculator instance.
        '''
        self.memory = memory    # memory (float, optional, default is 0)
        self.number = number    # number (float, optional, default is 0)
        
    def insert(self, number):
        '''
        Inserts the first number and updates the memory value.
        '''
        self.memory = number    # number (float) - the number to update the memory with.
        return self.memory      # return float - the updated memory value.
    
    def add(self, number):
        '''
        Performs addition by adding the provided number to the memory value.
        '''
        self.memory += number   # number (float) - the number to be added.
        return self.memory      # return float - the updated memory value.

    def subtract(self, number):
        '''
        Performs subtraction by subtracting the provided number from the memory value.
        '''
        self.memory -= number   # number (float) - the number to be subtracted.
        return self.memory      # return float - the updated memory value.
    
    def multiply(self, number):
        '''
        Performs multiplication by multiplying the memory value by the provided number.
        '''
        self.memory *= number   # number (float) - the number to multiply by.
        return self.memory      # return float - the updated memory value.
    
    def divide(self, number):
        '''
        Performs division by dividing the memory value by the provided number.
        '''
        self.memory /= number   # number (float) - the number to divide by.
        return self.memory      # return float - the updated memory value.
    
    def root(self, power):
        '''
        Calculates the root of the memory value with the specified power.
        '''
        self.memory = round(self.memory**(1/power))
                                # number (float) - the number to calculate the root of.
                                # power (float)- the power to use for the root operation.
        return self.memory      # return float - the updated memory value.
    
    def reset(self):
        '''
        Resets the memory value to 0.
        '''
        self.memory = 0         # return float - the updated memory value (0).
        return self.memory


