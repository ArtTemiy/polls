from django.contrib import admin
from polling.models import *
from django.forms import ModelForm


admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Result)
