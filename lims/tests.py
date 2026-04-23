import datetime
import csv
import io

from django.contrib.admin.sites import AdminSite
from django.urls import reverse
from django.test import RequestFactory
from django.test import TestCase
from .admin import PoolAdmin
from .models import Event, Location, Pool, PoolBox, PoolBoxPosition, Project, Sample, Subject
# Create your tests here.


class EventModelTests(TestCase):

    def test_event_is_not_complete_with_future_date(self):
        """
        Event.is_complete returns false when collection date is in future
        """
        date = datetime.date.today() + datetime.timedelta(days=30)
        future_event = Event(name="Test_event", date=date)
        self.assertIs(future_event.is_complete, False)

    def test_event_is_not_complete_with_current_date(self):
        """
        Event.is_complete returns false when collection date is today
        """
        date = datetime.date.today()
        today_event = Event(name="Test_event", date=date)
        self.assertIs(today_event.is_complete, False)

    def test_event_is_complete_with_past_date(self):
        """
        Event.is_complete returns false when collection date is in future
        """
        date = datetime.date.today() - datetime.timedelta(days=1)
        past_event = Event(name="Test_event", date=date)
        self.assertIs(past_event.is_complete, True)


class PoolModelTests(TestCase):
    
    def test_pool_with_box_position_returns_box(self):
        """
        Pool.box should return correct box if box position is set.
        """
        pool = Pool(name='TestPool')
        pool.save()
        box = PoolBox(box_name="Testbox")
        box.save()
        box_position = PoolBoxPosition(position=1, pool=pool)
        box_position.save()
        box = PoolBox.objects.get(box_name="Testbox")
        box.positions.add(PoolBoxPosition.objects.get(position=1))
        self.assertIs(pool.box_position.id, box_position.id)
        self.assertIs(pool.box.id, box.id)

    def test_pool_with_no_box_returns_none(self):
        """
        Pool.box should return correct box if box position is set.
        """
        pool = Pool(name='TestPool')
        self.assertIs(pool.box_position, None)
        self.assertIs(pool.box, None)


class PoolAdminTests(TestCase):

    def test_export_selected_pools_csv_returns_pool_sample_rows(self):
        project = Project.objects.create(name="Project 1")
        location = Location.objects.create(
            name="Location 1",
            project=project,
        )
        event = Event.objects.create(
            name="Event 1",
            date=datetime.date.today(),
            week=1,
        )
        subject = Subject.objects.create(
            first_name="Test",
            last_name="Subject",
            location=location,
        )
        sample = Sample.objects.create(
            name="S00001",
            subject=subject,
            location=location,
            collection_event=event,
            collection_status="Collected",
        )
        pool = Pool.objects.create(name="Pool 1")
        pool.samples.add(sample)

        request = RequestFactory().get("/admin/lims/pool/")
        model_admin = PoolAdmin(Pool, AdminSite())

        response = model_admin.export_selected_pools_csv(
            request,
            Pool.objects.filter(pk=pool.pk),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertIn("attachment; filename=", response["Content-Disposition"])

        rows = list(csv.DictReader(io.StringIO(response.content.decode("utf-8"))))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["Pool"], "Pool 1")
        self.assertEqual(rows[0]["Source Pool"], "Pool 1")
        self.assertEqual(rows[0]["Sample ID"], "S00001")
        self.assertEqual(rows[0]["Location"], "Location 1")

