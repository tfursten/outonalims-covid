from django.contrib import admin
from .models import (
    Subject, Sample, SampleBox, PoolBox,
    SampleBoxPosition, PoolBoxPosition, Location,
    Researcher, Event, Project, Pool, Label,
    Test, SampleResult, PoolResult, Race
)
# Register your models here.
admin.site.register([Subject, Sample, SampleBox, PoolBox, SampleBoxPosition, PoolBoxPosition, Location,
    Researcher, Event, Project, Pool, Label, Test, SampleResult, PoolResult, Race])
