import pytest
from decimal import Decimal
from django.utils import timezone
from apps.orders.models import Order
from django.core.exceptions import ValidationError


def test_order_creation_and_relationships(db, test_user, test_product):
    # ACT
    order = Order.objects.create(
        user=test_user,
        product=test_product,
        product_name="TV",
        amount=Decimal("50000.00"),
        carrier="BlueKart",
        tracking_number="TRK12345",
        created_at=timezone.now(),
    )

    saved_order = Order.objects.get(id=order.id)

    # Assert
    assert saved_order.product_name == "TV"
    assert saved_order.amount == Decimal("50000.00")
    assert saved_order.user == test_user
    assert saved_order.product == test_product


def test_order_has_correct_amount(db, test_user, test_product):
    # ACT
    order = Order.objects.create(
        user=test_user,
        product=test_product,
        product_name="TV",
        amount=Decimal("50000.00"),
        carrier="BlueKart",
        tracking_number="TRK12345",
        created_at=timezone.now(),
    )

    saved_order = Order.objects.get(id=order.id)

    # Assert
    assert saved_order.amount == Decimal("50000.00")


@pytest.mark.parametrize("status", ["pending", "dispatched", "delivered", "cancelled"])
def test_order_accepts_status(test_user, test_product, status):
    order = Order(
        user=test_user,
        product=test_product,
        product_name="TV",
        amount=Decimal("50000.00"),
        status=status,
        created_at=timezone.now(),
    )

    order.full_clean()

    assert order.status == status


def test_order_does_not_exist(db):
    with pytest.raises(Order.DoesNotExist):
        Order.objects.get(id=99999)


def test_order_default_status_pending(db, test_user, test_product):
    order = Order.objects.create(
        user=test_user,
        product=test_product,
        product_name="TV",
        amount=Decimal("50000.00"),
        created_at=timezone.now(),
    )

    assert order.status == "pending"


def test_order_product_relationship_null(db, test_user):
    order = Order.objects.create(
        user=test_user,
        product_name="TV",
        amount=Decimal("50000.00"),
        created_at=timezone.now(),
    )

    saved_order = Order.objects.get(id=order.id)

    assert saved_order.product is None


def test_order_string_representation(db, test_user):
    order = Order.objects.create(
        user=test_user,
        product_name="TV",
        amount=Decimal("50000.00"),
        created_at=timezone.now(),
    )

    saved_order = Order.objects.get(id=order.id)

    assert (
        str(saved_order) == f"Order #{order.id} - {order.product_name} ({order.status})"
    )


def test_order_rejects_invalid_status(test_user):
    order = Order(
        user=test_user,
        product_name="TV",
        amount=Decimal("50000.00"),
        status="flying",
        created_at=timezone.now(),
    )

    with pytest.raises(ValidationError):
        order.full_clean()
