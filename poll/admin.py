from django.contrib import admin

from .models import *

def register(model, modelAdmin=None):
    admin.site.register(model, modelAdmin)

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']})
    ]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

    inlines = [ChoiceInline]

class OptionInline(admin.StackedInline):
    model = Option
    extra = 1
    # classes =['collapse']
    fields = (
        'title',
        'avator',
        'abstract',
        'author',
        'description',
        'pub_time',
        'content',
        'count_vote'
    )
    readonly_fields = ('count_vote',)
    class Media:
        js = (
            'http://cdn.bootcss.com/jquery/2.2.4/jquery.min.js',
            '/static/js/inlinecollapsed.js',
        )

# class QuestionnaireInline(admin.TabularInline):
#     model = Questionnaire
#     extra = 1

# class QuestionnaireAdmin(admin.ModelAdmin):
#     inlines = [OptionInline]

class BuildingAdmin(admin.ModelAdmin):
    inlines = [OptionInline]
    readonly_fields = ['option_count']

# admin.site.register(Question, QuestionAdmin)
register(ActivityDetail)
register(Building, BuildingAdmin)
# register(Questionnaire, QuestionnaireAdmin)
# register(Option)

