# Requirement Gathering 
# Functional Requirement
# 1. Board of 3x3 (always 3 x 3)
# 2. Players always 2 (NEver more or less then 2)
# 3. Alternating turns
# 4. No game after winner being declared
# 5. Game end on khichdi and no winner declared (Draw)
# 6. Game states (Ongoing, Win, draw)
# 7. Two players each ahving their particular symbol
# 8. Start with o
# 9. Rules will decide winner



# Non Functional Requirement
# 1. Have good extensability
# 2. Good reusability
# 3. Reset button


# Classes -> 
#     Open for extension 
#     Closed for change


# Entities
# Board 
#     -> 2d 3x3 grid
#     -> addPlayerMark()
#     -> getBoard()

# Player
#     -> name
#     -> symbol
#     -> id

# Rules
#     -> getCurrentBoardState() -> BoardStates

# BoardStates
#     Ongoing
#     Won
#     Draw

# # ChanceManager -> 
# #     # HAndles chances of next player until end of the game

# GamePlayManager
#     # If game is in state of Won or Draw end it
#     # If game is not started Give player 0 a chance not x
#     -> He is responsible for giving chace to other player
#     -> He is responsible for handling winning and draw states


# Interactions -> 
# 1. GamePlayManager -> Rules
# 2. Player -> Board
# 3. Give chance to other player
# 4. Self Decision -> 
#     On winning declare a winner and end the game
#     On draw just End the game



from enum import Enum
from abc import ABC, abstractmethod
import uuid
from collections import Counter

BOARD_SIZE = 3

class BoardStates(Enum):
    ONGOING = "ONGOING"
    WON = "WON"
    DRAW = "DRAW"

class Symbol(Enum):
    CIRCLE = "O"
    CROSS = "X"

class PlayerInterface(ABC):
    pass

class Player(PlayerInterface):
    # Need validation to ensure no 2 player have same symbol
    def __init__(self, name, symbol, board):
        self._id = str(uuid.uuid4())
        self._name = name
        self._symbol = symbol
        self._board = board
    
    def makeMove(self):
        position = map(int, input("Enter pos: ").split(","))
        self._board.addMark(position, self._symbol)
    
    @property
    def symbol(self):
        return self._symbol
    
    @property
    def name(self):
        return self._name
    
    @property
    def id(self):
        return self._id

class BoardInterface(ABC):
    @abstractmethod
    def getBoard(self):
        pass
    
    @abstractmethod
    def addMark(self, position, symbol):
        pass

class Board(BoardInterface):
    def __init__(self):
        # Side effect but okay since this is known to be constant throughout
        self._boardSize = BOARD_SIZE
        self._board = [[None] * self._boardSize for i in range(self._boardSize)]
    
    def getBoard(self):
        return self._board;
    
    def addMark(self, position, symbol):
        i, j = position
        if(self._board[i][j] is not None): return False
        self._board[i][j] = symbol
        return True
    
    def printBoard(self):
        print("###########")
        for row in self._board:
            print(list(map(lambda x: x.value if x is not None else None, row)))
        print("###########")

class RulesInterface(ABC):
    @abstractmethod
    def getBoardState(self, board):
        pass

class RulesSet1(RulesInterface):
    def __init__(self):
        pass
    
    def _isSame(self, symbols):
        counts = Counter(symbols)
        countKeys = list(counts.keys())
        if(len(countKeys) == 1 and countKeys[0] is not None): 
            return True
        return False

    def _isWin(self, board):
        isWin = False

        # horizontal Check
        for i in range(len(board)):
            isSame = self._isSame(board[i])
            if(isSame): return True

        # Vertical check
        for i in range(len(board)):
            verticalArr = [board[j][i] for j in range(len(board))]
            isSame = self._isSame(verticalArr)
            if(isSame): return True
        
        # Forward Diagnol
        start, fd = 0, []
        for i in range(len(board)):
            fd.append(board[start + i][start + i])
        isSame = self._isSame(fd)
        if(isSame): return True

        # Backward Diagnol
        firstIdx, secondIdx, bd = 0, len(board) - 1, []
        for i in range(len(board)):
            bd.append(board[firstIdx + i][secondIdx - 1])
        isSame = self._isSame(fd)
        if(isSame): return True

        return False
    
    def _isDraw(self, board):
        for i in range(len(board)):
            for j in range(len(board)):
                if(board[i][j] is None):
                    return False
        return True

    def getBoardState(self, board):
        isWin = self._isWin(board.getBoard())
        if(isWin): return BoardStates.WON
        isDraw = self._isDraw(board.getBoard())
        if(isDraw): return BoardStates.DRAW
        return BoardStates.ONGOING

class ChanceManagerInterface(ABC):
    pass

class ChanceManager(ChanceManagerInterface):
    def __init__(self, players):
        self._currentChance = 0
        self._players = players
        self.sortPlayer()
    
    def sortPlayer(self):
        if(players[0].symbol != Symbol.CIRCLE):
            self._players = list(reversed(self._players))

    def nextChance(self):
        self._currentChance = (self._currentChance + 1) % (len(self._players))
        return self._players[self._currentChance]
    
    def getCurrentPlayer(self):
        return self._players[self._currentChance]

class GamePlayManager():
    def __init__(self, board, players, rules, chanceManager):
        self._board = board
        self._players = players
        self._gameState = BoardStates.ONGOING
        self._rules = rules
        self._chanceManager = chanceManager
        self._winner = None
    
    def setRules(self, rule):
        self._rules = rule
    
    def updateGameState(self):
        self._gameState = self._rules.getBoardState(self._board)
        

    def playGame(self):
        while(self._gameState == BoardStates.ONGOING):
            player = self._chanceManager.getCurrentPlayer()
            print("Chance of", player.name)
            self._board.printBoard()
            player.makeMove()
            self.updateGameState()
            if(self._gameState == BoardStates.WON): self._winner = player
            self._chanceManager.nextChance()
        print("Game Halted -> State = ", self._gameState)
        print("Winner is ", player.name)
        

if __name__ == "__main__":
    board = Board()
    player1 = Player("Chiya", Symbol.CROSS, board)
    player2 = Player("Kukku", Symbol.CIRCLE, board)
    players = [player1, player2]
    rule = RulesSet1()
    chanceManager = ChanceManager(players)
    gamePlayManager = GamePlayManager(board, players, rule, chanceManager)
    gamePlayManager.playGame()
