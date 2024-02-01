from framework.creature import Creature
from framework.level_base import LevelBase


class Level1(LevelBase):
    def __init__(self, screen, player):
        super().__init__(
            screen=screen,
            player=player,
            map_file='assets/Level1.tmx',
            #spawns={ 'steve': './assets/WiseWizard64.png'}
            spawns={
                'steve': Creature('./assets/WiseWizardSprites64.png'),
                'wickedwretch': Creature('./assets/WickedWretchSprites64.png'),
            }
        )
