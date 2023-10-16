from calculator_martynara import Calculator

calculator = Calculator()

'''
Test the insert function
'''

if calculator.insert(1) == 1:
    pass
else:
    raise AssertionError("Error in insert function")

'''
Test the addition function
'''

calculator.add(2)
if calculator.add(3) == 6:
    pass
else:
    raise AssertionError("Error in addition function")

'''
Test the subtraction function
'''

calculator.subtract(1)
calculator.subtract(2)
if calculator.subtract(2) == 1:
    pass
else:
    raise AssertionError("Error in subtraction function")


'''
Test the multiplication function
'''

calculator.multiply(3)
if calculator.multiply(9) == 27:
    pass
else:
    raise AssertionError("Error in multiplication function")

'''
Test the division function
'''

calculator.divide(1)
if calculator.divide(3) == 9:
    pass
else:
    raise AssertionError("Error in division function")

'''
Test the root function
'''

if calculator.root(2) == 3:
    pass
else:
    raise AssertionError("Error in root function")

'''
Test the reset function
'''

if calculator.reset() == 0:
    pass
else:
    raise AssertionError("Error in reset function")
    

'''
Test multiple function
'''

# Test 1
calculator.add(1000000)
calculator.add(2000000)
calculator.subtract(100)
calculator.subtract(900)
calculator.multiply(3)
if calculator.divide(1000) == 8997:
    pass
else:
    raise AssertionError("Error found in multiple functions!")

# Test 2
calculator.reset()
calculator.insert(8)
calculator.multiply(8)
calculator.multiply(8)
if calculator.multiply(8) == 4096:
    pass
else:
    raise AssertionError("Error found in multiple functions!")

# Test 3
calculator.divide(8)
if calculator.root(3) == 8:
    pass
else:
    raise AssertionError("Error found in multiple functions!")

print("Test successfull")


