import pytest
from box_sdk_gen import FileReferenceV2025R0

from src.box_ai_agents_toolkit.box_api_docgen_template import (
    box_docgen_template_create,
    box_docgen_template_delete,
    box_docgen_template_get_by_id,
    box_docgen_template_list,
    box_docgen_template_list_jobs,
    box_docgen_template_list_tags,
)


class DummyDocgenTemplateManager:
    def __init__(self):
        self.calls = []

    def create_docgen_template_v2025_r0(self, file):
        self.calls.append(('create', file))
        return {'template': file.id}

    def get_docgen_templates_v2025_r0(self, marker=None, limit=None):
        self.calls.append(('list', marker, limit))
        return {'marker': marker, 'limit': limit}

    def delete_docgen_template_by_id_v2025_r0(self, template_id):
        self.calls.append(('delete', template_id))
        return None

    def get_docgen_template_by_id_v2025_r0(self, template_id):
        self.calls.append(('get', template_id))
        return {'id': template_id}

    def get_docgen_template_tags_v2025_r0(
        self, template_id, template_version_id=None, marker=None, limit=None
    ):
        self.calls.append(('tags', template_id, template_version_id, marker, limit))
        return {'template_id': template_id, 'version': template_version_id}

    def get_docgen_template_job_by_id_v2025_r0(self, template_id, marker=None, limit=None):
        self.calls.append(('jobs', template_id, marker, limit))
        return {'template_id': template_id, 'marker': marker, 'limit': limit}


class DummyClient:
    def __init__(self):
        self.docgen_template = DummyDocgenTemplateManager()


@pytest.fixture
def dummy_client():
    return DummyClient()


def test_box_docgen_template_create(dummy_client):
    result = box_docgen_template_create(dummy_client, 'tmpl1')
    assert result == {'template': 'tmpl1'}
    assert len(dummy_client.docgen_template.calls) == 1
    call = dummy_client.docgen_template.calls[0]
    assert call[0] == 'create'
    # verify file reference
    assert isinstance(call[1], FileReferenceV2025R0)
    assert call[1].id == 'tmpl1'


def test_box_docgen_template_list(dummy_client):
    result = box_docgen_template_list(dummy_client, marker='x', limit=2)
    assert result == {'marker': 'x', 'limit': 2}
    assert dummy_client.docgen_template.calls == [('list', 'x', 2)]


def test_box_docgen_template_list_default_params(dummy_client):
    result = box_docgen_template_list(dummy_client)
    assert result == {'marker': None, 'limit': None}
    assert dummy_client.docgen_template.calls == [('list', None, None)]


def test_box_docgen_template_delete(dummy_client):
    result = box_docgen_template_delete(dummy_client, 'tmpl2')
    assert result is None
    assert dummy_client.docgen_template.calls == [('delete', 'tmpl2')]


def test_box_docgen_template_get_by_id(dummy_client):
    result = box_docgen_template_get_by_id(dummy_client, 'tmpl3')
    assert result == {'id': 'tmpl3'}
    assert dummy_client.docgen_template.calls == [('get', 'tmpl3')]


def test_box_docgen_template_list_tags(dummy_client):
    result = box_docgen_template_list_tags(
        dummy_client, 'tmpl4', template_version_id='v1', marker='m', limit=5
    )
    assert result == {'template_id': 'tmpl4', 'version': 'v1'}
    assert dummy_client.docgen_template.calls == [
        ('tags', 'tmpl4', 'v1', 'm', 5)
    ]


def test_box_docgen_template_list_jobs(dummy_client):
    result = box_docgen_template_list_jobs(
        dummy_client, 'tmpl5', marker='m2', limit=3
    )
    assert result == {'template_id': 'tmpl5', 'marker': 'm2', 'limit': 3}
    assert dummy_client.docgen_template.calls == [
        ('jobs', 'tmpl5', 'm2', 3)
    ]