from django.contrib import admin
from .models import Quote, Tag


    
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'source')
    list_filter = ('tags',)
    search_fields = ('content', 'author', 'source')
    autocomplete_fields=['tags']

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Quote, QuoteAdmin)
admin.site.register(Tag, TagAdmin)