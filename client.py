import asyncio
import uuid
import grpc
import es_pb2
import es_pb2_grpc


async def main():
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = es_pb2_grpc.ESStub(channel)
        response = await stub.SimpleRPC(
            es_pb2.Request(message="Hello, world!"),
            metadata=(("id", str(uuid.uuid4())),),
        )
        print(response)
        async for response in stub.SimpleSubsribe(
            es_pb2.Request(message="Hello, world!")
        ):
            print(response)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
