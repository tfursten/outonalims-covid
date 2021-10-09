from django.contrib import admin
from .models import (
    Subject, Sample, Box, Location,
    Researcher, Event, Project
)
# Register your models here.
admin.site.register([Subject, Sample, Box, Location,
    Researcher, Event, Project])
