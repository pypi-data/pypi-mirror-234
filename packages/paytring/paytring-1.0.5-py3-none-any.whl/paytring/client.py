from paytring.constant.url import URL
from paytring.resources.paytring import Paytring
from paytring.utility.utility import Utility
import requests
import base64

class Order(Paytring):

    def __init__(self):
        super().__init__()
        self.order_create_url = URL.ORDER_CREATE
        self.order_fetch_url = URL.FETCH_ORDER
        self.order_fetch_by_receipt_url = URL.FETCH_ORDER_BY_RECIEPT
        self.refund_url = URL.REFUND
        self.utility_obj = Utility()

    def create(self, receipt_id, amount, callback_url,customer_info, currency, pg=None, pg_pool_id=None):
        """
        Use to create an Order on Paytring

        Args(type=string):
            'receipt' : Receipt Id for the order
            'amount' :  Amount of Order
            'callback_url' : The URL where the PAYTRING will send success/failed etc. response.
            'customer_info' : Info. about Customer.
            'currency' : Currency in which the amount is entered 

        Returns:
            Order Dict created for given reciept ID
        """
        try:
            self.utility_obj.vaidate_customer_info(customer_info)
            self.utility_obj.validate_email(customer_info['email'])
            self.utility_obj.validate_phone(customer_info['phone'])
            self.utility_obj.validate_amount(amount)
            self.utility_obj.validate_callback_url(callback_url)
            self.utility_obj.validate_receipt(receipt_id)
            self.utility_obj.validate_currency(currency.upper())
        
            payload = {
                "key": self.key,
                "receipt_id": receipt_id,
                "amount": amount,
                "callback_url": callback_url,
                "cname": customer_info['cname'],
                "email": customer_info['email'],
                "phone": customer_info['phone'],
                "currency" : currency
            }

            if pg is not None:
                self.utility_obj.validate_pg(pg)
                payload['pg'] = pg

            if pg_pool_id is not None:
                self.utility_obj.validate_currency(pg_pool_id)
                payload['pg_pool_id'] = pg_pool_id

            hash = self.utility_obj.create_hash(payload)
            payload['hash'] = hash

            response = requests.post(self.order_create_url, payload)
            response = response.json()
            if response['status'] == True:
                    if 'url' in response.keys():
                        response['url'] = base64.b64decode(response['url']).decode('utf-8')
                    return {"response": response}
            return {"response": response}
        except Exception as e:
             return {"response" : str(e)}
        
    def fetch(self, order_id):
        """
        Use to fetch an Order on Paytring throu

        Args: 
            order_id : Id for which order object has to be retrieved
        
        Returns:
            Order Dict for given order_id
        """
        try:
            self.utility_obj.validate_order(order_id)

            payload = {
                "key": self.key,
                "id": order_id
            }
            hash = self.utility_obj.create_hash(payload)
            payload['hash'] = hash
            response = requests.post(self.order_fetch_url, payload)
            response = response.json()
            if response['status'] == True:
                return {"response": response}
            return {"response": response}
        except Exception as e:
            return {"response": str(e)}
        
    def fetch_by_receipt_id(self, receipt_id):
        """
        Use to fetch an Order on Paytring by receipt-id

        Args: 
            receipt_id : Id for which order object has to be retrieved
        
        Returns:
            Order Dict for given receipt_id
        """

        try:
            self.utility_obj.validate_receipt(receipt_id)

            payload = {
                "key": self.key,
                "id": receipt_id
            }
            hash = self.utility_obj.create_hash(payload)
            payload['hash'] = hash
            response = requests.post(self.order_fetch_by_receipt_url, payload)
            response = response.json()
            if response['status'] == True:
                return {"response": response}
            return {"response": response}
        except Exception as e:
            return {"response": str(e)}
        
    def refund(self, order_id):
        """
        Use to intaite refund on Paytring by order-id

        Args: 
            order_id : Id for which refund is to be intiated
        
        Returns:
            Dict containing 'status' and 'message'
        """

        try:
            payload = {
                "key": self.key,
                "id": order_id
            }
            hash = self.utility_obj.create_hash(payload)
            payload['hash'] = hash
            response = requests.post(self.refund_url, payload)
            response = response.json()
            if response['status'] == True:
                return {"response": response}
            return {"response": response}
        except Exception as e:
            return {"response": str(e)}
