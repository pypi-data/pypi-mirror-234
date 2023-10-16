import os

from prodvana.client import Client
from prodvana.proto.prodvana.desired_state import manager_pb2


def get_desired_state_details(client: Client) -> manager_pb2.DesiredStateSummary:
    desired_state_id = os.getenv("PVN_DESIRED_STATE_ID")
    assert desired_state_id, "PVN_DESIRED_STATE_ID not set"
    summary_resp = client.desired_state_manager.GetDesiredStateConvergenceSummary(
        manager_pb2.GetDesiredStateConvergenceReq(
            desired_state_id=desired_state_id,
        )
    )
    return summary_resp.summary
