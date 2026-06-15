from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from events.models import Event, EventRegistration, EventComment
from clubs.models import Club

User = get_user_model()


class EventModelTest(TestCase):
    def setUp(self):
        self.club = Club.objects.create(
            name="Test Club",
            description="Test Description",
            is_approved=True,
            manager=User.objects.create_user(username="manager", password="pass", role="club_manager", email="manager@test.com")
        )

    def test_event_creation(self):
        event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            date=timezone.now() + timedelta(days=1),
            max_participants=10,
            club=self.club
        )
        self.assertEqual(event.title, "Test Event")
        self.assertFalse(event.is_full())

    def test_event_is_full(self):
        event = Event.objects.create(
            title="Full Event",
            description="Test",
            date=timezone.now() + timedelta(days=1),
            max_participants=2,
            club=self.club
        )
        user1 = User.objects.create_user(username="user1", password="pass", email="user1@test.com")
        user2 = User.objects.create_user(username="user2", password="pass", email="user2@test.com")
        EventRegistration.objects.create(user=user1, event=event)
        EventRegistration.objects.create(user=user2, event=event)
        self.assertTrue(event.is_full())

    def test_is_user_registered(self):
        event = Event.objects.create(
            title="Event",
            description="Test",
            date=timezone.now() + timedelta(days=1),
            max_participants=10,
            club=self.club
        )
        user = User.objects.create_user(username="user", password="pass", email="user@test.com")
        self.assertFalse(event.is_user_registered(user))
        EventRegistration.objects.create(user=user, event=event)
        self.assertTrue(event.is_user_registered(user))


class EventRegistrationTest(TestCase):
    def setUp(self):
        self.club = Club.objects.create(
            name="Test Club",
            description="Test",
            is_approved=True,
            manager=User.objects.create_user(username="manager", password="pass", role="club_manager", email="manager@test.com")
        )
        self.event = Event.objects.create(
            title="Test Event",
            description="Test",
            date=timezone.now() + timedelta(days=1),
            max_participants=2,
            club=self.club
        )
        self.user = User.objects.create_user(username="student", password="pass", role="student", email="student@test.com")

    def test_registration_creation(self):
        reg = EventRegistration.objects.create(user=self.user, event=self.event)
        self.assertEqual(reg.user.username, "student")

    def test_unique_registration(self):
        EventRegistration.objects.create(user=self.user, event=self.event)
        with self.assertRaises(Exception):
            EventRegistration.objects.create(user=self.user, event=self.event)

    def test_cancel_registration(self):
        reg = EventRegistration.objects.create(user=self.user, event=self.event)
        self.assertEqual(self.event.registrations.count(), 1)
        reg.delete()
        self.assertEqual(self.event.registrations.count(), 0)


class EventCommentTest(TestCase):
    def setUp(self):
        self.club = Club.objects.create(
            name="Test Club",
            description="Test",
            is_approved=True,
            manager=User.objects.create_user(username="manager", password="pass", role="club_manager", email="manager@test.com")
        )
        self.event = Event.objects.create(
            title="Test Event",
            description="Test",
            date=timezone.now() + timedelta(days=1),
            max_participants=10,
            club=self.club
        )
        self.user = User.objects.create_user(username="student", password="pass", role="student", email="student@test.com")

    def test_comment_creation(self):
        comment = EventComment.objects.create(user=self.user, event=self.event, content="Test comment")
        self.assertEqual(comment.content, "Test comment")


class EventViewsTest(TestCase):
    def setUp(self):
        self.club = Club.objects.create(
            name="Test Club",
            description="Test",
            is_approved=True,
            manager=User.objects.create_user(username="manager", password="pass", role="club_manager", email="manager@test.com")
        )
        self.event = Event.objects.create(
            title="Test Event",
            description="Test",
            date=timezone.now() + timedelta(days=1),
            max_participants=2,
            club=self.club
        )
        self.student = User.objects.create_user(username="student", password="pass", role="student", email="student@test.com")
        self.another_student = User.objects.create_user(username="student2", password="pass", role="student", email="student2@test.com")

    def test_event_list(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_register_for_event(self):
        self.client.force_login(self.student)
        response = self.client.post(f'/events/{self.event.pk}/register/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(EventRegistration.objects.filter(user=self.student, event=self.event).exists())

    def test_register_twice(self):
        self.client.force_login(self.student)
        self.client.post(f'/events/{self.event.pk}/register/')
        response = self.client.post(f'/events/{self.event.pk}/register/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_cancel_registration(self):
        EventRegistration.objects.create(user=self.student, event=self.event)
        self.client.force_login(self.student)
        response = self.client.post(f'/events/{self.event.pk}/unregister/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(EventRegistration.objects.filter(user=self.student, event=self.event).exists())

    def test_cancel_registration_not_registered(self):
        self.client.force_login(self.student)
        response = self.client.post(f'/events/{self.event.pk}/unregister/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_cancel_registration_other_user(self):
        EventRegistration.objects.create(user=self.another_student, event=self.event)
        self.client.force_login(self.student)
        response = self.client.post(f'/events/{self.event.pk}/unregister/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_register_full_event(self):
        EventRegistration.objects.create(user=self.student, event=self.event)
        EventRegistration.objects.create(user=self.another_student, event=self.event)
        self.client.force_login(self.student)
        response = self.client.post(f'/events/{self.event.pk}/register/', follow=True)
        self.assertEqual(response.status_code, 200)