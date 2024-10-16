from django import template

register = template.Library()

MONTHS_TH = [
    "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
    "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
]

@register.filter
def add_class(field, css_class):
    """Add a CSS class to a form field."""
    return field.as_widget(attrs={'class': css_class})

@register.filter
def date_thai(date):
    """Format a date in Thai format."""
    if not date:
        return ""
    # Format: 23 พฤศจิกายน 2024
    return f"{date.day} {MONTHS_TH[date.month - 1]} {date.year}"
