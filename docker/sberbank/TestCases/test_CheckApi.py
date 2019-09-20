import requests
from uuid import UUID


url = 'http://127.0.0.1:8080/add_task'


def is_valid_uuid(uuid_to_test, version=4):
    """
    Check if uuid_to_test is a valid UUID.
    """
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False

    return str(uuid_obj) == uuid_to_test


def test_check_api_create_task():
    response = requests.get(url)
    expected_code = 200
    actual_code = response.status_code
    assert actual_code == expected_code, 'Сервис должен возвращать 200'
    assert is_valid_uuid(response.text, version=4), 'Неправильный формат uuid'
