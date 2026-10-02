"""Protect local renders and reject incomplete/corrupt release downloads."""

import hashlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import fetch_media
import manifest
import media


class DownloadTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name)
        self.folder = self.root / "styles" / "clay"
        self.folder.mkdir(parents=True)
        self.target = self.folder / "clay.mp4"
        self.content = b"verified release clip"
        self.item = {"size": len(self.content), "sha256": hashlib.sha256(self.content).hexdigest()}
        patches = [patch.object(manifest, "ROOT", self.root),
                   patch.object(media, "asset", return_value=self.item),
                   patch.object(media, "url", return_value="https://example.com/clay.mp4")]
        for mocked in patches:
            mocked.start()
            self.addCleanup(mocked.stop)

    def test_verified_download_is_reused_without_network(self):
        with patch.object(fetch_media, "urlopen", return_value=io.BytesIO(self.content)) as request:
            fetch_media.fetch("clay", "video")
            fetch_media.fetch("clay", "video")
            self.assertEqual(request.call_count, 1)
        self.assertEqual(self.target.read_bytes(), self.content)
        self.assertEqual(list(self.folder.iterdir()), [self.target])

    def test_corrupt_download_never_becomes_a_clip(self):
        with patch.object(fetch_media, "urlopen", return_value=io.BytesIO(b"incomplete")):
            with self.assertRaisesRegex(ValueError, "SHA-256"):
                fetch_media.fetch("clay", "video")
        self.assertEqual(list(self.folder.iterdir()), [])

    def test_local_rebuild_is_preserved(self):
        self.target.write_bytes(b"my local render")
        with patch.object(fetch_media, "urlopen") as request:
            with self.assertRaisesRegex(ValueError, "move it aside"):
                fetch_media.fetch("clay", "video")
            request.assert_not_called()
        self.assertEqual(self.target.read_bytes(), b"my local render")

    def test_concurrent_render_is_not_overwritten(self):
        def response(*args, **kwargs):
            self.target.write_bytes(b"concurrent render")
            return io.BytesIO(self.content)
        with patch.object(fetch_media, "urlopen", side_effect=response):
            with self.assertRaises(FileExistsError):
                fetch_media.fetch("clay", "video")
        self.assertEqual(self.target.read_bytes(), b"concurrent render")
        self.assertEqual(list(self.folder.iterdir()), [self.target])


if __name__ == "__main__":
    unittest.main()
