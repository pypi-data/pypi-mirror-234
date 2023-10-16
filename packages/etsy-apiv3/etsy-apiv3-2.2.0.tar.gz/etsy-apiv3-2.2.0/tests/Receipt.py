from typing import Coroutine
import unittest
from etsy_apiv3.models import Receipt, Transaction
from etsy_apiv3.utils import EtsySession, Response
from etsy_apiv3.resources import ReceiptResource
from etsy_apiv3.utils.RequestException import EtsyRequestException
import test_credentials

class TestReceipt(unittest.TestCase):
    
    SUCCESS_RECEIPT_ID = "2672482884"
    WRONG_RECEIPT_ID = "2672482222"
    SUCCESS_TRANSACTION_ID = "3246274562"
    WRONG_TRANSACTION_ID = "3246274561"
    SUCCESS_LISTING_ID = "963147161"
    WRONG_LISTING_ID = "963147162"
    WRONG_SHOP_ID = "3213213"
    
    def setUp(self) -> None:
        self.session = EtsySession(
            test_credentials.CLIENT_KEY, test_credentials.CLIENT_SECRET,
            test_credentials.TOKEN
        )
        self.resource = ReceiptResource(self.session)
        self.longMessage = True
        
    def test_get_receipt_by_id(self):
        success_receipt = self.resource.get_receipt_by_id(self.session.me.shop_id, self.SUCCESS_RECEIPT_ID)
        async_success_receipt = self.resource.aget_receipt_by_id(self.session.me.shop_id, self.SUCCESS_RECEIPT_ID)
        self.assertIsInstance(
            async_success_receipt, Coroutine
        )
        
        print(async_success_receipt)
        self.assertIsInstance(
            success_receipt, Receipt
        )
        
        with self.assertRaises(EtsyRequestException):
            self.resource.get_receipt_by_id(self.session.me.shop_id, self.WRONG_RECEIPT_ID)
    
    def test_get_receipts(self):
        receipts = self.resource.get_receipts(self.session.me.shop_id)
        self.assertIsInstance(
            receipts, Response
        )
        with self.assertRaises(EtsyRequestException):
            self.resource.get_receipts("321321321")
    
    def test_get_transaction_by_transaction_id(self):
        
        """
        Get Transaction By Success Transaction ID
        If transaction isinstance :class:`etsy_apiv3.models.Transaction`] return True
        Else Assert
        
        If Wrong Transaction ID Return EtsyRequestException return True
        Else AssertionError
        """
        
        transaction = self.resource.get_transaction_by_transaction_id(self.session.me.shop_id, self.SUCCESS_TRANSACTION_ID)
        self.assertIsInstance(transaction, Transaction, "Transaction Get Successfully By Transaction ID")
        with self.assertRaises(EtsyRequestException):
            self.resource.get_transaction_by_transaction_id(self.session.me.shop_id, self.WRONG_TRANSACTION_ID)
    
    def test_get_transactions_by_receipt_id(self):
        transactions = self.resource.get_transactions_by_receipt(self.session.me.shop_id, self.SUCCESS_RECEIPT_ID)
        self.assertIsInstance(
            transactions, Response
        )
        """with self.assertRaises(EtsyRequestException):
            self.resource.get_transactions_by_receipt(self.session.me.shop_id, self.WRONG_RECEIPT_ID)
        """
            
    def test_get_transactions_by_listing_id(self):
        transactions = self.resource.get_transactions_by_listing(self.session.me.shop_id, self.SUCCESS_LISTING_ID, 25)
        self.assertIsInstance(
            transactions, Response[Transaction]
        )
        with self.assertRaises(EtsyRequestException):
            self.resource.get_transactions_by_listing(self.session.me.shop_id, self.WRONG_LISTING_ID)
    
    def test_get_transactions_by_shop_id(self):
        transactions = self.resource.get_receipt_transactions_by_shop(self.session.me.shop_id)
        self.assertIsInstance(
            transactions, Response
        )
        with self.assertRaises(EtsyRequestException):
            self.resource.get_receipt_transactions_by_shop(self.WRONG_SHOP_ID)
        
    
unittest.main()
        