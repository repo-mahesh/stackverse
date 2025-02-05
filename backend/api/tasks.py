import os
from django.conf import settings
from datetime import datetime, timedelta
from celery import shared_task
from django.db.models import Min
from .models import Quote, DeliveredQuote 

@shared_task
def select_daily_quotes():
    """
    Select 3 quotes daily:
    - First from priority authors (if any)
    - Then from remaining quotes
    - Never repeat previously delivered quotes
    - Move through database incrementally
    """

    today = datetime.now().date() + timedelta(days=2)
    print(today)

    todays_quotes = (
        DeliveredQuote.objects.filter(delivery_date=today)
        .select_related("quote")
        .order_by("delivery_order")
    )

    if todays_quotes.count() == 3:
        print(delivered.quote for delivered in todays_quotes)
        return [delivered.quote for delivered in todays_quotes]

    delivered_ids = set(DeliveredQuote.objects.values_list('quote_id', flat=True))
    selected_quotes = []

    authors_file = os.path.join(settings.BASE_DIR, 'special_authors.txt')
    try:
        with open(authors_file, 'r') as file:
            authors = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("Authors file not found")
        authors = []

    if authors:
        for author in authors:
            if len(selected_quotes) >= 3:
                break

            next_quote = Quote.objects.filter(
                author__iexact=author
            ).exclude(
                id__in=delivered_ids
            ).order_by('id').first()

            if next_quote:
                selected_quotes.append(next_quote)

    if len(selected_quotes) < 3:
        remaining_needed = 3 - len(selected_quotes)

        current_selection_ids = [q.id for q in selected_quotes]
        excluded_ids = delivered_ids.union(current_selection_ids)

        remaining_quotes = Quote.objects.exclude(
            id__in=excluded_ids
        ).order_by('id')[:remaining_needed]

        selected_quotes.extend(remaining_quotes)

    for idx, quote in enumerate(selected_quotes):
        try:
            DeliveredQuote.objects.create(
                quote=quote,
                delivery_date=today,
                delivery_order=idx  
            )
        except Exception as e:
            print(f"Error delivering quote {quote.id}: {str(e)}")
            continue

    return selected_quotes
