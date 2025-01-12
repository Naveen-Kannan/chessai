# chess_game.py
import chess.engine
import chess
from chessboard import ChessBoard
import time
from display import start_server
from custom_engine import CustomEngine

class ChessGame:
    def __init__(self, engine_type="stockfish"):
        self.board = ChessBoard()
        if engine_type == "stockfish":
            self.engine = chess.engine.SimpleEngine.popen_uci("stockfish")
            self.engine_type = "stockfish"
        else:
            self.engine = CustomEngine()
            self.engine_type = "custom"
    
    def engine_move(self, think_time=0.01):
        if self.engine_type == "stockfish":
            result = self.engine.play(self.board.board, chess.engine.Limit(time=think_time))
            self.board.board.push(result.move)
            return str(result.move)
        else:
            move = self.engine.select_move(self.board.board)
            self.board.board.push(move)
            return str(move)
    
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
        if self.engine_type == "stockfish":
            self.engine.quit()

def custom_vs_custom():
    server = start_server()
    game = ChessGame(engine_type="custom")
    
    print("Custom Engine vs Custom Engine")
    try:
        while not game.is_game_over():
            move = game.engine_move()
            print(f"Move played: {move}")
            game.update_display()
            time.sleep(1)
        
        print(f"\nGame Over! Result: {game.get_result()}")
    
    finally:
        game.close()
        server.server_close()

def stockfish_vs_custom():
    server = start_server()
    game_as_white = ChessGame(engine_type="custom")
    stockfish = chess.engine.SimpleEngine.popen_uci("stockfish")
    
    print("Custom Engine (White) vs Stockfish (Black)")
    try:
        while not game_as_white.is_game_over():
            # Custom engine's move
            move = game_as_white.engine_move()
            print(f"Custom Engine plays: {move}")
            game_as_white.update_display()
            time.sleep(1)
            
            if game_as_white.is_game_over():
                break
                
            # Stockfish's move
            result = stockfish.play(game_as_white.board.board, chess.engine.Limit(time=0.01))
            game_as_white.board.board.push(result.move)
            print(f"Stockfish plays: {result.move}")
            game_as_white.update_display()
            time.sleep(1)
        
        print(f"\nGame Over! Result: {game_as_white.get_result()}")
    
    finally:
        game_as_white.close()
        stockfish.quit()
        server.server_close()

def play_vs_stockfish():
    server = start_server()
    game = ChessGame(engine_type="stockfish")
    
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
    game = ChessGame(engine_type="stockfish")
    
    try:
        while not game.is_game_over():
            move = game.engine_move()
            print(f"Move played: {move}")
            game.update_display()
            time.sleep(1)
        
        print(f"\nGame Over! Result: {game.get_result()}")
    
    finally:
        game.close()
        server.server_close()

if __name__ == "__main__":
    print("Select mode:")
    print("1: Stockfish vs Stockfish")
    print("2: Human vs Stockfish")
    print("3: Custom Engine vs Custom Engine")
    print("4: Custom Engine vs Stockfish")
    
    mode = input("Enter mode (1-4): ")
    
    if mode == "1":
        stockfish_vs_stockfish()
    elif mode == "2":
        play_vs_stockfish()
    elif mode == "3":
        custom_vs_custom()
    elif mode == "4":
        stockfish_vs_custom()
    else:
        print("Invalid mode selected")