import json
import zmq

pricing_data = {}

def get_competitor_price(request_data):

    request = request_data.get("request")
    upc = request.get("upc")
    request_id = request.get("id", "req-1")

    return {
        "api_type": "COMPETITOR_PRICE",
        "response": {
            "id": request_id,
            "competitor": pricing_data[upc]['retailer'],
            "upc": upc,
            "price": pricing_data[upc]['price']
        }
    }


def get_competitor_price_batch(request_data):

    requests = request_data.get("requests", [])
    responses = []

    for request in requests:
        request_id = request.get("id", "unknown")
        upc = request.get("upc")

        responses.append({
            "id": request_id,
            "competitor": pricing_data[upc]['retailer'],
            "upc": upc,
            "price": pricing_data[upc]['price']
        })

    return {
        "api_type": "COMPETITOR_PRICE_BATCH",
        "responses": responses
    }


def get_competitor_price_batch_flag(request_data):

    requests = request_data.get("requests", [])
    responses = []

    for request in requests:
        request_id = request.get("id", "unknown")
        upc = request.get("upc")
        provided_price = request.get("price")

        stored_price = float(pricing_data[upc]['price'])
        provided_price_float = float(provided_price)

        if provided_price_float > stored_price:
            comparison = "higher_price"
        elif provided_price_float < stored_price:
            comparison = "lower_price"
        else:
            comparison = "same_price"

        responses.append({
            "id": request_id,
            "competitor": pricing_data[upc]['retailer'],
            "upc": upc,
            "comparison": comparison
        })

    return {
        "api_type": "COMPETITOR_PRICE_BATCH_FLAG",
        "responses": responses
    }

if __name__ == "__main__":

    result = {}
    with open('pricing_data.json', 'r') as file:
        pricing_data = json.load(file)

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5678")

    print("Microservice is running...")

    while True:
        message = socket.recv_json()

        api_type = message.get("api_type", "").strip()

        if api_type == "COMPETITOR_PRICE":
            result = get_competitor_price(message)

        elif api_type == "COMPETITOR_PRICE_BATCH":
            result = get_competitor_price_batch(message)

        elif api_type == "COMPETITOR_PRICE_BATCH_FLAG":
            result = get_competitor_price_batch_flag(message)

        socket.send_json(result)