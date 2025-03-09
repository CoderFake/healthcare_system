import sys
import os
from pathlib import Path

parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from database.db_manager import DatabaseManager

def main():
    if len(sys.argv) < 2:
        print("Error: Backup file path is required")
        print(__doc__)
        sys.exit(1)
    
    backup_path = sys.argv[1]
    
    if not Path(backup_path).exists():
        print(f"Error: Backup file not found: {backup_path}")
        sys.exit(1)
    
    print(f"Warning: This will overwrite the current database with {backup_path}")
    confirm = input("Are you sure you want to continue? (y/N): ")
    
    if confirm.lower() != 'y':
        print("Restore cancelled.")
        sys.exit(0)
    
    try:
        db_manager = DatabaseManager()
        db_manager.restore(backup_path)
        print(f"Database successfully restored from: {backup_path}")
    except Exception as e:
        print(f"Error restoring database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()