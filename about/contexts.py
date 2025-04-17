def site_info(request):
    """
    Context processor to provide site information to all templates.
    This includes contact information, operating days, and social media links.
    Makes it easier to manage site wide information in one place.
    """
    contact_info = {
        'phone': '+353 89 271 3159',
        'email': 'info@specadetailing.ie',
        'address': '123 Main Street, Kildare, Ireland',
        'operating_days': 'Mon-Sun 8AM-8PM',
        'social_links': {
            'facebook': 'https://facebook.com/specadetailing',
        }
    }
    
    return {
        'contact_info': contact_info,
    }