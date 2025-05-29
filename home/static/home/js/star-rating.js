document.addEventListener('DOMContentLoaded', function() {
    const stars = document.querySelectorAll('.rating-stars label.star');
    const ratingContainer = document.querySelector('.rating-container');

    function highlightStars(rating) {
        stars.forEach(s => {
            const starValue = s.getAttribute('for').split('-')[1];
            const starIcon = s.querySelector('i');
            if (parseInt(starValue) <= parseInt(rating)) {
                starIcon.classList.remove('far');
                starIcon.classList.add('fas');
                s.style.color = '#ffc107';
            } else {
                starIcon.classList.remove('fas');
                starIcon.classList.add('far');
                s.style.color = '#e4e5e9';
            }
        });
    }

    function resetStarsToChecked() {
        const checkedRatingInput = document.querySelector('.rating-stars input[type="radio"]:checked');
        if (checkedRatingInput) {
            highlightStars(checkedRatingInput.value);
        } else {
            stars.forEach(s => {
                const starIcon = s.querySelector('i');
                starIcon.classList.remove('fas');
                starIcon.classList.add('far');
                s.style.color = '#e4e5e9';
            });
        }
    }

    resetStarsToChecked();

    ratingContainer.addEventListener('mouseover', function(e) {
        if (e.target.closest('label.star')) {
            const ratingValue = e.target.closest('label.star').getAttribute('for').split('-')[1];
            highlightStars(ratingValue);
        }
    });

    ratingContainer.addEventListener('mouseout', function() {
        resetStarsToChecked();
    });

    stars.forEach(star => {
        star.addEventListener('click', function() {
            const ratingValue = this.getAttribute('for').split('-')[1];
            highlightStars(ratingValue);
        });
    });
});