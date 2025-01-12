import chess
import chess.svg

class ChessBoard:
    def __init__(self, fen=None):
        # Initialize the board (default starting position if no FEN provided)
        self.board = chess.Board(fen) if fen else chess.Board()
    
    def display(self, save_path=None):
        """Generate SVG of current board position"""
        # Create SVG of the current board state
        svg_content = chess.svg.board(self.board, size=400)
        
        if save_path:
            # Save SVG file
            with open(save_path, 'w') as f:
                f.write(svg_content)
                
            # Optionally convert to PNG
            # png_path = save_path.replace('.svg', '.png')
            # cairosvg.svg2png(bytestring=svg_content.encode('utf-8'), write_to=png_path)
    
    def make_move(self, move):
        """Make a move using UCI notation (e.g., 'e2e4')"""
        try:
            move_obj = chess.Move.from_uci(move)
            if move_obj in self.board.legal_moves:
                self.board.push(move_obj)
                return True
            return False
        except ValueError:
            return False
    
    def get_legal_moves(self):
        """Get list of legal moves in UCI notation"""
        return [move.uci() for move in self.board.legal_moves]
    
    def is_game_over(self):
        """Check if the game is over"""
        return self.board.is_game_over()
    
    def get_result(self):
        """Get game result if game is over"""
        if self.board.is_checkmate():
            return "Checkmate"
        elif self.board.is_stalemate():
            return "Stalemate"
        elif self.board.is_insufficient_material():
            return "Draw (insufficient material)"
        elif self.board.is_fifty_moves():
            return "Draw (fifty move rule)"
        elif self.board.is_repetition():
            return "Draw (repetition)"
        return "Game in progress"
    
    def get_fen(self):
        """Get current position in FEN notation"""
        return self.board.fen()

# Example usage:
if __name__ == "__main__":
    # Create a board with starting position
    board = ChessBoard()
    
    # Or create a board from a specific position (FEN)
    custom_position = "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 1"
    board_custom = ChessBoard(custom_position)
    
    # Save the board visualization
    board_custom.display("current_position.svg")
    
    # Make some moves
    moves = ["e2e4", "e7e5", "g1f3"]
    for move in moves:
        if board.make_move(move):
            print(f"Made move: {move}")
        else:
            print(f"Invalid move: {move}")
    
    # Get legal moves
    print("\nLegal moves:", board.get_legal_moves())
    
    # Get current position in FEN
    print("\nCurrent FEN:", board.get_fen())