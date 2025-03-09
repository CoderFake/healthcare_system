import sys
import os
from pathlib import Path
from datetime import datetime

parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from database.db_setup import DatabaseSetup

def main():
    if len(sys.argv) < 2:
        print("Error: Migration name is required")
        print(__doc__)
        sys.exit(1)
    
    migration_name = sys.argv[1]
    db_setup = DatabaseSetup()
    migration_path = db_setup.create_migration(migration_name)
    
    print(f"Migration created: {migration_path}")
    print("Edit the file to add your database changes.")

if __name__ == "__main__":
    main()