from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from people.models import Person, Family
from management.models import CommitteeMember
from django.urls import reverse

User = get_user_model()

class CommitteeIntegrationTests(TestCase):
    def setUp(self):
        # Create Admin User
        self.admin_user = User.objects.create_superuser(
            username='admin', password='password', role='ADMIN'
        )
        self.client = Client()
        self.client.login(username='admin', password='password')
        
        # Create Family and Person
        self.family = Family.objects.create(hometown="Test Village")
        self.person = Person.objects.create(
            full_name="Test Person",
            family=self.family,
            mobile_number="1234567890"
        )
        
    def test_committee_limit(self):
        """Test that committee limit (47) works"""
        # Create 47 members
        for i in range(47):
            CommitteeMember.objects.create(
                name=f"Member {i}",
                designation="KAROBARI_SABHY", # Assuming this allows many
                village="Village",
                display_order=i
            )
            
        self.assertTrue(CommitteeMember.is_committee_full())
        self.assertEqual(CommitteeMember.get_available_slots(), 0)
        
        # Try to access add_to_committee view
        response = self.client.get(reverse('add_to_committee', args=[self.person.pk]))
        # Should redirect with error
        self.assertEqual(response.status_code, 302)
        
        # Verify message (optional, but good)
        # messages = list(response.context['messages'])  # Messages are in the next request usually if redirect
        
    def test_add_to_committee_flow(self):
        """Test adding a person to committee"""
        response = self.client.post(reverse('add_to_committee', args=[self.person.pk]), {
            'designation': 'PRAMUKH',
            'display_order': 1
        })
        
        self.assertRedirects(response, reverse('people_directory'))
        
        # Check link
        self.assertTrue(CommitteeMember.objects.filter(person=self.person).exists())
        member = CommitteeMember.objects.get(person=self.person)
        self.assertEqual(member.name, "Test Person")
        self.assertEqual(member.designation, "PRAMUKH")

    def test_already_in_committee(self):
        """Test adding someone who is already in committee"""
        CommitteeMember.objects.create(
            person=self.person,
            name="Test Person",
            designation="PRAMUKH",
            village="Village"
        )
        
        response = self.client.get(reverse('add_to_committee', args=[self.person.pk]))
        self.assertRedirects(response, reverse('people_directory'))
