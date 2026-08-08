# Coffee -> 
#     Starbhucks
#     Latte -> 5
#     Whipped Cream 15
#     AlmondMilk -> 60
#     Chocochip -> 20
#     SizeLarge -> 1.2x

# message -> 
#     Latte with Whipped Cream and  Almond Milk, Choco Chip, Large Size


from abc import ABC, abstractmethod

class Coffee(ABC):
    @abstractmethod
    def getCost(self):
        pass

    @abstractmethod
    def getMessage(self):
        pass

class Latte(Coffee):
    def __init__(self):
        self.latteCost = 5

    def getCost(self):
        return self.latteCost

    def getMessage(self):
        return ['latte']

class WhippedCreame(Coffee):
    def __init__(self, inner):
        self.whippedCreame = 15
        self.inner = inner

    def getCost(self):
        return self.inner.getCost() + self.whippedCreame

    def getMessage(self):
        return self.inner.getMessage() + ['WhippedCreame']

class AlmondMilk(Coffee):
    def __init__(self, inner):
        self.almondM = 60
        self.inner = inner

    def getCost(self):
        return self.inner.getCost() + self.almondM

    def getMessage(self):
        return self.inner.getMessage() + ['AlmondMilk']

class NormalMilk(Coffee):
    def __init__(self, inner):
        self.normalM = 15
        self.inner = inner

    def getCost(self):
        return self.inner.getCost() + self.normalM

    def getMessage(self):
        return self.inner.getMessage() + ['NormalMilk']
    
class ChocoChip(Coffee):
    def __init__(self, inner):
        self.ChocoC = 20
        self.inner = inner

    def getCost(self):
        return self.inner.getCost() + self.ChocoC

    def getMessage(self):
        return self.inner.getMessage() + ['ChocoChip']

class SizeSmall(Coffee):
    def __init__(self, inner):
        self.smallSizeCost = 1.5
        self.inner = inner

    def getCost(self):
        return self.inner.getCost() * self.smallSizeCost

    def getMessage(self):
        return self.inner.getMessage() + ['SizeSmall']

class SizeMedium(Coffee):
    def __init__(self, inner):
        self.mediumSizeCost = 2
        self.inner = inner

    def getCost(self):
        return self.inner.getCost() * self.mediumSizeCost

    def getMessage(self):
        return self.inner.getMessage() + ['SizeMedium']

class SizeLarge(Coffee):
    def __init__(self, inner):
        self.largeSizeCost = 3
        self.inner = inner

    def getCost(self):
        return self.inner.getCost() * self.largeSizeCost

    def getMessage(self):
        return self.inner.getMessage() + ['SizeLarge']

class CoffeeOther(ABC):
    @abstractmethod
    def getMoney(self):
        pass

    @abstractmethod
    def getString(self):
        pass

class SizeLarge(CoffeeOther):
    def __init__(self, inner):
        self.largeSizeCost = 3
        self.inner = inner

    def getMoney(self):
        return self.inner.getCost() * self.largeSizeCost

    def getString(self):
        return self.inner.getMessage() + ['SizeLarge']

class LargeSizeAdapter(Coffee):
    def __init__(self, n):
        self.n = n

    def getCost(self):
        return self.n.getMoney()

    def getMessage(self):
        return self.n.getString()


coffee = Latte()
coffee = WhippedCreame(coffee)
coffee = LargeSizeAdapter(SizeLarge(coffee))
coffee = AlmondMilk(coffee)

print(coffee.getMessage())
print(coffee.getCost())
