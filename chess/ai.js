/**
 * AI logic for computer opponent.
 */

export const materialValues = [0, 100, 320, 330, 500, 900, 2000, 100, 320, 330, 500, 900, 2000];

const pst = {
  1: [ // pawn
    0, 0, 0, 0, 0, 0, 0, 0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5, 5, 10, 25, 25, 10, 5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, -5, -10, 0, 0, -10, -5, 5,
    5, 10, 10, -20, -20, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0
  ],
  2: [ // knight
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
  ],
  3: [ // bishop
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 10, 10, 0, 0, 10, 10, -10,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
  ],
  4: [ // rook
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, 10, 10, 10, 10, 5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    0, 0, 5, 5, 5, 5, 0, 0
  ],
  5: [ // queen
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -5, 0, 5, 5, 5, 5, 0, -5,
    0, 0, 5, 5, 5, 5, 0, -5,
    -10, 5, 5, 5, 5, 5, 0, -10,
    -10, 0, 5, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20
  ],
  6: [ // king
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    20, 20, 0, 0, 0, 0, 20, 20,
    20, 30, 10, 0, 0, 10, 30, 20
  ]
};

/**
 * @param {Chess} chess
 * @returns {number} Evaluation score (positive good for white)
 */
export function evaluate(chess) {
  let score = 0;
  for (let i = 0; i < 64; i++) {
    const p = chess.board[i];
    if (p) {
      const sign = chess.getColor(p) === 'w' ? 1 : -1;
      score += sign * materialValues[p];
      let sq = i;
      if (chess.getColor(p) === 'b') sq = 63 - sq; // flip for black
      score += sign * pst[chess.getType(p)][sq];
    }
  }
  // Mobility
  score += (chess.turn === 'w' ? 1 : -1) * chess.generateAllLegalMoves().length * 0.1;
  // King safety (simple: pawn shield)
  const kingSq = chess.getKingSquare(chess.turn);
  const shieldDeltas = chess.turn === 'w' ? [7, 8, 9] : [-7, -8, -9];
  let shield = 0;
  shieldDeltas.forEach(d => {
    const s = kingSq + d;
    if (s >= 0 && s < 64 && chess.board[s] && chess.getType(chess.board[s]) === 1 && chess.getColor(chess.board[s]) === chess.turn) shield += 10;
  });
  score += (chess.turn === 'w' ? shield : -shield);
  return score;
}

const transposition = new Map();

/**
 * Quiescence search to handle captures beyond depth.
 * @param {Chess} chess
 * @param {number} alpha
 * @param {number} beta
 * @param {boolean} maximizing
 * @param {number} qdepth
 * @returns {number}
 */
function quiescence(chess, alpha, beta, maximizing, qdepth) {
  let stand = evaluate(chess);
  if (qdepth === 0) return stand;
  if (maximizing) {
    let maxEval = stand;
    const captures = chess.generateAllLegalMoves().filter(m => chess.board[m.to] !== 0);
    for (const move of captures) {
      chess.makeMove(move, false);
      const score = quiescence(chess, alpha, beta, false, qdepth - 1);
      chess.undoMove();
      maxEval = Math.max(maxEval, score);
      alpha = Math.max(alpha, maxEval);
      if (beta <= alpha) break;
    }
    return maxEval;
  } else {
    let minEval = stand;
    const captures = chess.generateAllLegalMoves().filter(m => chess.board[m.to] !== 0);
    for (const move of captures) {
      chess.makeMove(move, false);
      const score = quiescence(chess, alpha, beta, true, qdepth - 1);
      chess.undoMove();
      minEval = Math.min(minEval, score);
      beta = Math.min(beta, minEval);
      if (beta <= alpha) break;
    }
    return minEval;
  }
}

/**
 * Minimax with alpha-beta pruning.
 * @param {Chess} chess
 * @param {number} depth
 * @param {number} alpha
 * @param {number} beta
 * @param {boolean} maximizing
 * @returns {number}
 */
function minimax(chess, depth, alpha, beta, maximizing) {
  const hash = chess.zobristKey;
  const ttEntry = transposition.get(hash);
  if (ttEntry && ttEntry.depth >= depth) return ttEntry.score;

  if (depth === 0) {
    return quiescence(chess, alpha, beta, maximizing, 4);
  }

  if (chess.isCheckmate()) return maximizing ? -Infinity : Infinity;
  if (chess.isStalemate() || chess.isDraw()) return 0;

  let best = maximizing ? -Infinity : Infinity;
  let moves = chess.generateAllLegalMoves();
  // Move ordering: captures first, sorted by value
  moves.sort((a, b) => {
    const aVal = chess.board[a.to] ? materialValues[chess.board[a.to]] : 0;
    const bVal = chess.board[b.to] ? materialValues[chess.board[b.to]] : 0;
    return bVal - aVal;
  });

  for (const move of moves) {
    chess.makeMove(move, false);
    const val = minimax(chess, depth - 1, alpha, beta, !maximizing);
    chess.undoMove();
    if (maximizing) {
      best = Math.max(best, val);
      alpha = Math.max(alpha, best);
    } else {
      best = Math.min(best, val);
      beta = Math.min(beta, best);
    }
    if (beta <= alpha) break;
  }

  transposition.set(hash, { score: best, depth });
  return best;
}

/**
 * Finds best move for current turn.
 * @param {Chess} chess
 * @param {number} depth
 * @returns {object|null} Best move
 */
export function getBestMove(chess, depth) {
  if (depth === 0) {
    const moves = chess.generateAllLegalMoves();
    return moves[Math.floor(Math.random() * moves.length)] || null;
  }
  let bestMove = null;
  let bestValue = chess.turn === 'w' ? -Infinity : Infinity;
  const maximizing = chess.turn === 'w';
  let moves = chess.generateAllLegalMoves();
  moves.sort((a, b) => {
    const aVal = chess.board[a.to] ? materialValues[chess.board[a.to]] : 0;
    const bVal = chess.board[b.to] ? materialValues[chess.board[b.to]] : 0;
    return bVal - aVal;
  });
  for (const move of moves) {
    chess.makeMove(move, false);
    const val = minimax(chess, depth - 1, -Infinity, Infinity, !maximizing);
    chess.undoMove();
    if ((maximizing && val > bestValue) || (!maximizing && val < bestValue)) {
      bestValue = val;
      bestMove = move;
    }
  }
  return bestMove;
}
