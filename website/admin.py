from website.models import MP, Term, TermAlias, Sentiment
from django.contrib import admin

class MPAdmin(admin.ModelAdmin):
    list_display = ['name', 'party', 'constituency', 'twitter_handle']
    list_filter = ['party']
admin.site.register(MP, MPAdmin)

class TermAdmin(admin.ModelAdmin):
    list_display = ['title']
admin.site.register(Term, TermAdmin)
admin.site.register(TermAlias)
admin.site.register(Sentiment)
