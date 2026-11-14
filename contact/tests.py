from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import ContactInfo


class ContactPageTests(TestCase):
    def test_empty_contact_page_and_home_only_hero(self):
        response = self.client.get(reverse('contact'))
        self.assertContains(response, 'Contact details will be available soon.')
        self.assertNotContains(response, 'class="banner"')
        self.assertNotContains(self.client.get(reverse('gallery')), 'class="banner"')
        self.assertContains(self.client.get(reverse('home')), 'class="banner"')

    def test_public_details_are_rendered_and_escaped(self):
        ContactInfo.objects.create(email='artist@example.com', introduction='<script>alert(1)</script>', website_url='https://example.com', website_label='Art shop')
        response = self.client.get(reverse('contact'))
        self.assertContains(response, 'mailto:artist@example.com')
        self.assertContains(response, 'Art shop')
        self.assertContains(response, '&lt;script&gt;')
        self.assertNotContains(response, '<dt>Phone</dt>')

    def test_admin_can_edit_single_contact_record(self):
        user = get_user_model().objects.create_superuser('artist', 'artist@example.com', 'test-password')
        self.client.force_login(user)
        self.assertEqual(self.client.get(reverse('admin:contact_contactinfo_add')).status_code, 200)
        info = ContactInfo.objects.create()
        self.assertEqual(self.client.get(reverse('admin:contact_contactinfo_add')).status_code, 403)
        response = self.client.post(reverse('admin:contact_contactinfo_change', args=[info.pk]), {
            'heading': 'Art enquiries', 'introduction': 'Commissions welcome',
            'email': 'artist@example.com', 'phone': '', 'studio_details': '',
            'website_label': '', 'website_url': '', '_save': 'Save',
        })
        self.assertEqual(response.status_code, 302)
        self.assertContains(self.client.get(reverse('contact')), 'Art enquiries')
        self.assertContains(self.client.get(reverse('admin:index')), 'Manage your artwork and website')
