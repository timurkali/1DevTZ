import json
import uuid

import pytest
from django.contrib.auth import get_user_model

from . import helpers
from basic import models

User = get_user_model()


@pytest.fixture
def test_password():
    return 'ass123zzz'


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def api_client_with_credentials(db, create_user, api_client):
    user = create_user()
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)


@pytest.mark.django_db
@pytest.mark.parametrize('case, order_id', [
    ('pending_order', 1),
    ('new_order', 2),
])
def test_create_order(api_client_with_credentials, case, order_id):
    expected = helpers.get_fixture(f'client/create_order/{case}/expected.json')
    resp = api_client_with_credentials.post('/api/order/')

    expected['id'] = order_id

    assert resp.status_code == 201
    assert resp.data == expected


@pytest.mark.django_db
def test_get_product(api_client_with_credentials):
    expected = helpers.get_fixture('client/get_product/expected.json')
    category_data = helpers.get_fixture('category_create.json')
    product_data = helpers.get_fixture('product_create.json')
    models.Category(**category_data).save()
    models.Product(**product_data).save()

    resp = api_client_with_credentials.get('/api/product/')
    resp_data = json.loads(json.dumps(resp.data))

    assert resp.status_code == 200
    assert resp_data == expected
