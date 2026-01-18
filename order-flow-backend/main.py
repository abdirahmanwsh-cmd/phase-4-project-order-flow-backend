from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from app import create_app, db
from app.services.seed_admin import seed_admin
from seed_menu import seed_menu

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()   # Create all tables
        seed_admin()      # Seed admin user
        seed_menu()       # Seed menu items
    
    # Get port from environment variable for production (Render uses PORT env var)
    port = int(os.environ.get("PORT", 5555))
    debug = os.environ.get("FLASK_ENV", "development") == "development"
    
    app.run(host="0.0.0.0", debug=debug, port=port)
