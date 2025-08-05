# microserviceA_361

# Competitor Pricing Microservice – Communication Contract

The microservice provides competitor pricing data for specific UPCs via ZeroMQ using a JSON-based protocol. Supports three API types:

- `COMPETITOR_PRICE` – Get price for a single UPC  
- `COMPETITOR_PRICE_BATCH` – Get prices for multiple UPCs  
- `COMPETITOR_PRICE_BATCH_FLAG` – Compare your prices against competitor prices  

---

## Microservice Setup

**Binding Address:**  
The microservice listens on:

```
tcp://localhost:5678
```

---

## Request Format

Send a JSON message using `zmq.REQ` socket. The outer object must contain `api_type` and either a `request` (for single) or `requests` (for batch) as shown below.

---

###  `COMPETITOR_PRICE` – Single Price Lookup

#### Request Format:

```json
{
  "api_type": "COMPETITOR_PRICE",
  "request": {
    "id": "req-1",
    "upc": "123456789101"
  }
}
```

#### Response Format:

```json
{
  "api_type": "COMPETITOR_PRICE",
  "response": {
    "id": "req-1",
    "competitor": "RetailerA",
    "upc": "123456789101",
    "price": "19.99"
  }
}
```

---

### `COMPETITOR_PRICE_BATCH` – Batch Price Lookup

#### Request Format:

```json
{
  "api_type": "COMPETITOR_PRICE_BATCH",
  "requests": [
    {
      "id": "req-1",
      "upc": "123456789101"
    },
    {
      "id": "req-2",
      "upc": "123456789102"
    }
  ]
}
```

#### Response Format:

```json
{
  "api_type": "COMPETITOR_PRICE_BATCH",
  "responses": [
    {
      "id": "req-1",
      "competitor": "RetailerA",
      "upc": "123456789101",
      "price": "19.99"
    },
    {
      "id": "req-2",
      "competitor": "RetailerB",
      "upc": "123456789102",
      "price": "15.49"
    }
  ]
}
```

---

### `COMPETITOR_PRICE_BATCH_FLAG` – Compare Prices

#### Request Format:

```json
{
  "api_type": "COMPETITOR_PRICE_BATCH_FLAG",
  "requests": [
    {
      "id": "req-1",
      "upc": "123456789101",
      "price": "20.00"
    },
    {
      "id": "req-2",
      "upc": "123456789102",
      "price": "10.00"
    }
  ]
}
```

#### Response Format:

```json
{
  "api_type": "COMPETITOR_PRICE_BATCH_FLAG",
  "responses": [
    {
      "id": "req-1",
      "competitor": "RetailerA",
      "upc": "123456789101",
      "comparison": "higher_price"
    },
    {
      "id": "req-2",
      "competitor": "RetailerB",
      "upc": "123456789102",
      "comparison": "lower_price"
    }
  ]
}
```

---

## Example Python Code (Client Side)

```python
import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5678")

msg = {
    "api_type": "COMPETITOR_PRICE",
    "request": {
        "id": "req-1",
        "upc": "123456789101"
    }
}

socket.send_json(msg)
response = socket.recv_json()
print("Received response:", json.dumps(response, indent=2))
```

---

## Reminder
- Only UPCs that exist in `pricing_data.json` will return valid results.

---

## Pricing API Sequence Diagram

<img width="789" height="527" alt="Screenshot 2025-08-05 at 00 05 00" src="https://github.com/user-attachments/assets/641791c8-d836-4bfa-98bf-484a7fa7c299" />

