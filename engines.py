# my own attempt at creating a chess engine, simple tree search only
import chess
import random
import time

class StockfishEngine:
    def __init__(self):
        self.name = "StockfishEngine"
        self.engine = chess.engine.SimpleEngine.popen_uci("stockfish")
    
    def select_move(self, board, think_time=0.1):
        result = self.engine.play(board, chess.engine.Limit(think_time))
        return result.move
    
    def close(self):
        self.engine.quit()

class HumanEngine:
    def __init__(self):
        self.name = "HumanEngine"
    
    def select_move(self, board, think_time=0.1):
        move = "aaaa"
        #check if move is in uci format continuously
        while len(move) != 4 or move[0] not in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'] or not move[1].isdigit() or move[2] not in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'] or not move[3].isdigit():
            move = input("Enter your move (e.g. e2e4): ")

        chess.Move.from_uci(move)
        while move not in [move.uci() for move in board.legal_moves]:
            print("Invalid move! Try again.")
            move = input("Enter your move (e.g. e2e4): ")
        return chess.Move.from_uci(move)

class SimpleEngine:
    def __init__(self):
        self.name = "SimpleEngine"

        self.piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 300,
            chess.BISHOP: 300,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 0 
        }
    
    def get_moves(self, board):
        """Get list of legal moves from current position"""
        return list(board.legal_moves)
    
    def calculate_material(self, board):
        """
        Calculate material balance of position (positive is good for white)
        """
        score = 0
        
        for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
            white_pieces = len(board.pieces(piece_type, chess.WHITE))
            black_pieces = len(board.pieces(piece_type, chess.BLACK))
            score += (white_pieces - black_pieces) * self.piece_values[piece_type]
        
        return score
    
    def placement_score(self, board):
        """
        Calculate score based on piece positions.
        """
        score = 0
        
        knight_table = [
            [-50,-40,-30,-30,-30,-30,-40,-50],
            [-40,-20,  0,  0,  0,  0,-20,-40],
            [-30,  0, 10, 15, 15, 10,  0,-30],
            [-30,  5, 15, 20, 20, 15,  5,-30],
            [-30,  5, 15, 20, 20, 15,  5,-30],
            [-30,  0, 10, 15, 15, 10,  0,-30],
            [-40,-20,  0,  0,  0,  0,-20,-40],
            [-50,-40,-30,-30,-30,-30,-40,-50]
        ]
        
        bishop_table = [
            [-20,-10,-10,-10,-10,-10,-10,-20],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-10,  0,  5, 10, 10,  5,  0,-10],
            [-10,  5,  5, 10, 10,  5,  5,-10],
            [-10,  5,  5, 10, 10,  5,  5,-10],
            [-10,  0,  5, 10, 10,  5,  0,-10],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-20,-10,-10,-10,-10,-10,-10,-20]
        ]
        
        king_table = [
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-20,-30,-30,-40,-40,-30,-30,-20],
            [-10,-20,-20,-20,-20,-20,-20,-10],
            [ 20, 20,  0,  0,  0,  0, 20, 20],
            [ 20, 30, 10,  0,  0, 10, 30, 20]
        ]
        
        pawn_advance = [0, 0, 5, 10, 20, 35, 60, 0]
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is None:
                continue

            rank = chess.square_rank(square)
            file = chess.square_file(square) 
            
            if piece.color == chess.BLACK:
                rank = 7 - rank
            
            if piece.piece_type == chess.KNIGHT:
                bonus = knight_table[7-rank][file]
            elif piece.piece_type == chess.BISHOP:
                bonus = bishop_table[7-rank][file]
            elif piece.piece_type == chess.KING:
                bonus = king_table[7-rank][file]
            elif piece.piece_type == chess.PAWN:
                bonus = pawn_advance[rank]
            else:
                bonus = 0
            
            if piece.color == chess.WHITE:
                score += bonus
            else:
                score -= bonus
        
        return score
    
    def evaluate_position(self, board):
        """
        Evaluate current position (higher is better for white)
        """
        if board.is_checkmate():
            return -10000 if board.turn else 10000
        
        return self.calculate_material(board) + self.placement_score(board)
    
    def select_move(self, board, think_time=0.1):
        """
        Select best move from current position by evaluating each possible move
        """
        legal_moves = self.get_moves(board)
        if not legal_moves:
            return None
            
        best_move = []
        best_eval = float('-inf') if board.turn else float('inf')
        
        for move in legal_moves:
            # Make move on a copy of the board
            board_copy = board.copy()
            board_copy.push(move)
            
            # Evaluate resulting position
            eval = self.evaluate_position(board_copy)
            
            # Update best move if this position is better
            if board.turn == chess.WHITE: 
                if eval > best_eval + 10:
                    best_eval = eval
                    best_move = [move]
                elif eval > best_eval - 10:
                    best_move.append(move)
            else:
                if eval < best_eval - 10:
                    best_eval = eval
                    best_move = [move]
                elif eval < best_eval + 10:
                    best_move.append(move)
        
        print(f"Selected move leads to evaluation: {best_eval/100:+.2f} pawns")
        return random.choice(best_move)
    

class TreeEngine:
    def __init__(self):
        self.name = "TreeEngine"
        self.max_depth = 20 
        self.nodes_searched = 0 
        
        self.piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 300,
            chess.BISHOP: 300,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 0 
        }
    
    def quiescence(self, board, alpha, beta, start_time, time_limit, depth=0):
        """
        Quiescence search - evaluates captures until a quiet position
        """
        self.nodes_searched += 1
        
        if time.time() - start_time > time_limit * 0.95:
            return None
        
        stand_pat = self.evaluate_position(board)
        
        if depth > 10:
            return stand_pat
            
        if board.turn == chess.WHITE:
            alpha = max(alpha, stand_pat)
        else:
            beta = min(beta, stand_pat)
            
        if alpha >= beta:
            return stand_pat
            
        for move in board.legal_moves:
            if not board.is_capture(move):
                continue
                
            board.push(move)
            score = self.quiescence(board, alpha, beta, start_time, time_limit, depth + 1)
            board.pop()
            
            if score is None: 
                return None
                
            if board.turn == chess.WHITE:
                alpha = max(alpha, score)
            else:
                beta = min(beta, score)
                
            if alpha >= beta:
                break
                
        return alpha if board.turn == chess.WHITE else beta

    def alpha_beta(self, board, depth, alpha, beta, maximizing_player, start_time, time_limit):
        """
        Alpha-beta pruning search
        """
        self.nodes_searched += 1
        
        if time.time() - start_time > time_limit * 0.95:
            return None, None
            
        if board.is_game_over():
            if board.is_checkmate():
                return (-10000 if board.turn else 10000), None
            return 0, None  # Draw
        
        # start with captures 
        if depth <= 0:
            score = self.quiescence(board, alpha, beta, start_time, time_limit)
            if score is None:  # Out of time
                return None, None
            return score, None
        
        legal_moves = list(board.legal_moves)
        
        legal_moves.sort(key=lambda move: board.is_capture(move), reverse=True)
        
        best_move = legal_moves[0]
        
        if maximizing_player:
            max_eval = float('-inf')
            for move in legal_moves:
                board.push(move)
                eval, _ = self.alpha_beta(board, depth - 1, alpha, beta, False, start_time, time_limit)
                board.pop()
                
                if eval is None:  # Out of time
                    return None, None
                
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in legal_moves:
                board.push(move)
                eval, _ = self.alpha_beta(board, depth - 1, alpha, beta, True, start_time, time_limit)
                board.pop()
                
                if eval is None:  # Out of time
                    return None, None
                
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break  
            return min_eval, best_move
    
    def iterative_deepening(self, board, time_limit):
        """
        Keep going with more time left
        """
        start_time = time.time()
        best_move = None
        best_eval = None
        depth = 1
        
        while depth <= self.max_depth:
            self.nodes_searched = 0  # Reset counter for this depth
            
            if time.time() - start_time > time_limit * 0.8: 
                break
                
            # Run alpha-beta search at current depth
            eval, move = self.alpha_beta(
                board, 
                depth,
                float('-inf'),
                float('inf'),
                board.turn == chess.WHITE,
                start_time,
                time_limit
            )
            
            # stop if no time
            if eval is None:
                break
                
            best_eval = eval
            best_move = move
            
            depth += 1
        
        return best_move, best_eval
    
    def select_move(self, board, think_time=1.0):
        """
        Select best move using iterative deepening with alpha-beta search
        think_time: time limit in seconds
        """
        best_move, eval = self.iterative_deepening(board, think_time)
        
        if best_move:
            print(f"\nFinal evaluation: {eval/100:+.2f} pawns")
            return best_move
        else:
            # gg
            return list(board.legal_moves)[0]
    
    def get_name(self):
        return self.name
    
    def get_moves(self, board):
        """Get list of legal moves from current position"""
        return list(board.legal_moves)
    
    def calculate_material(self, board):
        """
        Calculate material balance of position (positive is good for white)
        """
        score = 0
        
        for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
            white_pieces = len(board.pieces(piece_type, chess.WHITE))
            black_pieces = len(board.pieces(piece_type, chess.BLACK))
            score += (white_pieces - black_pieces) * self.piece_values[piece_type]
        
        return score
    
    def placement_score(self, board):
        """
        Calculate score based on piece positions.
        """
        score = 0
        
        knight_table = [
            [-50,-40,-30,-30,-30,-30,-40,-50],
            [-40,-20,  0,  0,  0,  0,-20,-40],
            [-30,  0, 10, 15, 15, 10,  0,-30],
            [-30,  5, 15, 20, 20, 15,  5,-30],
            [-30,  5, 15, 20, 20, 15,  5,-30],
            [-30,  0, 10, 15, 15, 10,  0,-30],
            [-40,-20,  0,  0,  0,  0,-20,-40],
            [-50,-40,-30,-30,-30,-30,-40,-50]
        ]
        
        bishop_table = [
            [-20,-10,-10,-10,-10,-10,-10,-20],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-10,  0,  5, 10, 10,  5,  0,-10],
            [-10,  5,  5, 10, 10,  5,  5,-10],
            [-10,  5,  5, 10, 10,  5,  5,-10],
            [-10,  0,  5, 10, 10,  5,  0,-10],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-20,-10,-10,-10,-10,-10,-10,-20]
        ]
        
        king_table = [
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-20,-30,-30,-40,-40,-30,-30,-20],
            [-10,-20,-20,-20,-20,-20,-20,-10],
            [ 20, 20,  0,  0,  0,  0, 20, 20],
            [ 20, 30, 10,  0,  0, 10, 30, 20]
        ]
        
        pawn_advance = [0, 0, 5, 10, 20, 35, 60, 0]
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is None:
                continue

            rank = chess.square_rank(square)
            file = chess.square_file(square) 
            
            if piece.color == chess.BLACK:
                rank = 7 - rank
            
            if piece.piece_type == chess.KNIGHT:
                bonus = knight_table[7-rank][file]
            elif piece.piece_type == chess.BISHOP:
                bonus = bishop_table[7-rank][file]
            elif piece.piece_type == chess.KING:
                bonus = king_table[7-rank][file]
            elif piece.piece_type == chess.PAWN:
                bonus = pawn_advance[rank]
            else:
                bonus = 0
            
            if piece.color == chess.WHITE:
                score += bonus
            else:
                score -= bonus
        
        return score
    
    def evaluate_position(self, board):
        """
        Evaluate current position (higher is better for white)
        """
        if board.is_checkmate():
            return -10000 if board.turn else 10000
        elif board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition(): 
            return 0
        
        return self.calculate_material(board) + self.placement_score(board)
        """
        Select best move from current position by evaluating each possible move
        """
        legal_moves = self.get_moves(board)
        if not legal_moves:
            return None
            
        best_move = []
        best_eval = float('-inf') if board.turn else float('inf')
        
        for move in legal_moves:
            # Make move on a copy of the board
            board_copy = board.copy()
            board_copy.push(move)
            
            # Evaluate resulting position
            eval = self.evaluate_position(board_copy)
            
            # Update best move if this position is better
            if board.turn == chess.WHITE: 
                if eval > best_eval + 10:
                    best_eval = eval
                    best_move = [move]
                elif eval > best_eval - 10:
                    best_move.append(move)
            else:
                if eval < best_eval - 10:
                    best_eval = eval
                    best_move = [move]
                elif eval < best_eval + 10:
                    best_move.append(move)
        
        print(f"Selected move leads to evaluation: {best_eval/100:+.2f} pawns")
        return random.choice(best_move)