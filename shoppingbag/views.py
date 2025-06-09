from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from products.models import Product, GiftCard

# Create your views here.

def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a gift voucher to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
        messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
    else:
        bag[item_id] = quantity
        messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ Adjust the quantity of the specified product to the specified amount """

    product = get_object_or_404(Product, pk=item_id)

    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
            messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """ Remove the item from the shopping bag """

    product = get_object_or_404(Product, pk=item_id)

    try:
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

        request.session['bag'] = bag
        return HttpResponse(status=200)
    
    except Exception as e:

        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
    

def apply_gift_card(request):
    """Apply a gift card to the current order"""
    if request.method == 'POST':
        if 'remove_gift_card' in request.POST:
            if 'gift_card_code' in request.session:
                del request.session['gift_card_code']
            messages.success(request, 'Gift card removed!')
            return redirect(reverse('checkout'))
            
        gift_card_code = request.POST.get('gift_card_code').strip()
        
        try:
            gift_card = GiftCard.objects.get(code=gift_card_code, is_active=True)
            
            if gift_card.is_expired():
                messages.error(request, 'This gift card has expired.')
            elif gift_card.remaining_value <= 0:
                messages.error(request, 'This gift card has a zero balance.')
            else:
                request.session['gift_card_code'] = gift_card_code
                messages.success(request, f'Gift card applied! €{gift_card.remaining_value} will be used for this order.')
                
        except GiftCard.DoesNotExist:
            messages.error(request, 'Invalid gift card code. Please check and try again.')
    
    return redirect(reverse('checkout'))