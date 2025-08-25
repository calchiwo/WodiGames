/**
 * ChessEngine - Handles board state, moves, rules, FEN, PGN, etc.
 * No DOM access.
 */

function indexToAlg(index) {
  const file = 'abcdefgh'[index % 8];
  const rank = Math.floor(index / 8) + 1;
  return file + rank;
}

function algToIndex(alg) {
  const file = 'abcdefgh'.indexOf(alg[0]);
  const rank = parseInt(alg[1]) - 1;
  return rank * 8 + file;
}

function fileToAlg(file) {
  return 'abcdefgh'[file];
}

export class Chess {
  constructor(fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1') {
    this.board = new Array(64).fill(0);
    this.turn = 'w';
    this.castling = '';
    this.ep = -1;
    this.halfMoves = 0;
    this.moveNumber = 1;
    this.history = [];
    this.capturedWhite = []; // captured white pieces
    this.capturedBlack = []; // captured black pieces
    this.repetitionMap = new Map();
    this.zobristKey = 0n;
    // Zobrist keys (64-bit using BigInt)
    this.zobristPieces = Array.from({ length: 13 }, () => Array.from({ length: 64 }, () => BigInt(Math.floor(Math.random() * Number.MAX_SAFE_INTEGER)) ^ (BigInt(Math.floor(Math.random() * Number.MAX_SAFE_INTEGER)) << 32n)));
    this.zobristCastling = Array.from({ length: 16 }, () => BigInt(Math.floor(Math.random() * Number.MAX_SAFE_INTEGER)) ^ (BigInt(Math.floor(Math.random() * Number.MAX_SAFE_INTEGER)) << 32n));
    this.zobristEp = Array.from({ length: 64 }, () => BigInt(Math.floor(Math.random() * Number.MAX_SAFE_INTEGER)) ^ (BigInt(Math.floor(Math.random() * Number.MAX_SAFE_INTEGER)) << 32n));
    this.zobristTurn = BigInt(Math.floor(Math.random() * Number.MAX_SAFE_INTEGER)) ^ (BigInt(Math.floor(Math.random() * Number.MAX_SAFE_INTEGER)) << 32n);
    this.loadFen(fen);
    this.updateZobrist();
    this.repetitionMap.set(this.zobristKey, 1);
  }

  /**
   * @returns {string} Color of piece ('w', 'b', or null)
   */
  getColor(piece) {
    if (piece === 0) return null;
    return piece <= 6 ? 'w' : 'b';
  }

  /**
   * @returns {number} Type of piece (1=pawn,2=knight,3=bishop,4=rook,5=queen,6=king)
   */
  getType(piece) {
    if (piece === 0) return 0;
    return piece % 6 || 6;
  }

  /**
   * Loads board from FEN string.
   * @param {string} fen
   */
  loadFen(fen) {
    const parts = fen.split(' ');
    const placement = parts[0];
    let idx = 0;
    for (const char of placement) {
      if (/\d/.test(char)) {
        idx += parseInt(char);
      } else if (char !== '/') {
        this.board[idx] = this.charToPiece(char);
        idx++;
      }
    }
    this.turn = parts[1];
    this.castling = parts[2] === '-' ? '' : parts[2];
    this.ep = parts[3] === '-' ? -1 : algToIndex(parts[3]);
    this.halfMoves = parseInt(parts[4]);
    this.moveNumber = parseInt(parts[5]);
  }

  charToPiece(char) {
    const map = { P:1, N:2, B:3, R:4, Q:5, K:6, p:7, n:8, b:9, r:10, q:11, k:12 };
    return map[char] || 0;
  }

  pieceToChar(piece) {
    const map = ['', 'P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k'];
    return map[piece];
  }

  /**
   * @returns {string} Current FEN
   */
  generateFen() {
    let fen = '';
    for (let rank = 7; rank >= 0; rank--) {
      let empty = 0;
      for (let file = 0; file < 8; file++) {
        const p = this.board[rank * 8 + file];
        if (p === 0) {
          empty++;
        } else {
          if (empty > 0) fen += empty;
          fen += this.pieceToChar(p);
          empty = 0;
        }
      }
      if (empty > 0) fen += empty;
      if (rank > 0) fen += '/';
    }
    fen += ` ${this.turn} ${this.castling || '-'} ${this.ep === -1 ? '-' : indexToAlg(this.ep)} ${this.halfMoves} ${this.moveNumber}`;
    return fen;
  }

  updateZobrist() {
    this.zobristKey = 0n;
    for (let i = 0; i < 64; i++) {
      const p = this.board[i];
      if (p) this.zobristKey ^= this.zobristPieces[p][i];
    }
    let castIndex = 0;
    if (this.castling.includes('K')) castIndex |= 1;
    if (this.castling.includes('Q')) castIndex |= 2;
    if (this.castling.includes('k')) castIndex |= 4;
    if (this.castling.includes('q')) castIndex |= 8;
    this.zobristKey ^= this.zobristCastling[castIndex];
    if (this.ep !== -1) this.zobristKey ^= this.zobristEp[this.ep];
    if (this.turn === 'b') this.zobristKey ^= this.zobristTurn;
  }

  /**
   * Applies a move to the board.
   * @param {object} move - {from, to, promotion?}
   * @param {boolean} [pushHistory=true]
   */
  makeMove(move, pushHistory = true) {
    const from = move.from;
    const to = move.to;
    const piece = this.board[from];
    const captured = this.board[to];
    const historyEntry = {
      from, to, piece, captured,
      promotion: move.promotion,
      castling: this.castling,
      ep: this.ep,
      halfMoves: this.halfMoves,
      moveNumber: this.moveNumber,
      zobrist: this.zobristKey,
      san: this.moveToSan(move)
    };

    // Move piece
    this.board[to] = move.promotion ? this.charToPiece(move.promotion) : piece;
    this.board[from] = 0;

    // Capture
    if (captured) {
      if (this.getColor(captured) === 'w') {
        this.capturedWhite.push(captured);
      } else {
        this.capturedBlack.push(captured);
      }
      this.halfMoves = 0;
    }

    // Pawn reset half moves
    if (this.getType(piece) === 1) this.halfMoves = 0;
    else this.halfMoves++;

    // En passant
    if (this.getType(piece) === 1 && to === this.ep) {
      const pawnDir = this.turn === 'w' ? -8 : 8;
      const epCapturedSq = to + pawnDir;
      historyEntry.epCaptured = this.board[epCapturedSq];
      historyEntry.epCapturedSq = epCapturedSq;
      this.board[epCapturedSq] = 0;
      if (this.getColor(historyEntry.epCaptured) === 'w') {
        this.capturedWhite.push(historyEntry.epCaptured);
      } else {
        this.capturedBlack.push(historyEntry.epCaptured);
      }
    }

    // Double pawn push sets ep
    if (this.getType(piece) === 1 && Math.abs(from - to) === 16) {
      this.ep = (from + to) / 2;
    } else {
      this.ep = -1;
    }

    // Castling
    if (this.getType(piece) === 6 && Math.abs(from - to) === 2) {
      const isKingside = to > from;
      const rookFrom = isKingside ? to + 1 : to - 2;
      const rookTo = isKingside ? to - 1 : to + 1;
      historyEntry.castleRook = this.board[rookFrom];
      historyEntry.castleRookFrom = rookFrom;
      historyEntry.castleRookTo = rookTo;
      this.board[rookTo] = this.board[rookFrom];
      this.board[rookFrom] = 0;
    }

    // Update castling rights
    if (this.getType(piece) === 6) {
      this.castling = this.castling.replace(this.turn === 'w' ? /[KQ]/g : /[kq]/g, '');
    }
    if (this.getType(piece) === 4) {
      const homeRank = this.turn === 'w' ? 0 : 56;
      if (from === homeRank) this.castling = this.castling.replace(this.turn === 'w' ? 'Q' : 'q', '');
      if (from === homeRank + 7) this.castling = this.castling.replace(this.turn === 'w' ? 'K' : 'k', '');
    }
    if (captured && this.getType(captured) === 4) {
      const oppHomeRank = this.turn === 'w' ? 56 : 0;
      if (to === oppHomeRank) this.castling = this.castling.replace(this.turn === 'w' ? 'q' : 'Q', '');
      if (to === oppHomeRank + 7) this.castling = this.castling.replace(this.turn === 'w' ? 'k' : 'K', '');
    }

    // Promotion resets half moves
    if (move.promotion) this.halfMoves = 0;

    // Switch turn
    this.turn = this.turn === 'w' ? 'b' : 'w';
    if (this.turn === 'w') this.moveNumber++;

    // Update zobrist and repetition
    this.updateZobrist();
    const count = (this.repetitionMap.get(this.zobristKey) || 0) + 1;
    this.repetitionMap.set(this.zobristKey, count);

    if (pushHistory) this.history.push(historyEntry);
  }

  /**
   * Undoes the last move.
   */
  undoMove() {
    if (!this.history.length) return;
    const entry = this.history.pop();
    const from = entry.from;
    const to = entry.to;

    // Restore pieces
    this.board[from] = entry.piece;
    this.board[to] = entry.captured || 0;

    // Restore en passant capture
    if (entry.epCaptured) {
      this.board[entry.epCapturedSq] = entry.epCaptured;
      this.board[to] = 0;
      if (this.getColor(entry.epCaptured) === 'w') {
        this.capturedWhite.pop();
      } else {
        this.capturedBlack.pop();
      }
    }

    // Restore castling rook
    if (entry.castleRook) {
      this.board[entry.castleRookFrom] = entry.castleRook;
      this.board[entry.castleRookTo] = 0;
    }

    // Pop captured
    if (entry.captured && !entry.epCaptured) {
      if (this.getColor(entry.captured) === 'w') {
        this.capturedWhite.pop();
      } else {
        this.capturedBlack.pop();
      }
    }

    // Restore state
    this.castling = entry.castling;
    this.ep = entry.ep;
    this.halfMoves = entry.halfMoves;
    this.moveNumber = entry.moveNumber;
    this.turn = this.turn === 'w' ? 'b' : 'w';

    // Restore zobrist and repetition
    this.zobristKey = entry.zobrist;
    const count = this.repetitionMap.get(this.zobristKey);
    if (count > 1) this.repetitionMap.set(this.zobristKey, count - 1);
    else this.repetitionMap.delete(this.zobristKey);
  }

  /**
   * @param {number} square
   * @returns {object[]} Legal moves from square
   */
  getLegalMoves(square) {
    const pseudo = this.generatePseudoMoves(square);
    const legal = [];
    for (const move of pseudo) {
      this.makeMove(move, false);
      if (!this.isCheck()) legal.push(move);
      this.undoMove();
    }
    return legal;
  }

  generateAllLegalMoves() {
    const moves = [];
    for (let i = 0; i < 64; i++) {
      if (this.board[i] && this.getColor(this.board[i]) === this.turn) {
        moves.push(...this.getLegalMoves(i));
      }
    }
    return moves;
  }

  generatePseudoMoves(square, attacks = false) {
    const piece = this.board[square];
    if (!piece) return [];
    const type = this.getType(piece);
    const color = this.getColor(piece);
    switch (type) {
      case 1: return this.pawnMoves(square, color, attacks);
      case 2: return this.knightMoves(square, color, attacks);
      case 3: return this.bishopMoves(square, color, attacks);
      case 4: return this.rookMoves(square, color, attacks);
      case 5: return this.queenMoves(square, color, attacks);
      case 6: return this.kingMoves(square, color, attacks);
    }
    return [];
  }

  pawnMoves(square, color, attacks = false) {
    const moves = [];
    const dir = color === 'w' ? 8 : -8;
    const startRank = color === 'w' ? 1 : 6;
    const promRank = color === 'w' ? 6 : 1;
    const rank = Math.floor(square / 8);
    const fwd = square + dir;
    if (fwd >= 0 && fwd < 64 && this.board[fwd] === 0 && !attacks) {
      if (rank === promRank) {
        ['Q','R','B','N'].forEach(p => moves.push({from: square, to: fwd, promotion: color === 'w' ? p : p.toLowerCase()}));
      } else {
        moves.push({from: square, to: fwd});
      }
      if (rank === startRank) {
        const dbl = square + 2 * dir;
        if (this.board[dbl] === 0) moves.push({from: square, to: dbl});
      }
    }
    const caps = [square + dir - 1, square + dir + 1].filter(t => t >= 0 && t < 64 && Math.abs((t % 8) - (square % 8)) === 1);
    caps.forEach(t => {
      if (this.board[t] !== 0 && this.getColor(this.board[t]) !== color || t === this.ep || attacks) {
        if (rank === promRank) {
          ['Q','R','B','N'].forEach(p => moves.push({from: square, to: t, promotion: color === 'w' ? p : p.toLowerCase()}));
        } else {
          moves.push({from: square, to: t});
        }
      }
    });
    return moves;
  }

  knightMoves(square, color, attacks = false) {
    const moves = [];
    const deltas = [-17, -15, -10, -6, 6, 10, 15, 17];
    for (const d of deltas) {
      const t = square + d;
      if (t < 0 || t > 63) continue;
      if (Math.abs((t % 8) - (square % 8)) > 2 || Math.abs((t % 8) - (square % 8)) === 0) continue;
      const target = this.board[t];
      if (attacks || target === 0 || this.getColor(target) !== color) {
        moves.push({from: square, to: t});
      }
    }
    return moves;
  }

  slidingMoves(square, color, deltas, attacks = false) {
    const moves = [];
    for (const d of deltas) {
      let t = square + d;
      while (t >= 0 && t < 64 && Math.abs((t % 8) - ((t - d) % 8)) <= 1) {
        const target = this.board[t];
        if (target === 0) {
          if (attacks) moves.push({from: square, to: t});
          t += d;
          continue;
        }
        if (this.getColor(target) !== color || attacks) {
          moves.push({from: square, to: t});
        }
        break;
      }
    }
    return moves;
  }

  bishopMoves(square, color, attacks) {
    return this.slidingMoves(square, color, [-9, -7, 7, 9], attacks);
  }

  rookMoves(square, color, attacks) {
    return this.slidingMoves(square, color, [-8, -1, 1, 8], attacks);
  }

  queenMoves(square, color, attacks) {
    return [...this.rookMoves(square, color, attacks), ...this.bishopMoves(square, color, attacks)];
  }

  kingMoves(square, color, attacks = false) {
    const moves = [];
    const deltas = [-9, -8, -7, -1, 1, 7, 8, 9];
    for (const d of deltas) {
      const t = square + d;
      if (t < 0 || t > 63 || Math.abs((t % 8) - (square % 8)) > 1) continue;
      const target = this.board[t];
      if (attacks || target === 0 || this.getColor(target) !== color) {
        moves.push({from: square, to: t});
      }
    }
    if (!attacks) {
      const homeRank = color === 'w' ? 0 : 56;
      const oppColor = color === 'w' ? 'b' : 'w';
      if (this.castling.includes(color === 'w' ? 'K' : 'k')) {
        const kSide1 = homeRank + 5, kSide2 = homeRank + 6;
        if (this.board[kSide1] === 0 && this.board[kSide2] === 0 && !this.isAttacked(kSide1, oppColor) && !this.isAttacked(kSide2, oppColor)) {
          moves.push({from: square, to: homeRank + 6});
        }
      }
      if (this.castling.includes(color === 'w' ? 'Q' : 'q')) {
        const qSide1 = homeRank + 1, qSide2 = homeRank + 2, qSide3 = homeRank + 3;
        if (this.board[qSide1] === 0 && this.board[qSide2] === 0 && this.board[qSide3] === 0 && !this.isAttacked(qSide2, oppColor) && !this.isAttacked(qSide3, oppColor)) {
          moves.push({from: square, to: homeRank + 2});
        }
      }
    }
    return moves;
  }

  isAttacked(square, attackerColor) {
    for (let i = 0; i < 64; i++) {
      const p = this.board[i];
      if (p && this.getColor(p) === attackerColor) {
        const attacks = this.generatePseudoMoves(i, true);
        if (attacks.some(m => m.to === square)) return true;
      }
    }
    return false;
  }

  isCheck() {
    const kingSq = this.getKingSquare(this.turn);
    return this.isAttacked(kingSq, this.turn === 'w' ? 'b' : 'w');
  }

  getKingSquare(color) {
    const king = color === 'w' ? 6 : 12;
    return this.board.indexOf(king);
  }

  isCheckmate() {
    return this.isCheck() && this.generateAllLegalMoves().length === 0;
  }

  isStalemate() {
    return !this.isCheck() && this.generateAllLegalMoves().length === 0;
  }

  isDraw() {
    if (this.halfMoves >= 50) return true;
    if (this.repetitionMap.get(this.zobristKey) >= 3) return true;
    // Insufficient material
    const pieces = this.board.filter(p => p !== 0);
    if (pieces.length <= 2) return true;
    if (pieces.length === 3 && pieces.some(p => [2,3,8,9].includes(p))) return true;
    const bishops = pieces.filter(p => [3,9].includes(p));
    if (pieces.length === 4 && bishops.length === 2) {
      const sq1 = this.board.indexOf(bishops[0]);
      const sq2 = this.board.indexOf(bishops[1]);
      const color1 = (Math.floor(sq1 / 8) + sq1 % 8) % 2;
      const color2 = (Math.floor(sq2 / 8) + sq2 % 8) % 2;
      if (color1 === color2) return true;
    }
    return false;
  }

  /**
   * @param {object} move
   * @returns {string} SAN notation
   */
  moveToSan(move) {
    const pieceType = this.getType(this.board[move.from]);
    if (pieceType === 6 && Math.abs(move.from - move.to) === 2) {
      return move.to > move.from ? 'O-O' : 'O-O-O';
    }
    const types = ['', '', 'N', 'B', 'R', 'Q', 'K'];
    let san = types[pieceType];
    const fromFile = fileToAlg(move.from % 8);
    const fromRank = Math.floor(move.from / 8) + 1;
    const toAlg = indexToAlg(move.to);
    const captured = this.board[move.to] !== 0 || (pieceType === 1 && move.to === this.ep);

    // Disambiguation
    const candidates = [];
    for (let i = 0; i < 64; i++) {
      if (i !== move.from && this.board[i] === this.board[move.from]) {
        const moves = this.generatePseudoMoves(i);
        if (moves.some(m => m.to === move.to)) candidates.push(i);
      }
    }
    if (candidates.length > 0) {
      const sameFile = candidates.some(s => s % 8 === move.from % 8);
      const sameRank = candidates.some(s => Math.floor(s / 8) === Math.floor(move.from / 8));
      if (sameFile && sameRank) san += fromFile + fromRank;
      else if (sameFile) san += fromRank;
      else san += fromFile;
    }

    if (captured) san += 'x';
    san += toAlg;
    if (move.promotion) san += '=' + move.promotion.toUpperCase();

    // Check or mate
    this.makeMove(move, false);
    if (this.isCheck()) {
      san += this.generateAllLegalMoves().length === 0 ? '#' : '+';
    }
    this.undoMove();

    return san;
  }

  /**
   * @param {string} san
   * @returns {object|null} Move object
   */
  sanToMove(san) {
    if (san === 'O-O' || san === 'O-O+') {
      const king = this.getKingSquare(this.turn);
      return {from: king, to: king + 2};
    }
    if (san === 'O-O-O' || san === 'O-O-O+') {
      const king = this.getKingSquare(this.turn);
      return {from: king, to: king - 2};
    }
    const match = san.match(/([NBQRK])?([a-h])?([1-8])?(x)?([a-h][1-8])(=([NBQR]))?([+#])?/);
    if (!match) return null;
    const pieceType = match[1] ? {K:6,Q:5,R:4,B:3,N:2}[match[1]] : 1;
    const fromFile = match[2] ? 'abcdefgh'.indexOf(match[2]) : -1;
    const fromRank = match[3] ? parseInt(match[3]) - 1 : -1;
    const capture = !!match[4];
    const to = algToIndex(match[5]);
    const prom = match[7] ? match[7] : null;
    const candidates = [];
    for (let i = 0; i < 64; i++) {
      const p = this.board[i];
      if (this.getType(p) === pieceType && this.getColor(p) === this.turn) {
        const f = i % 8;
        const r = Math.floor(i / 8);
        if ((fromFile >= 0 && f !== fromFile) || (fromRank >= 0 && r !== fromRank)) continue;
        const moves = this.generatePseudoMoves(i);
        const matching = moves.find(m => m.to === to && (!!m.promotion === !!prom));
        if (matching && (capture === (this.board[to] !== 0 || (pieceType === 1 && to === this.ep)))) {
          candidates.push(i);
        }
      }
    }
    if (candidates.length !== 1) return null;
    const move = {from: candidates[0], to};
    if (prom) move.promotion = this.turn === 'w' ? prom : prom.toLowerCase();
    return move;
  }

  /**
   * @param {string} pgn
   */
  loadPGN(pgn) {
    // Extract moves, ignore headers/numbers
    const moveStrings = pgn.replace(/\d+\./g, '').replace(/\s+/g, ' ').trim().split(' ');
    this.loadFen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1');
    for (const san of moveStrings) {
      const move = this.sanToMove(san);
      if (move) this.makeMove(move);
    }
  }

  generatePGN() {
    let pgn = '';
    this.history.forEach((h, i) => {
      if (i % 2 === 0) pgn += `${Math.floor(i / 2) + 1}. `;
      pgn += `${h.san} `;
    });
    return pgn.trim();
  }

  /**
   * Performance test (move generation count)
   * @param {number} depth
   * @returns {number} Nodes
   */
  perft(depth) {
    if (depth === 0) return 1;
    const moves = this.generateAllLegalMoves();
    let nodes = 0;
    for (const move of moves) {
      this.makeMove(move, false);
      nodes += this.perft(depth - 1);
      this.undoMove();
    }
    return nodes;
  }
}

// Test positions for perft:
// 1. Starting: perft(1)=20, (2)=400, (3)=8902, (4)=197281, (5)=4865609
// 2. Kiwipete: r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1
// perft(1)=48, (2)=2039, (3)=97862, (4)=4085603, (5)=193690690
