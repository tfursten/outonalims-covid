import csv

from django.core.management.base import BaseCommand

from lims.models import Pool


COLUMNS = [
    ("pool_name", "Pool"),
    ("source_pool_name", "Source Pool"),
    ("sample_name", "Sample ID"),
    ("subject_id", "Subject ID"),
    ("subject_age", "Subject Age"),
    ("sex", "Sex"),
    ("location_name", "Location"),
    ("event_date", "Event Date"),
]


class Command(BaseCommand):
    help = (
        "List each pool's samples with subject ID, age, sex, location, "
        "and sample collection event date."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--pool",
            dest="pool_name",
            help="Limit the table to one pool name.",
        )
        parser.add_argument(
            "--direct-only",
            action="store_true",
            help="Only include samples directly assigned to each pool.",
        )
        parser.add_argument(
            "--output",
            "-o",
            help="Write the table to a CSV file instead of printing it.",
        )

    def handle(self, *args, **options):
        pools = Pool.objects.order_by("name")
        if options["pool_name"]:
            pools = pools.filter(name=options["pool_name"])

        rows = []
        recursive = not options["direct_only"]
        for pool in pools:
            seen_sample_ids = set()
            for sample, source_pool in iter_pool_samples(pool, recursive=recursive):
                if sample.pk in seen_sample_ids:
                    continue
                seen_sample_ids.add(sample.pk)
                rows.append(build_row(pool, source_pool, sample))

        if options["output"]:
            write_csv(options["output"], rows)
            self.stdout.write(
                self.style.SUCCESS(
                    "Wrote {0} rows to {1}".format(len(rows), options["output"])
                )
            )
            return

        self.stdout.write(format_table(rows))


def iter_pool_samples(pool, recursive=True, visited_pool_ids=None):
    if visited_pool_ids is None:
        visited_pool_ids = set()

    if pool.pk in visited_pool_ids:
        return

    visited_pool_ids.add(pool.pk)

    samples = pool.samples.select_related(
        "subject",
        "location",
        "collection_event",
    ).order_by("name")
    for sample in samples:
        yield sample, pool

    if not recursive:
        return

    for child_pool in pool.pools.order_by("name"):
        yield from iter_pool_samples(
            child_pool,
            recursive=recursive,
            visited_pool_ids=visited_pool_ids,
        )


def build_row(pool, source_pool, sample):
    subject = sample.subject
    return {
        "pool_name": pool.name,
        "source_pool_name": source_pool.name,
        "sample_name": sample.name,
        "subject_id": subject.subject_ui,
        "subject_age": subject.age,
        "sex": subject.sex,
        "location_name": sample.location.name if sample.location else "",
        "event_date": sample.collection_event.date.isoformat()
        if sample.collection_event.date
        else "",
    }


def write_csv(path, rows):
    fieldnames = [key for key, _label in COLUMNS]
    with open(path, "w", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writerow({key: label for key, label in COLUMNS})
        writer.writerows(rows)


def format_table(rows):
    if not rows:
        return "No pool samples found."

    widths = {}
    for key, label in COLUMNS:
        values = [label] + [format_value(row[key]) for row in rows]
        widths[key] = max(len(value) for value in values)

    header = "  ".join(
        label.ljust(widths[key])
        for key, label in COLUMNS
    )
    divider = "  ".join("-" * widths[key] for key, _label in COLUMNS)
    body = [
        "  ".join(
            format_value(row[key]).ljust(widths[key])
            for key, _label in COLUMNS
        )
        for row in rows
    ]
    return "\n".join([header, divider] + body)


def format_value(value):
    return "" if value is None else str(value)
