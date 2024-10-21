from stockfish import Stockfish
from flask import Flask, request, jsonify
from pathlib import Path


app = Flask(__name__)


def get_best_moves(
    fen: str,
    num_moves: int,
    depth: int = None,
    options: dict = None
):
    binary_path = Path(__file__).parent / "stockfish-ubuntu-x86-64-avx2"
    stockfish = Stockfish(str(binary_path.resolve()))
    if depth is not None:
        stockfish.set_depth(depth)
    if options is not None:
        stockfish.update_engine_parameters(options)

    stockfish.set_fen_position(fen)
    return stockfish.get_top_moves(num_moves)


@app.route('/best_moves', methods=['POST'])
def best_moves():
    data = request.json
    fen = data['fen']
    num_moves = data['num_moves']
    depth = data.get('depth')
    options = data.get('options', {})

    best_moves = get_best_moves(fen, num_moves, depth, options)
    return jsonify(best_moves)
