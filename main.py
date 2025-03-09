import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from database.db_setup import DatabaseSetup
from views.app import Application

def main():
    db_setup = DatabaseSetup()
    db_setup.setup()
    
    app = Application()
    app.start()

if __name__ == "__main__":
    main()