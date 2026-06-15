from django.test import TestCase
from django.contrib.auth import get_user_model
from clubs.models import Club

User = get_user_model()


class ClubViewsTest(TestCase):
    def setUp(self):
        self.club = Club.objects.create(
            name="Test Club",
            description="Test",
            is_approved=True,
            manager=User.objects.create_user(username="manager", password="pass", role="club_manager", email="manager@test.com")
        )
        self.student = User.objects.create_user(username="student", password="pass", role="student", email="student@test.com")
        self.another_student = User.objects.create_user(username="student2", password="pass", role="student", email="student2@test.com")

    def test_club_list(self):
        response = self.client.get('/clubs/')
        self.assertEqual(response.status_code, 200)

    def test_club_detail(self):
        response = self.client.get(f'/clubs/{self.club.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_join_club(self):
        self.client.force_login(self.student)
        response = self.client.post(f'/clubs/{self.club.pk}/join/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.student in self.club.members.all())

    def test_join_club_twice(self):
        self.client.force_login(self.student)
        self.client.post(f'/clubs/{self.club.pk}/join/')
        response = self.client.post(f'/clubs/{self.club.pk}/join/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_leave_club(self):
        self.club.members.add(self.student)
        self.client.force_login(self.student)
        response = self.client.post(f'/clubs/{self.club.pk}/leave/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.student in self.club.members.all())

    def test_leave_club_not_member(self):
        self.client.force_login(self.student)
        response = self.client.post(f'/clubs/{self.club.pk}/leave/', follow=True)
        self.assertEqual(response.status_code, 200)