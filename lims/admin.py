import csv
from datetime import date

from django.contrib import admin
from django.http import HttpResponse

from .management.commands.pool_sample_table import COLUMNS, build_row, iter_pool_samples
from .models import (
    Event,
    Label,
    Location,
    Pool,
    PoolBox,
    PoolBoxPosition,
    PoolResult,
    Project,
    Race,
    Researcher,
    Sample,
    SampleBox,
    SampleBoxPosition,
    SampleResult,
    Subject,
    Test,
)


@admin.register(Pool)
class PoolAdmin(admin.ModelAdmin):
    actions = ["export_selected_pools_csv"]

    @admin.action(description="Export selected pools with samples as CSV")
    def export_selected_pools_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        filename = "pool-samples-{0}.csv".format(date.today().isoformat())
        response["Content-Disposition"] = 'attachment; filename="{0}"'.format(filename)

        writer = csv.DictWriter(response, fieldnames=[key for key, _label in COLUMNS])
        writer.writerow({key: label for key, label in COLUMNS})

        for pool in queryset.order_by("name"):
            seen_sample_ids = set()
            for sample, source_pool in iter_pool_samples(pool, recursive=True):
                if sample.pk in seen_sample_ids:
                    continue
                seen_sample_ids.add(sample.pk)
                writer.writerow(build_row(pool, source_pool, sample))

        return response


admin.site.register(
    [
        Subject,
        Sample,
        SampleBox,
        PoolBox,
        SampleBoxPosition,
        PoolBoxPosition,
        Location,
        Researcher,
        Event,
        Project,
        Label,
        Test,
        SampleResult,
        PoolResult,
        Race,
    ]
)
