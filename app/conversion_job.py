"""
Asynchronous conversion job management
"""
import threading
import time
import uuid
from pathlib import Path
from typing import Dict, List, Optional
from enum import Enum
import logging

logger = logging.getLogger('media_converter.job')


class JobStatus(Enum):
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'


class FileStatus(Enum):
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'


class ConversionJob:
    """Manages asynchronous conversion jobs"""
    
    def __init__(self, job_id: str, files: List[Dict], settings: Dict):
        self.job_id = job_id
        self.files = files  # List of {type: 'video'|'image', path: str, ...}
        self.settings = settings  # {video: {...}, image: {...}}
        self.status = JobStatus.PENDING
        self.file_statuses = {f['path']: FileStatus.PENDING for f in files}
        self.results = {}  # {file_path: {success, output_path, ...}}
        self.errors = {}  # {file_path: error_message}
        self.progress = 0.0  # 0.0 to 1.0
        self.start_time = None
        self.end_time = None
        self.thread = None
        self.cancelled = False
        self.lock = threading.Lock()
    
    def start(self, converter_func):
        """Start conversion in background thread"""
        if self.status != JobStatus.PENDING:
            return
        
        self.status = JobStatus.PROCESSING
        self.start_time = time.time()
        self.thread = threading.Thread(target=self._run, args=(converter_func,), daemon=True)
        self.thread.start()
        logger.info(f"Job {self.job_id} started with {len(self.files)} files")
    
    def _run(self, converter_func):
        """Run conversion in background"""
        try:
            total_files = len(self.files)
            completed = 0
            
            for file_info in self.files:
                if self.cancelled:
                    self.status = JobStatus.CANCELLED
                    self.file_statuses[file_info['path']] = FileStatus.CANCELLED
                    break
                
                file_path = file_info['path']
                
                with self.lock:
                    self.file_statuses[file_path] = FileStatus.PROCESSING
                
                logger.debug(f"Processing file: {file_path}")
                
                try:
                    # Call converter function
                    result = converter_func(file_info, self.settings)
                    
                    with self.lock:
                        if result.get('success'):
                            self.file_statuses[file_path] = FileStatus.COMPLETED
                            self.results[file_path] = result
                            completed += 1
                        else:
                            self.file_statuses[file_path] = FileStatus.FAILED
                            self.errors[file_path] = result.get('error', 'Unknown error')
                            # Stop on failure (as per requirements)
                            self.status = JobStatus.FAILED
                            self.cancelled = True
                            break
                        
                        self.progress = completed / total_files
                
                except Exception as e:
                    logger.error(f"Error processing {file_path}: {e}", exc_info=True)
                    with self.lock:
                        self.file_statuses[file_path] = FileStatus.FAILED
                        self.errors[file_path] = str(e)
                        self.status = JobStatus.FAILED
                        self.cancelled = True
                    break
            
            if not self.cancelled:
                self.status = JobStatus.COMPLETED
                self.progress = 1.0
            
            self.end_time = time.time()
            logger.info(f"Job {self.job_id} completed: {self.status.value}")
        
        except Exception as e:
            logger.error(f"Job {self.job_id} failed: {e}", exc_info=True)
            self.status = JobStatus.FAILED
            self.end_time = time.time()
    
    def cancel(self):
        """Cancel running conversion"""
        if self.status in (JobStatus.PROCESSING, JobStatus.PENDING):
            self.cancelled = True
            self.status = JobStatus.CANCELLED
            logger.info(f"Job {self.job_id} cancelled")
    
    def get_status(self) -> Dict:
        """Get current job status"""
        with self.lock:
            file_statuses = {
                path: status.value for path, status in self.file_statuses.items()
            }
            
            return {
                'job_id': self.job_id,
                'status': self.status.value,
                'progress': round(self.progress * 100, 2),
                'total_files': len(self.files),
                'completed_files': sum(1 for s in self.file_statuses.values() if s == FileStatus.COMPLETED),
                'failed_files': sum(1 for s in self.file_statuses.values() if s == FileStatus.FAILED),
                'file_statuses': file_statuses,
                'results': self.results,
                'errors': self.errors,
                'start_time': self.start_time,
                'end_time': self.end_time,
                'elapsed_time': round((self.end_time or time.time()) - (self.start_time or time.time()), 2) if self.start_time else 0
            }


class JobManager:
    """Manages all conversion jobs"""
    
    def __init__(self):
        self.jobs: Dict[str, ConversionJob] = {}
        self.lock = threading.Lock()
    
    def create_job(self, files: List[Dict], settings: Dict) -> str:
        """Create a new conversion job"""
        job_id = str(uuid.uuid4())
        job = ConversionJob(job_id, files, settings)
        
        with self.lock:
            self.jobs[job_id] = job
        
        return job_id
    
    def get_job(self, job_id: str) -> Optional[ConversionJob]:
        """Get job by ID"""
        with self.lock:
            return self.jobs.get(job_id)
    
    def cancel_job(self, job_id: str) -> bool:
        """Cancel a job"""
        job = self.get_job(job_id)
        if job:
            job.cancel()
            return True
        return False
    
    def cleanup_old_jobs(self, max_age_seconds: int = 3600):
        """Remove old completed/failed jobs"""
        current_time = time.time()
        with self.lock:
            to_remove = []
            for job_id, job in self.jobs.items():
                if job.end_time and (current_time - job.end_time) > max_age_seconds:
                    to_remove.append(job_id)
            
            for job_id in to_remove:
                del self.jobs[job_id]
                logger.debug(f"Cleaned up old job: {job_id}")


# Global job manager instance
job_manager = JobManager()






