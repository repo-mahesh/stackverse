from rest_framework import serializers
from .models import Quote, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class QuoteSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Quote
        fields = ['id', 'content', 'author', 'source', 'tags']