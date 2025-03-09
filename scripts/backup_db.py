import sys
import os
from pathlib import Path
from datetime import datetime

parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from database.db_manager import DatabaseManager

def main():
    if len(sys.argv) > 1:
        backup_path = sys.argv[1]
    else:
        backup_dir = Path('backups')
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        backup_path = backup_dir / f"backup_{timestamp}.db"

    db_manager = DatabaseManager()
    backup_file = db_manager.backup(str(backup_path))
    
    print(f"Database successfully backed up to: {backup_file}")

if __name__ == "__main__":
    main()