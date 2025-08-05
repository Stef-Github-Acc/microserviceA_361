import json
import zmq


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5678")

    while True:
        print("\n")
        print("PRICING MICROSERVICE TEST CLIENT")
        print("1. Test COMPETITOR_PRICE")
        print("2. Test COMPETITOR_PRICE_BATCH")
        print("3. Test COMPETITOR_PRICE_BATCH_FLAG")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ")

        if choice == '4':
            break

        if choice in ['1', '2', '3']:
            print("\nEnter your JSON request:")
            json_input = input()

            request_data = json.loads(json_input)
            socket.send_json(request_data)

            response = socket.recv_json()
            print("\nResponse:")
            print(json.dumps(response, indent=2))
        else:
            print("Invalid choice")

    socket.close()
    context.term()


if __name__ == "__main__":
    main()