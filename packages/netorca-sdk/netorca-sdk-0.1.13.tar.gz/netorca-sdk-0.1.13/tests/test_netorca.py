from unittest.mock import MagicMock, create_autospec

import pytest

from netorca_sdk.auth import AbstractNetorcaAuth
from netorca_sdk.netorca import Netorca
from netorca_sdk.validations import ContextIn, InvalidContextError


@pytest.fixture
def auth_mock():
    """
    Fixture to create a MagicMock of the AbstractNetorcaAuth class.
    """
    auth = MagicMock(spec=AbstractNetorcaAuth)
    auth.fqdn = "https://api.example.com"
    return auth


@pytest.fixture
def endpoint_caller(auth_mock):
    """
    Fixture to create an instance of Netorca with a MagicMock of the AbstractNetorcaAuth class.
    """
    return Netorca(auth_mock)


@pytest.mark.parametrize(
    "status_code, result, error_message", [(200, {"result": "success"}, None), (404, None, "Could not fetch data")]
)
def test_get(status_code, result, error_message, auth_mock, endpoint_caller):
    """
    Test the 'get' operation of the Netorca 'caller' method with various response status codes.
    """
    auth_mock.get.return_value.status_code = status_code
    auth_mock.get.return_value.json.return_value = result if result else {"error": "not found"}

    if error_message:
        with pytest.raises(Exception, match=error_message):
            endpoint_caller.caller("deployed_items", "get", id=1)
    else:
        res = endpoint_caller.caller("deployed_items", "get", id=1)
        auth_mock.get.assert_called_once()
        assert res == result


@pytest.mark.parametrize(
    "status_code, result, error_message", [(201, {"result": "created"}, None), (400, None, "Could not create data")]
)
def test_create(status_code, result, error_message, auth_mock, endpoint_caller):
    """
    Test the 'post' operation of the Netorca 'caller' method with various response status codes.
    """
    auth_mock.post.return_value.status_code = status_code
    auth_mock.post.return_value.json.return_value = result if result else {"error": "bad request"}

    data = {"field": "value"}
    if error_message:
        with pytest.raises(Exception, match=error_message):
            endpoint_caller.caller("deployed_items", "create", data=data)
    else:
        res = endpoint_caller.caller("deployed_items", "create", data=data)
        auth_mock.post.assert_called_once()
        assert res == result


@pytest.mark.parametrize(
    "status_code, result, error_message", [(200, {"result": "updated"}, None), (400, None, "Could not update data")]
)
def test_update(status_code, result, error_message, auth_mock, endpoint_caller):
    """
    Test the 'update' operation of the Netorca 'caller' method with various response status codes.
    """
    auth_mock.patch.return_value.status_code = status_code
    auth_mock.patch.return_value.json.return_value = result if result else {"error": "bad request"}

    data = {"field": "new_value"}
    if error_message:
        with pytest.raises(Exception, match=error_message):
            endpoint_caller.caller("deployed_items", "update", id=1, data=data)
    else:
        res = endpoint_caller.caller("deployed_items", "update", id=1, data=data)
        auth_mock.patch.assert_called_once()
        assert res == result


@pytest.mark.parametrize(
    "status_code, result, error_message", [(204, {"status": "deleted"}, None), (404, None, "Could not delete data")]
)
def test_delete(status_code, result, error_message, auth_mock, endpoint_caller):
    """
    Test the 'delete' operation of the Netorca 'caller' method with various response status codes.
    """
    auth_mock.delete.return_value.status_code = status_code
    auth_mock.delete.return_value.json.return_value = {"error": "not found"} if status_code == 404 else None

    if error_message:
        with pytest.raises(Exception, match=error_message):
            endpoint_caller.caller("deployed_items", "delete", id=1)
    else:
        res = endpoint_caller.caller("deployed_items", "delete", id=1)
        assert res == result


def test_invalid_endpoint_or_operation(auth_mock, endpoint_caller):
    """
    Test function to ensure that an appropriate ValueError is raised when an invalid
    endpoint or operation is specified when calling the 'caller' method of the 'Netorca'
    class instance.
    """
    with pytest.raises(ValueError, match="Invalid endpoint"):
        endpoint_caller.caller("nonexistent_endpoint", "delete", id=1)

    with pytest.raises(ValueError, match="Invalid operation"):
        endpoint_caller.caller("deployed_items", "nonexistent_operation", id=1)


def test_create_url_context_handling(auth_mock, endpoint_caller):
    """
    Test function to ensure that the 'create_url' method of the 'Netorca' class returns the
    correct URL string for various context and ID values.
    """
    endpoint = "deployed_items"
    url_serviceowner = "https://api.example.com/v1/orcabase/serviceowner/deployed_items/"
    url_consumer = "https://api.example.com/v1/orcabase/consumer/deployed_items/"

    assert endpoint_caller.create_url(endpoint, context=ContextIn.SERVICEOWNER.value) == url_serviceowner
    assert endpoint_caller.create_url(endpoint, context=ContextIn.CONSUMER.value) == url_consumer

    # Test with default context value (assuming ContextIn.SERVICEOWNER is the default)
    assert endpoint_caller.create_url(endpoint) == url_serviceowner

    # Test with an invalid context value
    with pytest.raises(InvalidContextError):
        endpoint_caller.create_url(endpoint, context="wrong_context")

    # Test with a wrong context type (e.g., a string instead of a ContextIn)
    with pytest.raises(InvalidContextError):
        endpoint_caller.create_url(endpoint, context="service_owner")


def test_get_service_items(endpoint_caller, auth_mock, netorca):
    """
    Test if `netorca.get_service_items()` works the same as `netorca.caller("service_items", "get")`.
    """
    status_code = 200
    result = {"result": "success"}

    auth_mock.get.return_value.status_code = status_code
    auth_mock.get.return_value.json.return_value = result

    result_caller = endpoint_caller.caller("service_items", "get")
    result_get_service_items = netorca.get_service_items()

    assert result_caller == result_get_service_items


def test_create_deployed_item(endpoint_caller, auth_mock, netorca):
    """
    Test if `netorca.create_deployed_item()` works the same as `netorca.caller("change_instances", "patch")`.
    """
    change_instance_id = "change_instance_id"
    description = {"field": "value"}

    status_code = 200
    result = {"result": "success"}

    auth_mock.patch.return_value.status_code = status_code
    auth_mock.patch.return_value.json.return_value = result

    result_caller = endpoint_caller.caller(
        "change_instances", "patch", id=change_instance_id, data={"deployed_item": description}
    )
    result_create_deployed_item = netorca.create_deployed_item(change_instance_id, description)

    assert result_caller == result_create_deployed_item


def test_get_deployed_item(endpoint_caller, auth_mock, netorca):
    """
    Test if `netorca.get_deployed_item()` works the same as `netorca.caller("deployed_items", "get")`.
    """
    change_instance_id = "change_instance_id"

    status_code = 200
    result = {"result": "success"}

    auth_mock.get.return_value.status_code = status_code
    auth_mock.get.return_value.json.return_value = result

    result_caller = endpoint_caller.caller("deployed_items", "get", id=change_instance_id)
    result_get_deployed_item = netorca.get_deployed_item(change_instance_id)

    assert result_caller == result_get_deployed_item


def test_get_deployed_items(endpoint_caller, auth_mock, netorca):
    """
    Test if `netorca.get_deployed_items()` works the same as `netorca.caller("deployed_items", "get")`.
    """
    status_code = 200
    result = {"result": "success"}

    auth_mock.get.return_value.status_code = status_code
    auth_mock.get.return_value.json.return_value = result

    result_caller = endpoint_caller.caller("deployed_items", "get")
    result_get_deployed_items = netorca.get_deployed_items()

    assert result_caller == result_get_deployed_items


def test_get_service_item(endpoint_caller, auth_mock, netorca):
    """
    Test if `netorca.get_service_item()` works the same as `netorca.caller("service_items", "get")`.
    """
    service_item_id = "service_item_id"

    status_code = 200
    result = {"result": "success"}

    auth_mock.get.return_value.status_code = status_code
    auth_mock.get.return_value.json.return_value = result

    result_caller = endpoint_caller.caller("service_items", "get", id=service_item_id)
    result_get_service_item = netorca.get_service_item(service_item_id)

    assert result_caller == result_get_service_item


def test_get_change_instance(endpoint_caller, auth_mock, netorca):
    """
    Test if `netorca.get_change_instance()` works the same as `netorca.caller("change_instances", "get")`.
    """
    change_instance_id = "change_instance_id"

    status_code = 200
    result = {"result": "success"}

    auth_mock.get.return_value.status_code = status_code
    auth_mock.get.return_value.json.return_value = result

    result_caller = endpoint_caller.caller("change_instances", "get", id=change_instance_id)
    result_get_change_instance = netorca.get_change_instance(change_instance_id)

    assert result_caller == result_get_change_instance


def test_get_change_instances(endpoint_caller, auth_mock, netorca):
    """
    Test if `netorca.get_change_instances()` works the same as `netorca.caller("change_instances", "get")`.
    """
    status_code = 200
    result = {"result": "success"}

    auth_mock.get.return_value.status_code = status_code
    auth_mock.get.return_value.json.return_value = result

    result_caller = endpoint_caller.caller("change_instances", "get")
    result_get_change_instances = netorca.get_change_instances()

    assert result_caller == result_get_change_instances


def test_update_change_instance(endpoint_caller, auth_mock, netorca):
    """
    Test if `netorca.update_change_instance()` works the same as `netorca.caller("change_instances", "update")`.
    """
    change_instance_id = "change_instance_id"
    data = {"field": "new_value"}

    status_code = 200
    result = {"result": "success"}

    auth_mock.patch.return_value.status_code = status_code
    auth_mock.patch.return_value.json.return_value = result

    result_caller = endpoint_caller.caller("change_instances", "update", id=change_instance_id, data=data)
    result_update_change_instance = netorca.update_change_instance(change_instance_id, data)

    assert result_caller == result_update_change_instance


def test_get_service_config(endpoint_caller, auth_mock, netorca):
    """
    Test if `netorca.get_service_config()` works the same as `netorca.caller("service_configs", "get")`.
    """
    service_config_id = "service_config_id"

    status_code = 200
    result = {"result": "success"}

    auth_mock.get.return_value.status_code = status_code
    auth_mock.get.return_value.json.return_value = result

    result_caller = endpoint_caller.caller("service_configs", "get", id=service_config_id)
    result_get_service_config = netorca.get_service_config(service_config_id)

    assert result_caller == result_get_service_config


def test_get_service_configs(endpoint_caller, auth_mock, netorca):
    """
    Test if `netorca.get_service_configs()` works the same as `netorca.caller("service_configs", "get")`.
    """
    status_code = 200
    result = {"result": "success"}

    auth_mock.get.return_value.status_code = status_code
    auth_mock.get.return_value.json.return_value = result

    result_caller = endpoint_caller.caller("service_configs", "get")
    result_get_service_configs = netorca.get_service_configs()

    assert result_caller == result_get_service_configs
