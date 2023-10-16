# Paytring\Python

## Usage

```python
from paytring import Order

```

### Create Order

- Create instance of class Order
```python
order = Order()
```


---
Input Parameter

- Receipt ID(string)
- Amount(string)
- Callback Url(string)
- Customer Info ( Dictionary )

Function
```python
customer_info = {
    "cname": "test",
    "email": "abc@gmail.com",
    "phone": "phone"
}


order.Create(
    receipt_id,
    amount,
    callback_url
    customer_info
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

### Fetch Order
---
Input Parameter

- Order ID(string)

Function
```

order.Fetch(
    order_id
)
```

### Response
```

{
"status": true,
"order": {
"order_id": "365760761810649088",
"receipt_id": "bg6mxmsb",
"amount": 100,
"customer": {
"name": "John Doe",
"email": "test@test.com",
"phone": "9999999999"
},
"order_status": "success",
"unmapped_status": "captured",
"bank": {
"code": "UPI",
"mode": "UPI",
"ref_num": "213384143547"
}}}

```
