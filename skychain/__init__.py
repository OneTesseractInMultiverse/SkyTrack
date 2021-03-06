
#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import uuid
from flask import Flask
from flask_redis import FlaskRedis
from skychain.models.blockchain import Blockchain

# ------------------------------------------------------------------------------
# SETUP GENERAL APPLICATION
# ------------------------------------------------------------------------------
__version__ = '1.0.0'
sky_app = Flask('Brick')
sky_app.config.from_object('config')
sky_app.debug = True

# Connect to redis
redis_store = FlaskRedis(sky_app)

# Generate a globally unique address for this node
node_id = str(uuid.uuid4()).replace('-', '')

# Create the instance of blockchain
blockchain = Blockchain()

from skychain.endpoints import *