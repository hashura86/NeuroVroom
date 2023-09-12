from enum import Enum


class GameState(Enum):
    menu = 1
    game = 2
    game_over = 3
    about = 4

    def change_state(gameState, newState):
        return newState

 
            