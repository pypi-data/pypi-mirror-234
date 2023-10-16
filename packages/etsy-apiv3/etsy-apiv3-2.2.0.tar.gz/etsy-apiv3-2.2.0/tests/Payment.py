"""
Etsy Api V3 Sdk PaymentResource Tests.
"""
import unittest
from etsy_apiv3.models import Payment
from etsy_apiv3.utils import EtsySession, Response, EtsyRequestException
from etsy_apiv3.resources import PaymentResource

import test_credentials

class TestTransaction(unittest.TestCase):
    SUCCESS_RECEIPT_ID = "2672482884"
    WRONG_RECEIPT_ID = "2672482222"
    PAYMENT_IDS = [119519091349]
    WRONG_PAYMENT_IDS = [119519091322]
    LEDGER_ENTRY_IDS = []
    WRONG_LEDGER_ENTRY_IDS = []
    
    def setUp(self) -> None:
        self.session = EtsySession(
            test_credentials.CLIENT_KEY, test_credentials.CLIENT_SECRET,
            test_credentials.TOKEN
        )
        self.resource = PaymentResource(self.session)
        self.longMessage = True
    
    def test_get_payment_by_receipt_id(self):
        payment = self.resource.get_payment_by_receipt_id(self.session.me.shop_id, self.SUCCESS_RECEIPT_ID)
        self.assertIsInstance(
            payment, Response[Payment]
        )
        with self.assertRaises(EtsyRequestException):
            self.resource.get_payment_by_receipt_id(self.session.me.shop_id, self.WRONG_RECEIPT_ID)
    
    def test_get_shop_payments(self):
        payments = self.resource.get_shop_payments(self.session.me.shop_id, self.PAYMENT_IDS)
        self.assertIsInstance(
            payments, Response[Payment]
        )
        with self.assertRaises(EtsyRequestException):
            self.resource.get_payment_by_receipt_id(self.session.me.shop_id, self.WRONG_PAYMENT_IDS)

    
    def test_get_payment_by_account_ledger_entry_ids(self):
        payment = self.resource.get_payment_by_account_ledger_entry_ids(self.session.me.shop_id, self.LEDGER_ENTRY_IDS)
        self.assertIsInstance(
            payment, Response[Payment]
        )
        with self.assertRaises(EtsyRequestException):
            self.resource.get_payment_by_account_ledger_entry_ids(
                self.session.me.shop_id,
                self.WRONG_LEDGER_ENTRY_IDS
            )
    
    def test_get_payment__(self):
        self.resource.get_shop_payment_account_ledger_entries(self.session.me.shop_id, )
        pass
    
    
unittest.main()