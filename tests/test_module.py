import yuri
from tests import BaseTestCase


class ModuleTestCase(BaseTestCase):
    def test_exposes_version(self):
        self.assertTrue(hasattr(yuri, "__version__"))

    def test_exposes_camera(self):
        self.assertEqual(yuri.Camera, yuri.camera.Camera)
