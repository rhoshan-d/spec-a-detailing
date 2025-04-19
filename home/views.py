from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomerReview
from .forms import CustomerReviewForm
from checkout.models import Order

def index(request):
    """A view to return the index page with reviews"""
    if request.user.is_superuser:
        reviews = CustomerReview.objects.all().order_by('-created_date')[:8]
    else:
        reviews = CustomerReview.objects.filter(approved=True).order_by('-created_date')[:4]
    
    context = {
        'reviews': reviews,
    }
    
    return render(request, 'home/index.html', context)


@login_required
def add_review(request):
    """
    Leave a review only for customers
    who have made a purchase / past booking
    """
    user_has_ordered = Order.objects.filter(
        user_profile__user=request.user
    ).exists()
    user_has_ordered = True
    if not user_has_ordered:
        messages.error(
            request, 
            'Sorry, only customers who have made a purchase can leave reviews.'
        )
        return redirect(reverse('home'))
        
    if request.method == 'POST':
        form = CustomerReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            
            messages.success(
                request, 
                'Thank you! Your review has been submitted and is awaiting approval.'
            )
            return redirect(reverse('home'))
        else:
            messages.error(
                request, 
                'Failed to add review. Please ensure the form is valid.'
            )
    else:
        form = CustomerReviewForm()
        
    template = 'home/add_review.html'
    context = {
        'form': form,
    }
    
    return render(request, template, context)


@login_required
def delete_review(request, review_id):
    """Delete a review staff only"""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only staff members can remove reviews.')
        return redirect(reverse('home'))
        
    review = get_object_or_404(CustomerReview, pk=review_id)
    review.delete()
    messages.success(request, 'Review successfully removed.')
    return redirect(reverse('home'))


@login_required
def approve_review(request, review_id):
    """Approve a pending review staff only"""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only staff members can approve reviews.')
        return redirect(reverse('home'))
        
    review = get_object_or_404(CustomerReview, pk=review_id)
    review.approved = True
    review.save()
    messages.success(request, 'Review approved and now visible to all users.')
    return redirect(reverse('home'))


def all_reviews(request):
    """A view to show all approved reviews"""
    if request.user.is_superuser:
        reviews = CustomerReview.objects.all().order_by('-created_date')
    else:
        reviews = CustomerReview.objects.filter(approved=True).order_by('-created_date')
    
    context = {
        'reviews': reviews,
        'show_all': True
    }
    
    return render(request, 'home/reviews.html', context)