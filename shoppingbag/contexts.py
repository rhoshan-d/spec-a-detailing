from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product
from django.utils import timezone


def bag_contents(request):
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for item_id, item_data in bag.items():
        if isinstance(item_id, str):
            try:
                item_id = int(item_id)
            except ValueError:
                continue

        try:
            product = get_object_or_404(Product, pk=item_id)

            if isinstance(item_data, int):
                quantity = item_data
                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'total': quantity * product.price,
                })
                total += quantity * product.price
                product_count += quantity
            else:
                for size, quantity in item_data.items():
                    bag_items.append({
                        'item_id': item_id,
                        'quantity': quantity,
                        'product': product,
                        'size': size,
                        'total': quantity * product.price,
                    })
                    total += quantity * product.price
                    product_count += quantity
        except Exception as e:
            continue

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total
    applied_gift_card = None
    gift_card_value = 0

    if 'gift_card_code' in request.session and request.session['gift_card_code']:
        try:
            from products.models import GiftCard
            gift_card = None

            try:
                gift_card = GiftCard.objects.filter(
                    code=request.session['gift_card_code'],
                    is_active=True
                ).first()
            except Exception as e:
                print(f"Error fetching gift card: {e}")
                pass

            if gift_card:
                has_expired = False
                if hasattr(gift_card, 'expiry_date'):
                    has_expired = timezone.now() > gift_card.expiry_date
                    print(f"Gift card expired? {has_expired}")

                if not has_expired and hasattr(gift_card, 'remaining_value') and gift_card.remaining_value > 0:
                    applied_gift_card = gift_card
                    gift_card_value = min(
                        gift_card.remaining_value, grand_total)
                    new_grand_total = grand_total - gift_card_value
                    if new_grand_total > 0:
                        grand_total = new_grand_total

        except Exception as e:
            print(f"Error applying gift card: {e}")
            if 'gift_card_code' in request.session:
                del request.session['gift_card_code']

    if bag_items and grand_total <= 0:
        grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
        'applied_gift_card': applied_gift_card,
        'gift_card_value': gift_card_value,
    }

    return context
