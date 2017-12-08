import hashlib
import json
from time import time
import requests
from urllib.parse import urlparse


# =======================================================================================
# BLOCKCHAIN
# =======================================================================================

class Blockchain:
    
    """
        A blockchain is a digital ledger in which transactions made in bitcoin or another
        crypto currency are recorded chronologically and publicly. It can be said that is
        like a public database where new data are stored in a container called a block and
        each block is added to an immutable chain (blockchain) with data added in the past.

        The data on each transaction can be of any type.
    """

    # -----------------------------------------------------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------------------------------------------------
    def __init__(self):
        
        """
            Creates a instance of a blockchain that can record transactions and be
            validated
        """
        self.current_transactions = []
        self.chain = []
        self.nodes = set()
        self.new_block(previous_hash='1', proof=100)

    # -----------------------------------------------------------------------------------
    # REGISTER NODE
    # -----------------------------------------------------------------------------------
    def register_node(self, address):
        """
            Adds a new node to the set of nodes of nodes that are part of the blockchain
            :param address: Address of the node. Eg. 'http://192.168.0.5:5000'
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    # -----------------------------------------------------------------------------------
    # VALID CHAIN
    # -----------------------------------------------------------------------------------
    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
        :param chain: A blockchain
        :return: True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")

            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False
            last_block = block
            current_index += 1
        return True

    # -----------------------------------------------------------------------------------
    # VALID CHAIN
    # -----------------------------------------------------------------------------------
    def resolve_conflicts(self):
        """
            This is our consensus algorithm, it resolves conflicts by replacing our chain
            with the longest one in the network.
            :return: True if our chain was replaced, False if not
        """

        neighbours = self.nodes
        new_chain = None

        # Only a chain longer than ours is going to be accepted
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/api/v1/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True
        return False

    # -----------------------------------------------------------------------------------
    # NEW BLOCK
    # -----------------------------------------------------------------------------------
    def new_block(self, proof, previous_hash):
        """
            Create a new Block in the Blockchain
            :param proof: The proof given by the Proof of Work algorithm
            :param previous_hash: Hash of previous Block
            :return: New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []
        self.chain.append(block)
        return block

    # -----------------------------------------------------------------------------------
    # NEW TRANSACTION
    # -----------------------------------------------------------------------------------
    def new_transaction(self, sender, recipient, amount):
        """
            Creates a new transaction to go into the next mined Block
            :param sender: Address of the Sender
            :param recipient: Address of the Recipient
            :param amount: Amount
            :return: The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    # -----------------------------------------------------------------------------------
    # LAST_BLOCK
    # -----------------------------------------------------------------------------------
    @property
    def last_block(self):
        return self.chain[-1]

    # -----------------------------------------------------------------------------------
    # HASH
    # -----------------------------------------------------------------------------------
    @staticmethod
    def hash(block):
        """
            Creates a SHA-256 hash of a Block
            :param block: Block
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    # -----------------------------------------------------------------------------------
    # PROOF OF WORK
    # -----------------------------------------------------------------------------------
    def proof_of_work(self, last_proof):
        """
            Simple Proof of Work Algorithm:
             - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
             - p is the previous proof, and p' is the new proof
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    # -----------------------------------------------------------------------------------
    # PROOF OF WORK
    # -----------------------------------------------------------------------------------
    @staticmethod
    def valid_proof(last_proof, proof):
        """
            Validates the Proof
            :param last_proof: Previous Proof
            :param proof: Current Proof
            :return: True if correct, False if not.
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"