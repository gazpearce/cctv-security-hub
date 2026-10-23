"""
tests/test_challenger_m2vid_stress.py
======================================
Adversarial Stress Test & Empirical Quality Gate for Milestone M2-VID.
Author: M2-VID Challenger 1 (Adversarial Critic & Video Binary Specialist)

Validates:
1. Catalog Schema, Rule 45 Citadel Air-Gap, and Trade E-E-A-T Invariants.
2. Direct FFprobe Stream & Atom Probing across ALL 50 MP4 files:
   - H.264 High Profile, 1920x1080, progressive scan, 30fps.
   - AAC stereo audio, 48000 Hz, duration matching video duration within +/- 0.5s.
   - Binary atom inspection (+faststart: moov atom preceding mdat atom).
3. OpenCV Temporal Differencing across ALL 50 MP4 files:
   - Frame 0, Frame 300, Frame 900 sampling.
   - Mean Absolute Error (MAE) > 5.0 (rejects static freeze-frames and dummy loops).
4. WebP Thumbnail Visual & Scrim Contrast Integrity across ALL 50 WebP thumbnails:
   - Exact 1600x900 resolution.
   - Visual entropy > 4.0.
   - Dark footer scrim luminance < 110.0 (AAA contrast compliance).
5. Cryptographic SHA-256 Collision Defense across all 50 MP4s and 50 WebPs.
"""

import hashlib
import json
import os
import re
import struct
import subprocess
import sys
import unittest
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent


def get_mp4_atoms(file_path: Path):
    """Parses top-level MP4 container atoms and their byte offsets."""
    atoms = []
    with open(file_path, "rb") as f:
        file_size = f.seek(0, 2)
        f.seek(0)
        while f.tell() < file_size:
            header = f.read(8)
            if len(header) < 8:
                break
            size, atom_type = struct.unpack(">I4s", header)
            atom_name = atom_type.decode("ascii", errors="replace")
            pos = f.tell() - 8
            atoms.append((atom_name, size, pos))
            if size == 1:
                # 64-bit large size
                large_size = struct.unpack(">Q", f.read(8))[0]
                f.seek(pos + large_size)
            elif size == 0:
                # atom extends to end of file
                break
            else:
                f.seek(pos + size)
    return atoms


class TestCatalogAndMetadataAdversarial(unittest.TestCase):
    """Adversarial stress testing of catalog structure, Rule 45 Citadel Air-Gap, and E-E-A-T metadata."""

    @classmethod
    def setUpClass(cls):
        cls.catalog_file = REPO_ROOT / "video_stack_50_catalog.json"
        if not cls.catalog_file.exists():
            cls.catalog_file = REPO_ROOT / "category_manifests" / "video_stack_50_catalog.json"
        with open(cls.catalog_file, "r", encoding="utf-8") as f:
            cls.data = json.load(f)
        cls.videos = cls.data.get("videos", [])

    def test_01_catalog_has_exactly_50_videos(self):
        self.assertEqual(len(self.videos), 50, f"Expected 50 videos, found {len(self.videos)}")
        self.assertEqual(self.data.get("total_videos"), 50)

    def test_02_sequential_ids_vid001_through_vid050(self):
        ids = [v.get("video_id") for v in self.videos]
        expected = [f"VID-{i:03d}" for i in range(1, 51)]
        self.assertEqual(ids, expected)
        self.assertEqual(len(set(ids)), 50)

    def test_03_all_16_mandatory_fields_present_and_populated(self):
        required_fields = [
            "video_id", "slug", "title", "trade_category", "duration_sec",
            "video_path", "thumbnail_path", "script_narration", "tags",
            "description_tier1", "description_tier2", "description_tier3",
            "buffer_url", "blogger_shield_url", "hardware_standards", "timestamps"
        ]
        for v in self.videos:
            vid = v.get("video_id")
            for field in required_fields:
                self.assertIn(field, v, f"{vid} is missing field '{field}'")
                val = v[field]
                self.assertIsNotNone(val, f"{vid} has None for '{field}'")
                if isinstance(val, (str, list, dict)):
                    self.assertTrue(len(val) > 0, f"{vid} has empty value for '{field}'")

    def test_04_rule45_zero_raw_root_links(self):
        from verify_no_root_anchors import is_raw_root_violation
        for v in self.videos:
            vid = v.get("video_id")
            for desc_key in ("description_tier1", "description_tier2", "description_tier3"):
                desc = v.get(desc_key, "")
                for line in desc.splitlines():
                    self.assertFalse(
                        is_raw_root_violation(line),
                        f"Rule 45 raw root violation in {vid} {desc_key}: {line.strip()}"
                    )
            buf = v.get("buffer_url", "")
            self.assertFalse(
                is_raw_root_violation(buf),
                f"Rule 45 raw root violation in {vid} buffer_url: {buf}"
            )

    def test_05_tier3_strict_youtube_isolation(self):
        for v in self.videos:
            vid = v.get("video_id")
            t3 = v.get("description_tier3", "")
            self.assertNotIn("adicommunications.co.uk", t3.lower(),
                             f"{vid} Tier 3 description leaks adicommunications.co.uk domain")
            self.assertIn("https://www.youtube.com/@cctv.services", t3.lower(),
                          f"{vid} Tier 3 description missing required YouTube Apex link")

    def test_06_trade_eeat_invariants(self):
        for v in self.videos:
            vid = v.get("video_id")
            for key in ("description_tier1", "description_tier2"):
                text = v.get(key, "")
                self.assertIn("Gary Pearce", text, f"{vid} {key} missing 'Gary Pearce'")
                self.assertIn("07860 244 274", text, f"{vid} {key} missing '07860 244 274'")
                self.assertIn("£10M", text, f"{vid} {key} missing '£10M'")
                self.assertNotIn("Checkatrade", text, f"{vid} {key} references forbidden word Checkatrade")
                self.assertNotIn("0800", text, f"{vid} {key} references forbidden 0800 number")
                self.assertNotIn("CAI Member", text, f"{vid} {key} illegally claims CAI membership")


class TestFFprobeStreamAdversarial(unittest.TestCase):
    """Direct empirical ffprobe stream and container testing across all 50 MP4 files."""

    @classmethod
    def setUpClass(cls):
        catalog_file = REPO_ROOT / "video_stack_50_catalog.json"
        if not catalog_file.exists():
            catalog_file = REPO_ROOT / "category_manifests" / "video_stack_50_catalog.json"
        with open(catalog_file, "r", encoding="utf-8") as f:
            cls.videos = json.load(f).get("videos", [])

        cls.probes = {}
        for v in cls.videos:
            vid = v.get("video_id")
            rel_path = v.get("video_path")
            full_path = REPO_ROOT / rel_path
            if full_path.exists():
                cmd = [
                    "ffprobe", "-v", "quiet",
                    "-print_format", "json",
                    "-show_format", "-show_streams",
                    str(full_path)
                ]
                res = subprocess.run(cmd, capture_output=True, text=True)
                if res.returncode == 0:
                    cls.probes[vid] = json.loads(res.stdout)

    def test_07_all_50_mp4_files_exist_and_sized_appropriately(self):
        self.assertEqual(len(self.videos), 50)
        for v in self.videos:
            vid = v.get("video_id")
            path = REPO_ROOT / v.get("video_path")
            self.assertTrue(path.exists(), f"MP4 file missing for {vid} at {path}")
            size = path.stat().st_size
            self.assertGreaterEqual(size, 512_000, f"{vid} MP4 is suspiciously small ({size} bytes)")
            self.assertLessEqual(size, 100_000_000, f"{vid} MP4 exceeds 100 MB budget ({size} bytes)")

    def test_08_all_50_mp4_faststart_atom_order(self):
        """Validates that moov atom precedes mdat atom in binary structure (+faststart enabled)."""
        for v in self.videos:
            vid = v.get("video_id")
            path = REPO_ROOT / v.get("video_path")
            atoms = get_mp4_atoms(path)
            atom_names = [a[0] for a in atoms]
            self.assertIn("moov", atom_names, f"{vid} missing moov atom")
            self.assertIn("mdat", atom_names, f"{vid} missing mdat atom")
            moov_idx = atom_names.index("moov")
            mdat_idx = atom_names.index("mdat")
            self.assertLess(moov_idx, mdat_idx,
                            f"{vid} fails +faststart: moov (index {moov_idx}) appears after mdat (index {mdat_idx})")

    def test_09_all_50_mp4_video_stream_specs(self):
        """Asserts H.264 High Profile, 1920x1080, progressive, 30fps for all 50 files."""
        for v in self.videos:
            vid = v.get("video_id")
            probe = self.probes.get(vid)
            self.assertIsNotNone(probe, f"Could not probe {vid}")
            v_streams = [s for s in probe.get("streams", []) if s.get("codec_type") == "video"]
            self.assertEqual(len(v_streams), 1, f"{vid} must have exactly 1 video stream")
            stream = v_streams[0]
            self.assertEqual(stream.get("codec_name"), "h264", f"{vid} codec is not h264")
            self.assertEqual(stream.get("profile"), "High", f"{vid} profile is not High")
            self.assertEqual(stream.get("width"), 1920, f"{vid} width is not 1920")
            self.assertEqual(stream.get("height"), 1080, f"{vid} height is not 1080")
            self.assertEqual(stream.get("r_frame_rate"), "30/1", f"{vid} frame rate is not 30/1")
            field_order = stream.get("field_order", "progressive")
            self.assertIn(field_order, ("progressive", None, "unknown"), f"{vid} field_order is interlaced")

    def test_10_all_50_mp4_audio_stream_specs(self):
        """Asserts AAC stereo 48000 Hz audio for all 50 files."""
        for v in self.videos:
            vid = v.get("video_id")
            probe = self.probes.get(vid)
            self.assertIsNotNone(probe, f"Could not probe {vid}")
            a_streams = [s for s in probe.get("streams", []) if s.get("codec_type") == "audio"]
            self.assertEqual(len(a_streams), 1, f"{vid} must have exactly 1 audio stream")
            stream = a_streams[0]
            self.assertEqual(stream.get("codec_name"), "aac", f"{vid} audio codec is not aac")
            self.assertEqual(stream.get("sample_rate"), "48000", f"{vid} sample rate is not 48000 Hz")
            self.assertEqual(stream.get("channels"), 2, f"{vid} is not stereo (2 channels)")

    def test_11_all_50_mp4_audio_video_duration_sync(self):
        """Asserts audio duration matches video duration within +/- 0.5s for all 50 files."""
        for v in self.videos:
            vid = v.get("video_id")
            probe = self.probes.get(vid)
            self.assertIsNotNone(probe, f"Could not probe {vid}")
            v_stream = [s for s in probe.get("streams", []) if s.get("codec_type") == "video"][0]
            a_stream = [s for s in probe.get("streams", []) if s.get("codec_type") == "audio"][0]
            fmt = probe.get("format", {})

            v_dur = float(v_stream.get("duration") or fmt.get("duration", 0))
            a_dur = float(a_stream.get("duration") or fmt.get("duration", 0))
            delta = abs(v_dur - a_dur)
            self.assertLessEqual(delta, 0.5,
                                 f"{vid} audio/video duration desync: v={v_dur:.3f}s, a={a_dur:.3f}s (delta={delta:.3f}s > 0.5s)")


class TestOpenCVTemporalDynamicsAdversarial(unittest.TestCase):
    """Adversarially asserts temporal dynamics across all 50 MP4s to reject static freeze frames."""

    @classmethod
    def setUpClass(cls):
        catalog_file = REPO_ROOT / "video_stack_50_catalog.json"
        if not catalog_file.exists():
            catalog_file = REPO_ROOT / "category_manifests" / "video_stack_50_catalog.json"
        with open(catalog_file, "r", encoding="utf-8") as f:
            cls.videos = json.load(f).get("videos", [])

    def test_12_all_50_mp4s_temporal_frame_differencing_mae(self):
        """Empirically computes MAE between Frame 0, Frame 300, and Frame 900 across all 50 videos."""
        mae_threshold = 5.0
        failures = []

        for v in self.videos:
            vid = v.get("video_id")
            path = REPO_ROOT / v.get("video_path")
            cap = cv2.VideoCapture(str(path))
            if not cap.isOpened():
                failures.append(f"{vid}: Could not open video with OpenCV")
                continue

            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            if total_frames < 600:
                failures.append(f"{vid}: Total frames {total_frames} < 600 (<20s)")
                cap.release()
                continue

            # Frame 0
            ret0, f0 = cap.read()
            # Frame 300 (~10 seconds in)
            cap.set(cv2.CAP_PROP_POS_FRAMES, 300)
            ret300, f300 = cap.read()
            # Frame 900 (~30 seconds in)
            frame_sample_2 = min(900, total_frames - 30)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_sample_2)
            ret_sample_2, f_sample_2 = cap.read()
            cap.release()

            if not (ret0 and ret300 and ret_sample_2):
                failures.append(f"{vid}: Failed to read test frames")
                continue

            mae_0_300 = float(np.mean(np.abs(f0.astype(float) - f300.astype(float))))
            mae_300_sample2 = float(np.mean(np.abs(f300.astype(float) - f_sample_2.astype(float))))

            if mae_0_300 <= mae_threshold or mae_300_sample2 <= mae_threshold:
                failures.append(
                    f"{vid}: Static frame detected! MAE(0,300)={mae_0_300:.2f}, MAE(300,{frame_sample_2})={mae_300_sample2:.2f} <= {mae_threshold}"
                )

        self.assertEqual(len(failures), 0, f"Temporal dynamics check failed on:\n" + "\n".join(failures))


class TestThumbnailIntegrityAdversarial(unittest.TestCase):
    """Pillow and numpy analysis of all 50 WebP thumbnails."""

    @classmethod
    def setUpClass(cls):
        catalog_file = REPO_ROOT / "video_stack_50_catalog.json"
        if not catalog_file.exists():
            catalog_file = REPO_ROOT / "category_manifests" / "video_stack_50_catalog.json"
        with open(catalog_file, "r", encoding="utf-8") as f:
            cls.videos = json.load(f).get("videos", [])

    def test_13_all_50_thumbnails_geometry_entropy_and_scrim_contrast(self):
        """Validates 1600x900 resolution, entropy > 4.0, and dark scrim luminance < 110.0."""
        failures = []
        for v in self.videos:
            vid = v.get("video_id")
            path = REPO_ROOT / v.get("thumbnail_path")
            if not path.exists():
                failures.append(f"{vid}: Missing thumbnail at {path}")
                continue

            try:
                img = Image.open(path)
            except Exception as e:
                failures.append(f"{vid}: Cannot open thumbnail: {e}")
                continue

            # Geometry check
            if img.size != (1600, 900):
                failures.append(f"{vid}: Dimensions {img.size} != (1600, 900)")

            # Visual entropy check (ensures authentic photographic density)
            entropy = img.entropy()
            if entropy < 4.0:
                failures.append(f"{vid}: Low visual entropy {entropy:.2f} < 4.0")

            # Scrim luminance check on bottom 20%
            w, h = img.size
            scrim_box = (0, int(h * 0.8), w, h)
            scrim = img.crop(scrim_box)
            scrim_arr = np.array(scrim.convert("L"))
            mean_lum = float(scrim_arr.mean())

            if mean_lum >= 110.0:
                failures.append(f"{vid}: Scrim luminance {mean_lum:.2f} >= 110.0 (fails AAA contrast standard)")

        self.assertEqual(len(failures), 0, f"Thumbnail integrity check failed on:\n" + "\n".join(failures))


class TestSHA256CollisionDefenseAdversarial(unittest.TestCase):
    """Cryptographic SHA-256 collision check across all 50 MP4s and 50 WebPs."""

    @classmethod
    def setUpClass(cls):
        catalog_file = REPO_ROOT / "video_stack_50_catalog.json"
        if not catalog_file.exists():
            catalog_file = REPO_ROOT / "category_manifests" / "video_stack_50_catalog.json"
        with open(catalog_file, "r", encoding="utf-8") as f:
            cls.videos = json.load(f).get("videos", [])

    def test_14_sha256_uniqueness_across_50_mp4_videos(self):
        """Asserts 100% cryptographic uniqueness across all 50 MP4 video binaries."""
        hashes = {}
        for v in self.videos:
            vid = v.get("video_id")
            path = REPO_ROOT / v.get("video_path")
            with open(path, "rb") as f:
                h = hashlib.sha256(f.read()).hexdigest()
            self.assertNotIn(h, hashes, f"SHA-256 COLLISION detected! {vid} matches {hashes.get(h)}")
            hashes[h] = vid
        self.assertEqual(len(hashes), 50, f"Expected 50 unique MP4 hashes, found {len(hashes)}")

    def test_15_sha256_uniqueness_across_50_webp_thumbnails(self):
        """Asserts 100% cryptographic uniqueness across all 50 WebP thumbnail binaries."""
        hashes = {}
        for v in self.videos:
            vid = v.get("video_id")
            path = REPO_ROOT / v.get("thumbnail_path")
            with open(path, "rb") as f:
                h = hashlib.sha256(f.read()).hexdigest()
            self.assertNotIn(h, hashes, f"SHA-256 COLLISION detected! {vid} matches {hashes.get(h)}")
            hashes[h] = vid
        self.assertEqual(len(hashes), 50, f"Expected 50 unique WebP hashes, found {len(hashes)}")

    def test_16_zero_orphan_files_in_assets_videos(self):
        """Asserts exactly 50 MP4 files and 50 WebP thumbnails in assets/videos (no dangling temps)."""
        video_dir = REPO_ROOT / "assets" / "videos"
        all_files = list(video_dir.iterdir())
        mp4_files = [f for f in all_files if f.suffix == ".mp4"]
        webp_files = [f for f in all_files if f.suffix == ".webp"]
        other_files = [f for f in all_files if f.suffix not in (".mp4", ".webp")]

        self.assertEqual(len(mp4_files), 50, f"Found {len(mp4_files)} MP4s in assets/videos, expected 50")
        self.assertEqual(len(webp_files), 50, f"Found {len(webp_files)} WebPs in assets/videos, expected 50")
        self.assertEqual(len(other_files), 0, f"Found unexpected orphan files in assets/videos: {other_files}")


if __name__ == "__main__":
    unittest.main()
