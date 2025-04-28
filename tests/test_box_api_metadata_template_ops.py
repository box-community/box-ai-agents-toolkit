import pytest
from box_sdk_gen.managers.metadata_templates import (
    DeleteMetadataTemplateScope,
    GetMetadataTemplateScope,
    UpdateMetadataTemplateScope,
)

from src.box_ai_agents_toolkit.box_api_metadata_template import (
    box_metadata_template_create,
    box_metadata_template_delete,
    box_metadata_template_get,
    box_metadata_template_get_by_id,
    box_metadata_template_list,
    box_metadata_template_list_by_instance_id,
    box_metadata_template_update,
)


class DummyMetadataTemplatesManager:
    def __init__(self):
        self.calls = []

    def create_metadata_template(
        self,
        scope,
        display_name,
        *,
        template_key=None,
        hidden=None,
        fields=None,
        copy_instance_on_item_copy=None,
    ):
        self.calls.append(
            (
                'create',
                scope,
                display_name,
                template_key,
                hidden,
                fields,
                copy_instance_on_item_copy,
            )
        )
        return {'scope': scope, 'display_name': display_name}

    def get_enterprise_metadata_templates(self, marker=None, limit=None):
        self.calls.append(('list_enterprise', marker, limit))
        return {'marker': marker, 'limit': limit}

    def get_global_metadata_templates(self, marker=None, limit=None):
        self.calls.append(('list_global', marker, limit))
        return {'marker': marker, 'limit': limit}

    def get_metadata_template(self, scope, template_key):
        self.calls.append(('get', scope, template_key))
        return {'scope': scope, 'template_key': template_key}

    def get_metadata_template_by_id(self, template_id):
        self.calls.append(('get_by_id', template_id))
        return {'template_id': template_id}

    def update_metadata_template(self, scope, template_key, request_body):
        self.calls.append(('update', scope, template_key, request_body))
        return {'scope': scope, 'template_key': template_key, 'request_body': request_body}

    def delete_metadata_template(self, scope, template_key):
        self.calls.append(('delete', scope, template_key))
        return None

    def get_metadata_templates_by_instance_id(self, metadata_instance_id, marker=None, limit=None):
        self.calls.append(('list_by_instance', metadata_instance_id, marker, limit))
        return {'metadata_instance_id': metadata_instance_id, 'marker': marker, 'limit': limit}


class DummyClient:
    def __init__(self):
        self.metadata_templates = DummyMetadataTemplatesManager()


@pytest.fixture
def dummy_client():
    return DummyClient()


def test_box_metadata_template_create(dummy_client):
    result = box_metadata_template_create(
        dummy_client,
        'enterprise',
        'My Template',
        template_key='tmpl1',
        hidden=True,
        fields=[{'key': 'a'}],
        copy_instance_on_item_copy=False,
    )
    assert result == {'scope': 'enterprise', 'display_name': 'My Template'}
    assert dummy_client.metadata_templates.calls == [
        (
            'create',
            'enterprise',
            'My Template',
            'tmpl1',
            True,
            [{'key': 'a'}],
            False,
        )
    ]


def test_box_metadata_template_list_enterprise(dummy_client):
    result = box_metadata_template_list(dummy_client, 'enterprise', marker='m', limit=2)
    assert result == {'marker': 'm', 'limit': 2}
    assert dummy_client.metadata_templates.calls == [('list_enterprise', 'm', 2)]


def test_box_metadata_template_list_global(dummy_client):
    result = box_metadata_template_list(dummy_client, 'global', marker='x', limit=1)
    assert result == {'marker': 'x', 'limit': 1}
    assert dummy_client.metadata_templates.calls == [('list_global', 'x', 1)]


def test_box_metadata_template_list_invalid_scope(dummy_client):
    with pytest.raises(ValueError):
        box_metadata_template_list(dummy_client, 'invalid')


def test_box_metadata_template_get(dummy_client):
    scope = GetMetadataTemplateScope.ENTERPRISE
    result = box_metadata_template_get(dummy_client, scope, 'tmpl5')
    assert result == {'scope': scope, 'template_key': 'tmpl5'}
    assert dummy_client.metadata_templates.calls == [('get', scope, 'tmpl5')]


def test_box_metadata_template_get_by_id(dummy_client):
    result = box_metadata_template_get_by_id(dummy_client, 'id123')
    assert result == {'template_id': 'id123'}
    assert dummy_client.metadata_templates.calls == [('get_by_id', 'id123')]


def test_box_metadata_template_update(dummy_client):
    body = [{'op': 'replace', 'path': '/displayName', 'value': 'New'}]
    scope = UpdateMetadataTemplateScope.GLOBAL
    result = box_metadata_template_update(dummy_client, scope, 'tmpl6', body)
    assert result == {'scope': scope, 'template_key': 'tmpl6', 'request_body': body}
    assert dummy_client.metadata_templates.calls == [('update', scope, 'tmpl6', body)]


def test_box_metadata_template_delete(dummy_client):
    scope = DeleteMetadataTemplateScope.ENTERPRISE
    result = box_metadata_template_delete(dummy_client, scope, 'tmpl7')
    assert result is None
    assert dummy_client.metadata_templates.calls == [('delete', scope, 'tmpl7')]


def test_box_metadata_template_list_by_instance_id(dummy_client):
    result = box_metadata_template_list_by_instance_id(dummy_client, 'inst1', marker='a', limit=3)
    assert result == {'metadata_instance_id': 'inst1', 'marker': 'a', 'limit': 3}
    assert dummy_client.metadata_templates.calls == [('list_by_instance', 'inst1', 'a', 3)]