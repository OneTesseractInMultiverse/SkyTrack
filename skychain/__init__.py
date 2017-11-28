
#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import uuid
from flask import Flask
from skychain.models.blockchain import Blockchain

# ------------------------------------------------------------------------------
# SETUP GENERAL APPLICATION
# ------------------------------------------------------------------------------
__version__ = '1.0.0'
skytrack = Flask('Brick')
skytrack.config.from_object('config')
skytrack.debug = True

# Generate a globally unique address for this node
node_id = str(uuid.uuid4()).replace('-', '')

# Create the instance of blockchain
blockchain = Blockchain()

from skychain.endpoints import *