from enum import Enum


class GameState(Enum):
    menu = 1
    game = 2
    about = 3
    score = 4
    config = 5 #iniciar game -> config -> game

    def change_state(newState):
        return newState

 
            