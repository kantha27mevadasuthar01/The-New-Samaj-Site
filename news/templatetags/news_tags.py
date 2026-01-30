from django import template
from news.models import NewsAnnouncement

register = template.Library()

@register.inclusion_tag('news/ticker.html')
def news_ticker():
    # Fetch active announcements
    announcements = NewsAnnouncement.objects.filter(is_active=True).order_by('-created_at')
    
    # Determine speed (take the slowest one or average, or just use the first active one's speed)
    # For simplicity, if multiple exist, we might want to concatenate clear them.
    # But usually a ticker has one speed. Let's use the speed of the latest active item, or default 20.
    speed = 20
    if announcements.exists():
        speed = announcements.first().scroll_speed
        
    return {
        'announcements': announcements,
        'speed': speed
    }
