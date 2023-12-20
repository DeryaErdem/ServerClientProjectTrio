# client.py
import trio

async def process_data(): #We create the client which request data from server
    try:
        stream = await trio.open_tcp_stream("localhost", 8765)
        async with stream:
            while True:
                response = await stream.receive_some(4096)
                if not response:
                    break
                print(f"Received from server: {response.decode('utf-8')}") #We print the data we take from server.(String)
    except trio.ClosedResourceError:
        print("Server closed the connection")

if __name__ == "__main__":
    trio.run(process_data)
