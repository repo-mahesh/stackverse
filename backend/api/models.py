from django.db import models

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name
    
class Quote(models.Model):
    content = models.TextField()
    author = models.CharField(max_length=100)
    source = models.CharField(max_length=100, blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='quotes', blank=True)

    def __str__(self) -> str:
        return f"{self.content} - {self.author}"
    

# class DeliveredQuote(models.Model):
#     quote = models.ForeignKey('Quote', on_delete=models.CASCADE)
#     delivery_date = models.DateField()
    
#     class Meta:
#         unique_together = ['quote', 'delivery_date']
#         indexes = [
#             models.Index(fields=['delivery_date']),
#             models.Index(fields=['quote'])
#         ]

#     def __str__(self):
#         return f"Quote {self.quote.id} delivered on {self.delivery_date}"

from django.db import models
from django.utils.timezone import now

class DeliveredQuoteManager(models.Manager):
    def get_delivered_ids(self):
        return self.values_list('quote_id', flat=True)

    def get_todays_quotes(self):
        return self.filter(delivery_date=now().date()).select_related('quote')

class DeliveredQuote(models.Model):
    DELIVERY_ORDER_CHOICES = [
        (1, 'First'),
        (2, 'Second'),
        (3, 'Third')
    ]

    quote = models.ForeignKey('Quote', on_delete=models.CASCADE)
    delivery_date = models.DateField(default=now)
    delivery_order = models.SmallIntegerField(
        choices=DELIVERY_ORDER_CHOICES,
        default=1
    )

    objects = DeliveredQuoteManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['quote', 'delivery_date'],
                name='unique_quote_per_day'
            ),
        ]
        ordering = ['-delivery_date', 'delivery_order']

    def __str__(self):
        return f"Quote {self.quote.id} delivered on {self.delivery_date} (#{self.delivery_order})"


