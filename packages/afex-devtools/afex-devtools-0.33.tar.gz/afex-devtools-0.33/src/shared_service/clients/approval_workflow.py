from django.conf import settings
import grpc
from shared_service.gen_protos.approval_workflow_pb2_grpc import ApprovalWorkflowsServiceStub
from shared_service.gen_protos.approval_workflow_pb2 import InitiateApprovalPayload, ProcessApprovalPayload
from shared_service.grpc_handler import gRPCHandler
from any_case import converts_keys


class ApprovalWorkflowClient(gRPCHandler):
    def __init__(self):
        super().__init__()
        url = settings.APPROVAL_WORKFLOW_MS_SERVER_URL
        self.channel = grpc.insecure_channel(url)
        self.service = ApprovalWorkflowsServiceStub(self.channel)

    def initiate_approval(self, data, metadata):
        message = InitiateApprovalPayload(
            type=data.get("type"),
            recordId=data.get("record_id"),
            recordType=data.get("record_type"),
            priceWorth=data.get("price_worth"),
            locationId=data.get("location_id"),
            createdBy=converts_keys(data.get("created_by"), case="camel"),
            allowAutoApproval=data.get("allow_auto_approval", True),

        )
        return self.grpc_call(call=self.service.initiateApproval, message=message, metadata=metadata)

    def process_approval(self, data, metadata):
        message = ProcessApprovalPayload(
            requestId=data.get("request_id"),
            comment=data.get("comment"),
            priceWorth=data.get("price_worth"),
            action=data.get("action"),
            createdBy=converts_keys(data.get("created_by"), case="camel"),
            isRevert=data.get("is_revert", False),
        )
        return self.grpc_call(call=self.service.processApproval, message=message, metadata=metadata)

    
