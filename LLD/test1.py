# Calculator

# c = Calculator()
    # - input
    # - add
    # - equal 

# c.input(2)
#  .add()
#  .input(6)
#  .equals()

# prints -> 8

# class Calculator




class Calculator:
    def __init__(self):
        self.expr = ""

    def input(self, num):
        self.expr += str(num)
        return self
    
    def add(self):
        self.expr += "+"
        return self

    def minus(self):
        self.expr += "-"
        return self

    def multi(self):
        self.expr += '*'
        return self
        
    def equals(self):
        print(eval(self.expr))
        return self

c = Calculator()
c.input(2).add().input(6).equals()