import pytest
from decimal import Decimal
from django.contrib.auth.models import User
from apps.orders.models import Product


@pytest.fixture(scope="function")
def test_user(db):
    return User.objects.create_user(
        username="testuser",
        email="testuser@mail.com",
        password="test@123",
    )


@pytest.fixture
def test_product(db):
    return Product.objects.create(
        name="TV",
        price=Decimal("50000.00"),
        category="Electronics",
        in_stock=True,
    )
