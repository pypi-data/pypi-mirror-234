# Paytring\Python
---
### Installation
---
The source code is currently hosted on GitHub at : https://github.com/paytring/python-sdk

Binary installers for the latest released version are available at the Python Package Index (PyPI)

```
pip install paytring
```
## Set-Up Environment Variables
---
```
import  os
os.environ['key'] = "your_key"
os.environ['secret'] = "your_secret"
```
## Payment Usage
---
```
from paytring.client import Order
```

#### Create Instance
```
order = Order()
```

## Create Order
---
##### Input Parameter

- Receipt ID(string)
- Payment_Info (Dictionary)
- Callback Url(string)
- Customer Info ( Dictionary )

###### Optional Parameters
- Billing Info ( Dictionary )
- Shipping Info ( Dictionary )
- Notes ( Dictionary )
- TPV ( Dictionary )
- PG (String)
- PG Pool ID (String)


#### Methods

```python
payment_info = {
    "amount": "100",
    "currency": "INR"  # currency INR or USD
}

customer_info = {
    "cname": "test",
    "email": "abc@gmail.com" -> it will be baseEncode256,
    "phone": "9999999999"
}

billing_info = {
    "firstname" : "John",
    "lastname" : "Doe",
    "phone" : "09999999999",
    "line1" : "Address Line 1",
    "line2" : "Address Line 2",
    "city" : "Gurugram",
    "state" : "Haryana",
    "country" : "India",
    "zipcode" : "122001"
}

shipping_info = {
    "firstname" : "John",
    "lastname" : "Doe",
    "phone" : "09999999999",
    "line1" : "Address Line 1",
    "line2" : "Address Line 2",
    "city" : "Gurugram",
    "state" : "Haryana",
    "country" : "India",
    "zipcode" : "122001"
}

notes = {
    "udf1" : "udf1",
    "udf2" : "udf2",
    "udf3" : "udf3",
}

tpv = [
    {
        "name": "Test",
        "account_number": "0000001234567890",
        "ifsc": "BankIFSC0001"
    }
]


response = order.create(
    receipt_id,
    callback_url,
    payment_info,
    customer_info,
    billing_info(optioanl),
    shipping_info(optioanl),
    notes(optioanl),
    tpv(optioanl),
    pg(optioanl),
    pg_pool_id(optional)
)
```

#### Response

```
{
"status": true,
"url": "www.makepayment.com",
"order_id": "365769619161481216"
}
```

## Fetch Order
---
##### Input Paramete

- Order ID(string)

#### Methods
```

order.fetch(
    order_id
)
```

### Response
```
{
    "status": true,
    "order": {
        "order_id": "489651149222183338",
        "receipt_id": "testmode323",
        "pg_transaction_id": "489651179018519803",
        "amount": 100,
        "currency": "INR",
        "pg": "RazorPay",
        "method": "UPI",
        "order_status": "success",
        "unmapped_status": "captured",
        "customer": {
            "name": "John",
            "email": "abc@gmail.com",
            "phone": "9999999999"
        },
        "notes": {
            "udf1": "",
            "udf2": "",
            "udf3": "",
            "udf4": "",
            "udf5": "",
            "udf6": "",
            "udf8": "",
            "udf9": "",
            "udf10": ""
        },
        "billing_address": {
            "firstname": "",
            "lastname": "",
            "phone": "",
            "line1": "",
            "line2": "",
            "city": "",
            "state": "",
            "country": "",
            "zipcode": ""
        },
        "shipping_address": {
            "firstname": "",
            "lastname": "",
            "phone": "",
            "line1": "",
            "line2": "",
            "city": "",
            "state": "",
            "country": "",
            "zipcode": ""
        },
        "additional_charges": 0,
        "mdr": ""
    }
}
```

## Fetch Order By Receipt-ID
---
#### Input Paramete

- Receipt ID(string)

#### Methods
```

order.fetch_by_receipt_id(
    receipt_id
)
```

### Response
```
{
    "status": true,
    "order": {
        "order_id": "489651149222183338",
        "receipt_id": "testmode323",
        "pg_transaction_id": "489651179018519803",
        "amount": 100,
        "currency": "INR",
        "pg": "RazorPay",
        "method": "UPI",
        "order_status": "success",
        "unmapped_status": "captured",
        "customer": {
            "name": "test",
            "email": "abc@gmail.com",
            "phone": "9999999999"
        },
        "notes": {
            "udf1": "",
            "udf2": "",
            "udf3": "",
            "udf4": "",
            "udf5": "",
            "udf6": "",
            "udf8": "",
            "udf9": "",
            "udf10": ""
        },
        "billing_address": {
            "firstname": "",
            "lastname": "",
            "phone": "",
            "line1": "",
            "line2": "",
            "city": "",
            "state": "",
            "country": "",
            "zipcode": ""
        },
        "shipping_address": {
            "firstname": "",
            "lastname": "",
            "phone": "",
            "line1": "",
            "line2": "",
            "city": "",
            "state": "",
            "country": "",
            "zipcode": ""
        },
        "additional_charges": 0,
        "mdr": ""
    }
}
```

## Refund Order
---
##### Input Paramete

- Order ID(string)

#### Methods
```

order.refund(
    order_id
)
```

### Response

#### Success Response
```
{
    "status": true,
    "message": "Refund has been initiated"
}
```
#### Error Response 
```
{
    "status": false,
    "error": {
        "message": "error message here",
        "code": 204
    }
}
```


## Subscription Usage
---
```
from paytring.client import Subscription
```

#### Create Instance
```
subscription = Subscription()
```

## Create Plan
---
##### Input Parameter

- Plan ID(string)
- Payment_Info (Dictionary)
- Plan Info ( Dictionary )
- Notes ( Dictionary ) 


#### Methods

```python
payment_info = {
    "amount": "100",
    "currency": "INR"  # currency INR or USD
}

plan_info = {
    "title": "Daily 1 rupee plan",
    "description": "test plan",
    "frequency": "1",
    "cycle": "12",
}

notes = {
    "udf1" : "udf1",
    "udf2" : "udf2",
    "udf3" : "udf3",
}

response = subscription.create_plan(
    plan_id,
    payment_info,
    plan_info,
    notes
)
```

#### Response

```
{
    'status': True,
    'plan_id': '552678261629388919'
}
```

## Fetch Plan
---
##### Input Paramete

- Plan ID(string)

#### Methods
```

subscription.fetch_plan(
    plan_id
)
```

### Response
```
{
    'status': True,
    'plan': {
        'plan_id': '552678261629388919', 
        'mer_reference_id': 'PLAN1234768547984', 
        'amount': 100, 
        'currency': 'INR', 
        'plan_status': 'created', 
        'frequency': '1', 
        'cycle': '12', 
        'notes': {
            'udf1': 'udf1',
            'udf2': 'udf2', 
            'udf3': 'udf3'
        }
    }
}
```

## Fetch Plan By Receipt-ID
---
#### Input Paramete

- Receipt ID(string)

#### Methods
```

subscription.fetch_plan_by_receipt_id(
    receipt_id
)
```

### Response
```
{
    'status': True,
    'plan': {
        'plan_id': '552678261629388919', 
        'mer_reference_id': 'PLAN1234768547984', 
        'amount': 100, 
        'currency': 'INR', 
        'plan_status': 'created', 
        'frequency': '1', 
        'cycle': '12', 
        'notes': {
            'udf1': 'udf1',
            'udf2': 'udf2', 
            'udf3': 'udf3'
        }
    }
}
```
#### Error Response 
```
{
    "status": false,
    "error": {
        "message": "error message here",
        "code": 204
    }
}
```

## Create Subscription
---
##### Input Parameter

- Receipt ID (string)
- Plan ID (string)
- Callback Url(string)
- Customer Info ( Dictionary )

###### Optional Parameters
- Billing Info ( Dictionary )
- Shipping Info ( Dictionary )
- Notes ( Dictionary )
- PG (String)
- PG Pool ID (String)


#### Methods

```python
payment_info = {
    "amount": "100",
    "currency": "INR"  # currency INR or USD
}

customer_info = {
    "cname": "test",
    "email": "abc@gmail.com" -> it will be baseEncode256,
    "phone": "9999999999"
}

billing_info = {
    "firstname" : "John",
    "lastname" : "Doe",
    "phone" : "09999999999",
    "line1" : "Address Line 1",
    "line2" : "Address Line 2",
    "city" : "Gurugram",
    "state" : "Haryana",
    "country" : "India",
    "zipcode" : "122001"
}

shipping_info = {
    "firstname" : "John",
    "lastname" : "Doe",
    "phone" : "09999999999",
    "line1" : "Address Line 1",
    "line2" : "Address Line 2",
    "city" : "Gurugram",
    "state" : "Haryana",
    "country" : "India",
    "zipcode" : "122001"
}

notes = {
    "udf1" : "udf1",
    "udf2" : "udf2",
    "udf3" : "udf3",
}


response = subscription.create_subscription(
    receipt_id,
    plan_id,
    callback_url,
    customer_info,
    billing_info(optioanl),
    shipping_info(optioanl),
    notes(optioanl),
    pg(optioanl),
    pg_pool_id(optional)
)
```

#### Response

```
{
"status": true,
"url": "https://api.paytring.com/pay/subscription/87583758943797",
"subscription_id": "87583758943797"
}
```

## Fetch Subscription
---
##### Input Paramete

- Subscription ID(string)

#### Methods
```

subscription.fetch_subscription(
    subscription_id
)
```

### Response
```
{
    'status': True,
    'subscription': {
        'subscription_id': '552679210171237835', 
        'mer_reference_id': '6574363653869523845', 
        'amount': 100, 
        'currency': 'INR', 
        'subscription_status': 'active'
    }
}
```

## Fetch Subscription By Receipt-ID
---
#### Input Paramete

- Receipt ID(string)

#### Methods
```

subscription.fetch_subscription_by_receipt_id(
    receipt_id
)
```

### Response
```
{
    'status': True,
    'subscription': {
        'subscription_id': '552679210171237835', 
        'mer_reference_id': '6574363653869523845', 
        'amount': 100, 
        'currency': 'INR', 
        'subscription_status': 'active'
    }
}
```

#### Error Response 
```
{
    "status": false,
    "error": {
        "message": "error message here",
        "code": 204
    }
}
```