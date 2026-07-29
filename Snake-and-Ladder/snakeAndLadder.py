# Add any additional imports here
from abc import ABC, abstractmethod
from collections import defaultdict
import uuid
from dataclasses import dataclass
import random


class Player():
    #  Need to make this frozen maybe by using setters
    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name

    

class DiceInterface(ABC):
    @abstractmethod
    def roll():
        pass

class Dice(DiceInterface):
    def __init__(self, faceCount):
        self.faceCount = faceCount

    def roll(self):
        return random.randint(1, self.faceCount)


# Save all players state
# Add a new rule class
class BoardInterface(ABC):
    @abstractmethod
    def getPosition(self, player):
        pass
    
    @abstractmethod
    def updatePlayerPosition(self, newPosition, player):
        pass

class Board:
    def __init__(self, boardSize, players, boardEntities):
        self._boardSize = boardSize
        self._players = players
        self._playerPosition = defaultdict(int)
        self._boardEntities = boardEntities

    def getPosition(self, player):
        return self._playerPosition[player.id]
    
    def updatePlayerPosition(self, newPosition, player):
        entityEffect = newPosition
        for entity in self._boardEntities:
            entityEffect = entity.effect(entityEffect)
        self._playerPosition[player.id] = entityEffect
        return entityEffect, entityEffect >= self._boardSize
    


class BoardEntityInterface(ABC):
    @abstractmethod
    def effect(self, position):
        pass

class Snakes(BoardEntityInterface):
    # Can keep a snake validator that a snake only takes you down not upp
    def __init__(self, snakeList):
        self.snakeList = dict(snakeList)
    
    def effect(self, position):
        if(position in self.snakeList):
            return self.snakeList[position]
        return position

class Ladder(BoardEntityInterface):
    # Can keep a ladder validator that a ladder only takes you up not down
    def __init__(self, ladderList):
        self.ladderList = dict(ladderList)
    
    def effect(self, position):
        if(position in self.ladderList):
            return self.ladderList[position]
        return position
    
class GamePlayInterface(ABC):
    pass

class GamePlay(GamePlayInterface):
    def __init__(self, players, dice, board):
        self._players = players
        self._dice = dice
        self._board = board
        self.currentPlayer = 0  # starting with first players chance
        self._isGameEnded = False
        self.winner = None
    
    def _playTurn(self):
        player = self._players[self.currentPlayer]
        print("Chance of ", player.name)
        position = self._board.getPosition(player)
        roll = self._dice.roll()
        newPosition = position + roll
        newPos, isWon = self._board.updatePlayerPosition(newPosition, player)
        print(player.name, "Rolled ", roll, isWon, newPosition)
        return roll, isWon
    
    def setWon(self, player):
        self.winner = player
        self._isGameEnded = True

    def playChance(self):
        if(self._isGameEnded): print("Game Already Ended")
        player = self._players[self.currentPlayer]
        originalPos = self._board.getPosition(player)
        roll, isWon = self._playTurn()
        if(isWon): return self.setWon(player)
        depth = 0
        while(roll == 6 and depth < 3): 
            roll, isWon = self._playTurn()
            if(isWon): return self.setWon(player)
            depth += 1
        if(depth == 3): self._board.updatePlayerPosition(originalPos, player)
        self.currentPlayer = (self.currentPlayer + 1) % len(self._players)
        return 
    
    def playGame(self):
        while(not self._isGameEnded):
            self.playChance()
        print("Winner Is ", self.winner.name)






# Create instances of your classes and test your solution here
def main():
    player1 = Player("Chiya")
    player2 = Player("Kukku")
    players = [player1, player2]
    ladder = Ladder([(0, 15), (6, 17), (3, 50), (27, 74), (35, 47), (55, 75)])
    snakes = Snakes([(74, 6), (55, 15), (97, 59), (39, 13), (99, 27)])
    board = Board(
        100,
        players,
        [ladder, snakes]
    )
    dice = Dice(6)
    gameplay = GamePlay(players, dice, board)
    gameplay.playGame()

if __name__ == "__main__":
    main()
