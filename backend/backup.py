import os
import gzip
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

from backend.config import BASE_DIR, DB_PATH

BACKUP_DIR = BASE_DIR / "data" / "backups"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

class DatabaseBackupService:
    @staticmethod
    def create_local_snapshot() -> Path:
        """
        Creates an atomic, consistent point-in-time snapshot of the SQLite database
        using the official SQLite Online Backup API (prevents corruption during active writes).
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        raw_snapshot_path = BACKUP_DIR / f"allsarkarijobs_{timestamp}.db"
        compressed_path = BACKUP_DIR / f"allsarkarijobs_{timestamp}.db.gz"

        print(f"[Backup] Initiating safe SQLite atomic backup from {DB_PATH}...")

        # 1. Atomic backup via SQLite Online Backup API
        src_conn = sqlite3.connect(DB_PATH)
        dest_conn = sqlite3.connect(raw_snapshot_path)
        with dest_conn:
            src_conn.backup(dest_conn)
        dest_conn.close()
        src_conn.close()

        # 2. Compress with gzip (reduces 20MB database to ~2-3MB)
        with open(raw_snapshot_path, "rb") as f_in:
            with gzip.open(compressed_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

        # Remove uncompressed raw snapshot
        if raw_snapshot_path.exists():
            raw_snapshot_path.unlink()

        file_size_kb = compressed_path.stat().st_size / 1024
        print(f"[Backup] Successfully created compressed snapshot: {compressed_path.name} ({file_size_kb:.1f} KB)")

        # 3. Clean up older backups (keep last 7 local backups)
        DatabaseBackupService.prune_old_backups(keep=7)

        return compressed_path

    @staticmethod
    def prune_old_backups(keep: int = 7):
        """Removes backups older than the last N snapshots to save disk space."""
        backups = sorted(BACKUP_DIR.glob("allsarkarijobs_*.db.gz"), key=os.path.getmtime, reverse=True)
        if len(backups) > keep:
            for old_file in backups[keep:]:
                try:
                    old_file.unlink()
                    print(f"[Backup] Pruned old snapshot: {old_file.name}")
                except Exception as e:
                    print(f"[Backup] Error pruning {old_file.name}: {e}")

    @staticmethod
    def upload_to_google_drive(file_path: Path, credentials_file: Optional[str] = "google_credentials.json") -> bool:
        """
        Uploads the compressed backup to Google Drive.
        Requires google-api-python-client and google-auth.
        """
        creds_path = BASE_DIR / (credentials_file or "google_credentials.json")
        if not creds_path.exists():
            print(f"[Backup] Google Drive credentials not found at {creds_path}.")
            print("[Backup] Local compressed snapshot preserved safely in 'data/backups/'.")
            return False

        try:
            from google.oauth2 import service_account
            from googleapiclient.discovery import build
            from googleapiclient.http import MediaFileUpload

            SCOPES = ["https://www.googleapis.com/auth/drive.file"]
            creds = service_account.Credentials.from_service_account_file(str(creds_path), scopes=SCOPES)
            service = build("drive", "v3", credentials=creds)

            file_metadata = {
                "name": file_path.name,
                "description": "AllSarkariJobs Automated Database Backup"
            }
            media = MediaFileUpload(str(file_path), mimetype="application/gzip")

            uploaded_file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields="id"
            ).execute()

            print(f"[Backup] Uploaded to Google Drive successfully! File ID: {uploaded_file.get('id')}")
            return True
        except ImportError:
            print("[Backup] To enable direct Google Drive upload, run: pip install google-api-python-client google-auth")
            return False
        except Exception as e:
            print(f"[Backup] Google Drive upload error: {e}")
            return False

    @classmethod
    def run_backup(cls):
        """Runs the complete backup pipeline (Snapshot -> Compression -> Cloud Upload)."""
        snapshot = cls.create_local_snapshot()
        cls.upload_to_google_drive(snapshot)
        return snapshot

if __name__ == "__main__":
    print("=" * 60)
    print("AllSarkariJobs Automated Backup Utility")
    print("=" * 60)
    saved_file = DatabaseBackupService.run_backup()
    print("Backup completed successfully! Location:", saved_file)
