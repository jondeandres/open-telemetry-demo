from concurrent import futures
import grpc


from opentelemetry.proto.collector.trace.v1 import trace_service_pb2_grpc
from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import (
    ExportTraceServiceRequest,
    ExportTraceServiceResponse
)


class OTLPServicer(trace_service_pb2_grpc.TraceServiceServicer):
    def Export(self, request: ExportTraceServiceRequest, context: grpc.ServicerContext) -> ExportTraceServiceResponse:
        print(request)

        return ExportTraceServiceResponse()


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    trace_service_pb2_grpc.add_TraceServiceServicer_to_server(
        OTLPServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print('Listening on 50051')
    server.wait_for_termination()


if __name__ == '__main__':
    main()
