from apps.orders.models import Order, RefundRequest
from django.utils import timezone
from .data.tracking_data import DELIVERY_DATA


def get_order_details(order_id: int) -> dict:
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return {"error": f"Order #{order_id} not found."}

    return {
        "order_id": order.id,
        "product_name": order.product_name,
        "amount": str(order.amount),
        "status": order.status,
        "carrier": order.carrier,
        "tracking_number": order.tracking_number,
        "delivery_address": order.delivery,
        "ordered_on": order.created_at.strftime("%d %b %Y"),
        "days_since_order": (timezone.now() - order.created_at).days,
    }


def get_refund_history(user_id: int) -> dict:
    refunds = RefundRequest.objects.filter(user_id=user_id).order_by("-created_at")

    history = []
    for refund in refunds:
        history.append(
            {
                "order.id": refund.order.id,
                "product": refund.order.product_name,
                "reason": refund.reason,
                "status": refund.status,
                "requested_on": refund.created_at.strftime("%d %b %Y"),
            }
        )

    return {
        "total_refund_requests": len(history),
        "history": history,
    }


def check_delivery_status(tracking_number: str, carrier: str) -> dict:
    default_response = {
        "status": "Unknown",
        "last_location": "Tracking infounavailable",
        "last_update": "N/A",
        "estimated_delivery": "Contact carrier directly",
        "delay_reason": "No updates from carrier",
    }
    result = dict(DELIVERY_DATA.get(tracking_number, default_response))
    result["tracking_number"] = tracking_number
    result["carrier"] = carrier

    return result
