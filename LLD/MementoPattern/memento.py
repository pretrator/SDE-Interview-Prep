class Typing():
    def __init__(self, ):
        self.content = ""

    def typeIt(self, chr):
        self.content += " " + chr
        print(self.content)

    def save(self):
        return TypeMemento(self.content)

    def restore(self, memento):
        self.content = memento.content
        print(self.content)

class TypeMemento():
    def __init__(self, content):
        self.content = content

class UndoManager():
    def __init__(self):
        self.stack = []

    def onSave(self, memento):
        self.stack.append(memento)

    def restore(self):
        return self.stack.pop()

class TypeManager():
    def __init__(self):
        self.type = Typing()
        self.undoManager = UndoManager()

    def saveState(self):
        memento = self.type.save()
        self.undoManager.onSave(memento)

    def typed(self, txt):
        self.saveState()
        self.type.typeIt(txt)
        
    def commandZ(self):
        mem = self.undoManager.restore()
        self.type.restore(mem)


tpManager = TypeManager()
tpManager.typed('Changu')
tpManager.typed('Mangu')
tpManager.typed('pucchu ')
tpManager.typed('la')
tpManager.typed('billu')
tpManager.commandZ()
tpManager.commandZ()
tpManager.commandZ()
tpManager.typed('Quack Quack')
tpManager.typed('Woof Woof')
tpManager.typed('Meow Meow')
tpManager.commandZ()
tpManager.commandZ()
tpManager.commandZ()