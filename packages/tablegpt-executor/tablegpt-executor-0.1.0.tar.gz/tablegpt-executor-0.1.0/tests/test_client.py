import pytest
from tablegpt_executor_client.client import SyncClient, AsyncClient
from tablegpt_executor_client.schemas import ExecutionResult
from tablegpt_executor_client.errors import OperatorRuntimeError


@pytest.mark.skip
def test_sync_client_ok(single_operation):
    client = SyncClient(base_url="http://127.0.0.1:8000")
    resp = client.execution(single_operation=single_operation)
    assert isinstance(resp, ExecutionResult)
    assert resp.result["df2"].s3_url.startswith("s3://")


@pytest.mark.skip
@pytest.mark.asyncio
async def test_async_client_ok(single_operation):
    client = AsyncClient(base_url="http://127.0.0.1:8000")
    resp = await client.execution(single_operation=single_operation)
    assert isinstance(resp, ExecutionResult)
    assert resp.result["df2"].s3_url.startswith("s3://")


@pytest.mark.skip
def test_sync_client_error(error_operation):
    client = SyncClient(base_url="http://127.0.0.1:8000")
    with pytest.raises(OperatorRuntimeError):
        client.execution(single_operation=error_operation)


@pytest.mark.skip
@pytest.mark.asyncio
async def test_async_client_error(error_operation):
    client = AsyncClient(base_url="http://127.0.0.1:8000")
    with pytest.raises(OperatorRuntimeError):
        resp = await client.execution(single_operation=error_operation)
