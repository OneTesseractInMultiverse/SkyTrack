from skychain import sky_app, blockchain, node_id
from flask import jsonify, request
import datetime


# --------------------------------------------------------------------------
# GET: /API/V1/CHAIN
# --------------------------------------------------------------------------
@sky_app.route('/api/v1/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


# --------------------------------------------------------------------------
# GET: /API/V1/CHAIN/MINE
# --------------------------------------------------------------------------
@sky_app.route('/api/v1/chain/mine', methods=['GET'])
def get_my_chain():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_id,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    stamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

    response = {
        'message': f'New block forged at:[{stamp}]',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }

    return jsonify(response), 200
