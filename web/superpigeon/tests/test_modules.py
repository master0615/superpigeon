from django.test import TestCase

class ModulesTestCase(TestCase):

    def test_modules(self):
        from superpigeon import settings
        for i in settings.INSTALLED_APPS:
            try:
                __import__(i)
            except ImportError:
                return False
