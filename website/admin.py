from website.models import Politico, Term, TermAlias, Sentiment, Media
from django.contrib import admin

class PoliticoAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'party', 'constituency', 'twitter_handle']
    list_filter = ['type', 'party']
admin.site.register(Politico, PoliticoAdmin)

class TermAdmin(admin.ModelAdmin):
    list_display = ['title']

admin.site.register(Media)
admin.site.register(Term, TermAdmin)
admin.site.register(TermAlias)
admin.site.register(Sentiment)
