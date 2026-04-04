import os
import psutil

class USBDetector:
    """Detects removable USB drives on Windows systems."""
    
    def __init__(self):
        self.previous_drives = set()

    def get_removable_drives(self):
        """Returns a list of drive letters for removable storage."""
        removable_drives = []
        for partition in psutil.disk_partitions():
            # On Windows, 'removable' is usually the indicator
            if 'removable' in partition.opts or partition.fstype == '':
                # We check if the path exists to avoid ghost drives
                if os.path.exists(partition.mountpoint):
                    removable_drives.append(partition.mountpoint)
        return removable_drives

    def detect_changes(self):
        """Returns (added_drives, removed_drives)"""
        current_drives = set(self.get_removable_drives())
        added = current_drives - self.previous_drives
        removed = self.previous_drives - current_drives
        self.previous_drives = current_drives
        return list(added), list(removed)
