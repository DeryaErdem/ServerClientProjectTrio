# server.py
import trio

connected_clients = set()  # Maintain a set to track connected clients

async def stream_data(stream):  # data stream function
    connected_clients.add(stream)  # Add the new client to the set whenever a new client connects to the server
    print(f"New client connected. Total clients: {len(connected_clients)}")  # To be able to see the clients in the server. We print it into the log.

    count = 0  # we create a variable to track the unique messages for clients. Every client takes messages as a data point: 0 first and it increases over time
    try:
        while True:  # it opens the server
            data = f"Data Point {count}"
            await stream.send_all(data.encode('utf-8'))
            count += 1
            await trio.sleep(1)  # Stream data every 1 second; we can send it faster if needed
    except trio.BrokenResourceError:  # We do not take these errors often, but they are here for safety.
        print("Client closed the connection")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        connected_clients.remove(stream)  # Remove the disconnected client from the set
        print(f"Closing the server connection. Remaining clients: {len(connected_clients)}")  # if there is no error while the client is leaving the server, we print this log message.

async def main():
    print("WebSocket server started. Waiting for connections...")  # when we run the python file, we take this message as the first log
    await trio.serve_tcp(stream_data, port=8765)

if __name__ == "__main__":
    trio.run(main)
