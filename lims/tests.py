import datetime
from django.urls import reverse
from django.test import TestCase
from .models import (Event, Pool, PoolBox, PoolBoxPosition)
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


