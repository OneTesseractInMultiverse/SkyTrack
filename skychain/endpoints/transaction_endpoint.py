from skychain import sky_app, blockchain, node_id
from flask import jsonify, request


# --------------------------------------------------------------------------
# POST: /API/V1/TRANSACTION
# --------------------------------------------------------------------------
@sky_app.route('/api/v1/transaction', methods=['POST'])
def post_transaction():
    values = request.get_json()
    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return jsonify({"err": "Some of the required values are not present"}), 400
    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


