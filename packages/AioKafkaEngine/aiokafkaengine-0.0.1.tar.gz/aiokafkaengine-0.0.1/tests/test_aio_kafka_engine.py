import os
import sys

# Get the path to the parent directory (one folder up from the test file)
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(parent_directory)

# Append the "src" folder to the Python path
src_folder = os.path.join(parent_directory, "src")
print(src_folder)

sys.path.append(src_folder)

import asyncio
from AioKafkaEngine.AioKafkaEngine import AioKafkaEngine
import pytest

@pytest.mark.asyncio
async def test_main():
    print("main")
    bootstrap_servers = ["localhost:9094"]
    topic = "test_topic"
    group_id = "test_group"
    engine = AioKafkaEngine(bootstrap_servers=bootstrap_servers, topic=topic)

    input_msg = {"key": "value"}

    print("start_consumer")
    await engine.start_consumer(group_id=group_id)
    print("start_producer")
    await engine.start_producer()
    
    await asyncio.gather(*[
        engine.produce_messages(),
        engine.consume_messages()
    ])

    print("put msg")
    await engine.send_queue.put(input_msg)
    
    print("get_msg")
    msg = await engine.receive_queue.get()

    assert msg == input_msg

    await asyncio.gather(*[
        engine.stop_consumer(),
        engine.stop_producer()
    ])

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_main())