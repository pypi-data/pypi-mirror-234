from dataclasses import dataclass
from typing import List, Union
from etsy_apiv3.utils import EtsySession, Response
from etsy_apiv3.models import Payment, PaymentAccountLedgerEntry
from etsy_apiv3.utils.EtsyOauth2Session import EtsyOauth2Session

@dataclass
class PaymentResource:
    
    session: Union[EtsySession, EtsyOauth2Session]
    
    def get_shop_payments(self, shop_id: int, payment_ids: List[int]) -> Response[Payment]:
        endpoint = f"shops/{shop_id}/payments"
        params = {
            "payment_ids": payment_ids
        }
        response = self.session.request(endpoint, params=params)
        return Response[Payment](**response)
    
    def get_payment_by_receipt_id(self, shop_id: int, receipt_id: int) -> Response[Payment]:
        endpoint = f"shops/{shop_id}/receipts/{receipt_id}/payments"
        response = self.session.request(endpoint)
        return Response[Payment](**response)
    
    def get_payment_by_account_ledger_entry_ids(self, shop_id: int, ledger_entry_ids: List[int]) -> Response[Payment]:
        endpoint = f"shops/{shop_id}/payment-account/ledger-entries/payments"
        params = {
            "ledger_entry_ids": ledger_entry_ids
        }
        response = self.session.request(endpoint, params=params)
        return Response[Payment](**response)
    
    def get_shop_payment_account_ledger_entry(self, shop_id: int, ledger_entry_id: int) -> PaymentAccountLedgerEntry:
        endpoint = f"shops/{shop_id}/payment-account/ledger-entries/{ledger_entry_id}"
        response = self.session.request(endpoint)
        return PaymentAccountLedgerEntry(**response)
    
    def get_shop_payment_account_ledger_entries(self, shop_id: int, min_created: int, max_created: int, limit: int = 25, offset: int = 0) -> Response[PaymentAccountLedgerEntry]:
        """_summary_

        Args:
            shop_id (int): Target Shop ID
            min_created (int): The earliest unix timestamp for when a record was created. 
            max_created (int): The latest unix timestamp for when a record was created.
            limit (int, optional): The maximum number of results to return. Defaults to 25.
            offset (int, optional): The number of records to skip before selecting the first result. Defaults to 0.
        Returns:
            Response[PaymentAccountLedgerEntry]: Response Object By PaymentAccountLedgerEntry
        """
        endpoint = f"shops/{shop_id}/payment-account/ledger-entries"
        response = self.session.request(endpoint)
        return Response[PaymentAccountLedgerEntry](**response)
    
    
    