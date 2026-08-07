class Beverage:
    def __init__(self):
        pass
        
    def step1(self):
        print('Bhagona on the flame')

    def step2(self):
        print('Pani in the bhagona')

    def step3(self):
        print('Switch on the gas')
        
    def step4(self):
        print('Doodh daalo')

    def step5(self):
        print('Cheeni Daalo')

    def step6(self):
        raise NotImplementedError('')
    
    def step7(self):
        print('Adrak daalo')

    def step8(self):
        print('Wait for 10 min')

    def step9(self):
        print('Filter in the cup')

    def beveragebanao(self):
        self.step1()
        self.step2()
        self.step3()
        self.step4()
        self.step5()
        self.step6()
        self.step7()
        self.step8()
        self.step9()


class Tea(Beverage):
    def __init__(self):
        pass

    def step6(self):
        print("chai patti daalo")
        

class Coffee(Beverage):
    def step2(self):
        pass

    def step6(self):
        print('coffee daalo')

    def step7(self):
        pass

t = Tea()
t.beveragebanao()
print('//////////////////////')
c = Coffee()
c.beveragebanao()