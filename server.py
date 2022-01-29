import asyncio
import grpc
import es_pb2_grpc
import es_pb2


class Servicer(es_pb2_grpc.ESServicer):
    async def SimpleRPC(self, request, context):
        print(context.invocation_metadata())
        return es_pb2.Response(message="Hello, " + request.message)

    async def SimpleSubsribe(self, request, context):
        context.add_done_callback(lambda : print("done"))
        for i in range(10):
            await asyncio.sleep(1)
            print(i)
            yield es_pb2.Response(message="Hello, " + request.message)
            print(i)


async def serve():
    server = grpc.aio.server(options=(("grpc.keepalive_timeout_ms", 100 ),))
    es_pb2_grpc.add_ESServicer_to_server(Servicer(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(serve())
