#!/usr/bin/env python3
"""
Script to drop all tables from the Goongram database.
This will permanently delete all data in the database.
"""

import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app():
    """Create Flask app with database configuration"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app

def drop_all_tables():
    """Drop all tables from the database"""
    app = create_app()
    db = SQLAlchemy(app)
    
    with app.app_context():
        try:
            print("🗑️  Starting to drop all tables...")
            
            # Get all table names
            inspector = db.inspect(db.engine)
            table_names = inspector.get_table_names()
            
            if not table_names:
                print("✅ No tables found in database.")
                return
            
            print(f"📋 Found {len(table_names)} tables: {', '.join(table_names)}")
            
            # Confirm before proceeding
            response = input("\n⚠️  WARNING: This will permanently delete ALL data in the database.\nType 'YES' to continue: ")
            
            if response != 'YES':
                print("❌ Operation cancelled.")
                return
            
            # Drop all tables
            print("\n🔥 Dropping all tables...")
            db.drop_all()
            
            # Verify tables are dropped
            inspector = db.inspect(db.engine)
            remaining_tables = inspector.get_table_names()
            
            if not remaining_tables:
                print("✅ All tables have been successfully dropped!")
                print("💡 You can recreate the tables by running: flask db upgrade")
            else:
                print(f"⚠️  Some tables still exist: {', '.join(remaining_tables)}")
                
        except Exception as e:
            print(f"❌ Error dropping tables: {e}")
            return False
    
    return True

def drop_migration_versions():
    """Drop the alembic version table to reset migrations"""
    app = create_app()
    db = SQLAlchemy(app)
    
    with app.app_context():
        try:
            # Drop alembic version table if it exists
            db.engine.execute("DROP TABLE IF EXISTS alembic_version")
            print("✅ Migration version table dropped.")
        except Exception as e:
            print(f"ℹ️  Migration version table cleanup: {e}")

if __name__ == "__main__":
    print("🚀 Goongram Database Table Dropper")
    print("=" * 40)
    
    # Check if DATABASE_URL is set
    if not os.getenv("DATABASE_URL"):
        print("❌ DATABASE_URL environment variable not found!")
        print("   Make sure your .env file contains DATABASE_URL")
        sys.exit(1)
    
    # Drop all tables
    if drop_all_tables():
        # Ask if user wants to also reset migrations
        reset_migrations = input("\n🔄 Do you want to reset migrations as well? (y/n): ").lower()
        if reset_migrations in ['y', 'yes']:
            drop_migration_versions()
            print("💡 To reinitialize migrations, run:")
            print("   flask db init")
            print("   flask db migrate -m 'initial migration'")
            print("   flask db upgrade")
        else:
            print("💡 Migrations left intact. Run 'flask db upgrade' to recreate tables.")
    
    print("\n🎉 Script completed!")
