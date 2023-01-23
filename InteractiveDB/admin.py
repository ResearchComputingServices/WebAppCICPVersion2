from django.contrib import admin
from InteractiveDB.models import SurveyTable, QuestionTable, ChoiceTable, UserTable, UserResponseTable
# Register your models here.

admin.site.register(SurveyTable)
admin.site.register(QuestionTable)
admin.site.register(ChoiceTable)
admin.site.register(UserTable)
admin.site.register(UserResponseTable)