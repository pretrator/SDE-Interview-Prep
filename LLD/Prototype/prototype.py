import math

class Circle():
    def __init__(self, r):
        self.r = r

    def perimeter(self):
        return 2 * math.pi * self.r

    def area(self):
        return math.pi * self.r * self.r

    def getRadius(self):
        return self.r;

    def clone(self):
        return Circle(self.getRadius())

    def increaseRadius(self):
        self.r += 1

c1 = Circle(5)
c2 = c1.clone()

print(c1.area())
c1.increaseRadius()
print(c2.area())
print(c1.getRadius(), c2.getRadius())