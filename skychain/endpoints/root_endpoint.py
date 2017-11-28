from skychain import skytrack
from flask import jsonify, request


# --------------------------------------------------------------------------
# GET: /ACCOUNT
# --------------------------------------------------------------------------
@skytrack.route('/', methods=['GET'])
def get_root():
    """
        Gets the requester's IP Address and the User Agent and builds a tiny
        service status response message
        :return: Status response json
    """
    return jsonify(
        {
            "ApiPlatform": "Sky Blockchain API 1.0.0",
            "IP Address": request.remote_addr,
            "User Agent": request.headers.get('User-Agent')
        }
    ), 200