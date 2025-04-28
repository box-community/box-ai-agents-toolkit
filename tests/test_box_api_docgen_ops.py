import pytest
from box_sdk_gen import (
    CreateDocgenBatchV2025R0DestinationFolder,
    DocGenDocumentGenerationDataV2025R0,
    FileReferenceV2025R0,
)

from src.box_ai_agents_toolkit.box_api_docgen import (
    box_docgen_create_batch,
    box_docgen_get_job_by_id,
    box_docgen_list_jobs,
    box_docgen_list_jobs_by_batch,
)


class DummyDocgenManager:
    def __init__(self):
        self.calls = []

    def get_docgen_job_by_id_v2025_r0(self, job_id: str):
        self.calls.append(('get_by_id', job_id))
        return f"job:{job_id}"

    def get_docgen_jobs_v2025_r0(self, marker=None, limit=None):
        self.calls.append(('list_jobs', marker, limit))
        return {'marker': marker, 'limit': limit}

    def get_docgen_batch_job_by_id_v2025_r0(self, batch_id: str, marker=None, limit=None):
        self.calls.append(('list_jobs_by_batch', batch_id, marker, limit))
        return {'batch_id': batch_id, 'marker': marker, 'limit': limit}

    def create_docgen_batch_v2025_r0(
        self,
        file,
        input_source: str,
        destination_folder,
        output_type: str,
        document_generation_data: list,
    ):
        self.calls.append(
            (
                'create_batch',
                file,
                input_source,
                destination_folder,
                output_type,
                document_generation_data,
            )
        )
        return {'created': True}


class DummyClient:
    def __init__(self):
        self.docgen = DummyDocgenManager()


@pytest.fixture
def dummy_client():
    return DummyClient()


def test_box_docgen_get_job_by_id(dummy_client):
    result = box_docgen_get_job_by_id(dummy_client, '123')
    assert result == 'job:123'
    assert dummy_client.docgen.calls == [('get_by_id', '123')]


def test_box_docgen_list_jobs(dummy_client):
    result = box_docgen_list_jobs(dummy_client, marker='m', limit=5)
    assert result == {'marker': 'm', 'limit': 5}
    assert dummy_client.docgen.calls == [('list_jobs', 'm', 5)]


def test_box_docgen_list_jobs_default_params(dummy_client):
    result = box_docgen_list_jobs(dummy_client)
    assert result == {'marker': None, 'limit': None}
    assert dummy_client.docgen.calls == [('list_jobs', None, None)]


def test_box_docgen_list_jobs_by_batch(dummy_client):
    result = box_docgen_list_jobs_by_batch(dummy_client, 'batch1', marker='m2', limit=10)
    assert result == {'batch_id': 'batch1', 'marker': 'm2', 'limit': 10}
    assert dummy_client.docgen.calls == [('list_jobs_by_batch', 'batch1', 'm2', 10)]


def test_box_docgen_create_batch(dummy_client):
    data_input = [
        {'generated_file_name': 'file1', 'user_input': {'a': 'b'}},
        {'generated_file_name': 'file2', 'user_input': {'x': 'y'}},
    ]
    result = box_docgen_create_batch(
        dummy_client, 'f1', 'api', 'dest', 'pdf', data_input
    )
    assert result == {'created': True}
    # verify call
    assert len(dummy_client.docgen.calls) == 1
    call = dummy_client.docgen.calls[0]
    assert call[0] == 'create_batch'
    # file reference
    assert isinstance(call[1], FileReferenceV2025R0)
    assert call[1].id == 'f1'
    # input source
    assert call[2] == 'api'
    # destination folder
    assert isinstance(call[3], CreateDocgenBatchV2025R0DestinationFolder)
    assert call[3].id == 'dest'
    # output type
    assert call[4] == 'pdf'
    # document generation data
    assert isinstance(call[5], list)
    assert len(call[5]) == 2
    assert all(isinstance(item, DocGenDocumentGenerationDataV2025R0) for item in call[5])
    assert call[5][0].generated_file_name == 'file1'
    assert call[5][1].generated_file_name == 'file2'