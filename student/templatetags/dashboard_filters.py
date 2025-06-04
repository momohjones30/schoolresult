from django import template

register = template.Library()

@register.filter
def avg_score(results):
    if not results:
        return "N/A"
    total = sum(r.total for r in results)
    return f"{total / len(results):.1f}%"

@register.filter
def best_subject(results):
    if not results:
        return "N/A"
    best = max(results, key=lambda r: r.total)
    return f"{best.subject.NameOfSubject} ({best.total}%)"

@register.filter
def needs_improvement(results):
    if not results:
        return "N/A"
    worst = min(results, key=lambda r: r.total)
    return f"{worst.subject.NameOfSubject} ({worst.total}%)"