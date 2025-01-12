# chess_game.py
import chess.engine
import chess
from chessboard import ChessBoard
import time
from display import start_server

class ChessGame:
    def __init__(self):
        self.board = ChessBoard()
        self.engine = chess.engine.SimpleEngine.popen_uci("stockfish")
    
    def engine_move(self, think_time=0.01):
        result = self.engine.play(self.board.board, chess.engine.Limit(time=think_time))
        self.board.board.push(result.move)
        return str(result.move)
    
    def player_move(self, move_uci):
        try:
            move = chess.Move.from_uci(move_uci)
            if move in self.board.board.legal_moves:
                self.board.board.push(move)
                return True
        except ValueError:
            pass
        return False
    
    def update_display(self):
        self.board.display("game.svg")
    
    def is_game_over(self):
        return self.board.board.is_game_over()
    
    def get_result(self):
        return self.board.get_result()
    
    def close(self):
        self.engine.quit()

def play_vs_stockfish():
    server = start_server()
    game = ChessGame()
    
    print("Play as White against Stockfish!")
    print("Enter moves in UCI format (e.g., e2e4, g1f3)")
    print("Type 'quit' to end the game\n")
    
    game.update_display()
    
    try:
        while not game.is_game_over():
            # Player's turn
            while True:
                move = input("\nYour move: ").strip().lower()
                if move == 'quit':
                    return
                if game.player_move(move):
                    break
                print("Illegal move! Try again.")
            
            game.update_display()
            if game.is_game_over():
                break
            
            # Engine's turn
            print("\nStockfish is thinking...")
            engine_move = game.engine_move()
            print(f"Stockfish plays: {engine_move}")
            game.update_display()
        
        print(f"\nGame Over! Result: {game.get_result()}")
    
    finally:
        game.close()
        server.server_close()

def stockfish_vs_stockfish():
    server = start_server()
    game = ChessGame()
    
    try:
        while not game.is_game_over():
            move = game.engine_move()
            print(f"Move played: {move}")
            game.update_display()
            time.sleep(1)  # Pause to see the position
        
        print(f"\nGame Over! Result: {game.get_result()}")
    
    finally:
        game.close()
        server.server_close()

if __name__ == "__main__":
    mode = input("Select mode (1 for Engine vs Engine, 2 for Human vs Engine): ")
    if mode == "1":
        stockfish_vs_stockfish()
    else:
        play_vs_stockfish()