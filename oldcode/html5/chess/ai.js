// ai.js
/**
 * @fileoverview AI logic for the chess game.
 * @module ai.js
 * @requires The ChessEngine class from chess.js
 */

/**
 * Minimax algorithm with Alpha-Beta Pruning.
 * @param {Object} engine - A clone of the ChessEngine instance.
 * @param {number} depth - The current search depth.
 * @param {string} playerColor - The color of the AI ('w' or 'b').
 * @param {number} alpha - The alpha value.
 * @param {number} beta - The beta value.
 * @returns {Object} An object containing the best move and its score.
 */
export async function minimax(engine, depth, playerColor, alpha = -Infinity, beta = Infinity) {
    // Base case: check for game over or depth limit
    if (depth === 0 || engine.getGameStatus() !== 'ongoing') {
        return { score: evaluateBoard(engine, playerColor) };
    }

    const legalMoves = engine.getLegalMoves();
    let bestScore = engine.turn === playerColor ? -Infinity : Infinity;
    let bestMove = null;

    // Sort moves for better alpha-beta pruning (captures first)
    // ... (Move ordering logic)

    for (const move of legalMoves) {
        const newEngine = new engine.constructor(engine.toFen());
        newEngine.makeMove(move);

        const result = await minimax(newEngine, depth - 1, playerColor, alpha, beta);
        const score = result.score;

        if (newEngine.turn === playerColor) {
            // Maximizing player
            if (score > bestScore) {
                bestScore = score;
                bestMove = move;
            }
            alpha = Math.max(alpha, bestScore);
        } else {
            // Minimizing player
            if (score < bestScore) {
                bestScore = score;
                bestMove = move;
            }
            beta = Math.min(beta, bestScore);
        }

        if (beta <= alpha) {
            break; // Alpha-beta cutoff
        }
    }
    
    return { score: bestScore, move: bestMove };
}

/**
 * The evaluation function for the board state.
 * @param {Object} engine - The ChessEngine instance.
 * @param {string} playerColor - The color of the AI.
 * @returns {number} The evaluated score.
 */
function evaluateBoard(engine, playerColor) {
    let score = 0;
    const myColor = playerColor;
    const oppColor = myColor === 'w' ? 'b' : 'w';

    // 1. Material Advantage
    const pieceValues = { 'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 20000 };
    engine.board.forEach(piece => {
        if (piece) {
            const value = pieceValues[piece.toUpperCase()];
            if (piece.toLowerCase() === myColor) {
                score += value;
            } else {
                score -= value;
            }
        }
    });

    // 2. Piece-Square Tables (add positional value)
    const pieceSquareTables = {
        // ... (Define tables for each piece, e.g., pawn, knight, etc.)
    };

    // 3. Mobility (Number of legal moves)
    const myMoves = engine.getLegalMoves().length;
    const oppMoves = engine.constructor.getLegalMovesForColor(engine, oppColor).length; // Need a helper for this
    score += (myMoves - oppMoves) * 10;

    // 4. King Safety
    if (engine.isCheck(oppColor)) {
        score += 500;
    }
    if (engine.isCheck(myColor)) {
        score -= 500;
    }

    return score;
}

/**
 * AI function to get a random legal move.
 * @param {Object} engine - The ChessEngine instance.
 * @returns {Object} A random legal move.
 */
function getRandomMove(engine) {
    const legalMoves = engine.getLegalMoves();
    if (legalMoves.length === 0) return null;
    const randomIndex = Math.floor(Math.random() * legalMoves.length);
    return legalMoves[randomIndex];
}
