# chess_game.py
import chess.engine
import chess
from chessboard import ChessBoard
import time
from display import start_server
from engines import SimpleEngine, StockfishEngine, HumanEngine, TreeEngine

class ChessGame:
    def __init__(self, engine_white="stockfish", engine_black="stockfish"):
        self.chessboard = ChessBoard()
        if engine_white == "stockfish":
            self.white_engine = StockfishEngine()
            self.white_engine_type = "stockfish"
        elif engine_white == "simple":
            self.white_engine = SimpleEngine()
            self.white_engine_type = "simple"
        elif engine_white == "human":
            self.white_engine = HumanEngine()
            self.white_engine_type = "human"
        elif engine_white == "tree":
            self.white_engine = TreeEngine()
            self.white_engine_type = "tree"
        else :
            raise ValueError("Invalid engine type for white")
        
        if engine_black == "stockfish":
            self.black_engine = StockfishEngine()
            self.black_engine_type = "stockfish"
        elif engine_black == "simple":
            self.black_engine = SimpleEngine()
            self.black_engine_type = "simple"
        elif engine_black == "human":
            self.black_engine = HumanEngine()
            self.black_engine_type = "human"
        elif engine_black == "tree":    
            self.black_engine = TreeEngine()
            self.black_engine_type = "tree"
        else:
            raise ValueError("Invalid engine type for black")
    
    def engine_move(self, think_time=0.01):
        if self.chessboard.board.turn == chess.WHITE:
            move = self.white_engine.select_move(self.chessboard.board, think_time)
        else:
            move = self.black_engine.select_move(self.chessboard.board, think_time)

        self.chessboard.make_move(move.uci())

        return move.uci()
    
    def update_display(self):
        self.chessboard.display("game.svg")
    
    def is_game_over(self):
        return self.chessboard.board.is_game_over()
    
    def get_result(self):
        return self.chessboard.get_result()
    
    def close(self):
        if self.white_engine_type == "stockfish":
            self.white_engine.close()
        if self.black_engine_type == "stockfish":
            self.black_engine.close()

if __name__ == "__main__":
    player1 = input("Enter engine for white (stockfish/simple/human/tree): ")
    player2 = input("Enter engine for black (stockfish/simple/human/tree): ")

    num_games = int(input("Enter number of games: "))


    server = start_server()

    for i in range(num_games):
        game = ChessGame(player1, player2)
        game.update_display()

        try:
            while not game.is_game_over():
                move = game.engine_move(think_time=0.3)
                print(f"Move played: {move}")
                game.update_display()
                # time.sleep(0.1)
            
            print(f"\nGame Over! Result: {game.get_result()}")
        
        finally:
            game.close()
        
    server.server_close()