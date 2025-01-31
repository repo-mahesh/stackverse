import os
from django.conf import settings
from datetime import datetime
from celery import shared_task
from django.db.models import Min
from .models import Quote, DeliveredQuote  # Assuming you'll create DeliveredQuote model

@shared_task
def select_daily_quotes():
    """
    Select 3 quotes daily:
    - First from priority authors (if any)
    - Then from remaining quotes
    - Never repeat previously delivered quotes
    - Move through database incrementally
    """
    # Step 1: Read authors from the file
    authors_file = os.path.join(settings.BASE_DIR, 'special_authors.txt')
    try:
        with open(authors_file, 'r') as file:
            authors = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("Authors file not found")
        authors = []

    # Get all previously delivered quote IDs
    delivered_ids = set(DeliveredQuote.objects.values_list('quote_id', flat=True))
    selected_quotes = []

    # Step 2: First try to get quotes from specified authors
    if authors:
        for author in authors:
            if len(selected_quotes) >= 3:
                break

            # Find the next undelivered quote from this author
            next_quote = Quote.objects.filter(
                author__iexact=author
            ).exclude(
                id__in=delivered_ids
            ).order_by('id').first()

            if next_quote:
                selected_quotes.append(next_quote)

    # Step 3: Fill remaining slots with quotes from any author
    if len(selected_quotes) < 3:
        remaining_needed = 3 - len(selected_quotes)
        
        # Exclude already selected and previously delivered quotes
        current_selection_ids = [q.id for q in selected_quotes]
        excluded_ids = delivered_ids.union(current_selection_ids)
        
        remaining_quotes = Quote.objects.exclude(
            id__in=excluded_ids
        ).order_by('id')[:remaining_needed]
        
        selected_quotes.extend(remaining_quotes)

    # Step 4: Save the delivered quotes with today's date
    today = datetime.now().date()
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
