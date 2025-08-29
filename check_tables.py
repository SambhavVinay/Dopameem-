#!/usr/bin/env python3
"""
Script to check the current status of database tables.
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_database_tables():
    """Check what tables currently exist in the database"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    
    with app.app_context():
        try:
            print("🔍 Checking database table status...")
            
            # Get database engine inspector
            inspector = db.inspect(db.engine)
            table_names = inspector.get_table_names()
            
            if not table_names:
                print("✅ SUCCESS: No tables found in database - all tables have been dropped!")
                return True
            else:
                print(f"📋 Found {len(table_names)} tables still in database:")
                for i, table in enumerate(table_names, 1):
                    print(f"   {i}. {table}")
                
                print("\n❌ Tables still exist - they have NOT been dropped yet.")
                print("\nTo drop these tables, you need to:")
                print("1. Connect to your database directly (using pgAdmin, psql, or your hosting dashboard)")
                print("2. Run the SQL commands I provided earlier")
                return False
                
        except Exception as e:
            print(f"❌ Could not connect to database: {e}")
            print("\nThis could mean:")
            print("1. Database is not accessible from your local machine")
            print("2. Database credentials are not set up")
            print("3. Database server is down or unreachable")
            print("\nYou'll need to check your database status through your hosting provider.")
            return None

if __name__ == "__main__":
    print("🚀 Database Table Status Checker")
    print("=" * 40)
    
    if not os.getenv("DATABASE_URL"):
        print("❌ DATABASE_URL environment variable not found!")
        print("   Create a .env file with DATABASE_URL=your_database_connection_string")
    else:
        check_database_tables()
