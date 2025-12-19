# core/context_processors.py

def base_context(request):
    """
    Provides general context data for all templates.
    """
    return {
        'site_name': 'Samaj Site',
        'user': request.user,
    }
