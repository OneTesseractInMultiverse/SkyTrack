import hashlib
import json
from unittest import TestCase
from skychain.models.blockchain import Blockchain


class BlockchainTestCase(TestCase):

    def setUp(self):
        self.blockchain = Blockchain()

    def create_block(self, proof=123, previous_hash='abc'):
        self.blockchain.new_block(proof, previous_hash)

    def create_transaction(self, sender='a', recipient='b', amount=1):
        self.blockchain.new_transaction(
            sender=sender,
            recipient=recipient,
            amount=amount
        )


# =======================================================================================
# TEST CLASS TEST REGISTER NODES
# =======================================================================================
class TestRegisterNodes(BlockchainTestCase):
    
    """
        This test class contains all the test cases for node registration
    """

    # -----------------------------------------------------------------------------------
    # TEST VALID NODES
    # -----------------------------------------------------------------------------------
    def test_valid_nodes(self):
        # Prepare
        blockchain = Blockchain()
        # Act
        blockchain.register_node('http://192.168.0.1:5000')
        # Assert
        self.assertIn('192.168.0.1:5000', blockchain.nodes)

    # -----------------------------------------------------------------------------------
    # TEST MALFORMED NODES
    # -----------------------------------------------------------------------------------
    def test_malformed_nodes(self):
        # Prepare
        blockchain = Blockchain()
        # Act
        blockchain.register_node('http//192.168.0.1:5000')
        # Assert
        self.assertNotIn('192.168.0.1:5000', blockchain.nodes)

    # -----------------------------------------------------------------------------------
    # TEST IDEMPOTENCY
    # -----------------------------------------------------------------------------------
    def test_idempotency(self):
        # Prepare
        blockchain = Blockchain()
        # Act
        blockchain.register_node('http://192.168.0.1:5000')
        blockchain.register_node('http://192.168.0.1:5000')
        # Assert
        assert len(blockchain.nodes) == 1


# =======================================================================================
# TEST CLASS BLOCKS AND TRANSACTIONS
# =======================================================================================
class TestBlocksAndTransactions(BlockchainTestCase):

    # -----------------------------------------------------------------------------------
    # TEST BLOCK CREATION
    # -----------------------------------------------------------------------------------
    def test_block_creation(self):
        self.create_block()

        latest_block = self.blockchain.last_block

        # The genesis block is create at initialization, so the length should be 2
        assert len(self.blockchain.chain) == 2
        assert latest_block['index'] == 2
        assert latest_block['timestamp'] is not None
        assert latest_block['proof'] == 123
        assert latest_block['previous_hash'] == 'abc'

    # -----------------------------------------------------------------------------------
    # TEST CREATE TRANSACTION
    # -----------------------------------------------------------------------------------
    def test_create_transaction_is_not_null(self):
        # Prepare
        self.create_transaction()
        # Act
        transaction = self.blockchain.current_transactions[-1]
        # Assert
        assert transaction
        
    # -----------------------------------------------------------------------------------
    # TEST CREATE TRANSACTION RECIPIENT IS B
    # -----------------------------------------------------------------------------------
    def test_create_transaction_recipient_is_valid(self):
        # Prepare
        self.create_transaction()
        # Act
        transaction = self.blockchain.current_transactions[-1]
        # Assert
        assert transaction['recipient'] == 'b'
        
    # -----------------------------------------------------------------------------------
    # TEST CREATE TRANSACTION AMOUNT IS VALID
    # -----------------------------------------------------------------------------------
    def test_create_transaction_amount_is_valid(self):
        # Prepare
        self.create_transaction()
        # Act
        transaction = self.blockchain.current_transactions[-1]
        # Assert
        assert transaction['amount'] == 1
    
    # -----------------------------------------------------------------------------------
    # TEST CREATE TRANSACTION SENDER IS A
    # -----------------------------------------------------------------------------------
    def test_create_transaction_sender_is_a(self):
        # Prepare
        self.create_transaction()
        # Act
        transaction = self.blockchain.current_transactions[-1]
        # Assert
        assert transaction['sender'] == 'a'
        
    # -----------------------------------------------------------------------------------
    # TEST CREATE TRANSACTION RECIPIENT IS B
    # -----------------------------------------------------------------------------------
    def test_create_transaction_recipient_is_b(self):
        # Prepare
        self.create_transaction()
        # Act
        transaction = self.blockchain.current_transactions[-1]
        # Assert
        assert transaction['recipient'] == 'b'
        
    # -----------------------------------------------------------------------------------
    # TEST CREATE TRANSACTION AMOUNT IS ONE
    # -----------------------------------------------------------------------------------
    def test_create_transaction_amount_is_one(self):
        # Prepare
        self.create_transaction()
        # Act
        transaction = self.blockchain.current_transactions[-1]
        # Assert
        assert transaction['amount'] == 1
    
    # -----------------------------------------------------------------------------------
    # TEST BLOCK RESETS TRANSACTION INITIAL LENGTH IS ONE
    # -----------------------------------------------------------------------------------
    def test_block_resets_transactions_initial_length_is_one(self):
        # Assert
        self.create_transaction()
        # Act
        initial_length = len(self.blockchain.current_transactions)
        self.create_block()
        current_length = len(self.blockchain.current_transactions)
        #Assert
        assert initial_length == 1
        
    # -----------------------------------------------------------------------------------
    # TEST BLOCK RESETS TRANSACTION CURRENT LENGTH IS ZERO
    # -----------------------------------------------------------------------------------
    def test_block_resets_transactions_current_length_is_zero(self):
        # Assert
        self.create_transaction()
        # Act
        initial_length = len(self.blockchain.current_transactions)
        self.create_block()
        current_length = len(self.blockchain.current_transactions)
        #Assert
        assert current_length == 0

    # -----------------------------------------------------------------------------------
    # TEST RETURN LAST BLOCK
    # -----------------------------------------------------------------------------------
    def test_return_last_block(self):
        # Prepare
        self.create_block()
        # Act
        created_block = self.blockchain.last_block
        # Assert
        assert created_block is self.blockchain.chain[-1]
        
    # -----------------------------------------------------------------------------------
    # TEST RETURN LAST BLOCK LENGTH
    # -----------------------------------------------------------------------------------
    def test_return_last_block_length(self):
        # Prepare
        self.create_block()
        # Act
        created_block = self.blockchain.last_block
        # Assert
        assert len(self.blockchain.chain) == 2


# =======================================================================================
# TEST CLASS TEST HASHING AND PROOFS
# =======================================================================================
class TestHashingAndProofs(BlockchainTestCase):

    # -----------------------------------------------------------------------------------
    # TEST HASH LENGTH IS CORRECT
    # -----------------------------------------------------------------------------------
    def test_hash_length_is_correct(self):
        #Prepare
        self.create_block()
        # Act
        new_block = self.blockchain.last_block
        new_block_json = json.dumps(self.blockchain.last_block, sort_keys=True).encode()
        new_hash = hashlib.sha256(new_block_json).hexdigest()
        # Assert
        assert len(new_hash) == 64
        
    # -----------------------------------------------------------------------------------
    # TEST HASH IS CORRECT
    # -----------------------------------------------------------------------------------
    def test_hash_is_correct(self):
        #Prepare
        self.create_block()
        # Act
        new_block = self.blockchain.last_block
        new_block_json = json.dumps(self.blockchain.last_block, sort_keys=True).encode()
        new_hash = hashlib.sha256(new_block_json).hexdigest()
        # Assert
        assert new_hash == self.blockchain.hash(new_block)