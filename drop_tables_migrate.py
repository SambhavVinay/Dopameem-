#!/usr/bin/env python3
"""
Alternative script to drop all tables using Flask-Migrate commands.
This approach works with your existing migration setup.
"""

import os
import subprocess
import sys

def run_flask_command(command):
    """Run a Flask command and return the result"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            cwd=os.getcwd()
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def drop_tables_with_migrate():
    """Drop tables using Flask-Migrate downgrade"""
    print("🚀 Dropping Tables Using Flask-Migrate")
    print("=" * 40)
    
    # Check if flask is available
    success, stdout, stderr = run_flask_command("flask --version")
    if not success:
        print("❌ Flask CLI not available. Make sure Flask is installed.")
        return False
    
    print("📋 Current migration status:")
    success, stdout, stderr = run_flask_command("flask db current")
    if success:
        print(f"Current revision: {stdout.strip()}")
    else:
        print("⚠️  Could not determine current migration status")
    
    # Show migration history
    print("\n📜 Migration history:")
    success, stdout, stderr = run_flask_command("flask db history")
    if success:
        print(stdout)
    
    # Ask user for confirmation
    response = input("\n⚠️  Do you want to downgrade to base (drop all tables)? (y/n): ").lower()
    if response not in ['y', 'yes']:
        print("❌ Operation cancelled.")
        return False
    
    # Downgrade to base (this will drop all tables)
    print("\n🔥 Downgrading to base (dropping all tables)...")
    success, stdout, stderr = run_flask_command("flask db downgrade base")
    
    if success:
        print("✅ Successfully dropped all tables!")
        print(stdout)
        
        # Ask if user wants to delete migration files
        delete_migrations = input("\n🗑️  Do you want to delete all migration files? (y/n): ").lower()
        if delete_migrations in ['y', 'yes']:
            import shutil
            migrations_dir = os.path.join(os.getcwd(), "migrations", "versions")
            if os.path.exists(migrations_dir):
                try:
                    # Remove all migration files
                    for filename in os.listdir(migrations_dir):
                        file_path = os.path.join(migrations_dir, filename)
                        if os.path.isfile(file_path) and filename.endswith('.py'):
                            os.remove(file_path)
                            print(f"🗑️  Deleted: {filename}")
                    
                    print("✅ All migration files deleted!")
                    print("\n💡 To start fresh:")
                    print("   flask db migrate -m 'Initial migration'")
                    print("   flask db upgrade")
                except Exception as e:
                    print(f"❌ Error deleting migration files: {e}")
        
        return True
    else:
        print("❌ Error dropping tables:")
        print(stderr)
        return False

def show_manual_sql():
    """Show manual SQL commands to drop tables"""
    print("\n" + "=" * 50)
    print("🛠️  MANUAL SQL COMMANDS TO DROP TABLES")
    print("=" * 50)
    
    print("\nIf the migration approach doesn't work, you can manually run these SQL commands:")
    print("(Connect to your database using psql, pgAdmin, or your preferred SQL client)\n")
    
    # Based on the models in app.py, here are the tables in dependency order
    sql_commands = [
        "-- Drop tables in reverse dependency order to avoid foreign key constraints",
        "DROP TABLE IF EXISTS alembic_version CASCADE;",
        "DROP TABLE IF EXISTS dops_comments CASCADE;",
        "DROP TABLE IF EXISTS comments CASCADE;", 
        "DROP TABLE IF EXISTS requests CASCADE;",
        "DROP TABLE IF EXISTS followers CASCADE;",
        "DROP TABLE IF EXISTS posts CASCADE;",
        "DROP TABLE IF EXISTS dops CASCADE;",
        "DROP TABLE IF EXISTS gooners CASCADE;",
        "",
        "-- Alternative: Drop all tables at once (if foreign key checks are disabled)",
        "-- DROP SCHEMA public CASCADE;",
        "-- CREATE SCHEMA public;",
        "-- GRANT ALL ON SCHEMA public TO postgres;",
        "-- GRANT ALL ON SCHEMA public TO public;",
    ]
    
    for command in sql_commands:
        print(command)
    
    print("\n💡 After dropping tables manually:")
    print("   flask db stamp head  # Mark current migration as applied")
    print("   flask db downgrade base  # Reset migration state") 
    print("   flask db upgrade  # Recreate tables from migrations")

if __name__ == "__main__":
    # Try the migration approach first
    if not drop_tables_with_migrate():
        # If that fails, show manual SQL commands
        show_manual_sql()
    
    print("\n🎉 Script completed!")
