from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomerReview
from .forms import CustomerReviewForm
from checkout.models import Order
from django.conf import settings

def index(request):
    """A view to return the index page with reviews"""
    if request.user.is_superuser:
        reviews = CustomerReview.objects.all().order_by('-created_date')[:8]
    elif request.user.is_authenticated:
        approved_reviews = CustomerReview.objects.filter(approved=True).order_by('-created_date')
        user_reviews = CustomerReview.objects.filter(user=request.user, approved=False).order_by('-created_date')
        reviews = (approved_reviews | user_reviews).distinct().order_by('-created_date')[:4]
    else:
        reviews = CustomerReview.objects.filter(approved=True).order_by('-created_date')[:4]
    
    context = {
        'reviews': reviews,
        'DISCOUNT_THRESHOLD': settings.DISCOUNT_THRESHOLD,
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
    """
    Delete a review staff can delete any,
    users can only delete their own pending reviews
    """
    review = get_object_or_404(CustomerReview, pk=review_id)
    
    if request.user.is_superuser:
        review.delete()
        messages.success(request, 'Review successfully removed.')
        return redirect(reverse('home'))
    
    if review.user == request.user:
        if not review.approved:
            review.delete()
            messages.success(request, 'Your review has been deleted.')
        else:
            messages.error(request, 'You cannot delete reviews that have been approved. Please contact admin.')
    else:
        messages.error(request, 'Sorry, you can only delete your own reviews.')
        
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
    """A view to show all approved reviews and users own reviews"""
    if request.user.is_superuser:
        reviews = CustomerReview.objects.all().order_by('-created_date')
    elif request.user.is_authenticated:
        approved_reviews = CustomerReview.objects.filter(approved=True).order_by('-created_date')
        user_reviews = CustomerReview.objects.filter(user=request.user, approved=False).order_by('-created_date')
        reviews = (approved_reviews | user_reviews).distinct().order_by('-created_date')
    else:
        reviews = CustomerReview.objects.filter(approved=True).order_by('-created_date')
    
    context = {
        'reviews': reviews,
        'show_all': True
    }
    
    return render(request, 'home/reviews.html', context)



@login_required
def edit_review(request, review_id):
    """Edit a review only for review owner and only if not approved yet"""
    review = get_object_or_404(CustomerReview, pk=review_id)
    
    if review.user != request.user and not request.user.is_superuser:
        messages.error(request, 'Sorry, you can only edit your own reviews.')
        return redirect(reverse('home'))
    
    if review.approved and not request.user.is_superuser:
        messages.error(request, 'Sorry, you cannot edit reviews that have already been approved.')
        return redirect(reverse('home'))
        
    if request.method == 'POST':
        form = CustomerReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review successfully updated.')
            return redirect(reverse('home'))
        else:
            messages.error(request, 'Failed to update review. Please ensure the form is valid.')
    else:
        form = CustomerReviewForm(instance=review)
        
    template = 'home/edit_review.html'
    context = {
        'form': form,
        'review': review,
    }
    
    return render(request, template, context)