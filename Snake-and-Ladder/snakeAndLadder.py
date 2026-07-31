# Saanp and Sidhi 

# Requirement Gathering
# Functional Requirement 
# 1. Board jispar game khel sake
# 2. Dice ho jissey random number generate hoga
# 3. On reaching 100 the reached player is declared winner, no more moves after someone has won
#     - Need specific number to go to 100 not more can be less
# 4. No bar on player count
# 5. Specific dice number to for opening 
# 5. Ladder will take you up somewhere
# 6. Snake will take you down somewhere
# 7. Alternative turns
# 8. 6 give more turns
#     - 3 6s sadd jata hai
# 9. 

# Non - Functional Requirements
# 1. Maintainability
# 2. Extendibility
# 3. User feedback -> print() on console


# Entity
# 1. Board
    # -> board
    #     -> players
    #     -> snakes 
    #     -> ladders
    #     -> start and end

# 2. Player
    # -> name
    # -> id

# 3. Snake
    # start is always bigger then end validate it
    # start 
    # end

# 4. Ladder
    # end is always bigger then start (validate it)
    # start
    # end

# 5. Dice
    # faceCount 
    # roll -> 1 -> facecount -> random
    # seed addition

# 6. GameState
    # ONGOING
    # WON

# 7. Rules
    # Rule will contain logic logic of multiple 6
    # Opening Rule
    # Winning Rule

# 8. ChanceManager
    # will execute chance logic given states of the player
    # nextTurn 
        # Will check rule and tell whose turn is next
    # currentTurn


# 9. GamePlay

# Any real world system
    # Encapsulation 
    # Open closed principle -> 
    #     Open for extension 
    #     Closed for modification


from abc import ABC, abstractmethod
import random
from enum import Enum
import uuid

BOARD_START_POS = 1
ELIGIBLE_FIRST_FACE_VALUES = [6]
TURN_CANCELLATION_NUMBER = 6

class DiceInterface(ABC):
    @abstractmethod
    def roll():
        pass

class Dice(DiceInterface):
    def __init__(self, facecount, seed = None):
        self._faceCount = facecount
        if(seed is not None):
            random.seed(seed)

    def roll(self):
        return random.randint(1, self._faceCount)


class GameStates(Enum):
    ONGOING = "ONGOING"
    WON = "WON"

class BoardEntity(ABC):
    @abstractmethod
    def effect():
        pass

class Snake(BoardEntity):
    # The head and the tail of the snake heed to be inclusive of the board range
    def __init__(self, head, tail):
        if(head < tail):
            raise ValueError("Snakes cannot have tail above head")
        self._head = head
        self._tail = tail
    
    def effect(self, currentPos):
        if(currentPos == self._head):
            print("Snake Bite", self._tail)
            return self._tail
        return currentPos

class Ladder(BoardEntity):
    # The top and bottom of the Ladder need to be inclusive of the board range
    def __init__(self, bottom, top):
        if(top < bottom):
            raise ValueError("Ladder cannot have top below bottom, its Crazy")
        self._top = top
        self._bottom = bottom
    
    def effect(self, currentPos):
        if(currentPos == self._bottom):
            print("Ladder", self._top)
            return self._top
        return currentPos


class Player():
    def __init__(self, name):
        self._name = name
        self._id = str(uuid.uuid4())
    
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name



class ChanceManagerInterface(ABC):
    @abstractmethod
    def nextTurn(self, faceValue):
        pass
    
    @abstractmethod
    def getCurrentPlayer(self):
        pass
    
    @abstractmethod
    def getCurrentPlayerTurnCount(self):
        pass


# 8. ChanceManager
    # will execute chance logic given states of the player
    # nextTurn 
        # Will check rule and tell whose turn is next
    # currentTurn

class ChanceManager(ChanceManagerInterface):
    def __init__(self, players, startingPlayerIdx, rules):
        self._players = players
        self._currentChance = startingPlayerIdx
        self._countTurns = 0
        self._rules = rules

    def nextTurn(self, faceValue):
        isNextPlayersTurn = self._rules.isNextPlayersTurn(faceValue, self._countTurns)
        if(isNextPlayersTurn):
            self._currentChance = (self._currentChance + 1) % len(self._players)
            self._countTurns = 0
            return self.getCurrentPlayer()
        self._countTurns += 1
        return self.getCurrentPlayer()
    
    def getCurrentPlayer(self):
        return self._players[self._currentChance]
    
    def getCurrentPlayerTurnCount(self):
        return self._countTurns
    


class RuleInterface(ABC):
    @abstractmethod
    def isWon(self, player):
        pass
    
    @abstractmethod
    def moveEligibility(self, faceValue, player, countTurns):
        pass
    
    @abstractmethod
    def isNextPlayersTurn(self, faceValue, countTurns):
        pass

# 7. Rules
    # Rule will contain logic logic of multiple 6
    # Opening Rule
    # Winning Rule

class RuleSet1(RuleInterface):
    def __init__(self, board):
        self._board = board
        self._eligibleFirstFaceValues = ELIGIBLE_FIRST_FACE_VALUES
        self._turnCanCellation = TURN_CANCELLATION_NUMBER

    def isWon(self, player):
        position = self._board.getPlayerPosition(player)
        return self._board._winningPos == position

    def moveEligibility(self, faceValue, player, countTurns):
        position = self._board.getPlayerPosition(player)
        # 666 cancellation of move
        if(faceValue == self._turnCanCellation and countTurns == 2):
            return False
        
        if(position == self._board.startPos):
            if(faceValue in self._eligibleFirstFaceValues): return True
            return False
        elif(position + faceValue > self._board.winningPos):
            return False
        return True
    
    def isNextPlayersTurn(self, faceValue, countTurns):
        if(faceValue == self._turnCanCellation and countTurns < 3):
            return True
        if(faceValue == self._turnCanCellation):
            return False
        return True
        


# input -> faceValue, position
# return -> whoseTurn, eligibleToMove

# opening rule
#     -> eligible to move or not
# winning rule
#     -> if it has reached 100 it is a win
#     -> eligible to move or not given it is near 100
# triple 6 rule
#     -> Invalidate all the last 3 turns
#     -> give turn to other
# multi6 rule
#     -> on a 6 do not give chance to other

class BoardInterface(ABC):
    @abstractmethod
    def entityEffect(self, position):
        pass
    
    @abstractmethod
    def setPosition(self, moveCount, player):
        pass
    
    @abstractmethod
    def getPlayerPosition(self, player):
        pass

class Board(BoardInterface):
    # Board is always a square
    def __init__(self, sideSize, startPos, boardEntity = [], players = []):
        self._sideSize = sideSize
        self._startingPos = BOARD_START_POS # start position never change
        self._winningPos = (self._sideSize * self._sideSize)
        self._boardEntity = boardEntity
        self._players = players
        self._playerPositions = dict([(player.id, self._startingPos) for player in self._players])
    
    @property
    def winningPos(self):
        return self._winningPos
    
    @property
    def startPos(self):
        return self._startingPos
    
    def entityEffect(self, position):
        for entity in self._boardEntity:
            position = entity.effect(position)
        return position

    def setPosition(self, moveCount, player):
        oldPos = self._playerPositions[player.id]
        newPos = oldPos + moveCount
        newPosition = self.entityEffect(newPos)
        print("Final position of", player.name, newPosition)
        self._playerPositions[player.id] = newPosition
    
    def getPlayerPosition(self, player):
        return self._playerPositions[player.id]
    
    def addBoardEntity(self, entity):
        self._boardEntity.append(entity)
        return self
    
    def addPlayer(self, player):
        self._players.append(player)
        self._playerPositions[player.id] = self._startingPos
        return self


class GamePlay():
    def __init__(self, chanceManager = None, dice = None, board = None, rules = None):
        self._gameState = GameStates.ONGOING
        self._chanceManager = chanceManager
        self._dice = dice
        self._board = board
        self._rules = rules
        self._winner = None

    def _updateGameStatus(self, player):
        isPlayerWon = self._rules.isWon(player)
        if(isPlayerWon):
            self._gameState = GameStates.WON
            self._winner = player

    def playGame(self):
        if(self._chanceManager is None or self._dice is None or self._board is None or self._rules is None):
            return print("Complete Initialtion to play the game")
        while(self._gameState == GameStates.ONGOING):
            playerWithChance = self._chanceManager.getCurrentPlayer()
            print("Chance of ", playerWithChance.name)
            faceValue = self._dice.roll()
            print("Rolled Value", faceValue)
            turnCount = self._chanceManager.getCurrentPlayerTurnCount()
            isMoveEligible = self._rules.moveEligibility(faceValue, playerWithChance, turnCount)
            if(isMoveEligible): 
                print("Allowed to move")
                self._board.setPosition(faceValue, playerWithChance)
            self._updateGameStatus(playerWithChance)
            self._chanceManager.nextTurn(faceValue)
        print("Player", self._winner.name, "has won")

    def setChanceManager(self, chanceManager):
        self._chanceManager = chanceManager
        return self
    
    def setDice(self, dice):
        self._dice = dice
        return self
    
    def setBoard(self, board):
        self._board = board
        return self
    
    def setRules(self, rules):
        self._rules = rules
        return self
            
if __name__ == "__main__":
    players = [Player("Chiya"), Player("Lucky")]
    board = (Board(10, 0)
        .addBoardEntity(Snake(12, 6))
        .addBoardEntity(Snake(99, 10))
        .addBoardEntity(Snake(90, 70))
        .addBoardEntity(Ladder(2, 45))
        .addBoardEntity(Ladder(22, 72))
        .addBoardEntity(Ladder(15, 20))
        .addPlayer(players[0])
        .addPlayer(players[1])
    )

    rules = RuleSet1(board)
    chanceManager = ChanceManager(players, 0, rules)
    gamePlay = (GamePlay()
                    .setDice(Dice(6))
                    .setBoard(board)
                    .setRules(rules)
                    .setChanceManager(chanceManager)
                    .playGame()
    )
# We have allowed multiple players to occupy same position