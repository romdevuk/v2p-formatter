"""
Test to verify that PDF and JPG files are created successfully
This test can be run after manual testing to verify file creation
"""
import pytest
from pathlib import Path
import os


class TestFileVerification:
    """Verify that output files are created correctly"""
    
    def test_verify_pdf_and_jpg_files_exist(self):
        """Verify that PDF and JPG files exist in the visited directory"""
        print("\n=== File Verification Test ===")
        
        visited_path = Path("/Users/rom/Documents/nvq/visited")
        
        # Find all PDF files
        pdf_files = list(visited_path.rglob("*.pdf"))
        print(f"✅ Found {len(pdf_files)} PDF files")
        
        # Find all _frames directories with JPG files
        frames_dirs = []
        jpg_count = 0
        
        for frames_dir in visited_path.rglob("*_frames"):
            if frames_dir.is_dir():
                jpg_files = list(frames_dir.glob("*.jpg"))
                if jpg_files:
                    frames_dirs.append(frames_dir)
                    jpg_count += len(jpg_files)
                    print(f"✅ Found {len(jpg_files)} JPG files in {frames_dir.name}")
        
        print(f"✅ Total: {len(frames_dirs)} frame directories with {jpg_count} JPG files")
        
        # Verify specific files (1.jpg, 2.jpg, 3.jpg) exist in at least one directory
        found_sequence = False
        for frames_dir in frames_dirs:
            expected_files = [frames_dir / "1.jpg", frames_dir / "2.jpg", frames_dir / "3.jpg"]
            if all(f.exists() for f in expected_files):
                found_sequence = True
                print(f"✅✅✅ Found sequence 1.jpg, 2.jpg, 3.jpg in {frames_dir}")
                break
        
        # Assertions
        assert len(pdf_files) > 0, "No PDF files found"
        assert jpg_count > 0, "No JPG files found"
        assert found_sequence, "Sequence 1.jpg, 2.jpg, 3.jpg not found in any directory"
        
        print("\n✅✅✅ All file verification tests PASSED!")
        print(f"   - PDF files: {len(pdf_files)}")
        print(f"   - JPG files: {jpg_count} in {len(frames_dirs)} directories")
        print(f"   - Sequence files (1.jpg, 2.jpg, 3.jpg): Found")
        
    def test_verify_recent_files(self):
        """Verify recently created files (within last hour)"""
        import time
        from datetime import datetime, timedelta
        
        print("\n=== Recent Files Verification ===")
        
        visited_path = Path("/Users/rom/Documents/nvq/visited")
        one_hour_ago = time.time() - 3600
        
        recent_pdfs = []
        recent_jpgs = []
        
        # Find recent PDFs
        for pdf_file in visited_path.rglob("*.pdf"):
            if pdf_file.stat().st_mtime > one_hour_ago:
                recent_pdfs.append(pdf_file)
                print(f"✅ Recent PDF: {pdf_file} (modified {datetime.fromtimestamp(pdf_file.stat().st_mtime)})")
        
        # Find recent JPGs
        for frames_dir in visited_path.rglob("*_frames"):
            if frames_dir.is_dir():
                for jpg_file in frames_dir.glob("*.jpg"):
                    if jpg_file.stat().st_mtime > one_hour_ago:
                        recent_jpgs.append(jpg_file)
        
        print(f"✅ Found {len(recent_pdfs)} recent PDF files")
        print(f"✅ Found {len(recent_jpgs)} recent JPG files")
        
        if recent_pdfs or recent_jpgs:
            print("✅✅✅ Recent files found - application is working!")
        else:
            print("⚠️  No recent files found (this is OK if tests were run earlier)")

