from django.test import TestCase
from django.utils import timezone
from unittest.mock import patch, mock_open
from datetime import date, timedelta
from .models import Quote, Tag, DeliveredQuote
from .tasks import select_daily_quotes
from django.db import connection

class QuoteDeliveryTests(TestCase):
    def setUp(self):
        # Create test quotes
        self.quotes = []
        for i in range(0, 6):
            quote = Quote.objects.create(
                content=f"Quote {i}",
                author=f"Author {i}",
                source=f"Source {i}"
            )
            self.quotes.append(quote)

    def test_initial_quote_selection(self):
        """Test first-time quote selection with no previous deliveries"""
        selected = select_daily_quotes()
        
        self.assertEqual(len(selected), 3, "Should select exactly 3 quotes")
        
        delivered = DeliveredQuote.objects.all()
        for idx, quote in enumerate(selected):
            assert delivered[idx].quote == quote
        
        self.assertEqual(delivered.count(), 3, "Should have 3 delivered quotes")

    def test_no_duplicate_deliveries(self):
        """Test that quotes aren't delivered twice"""
        first_delivery = select_daily_quotes()
        
        second_delivery = select_daily_quotes()
        
        intersection = set(first_delivery) & set(second_delivery)
        self.assertEqual(len(intersection), 0, f"Found duplicate quotes: {intersection}")

class DeliveredQuoteModelTests(TestCase):
    def setUp(self):
        self.quote = Quote.objects.create(
            content="Test Quote",
            author="Test Author",
            source="Test Source"
        )

    def test_manager_methods(self):
        """Test custom manager methods"""
        today = timezone.now().date()
        delivered = DeliveredQuote.objects.create(
            quote=self.quote,
            delivery_date=today,
            delivery_order=1
        )
        
        delivered_ids = DeliveredQuote.objects.get_delivered_ids()
        
        self.assertEqual(
            list(delivered_ids), 
            [self.quote.id], 
            f"Expected [{self.quote.id}], got {list(delivered_ids)}"
        )
        
        todays_quotes = DeliveredQuote.objects.get_todays_quotes()
        self.assertEqual(
            todays_quotes.count(), 
            1, 
            f"Expected 1 quote, got {todays_quotes.count()}"
        )

    def test_unique_constraints(self):
        """Test that unique constraints are enforced"""
        today = timezone.now().date()
        
        delivered1 = DeliveredQuote.objects.create(
            quote=self.quote,
            delivery_date=today,
            delivery_order=1
        )
        
        with self.assertRaises(Exception) as context:
            delivered2 = DeliveredQuote.objects.create(
                quote=self.quote,
                delivery_date=today,
                delivery_order=1
            )
