"""
Test deface "existing output" flow: return to page shows converted files,
and Generate Documents works from existing deface folder (no session).
"""
import json
import shutil
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import create_app
from config import OUTPUT_FOLDER


# Minimal JPEG bytes (valid tiny image)
TINY_JPEG = (
    b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00'
    b'\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c'
    b'\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a'
    b'\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x0b\x08'
    b'\x00\x01\x00\x01\x01\x01\x11\x00\xff\xc4\x00\x1f\x00\x00\x01\x05\x01'
    b'\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04'
    b'\x05\x06\x07\x08\t\n\x0b\xff\xc4\x00\xb5\x10\x00\x02\x01\x03\x03\x02'
    b'\x04\x03\x05\x05\x04\x04\x00\x00\x01}\x01\x02\x03\x00\x04\x11\x05\x12'
    b'\x21\x31A\x06\x13Qa\x07"q\x142\x81\x91\xa1\x08#B\xb1\xc1\x15R\xd1'
    b'\xf0$3br\x82\t\n\x16\x17\x18\x19\x1a%&\'()*456789:CDEFGHIJSTUVWXYZ'
    b'cdefghijstuvwxyz\x83\x84\x85\x86\x87\x88\x89\x8a\x92\x93\x94\x95\x96'
    b'\x97\x98\x99\x9a\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xb2\xb3\xb4\xb5'
    b'\xb6\xb7\xb8\xb9\xba\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xd2\xd3\xd4'
    b'\xd5\xd6\xd7\xd8\xd9\xda\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xf1'
    b'\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xff\xda\x00\x08\x01\x01\x00\x00'
    b'?\x00\xfc\xff\xd9'
)


class TestDefaceExistingAndGenerate(unittest.TestCase):
    """Test deface_existing and generate_deface_documents from existing folder."""

    TEST_QUAL = "_test_deface_existing_qual"
    TEST_LEARNER = "_test_deface_existing_learner"

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.deface_dir = OUTPUT_FOLDER / self.TEST_QUAL / self.TEST_LEARNER / "deface"
        self.deface_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        parent = OUTPUT_FOLDER / self.TEST_QUAL
        if parent.exists():
            shutil.rmtree(parent, ignore_errors=True)

    def test_deface_existing_empty_returns_empty_list(self):
        """GET deface_existing with no files in deface folder returns items: []."""
        # deface_dir exists but is empty (or we could remove it for this test)
        response = self.client.get(
            "/v2p-formatter/deface_existing",
            query_string={
                "qualification": self.TEST_QUAL,
                "learner": self.TEST_LEARNER,
            },
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("items", data)
        self.assertIsInstance(data["items"], list)

    def test_deface_existing_returns_saved_files(self):
        """GET deface_existing returns items when deface folder has image/video files."""
        (self.deface_dir / "deface_test_image.jpg").write_bytes(TINY_JPEG)
        response = self.client.get(
            "/v2p-formatter/deface_existing",
            query_string={
                "qualification": self.TEST_QUAL,
                "learner": self.TEST_LEARNER,
            },
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("items", data)
        self.assertGreaterEqual(len(data["items"]), 1)
        item = data["items"][0]
        self.assertEqual(item.get("original_name"), "test_image.jpg")
        self.assertEqual(item.get("type"), "image")
        self.assertTrue(item.get("from_existing"))

    def test_generate_deface_documents_from_existing_folder(self):
        """POST generate_deface_documents with qual+learner and no session_id uses existing deface folder."""
        (self.deface_dir / "deface_test_image.jpg").write_bytes(TINY_JPEG)
        response = self.client.post(
            "/v2p-formatter/generate_deface_documents",
            data=json.dumps({
                "qualification": self.TEST_QUAL,
                "learner": self.TEST_LEARNER,
                "filename": "existing_test_report",
                "output_format": "media",
                "quality": 95,
                "max_size": "640x480",
                "image_order": [1],
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200, response.get_data(as_text=True))
        data = response.get_json()
        self.assertTrue(data.get("success"), data.get("error"))
        self.assertIn("output_folder_path", data)
        self.assertIn("deface", data["output_folder_path"])
        # Media format: expect exported standalone images
        self.assertIn("exported_standalone_images", data)
        self.assertGreaterEqual(len(data["exported_standalone_images"]), 1)

    def test_generate_deface_documents_requires_qual_learner_when_no_session(self):
        """POST generate_deface_documents with no session_id and no qual/learner returns 400."""
        response = self.client.post(
            "/v2p-formatter/generate_deface_documents",
            data=json.dumps({
                "filename": "report",
                "output_format": "media",
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data.get("success"))
        self.assertIn("qualification", data.get("error", "").lower())


if __name__ == "__main__":
    unittest.main()
