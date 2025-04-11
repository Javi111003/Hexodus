from random import Random

from src.Utils.Algorithms.A_star import a_star_hex
from src.Core.HexGame import HexGame
from src.Entities.HexBoard import HexBoard
from src.Entities.AIPlayer import AIPlayer
from src.Entities.RandomPlayer import RandomPlayer


def main():
    print("=== JUEGO HEX ===")
    print("Instrucciones:")
    print("- 🟥 (Rojo: 1) debe conectar los lados izquierdo y derecho")
    print("- 🟦 (Azul: 2) debe conectar los lados superior e inferior")
    print("- Ingresa movimientos como 'fila columna' (ej. '5 5')")

    matrix = [
                  [0,0,0,0,0],
                  [0,0,0,0,0],
                  [0,0,0,0,0],
                  [0,0,0,0,0],
                  [0,0,0,0,0]]

    init_board = HexBoard(size=25)
    game = HexGame(size=25)
    ai2 = RandomPlayer(2)
    ai1 = AIPlayer(1)
    a_star_test = a_star_hex(init_board, 1)
    print(f"la cantidad minima de movimientos necesarios es {a_star_test}")
    while not game.game_over:
        game.print_board()
        print(f"\nTurno del jugador {game.current_player_id}")

        while True:
            try:
                if game.current_player_id == 1:  # Jugador 1 (IA)
                    move = ai1.play(game.hex_board)
                else:  # Jugador 2 (humano)
                    #move = input("Ingresa tu movimiento (fila columna): ").strip().split()
                    move = ai2.play(game.hex_board)
                row, col = map(int, move)
                success, message = game.make_move(row, col)

                if not success:
                    print(message)
                    continue
                if message:  # Mensaje de victoria
                    print(message)
                break
            except ValueError:
                print("Por favor ingresa números válidos")
            except KeyboardInterrupt:
                print("\nJuego terminado por el usuario")
                return

    game.print_board()
    print(f"\n¡Juego terminado! Ganador: {game.winner}")


if __name__ == "__main__":
    main()