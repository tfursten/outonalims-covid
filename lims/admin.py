from django.contrib import admin
from .models import (
    Subject, Sample, Box, Location,
    Researcher, Event, Project, Pool, Label,
    Test, TestResult, Race
)
# Register your models here.
admin.site.register([Subject, Sample, Box, Location,
    Researcher, Event, Project, Pool, Label, Test, TestResult, Race])
