import os
import subprocess
import sys
import tempfile
from pathlib import Path
from django.test import TestCase
from django.urls import reverse
from gallery.models import Album, GalleryImage


class DeploymentTests(TestCase):
    def test_root_home_and_legacy_redirect(self):
        self.assertEqual(reverse('home'), '/')
        self.assertEqual(self.client.get('/').status_code, 200)
        self.assertRedirects(self.client.get('/MainPage/'), '/', status_code=301)

    def test_private_artwork_is_not_published(self):
        album = Album.objects.create(title='Collection')
        GalleryImage.objects.create(album=album, title='Private sketch', image='gallery/private.jpg', is_public=False)
        GalleryImage.objects.create(album=album, title='Published artwork', image='gallery/public.jpg', is_public=True)
        response = self.client.get(reverse('gallery'))
        self.assertContains(response, 'Published artwork')
        self.assertNotContains(response, 'Private sketch')

    def test_production_requires_secret(self):
        env = dict(os.environ, DJANGO_SETTINGS_MODULE='laneslane.production')
        env.pop('DJANGO_SECRET_KEY', None)
        env['DJANGO_ENV_FILE'] = '/nonexistent/laneslane-test.env'
        result = subprocess.run([sys.executable, '-c', 'import django; django.setup()'], env=env, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Set DJANGO_SECRET_KEY', result.stderr)

    def test_apache_entrypoint_loads_server_configuration(self):
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / 'production.env'
            config.write_text('DJANGO_SECRET_KEY=' + 'x' * 64 + '\nDJANGO_ALLOWED_HOSTS=art.example.com\n')
            env = dict(os.environ, DJANGO_ENV_FILE=str(config))
            for name in ('DJANGO_SECRET_KEY', 'DJANGO_ALLOWED_HOSTS'):
                env.pop(name, None)
            result = subprocess.run([
                sys.executable, '-c',
                "import runpy; runpy.run_path('deploy/apache.wsgi'); "
                "from django.conf import settings; "
                "assert not settings.DEBUG; "
                "assert settings.ALLOWED_HOSTS == ['art.example.com']; "
                "assert settings.SESSION_COOKIE_SECURE"
            ], env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
