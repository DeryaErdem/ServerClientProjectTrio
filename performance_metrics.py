import trio
import time
import psutil

async def measure_latency():
    stream = await trio.open_tcp_stream("localhost", 8765)
    start_time = time.time()
    await stream.receive_some(4096)
    latency = time.time() - start_time
    print(f"Latency: {latency:.10f} seconds")

async def measure_throughput(messages_to_send):
    stream = await trio.open_tcp_stream("localhost", 8765)
    start_time = time.time()
    total_data_size = 0

    for _ in range(messages_to_send):
        data = b"Performance Test Message"
        await stream.send_all(data)
        total_data_size += len(data)

    elapsed_time = time.time() - start_time
    throughput = messages_to_send / elapsed_time
    print(f"Throughput: {throughput:.4f} messages per second")
    print(f"Total Data Size: {total_data_size} bytes")
async def measure_resource_utilization(duration_seconds):
    async def measure():
        while True:
            cpu_percent = psutil.cpu_percent()
            memory_percent = psutil.virtual_memory().percent
            print(f"CPU Usage: {cpu_percent}% | Memory Usage: {memory_percent}%")
            await trio.sleep(5)

    # Use move_on_after to limit the execution to the specified duration
    with trio.move_on_after(duration_seconds):
        await measure()


async def measure_scalability(num_clients, messages_per_client):
    async def simulate_client(client_id):
        print(
            f"\nScalability Test: {num_clients} clients will try to take {messages_per_client} messages each. Please wait...\n")
        try:
            stream = await trio.open_tcp_stream("localhost", 8765)
            async with stream:
                for _ in range(messages_per_client):
                    message = f"Client {client_id} Message"
                    await stream.send_all(message.encode())

                    # Wait for the server's response
                    response = await stream.receive_some(4096)
                    if not response:
                        break
                    print(f"Received from server: {response.decode('utf-8')}")
        except trio.ClosedResourceError:
            print("Server closed the connection")

    async def run_simulation():
        async with trio.open_nursery() as nursery:
            for client_id in range(num_clients):
                nursery.start_soon(simulate_client, client_id)

    await run_simulation()


async def main():
    print("Running Latency Measurement:")
    await measure_latency()

    print("\nRunning Throughput Measurement please wait:")
    await measure_throughput(10000)

    resource_utilization_duration = 10
    print("\nRunning Resource Utilization Measurement please wait:")
    await measure_resource_utilization(resource_utilization_duration)


    print("\nRunning Scalability Test please wait:")
    await measure_scalability(num_clients=20, messages_per_client=10)
    print("\nScalability Test Completed. Testing is over!")

if __name__ == "__main__":
    trio.run(main)
