# my own attempt at creating a chess engine
import chess
import random

class CustomEngine:
    def __init__(self):
        self.name = "KannanKompute"
    
    def get_moves(self, board):
        """Get list of legal moves from current position"""
        return list(board.legal_moves)
    
    def evaluate_position(self, board):
        """
        Evaluate current position (higher is better for white)
        """
        if board.is_checkmate():
            return -10000 if board.turn else 10000
        return 0 
    
    def select_move(self, board):
        """
        Select best move from current position
        """
        legal_moves = self.get_moves(board)
        if legal_moves:
            return random.choice(legal_moves)
        return None