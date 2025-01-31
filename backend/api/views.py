from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuoteSerializer
from .tasks import select_daily_quotes

class DailyQuotesView(APIView):
    """
    Endpoint to fetch daily quotes.
    """
    def get(self, request, *args, **kwargs):
        quotes = select_daily_quotes()
        serializer = QuoteSerializer(quotes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)