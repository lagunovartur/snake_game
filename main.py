from game import Game

game = Game()

while game.running:

    game.game_loop()

    if not game.KEYS['K_PAUSE']:
        game.curr_frame.display()
