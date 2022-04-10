from src.game import Game

game = Game(500, 500)

running = True
game.createOption("ok")
while running:
    game.checkEvents()