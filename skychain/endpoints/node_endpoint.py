from skychain import sky_app, blockchain, node_id
from flask import jsonify, request


# --------------------------------------------------------------------------
# GET: /API/V1/NODE/
# --------------------------------------------------------------------------
@sky_app.route('/api/v1/node', methods=['POST'])
def post_node():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return jsonify({"msg", "Please supply a valid list of nodes"}), 400
    for node in nodes:
        blockchain.register_node(node)
    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


# --------------------------------------------------------------------------
# GET: /API/V1/NODE/CONFLICT_STATUS
# --------------------------------------------------------------------------
@sky_app.route('/api/v1/node/conflict_status', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()
    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }
    return jsonify(response), 200