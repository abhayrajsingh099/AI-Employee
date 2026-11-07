from decimal import Decimal

from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from apps.orders.models import Order

def test_order_list_requires_login(client):
    response = client.get(reverse("orders_list"))

    assert response.status_code == 302

def test_orders_list_shows_only_logged_in_users_orders(
    client, test_user, test_product, db
):
    # Arrange
    another_user = User.objects.create_user(
        username="another_user",
        password="test123",
    )

    order1 = Order.objects.create(
        user=test_user,
        product=test_product,
        product_name="TV",
        amount=Decimal("50000.00"),
        created_at=timezone.now(),
    )

    order2 = Order.objects.create(
        user=another_user,
        product=test_product,
        product_name="Laptop",
        amount=Decimal("70000.00"),
        created_at=timezone.now(),
    )

    # Act
    client.force_login(test_user)
    response = client.get(reverse("orders_list"))

    # Assert
    assert response.status_code == 200
    assert order1 in response.context["orders"]
    assert order2 not in response.context["orders"]

def test_order_detail_requires_auth(client):
    response = client.get(reverse("order_detail", kwargs={'order_id':1}))

    assert response.status_code == 302

def test_user_cannot_access_another_users_order_detail(
    client, test_user, test_product, db
):
    # Arrange
    another_user = User.objects.create_user(
        username="another_user",
        password="test123",
    )

    order1 = Order.objects.create(
        user=another_user,
        product=test_product,
        product_name="Laptop",
        amount=Decimal("70000.00"),
        created_at=timezone.now(),
    )

    # Act
    client.force_login(test_user)
    response = client.get(reverse("order_detail", kwargs={'order_id':order1.id}))

    # Assert
    assert response.status_code == 404

def test_order_detail_returns_404_for_nonexistent_order(client, test_user):
    
    client.force_login(test_user)
    response = client.get(reverse("order_detail", kwargs={'order_id':9999}))

    assert response.status_code == 404