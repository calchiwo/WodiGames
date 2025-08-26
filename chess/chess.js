// chess.js
/**
 * @fileoverview Main chess game logic and UI controller.
 * @module chess.js
 * @requires ./ai.js
 */

import { minimax } from './ai.js';

// Global game state variables (managed by the UI controller)
let chessEngine;
let selectedSquare = null;
let lastMove = null;
let aiDifficulty = 0;
let playerColor = 'white';
let currentPieceStyle = 'unicode'; // 'unicode' or 'svg'
let isBoardFlipped = false;

// Piece representations
const unicodePieces = {
    'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
    'p': '♟︎', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
};

const svgPieces = {
    'P': 'assets/pieces/wP.svg', 'N': 'assets/pieces/wN.svg', 'B': 'assets/pieces/wB.svg', 'R': 'assets/pieces/wR.svg', 'Q': 'assets/pieces/wQ.svg', 'K': 'assets/pieces/wK.svg',
    'p': 'assets/pieces/bP.svg', 'n': 'assets/pieces/bN.svg', 'b': 'assets/pieces/bB.svg', 'r': 'assets/pieces/bR.svg', 'q': 'assets/pieces/bQ.svg', 'k': 'assets/pieces/bK.svg'
};

const pieceSets = {
    unicode: unicodePieces,
    svg: svgPieces
};

// DOM elements
const boardEl = document.getElementById('chessboard');
const turnInfoEl = document.getElementById('turnInfo');
const gameStatusEl = document.getElementById('gameStatusInfo');
const moveListEl = document.getElementById('moveList');
const capturedWhiteEl = document.querySelector('.captured-white');
const capturedBlackEl = document.querySelector('.captured-black');
const promotionModal = document.getElementById('promotionModal');
const textInputModal = document.getElementById('textInputModal');

/**
 * The core chess engine class.
 * Manages the board state, move generation, and game rules.
 * This class is pure logic and has no direct DOM manipulation.
 */
class ChessEngine {
    constructor(fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1') {
        this.board = [];
        this.turn = 'w';
        this.castling = { w: { K: true, Q: true }, b: { K: true, Q: true } };
        this.enPassant = null;
        this.halfMoves = 0;
        this.fullMoves = 1;
        this.history = [];
        this.historyIndex = -1;
        this.zobrist = new Zobrist();
        this.historyHash = new Set();
        this.capturedPieces = { w: [], b: [] };
        this.loadFen(fen);
        this.updateZobristHash();
    }

    /**
     * Loads a position from a FEN string.
     * @param {string} fen FEN string.
     */
    loadFen(fen) {
        // ... (FEN loading logic here)
    }

    /**
     * Generates a FEN string for the current board state.
     * @returns {string} The FEN string.
     */
    toFen() {
        // ... (FEN generation logic here)
    }

    /**
     * Updates the Zobrist hash based on the current board state.
     */
    updateZobristHash() {
        this.zobrist.updateHash(this);
    }

    /**
     * Makes a move on the board.
     * @param {Object} move - The move object.
     * @param {number} move.from - The starting square index.
     * @param {number} move.to - The destination square index.
     * @param {string} [move.promotion] - The piece to promote to (e.g., 'Q').
     */
    makeMove(move) {
        // ... (Detailed move execution logic: update board, castling rights, en passant, etc.)
    }

    /**
     * Reverts the last move from history.
     */
    undoMove() {
        // ... (Undo logic: pop history, restore board, state)
    }

    /**
     * Generates all pseudo-legal moves for the current side.
     * @returns {Array<Object>} An array of move objects.
     */
    generateMoves() {
        // ... (Move generation logic for each piece type)
    }

    /**
     * Filters pseudo-legal moves to return only legal moves.
     * @returns {Array<Object>} An array of legal move objects.
     */
    getLegalMoves() {
        const pseudoLegalMoves = this.generateMoves();
        return pseudoLegalMoves.filter(move => {
            // ... (Checks if move leaves king in check)
        });
    }

    /**
     * Checks if a side is in check.
     * @param {string} color - The color to check ('w' or 'b').
     * @returns {boolean} True if the side is in check.
     */
    isCheck(color = this.turn) {
        // ... (Logic to check for check)
    }

    /**
     * Checks if the current position is a checkmate.
     * @returns {boolean} True if checkmate.
     */
    isCheckmate() {
        return this.isCheck() && this.getLegalMoves().length === 0;
    }

    /**
     * Checks if the current position is a stalemate.
     * @returns {boolean} True if stalemate.
     */
    isStalemate() {
        return !this.isCheck() && this.getLegalMoves().length === 0;
    }

    /**
     * Checks for draw by insufficient material.
     * @returns {boolean} True if insufficient material.
     */
    isInsufficientMaterial() {
        // ... (Logic for insufficient material)
    }

    /**
     * Checks for draw by threefold repetition.
     * @returns {boolean} True if threefold repetition.
     */
    isThreefoldRepetition() {
        // ... (Logic to check for repetition using Zobrist hash history)
    }

    /**
     * Checks for draw by the 50-move rule.
     * @returns {boolean} True if 50-move rule applies.
     */
    isFiftyMoveRule() {
        return this.halfMoves >= 100;
    }

    /**
     * Returns the game status: 'ongoing', 'checkmate', 'stalemate', 'draw'.
     * @returns {string} The game status.
     */
    getGameStatus() {
        // ... (Game status logic)
    }

    /**
     * Perft test function to validate move generation.
     * @param {number} depth - The depth to search.
     * @returns {number} The total number of nodes at the given depth.
     */
    perft(depth) {
        // ... (Perft logic for move generation validation)
    }
}

// Zobrist Hashing implementation
class Zobrist {
    constructor() {
        this.table = {};
        this.pieces = ['P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k'];
        this.squares = Array.from({ length: 64 }, (_, i) => i);
        this.initializeTable();
        this.blackToMove = Math.random();
        this.castling = {
            'wK': Math.random(), 'wQ': Math.random(),
            'bK': Math.random(), 'bQ': Math.random()
        };
        this.enPassant = Array.from({ length: 8 }, (_, i) => Math.random());
    }

    initializeTable() {
        // ... (Populate random numbers for each piece on each square)
    }

    updateHash(engine) {
        // ... (Calculate hash based on current board state)
    }
}

// --- UI Logic and Event Handlers ---

/**
 * Initializes the game board and controls.
 */
function initGame() {
    chessEngine = new ChessEngine();
    renderBoard();
    updateUI();
    setupListeners();
    loadSettings();
}

/**
 * Renders the chessboard and pieces.
 */
function renderBoard() {
    // ... (DOM creation for board, squares, pieces, coordinates)
}

/**
 * Updates the board UI to match the engine's state.
 */
function updateUI() {
    // ... (Clears highlights, updates piece positions, turn info, captured pieces, move list)
}

/**
 * Handles a square click event.
 * @param {Event} event - The click event.
 */
function onSquareClick(event) {
    const squareEl = event.currentTarget;
    const pieceEl = squareEl.querySelector('.piece');
    const squareIndex = parseInt(squareEl.dataset.index);

    if (selectedSquare) {
        // A piece is already selected, try to move it
        const fromIndex = selectedSquare.dataset.index;
        const move = { from: parseInt(fromIndex), to: squareIndex };
        
        // ... (Check for promotion and make move)
        handleMove(move);

    } else if (pieceEl && pieceEl.dataset.color === chessEngine.turn) {
        // No piece selected, select this one
        selectedSquare = squareEl;
        selectedSquare.classList.add('highlight-selected');
        highlightLegalMoves(squareIndex);
    }
}

/**
 * Handles the completion of a move, including UI updates and AI turn.
 * @param {Object} move - The move object.
 */
function handleMove(move) {
    const legalMoves = chessEngine.getLegalMoves();
    const isLegal = legalMoves.some(m => m.from === move.from && m.to === move.to && (m.promotion || '') === (move.promotion || ''));

    if (isLegal) {
        chessEngine.makeMove(move);
        selectedSquare = null;
        lastMove = move;
        updateUI();
        playSound('move');
        
        if (chessEngine.getGameStatus() === 'ongoing' && aiDifficulty > 0) {
            setTimeout(handleAITurn, 500);
        }
    } else {
        selectedSquare.classList.remove('highlight-selected');
        clearHighlights();
        selectedSquare = null;
    }
}

/**
 * Handles the AI's turn.
 */
async function handleAITurn() {
    const aiColor = playerColor === 'white' ? 'b' : 'w';
    if (chessEngine.turn !== aiColor) return;
    
    // ... (Call to minimax or random move based on difficulty)
    const move = await minimax(chessEngine, aiDifficulty, aiColor);
    
    if (move) {
        chessEngine.makeMove(move);
        lastMove = move;
        updateUI();
        playSound('move');
    }
}

/**
 * Sets up all main event listeners for the UI.
 */
function setupListeners() {
    // ... (Listeners for New Game, AI difficulty, Flip Board, Undo/Redo, Themes, etc.)
}

/**
 * Prompts the user for a promotion choice.
 * @param {Object} move - The move object.
 * @returns {Promise<string>} A promise that resolves with the chosen piece ('Q', 'R', 'B', 'N').
 */
function handlePromotion(move) {
    // ... (Modal logic for promotion)
}

/**
 * Highlights all legal moves for a given square.
 * @param {number} squareIndex - The index of the square to highlight moves for.
 */
function highlightLegalMoves(squareIndex) {
    const legalMoves = chessEngine.getLegalMoves();
    legalMoves.forEach(move => {
        if (move.from === squareIndex) {
            // ... (Add 'legal-move' class and check for piece presence)
        }
    });
}

/**
 * Clears all legal move highlights.
 */
function clearHighlights() {
    // ... (Removes 'legal-move' and 'highlight-selected' classes)
}

/**
 * Helper to get SAN notation for a move.
 * @param {Object} move - The move object.
 * @returns {string} The SAN string.
 */
function getSan(move) {
    // ... (SAN generation logic)
}

/**
 * Handles the AI hint feature.
 */
async function handleHint() {
    // ... (Calls minimax with depth 3 and highlights the best move)
}

/**
 * Plays a sound effect.
 * @param {string} soundName - The name of the sound ('move', 'capture', etc.).
 */
function playSound(soundName) {
    // ... (Audio logic with mute toggle)
}

// --- Initial setup ---
document.addEventListener('DOMContentLoaded', initGame);
