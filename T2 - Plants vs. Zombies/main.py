import sys
from dccruz import Game


if __name__ == '__main__':
    def hook(type_, value, traceback):
        print(type_)
        print(traceback)
    sys.__excepthook__ = hook

    game = Game(sys.argv)
    game.comenzar()

    sys.exit(game.exec())