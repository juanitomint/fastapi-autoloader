import unittest
from fastapi import FastAPI
from fastapi_autoloader.autoloader import AutoLoader
import os
import tempfile
import shutil

class DummyRouter:
    pass

class TestAutoLoader(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for controllers
        self.temp_dir = tempfile.mkdtemp()
        self.app = FastAPI()
        # Create a dummy controller file with a router
        controller_code = """
from fastapi import APIRouter
router = APIRouter()
@router.get('/dummy')
def dummy():
    return {'msg': 'ok'}
"""
        os.makedirs(os.path.join(self.temp_dir, "sub"))
        with open(os.path.join(self.temp_dir, "sub", "dummy.py"), "w") as f:
            f.write(controller_code)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_load_finds_router(self):
        loader = AutoLoader(target_dir=self.temp_dir)
        loader.load(self.app)
        # Should have loaded one module
        self.assertEqual(len(loader.modules), 1)
        # The route should be present in the app
        routes = [route.path for route in self.app.routes]
        self.assertIn("/dummy", routes)

    def test_load_no_router(self):
        # Create a file without a router
        with open(os.path.join(self.temp_dir, "no_router.py"), "w") as f:
            f.write("def foo(): return 42\n")
        loader = AutoLoader(target_dir=self.temp_dir)
        loader.load(self.app)
        # Only the dummy router should be loaded
        self.assertEqual(len(loader.modules), 1)

if __name__ == "__main__":
    unittest.main()
