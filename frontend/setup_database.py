#!/usr/bin/env python3
"""
Database Setup Script for Alumni Management Platform
This script creates the PostgreSQL database and sets up the initial configuration.
"""

import os
import sys
import subprocess
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def check_postgresql_connection():
    """Check if PostgreSQL is running and accessible"""
    try:
        # Try to connect to the default postgres database
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="postgres",
            user="postgres"
        )
        conn.close()
        print("✅ PostgreSQL connection successful")
        return True
    except psycopg2.OperationalError as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False

def create_database():
    """Create the alumni_platform database"""
    try:
        # Connect to postgres database
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="postgres",
            user="postgres"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'alumni_platform'")
        exists = cursor.fetchone()
        
        if exists:
            print("✅ Database 'alumni_platform' already exists")
        else:
            # Create database
            cursor.execute("CREATE DATABASE alumni_platform")
            print("✅ Database 'alumni_platform' created successfully")
        
        # Create extensions
        cursor.execute("""
            CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
            CREATE EXTENSION IF NOT EXISTS "pg_trgm";
            CREATE EXTENSION IF NOT EXISTS "unaccent";
        """)
        print("✅ PostgreSQL extensions created")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Error creating database: {e}")
        return False

def test_database_connection():
    """Test connection to the new database"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="alumni_platform",
            user="postgres"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ Connected to alumni_platform database: {version[0]}")
        cursor.close()
        conn.close()
        return True
    except psycopg2.Error as e:
        print(f"❌ Error connecting to alumni_platform database: {e}")
        return False

def install_requirements():
    """Install required Python packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "psycopg2-binary"])
        print("✅ psycopg2-binary installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing psycopg2-binary: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Alumni Management Platform Database...")
    print("=" * 50)
    
    # Install requirements
    print("\n1. Installing required packages...")
    if not install_requirements():
        print("❌ Failed to install requirements")
        return False
    
    # Check PostgreSQL connection
    print("\n2. Checking PostgreSQL connection...")
    if not check_postgresql_connection():
        print("❌ PostgreSQL is not running or not accessible")
        print("Please start PostgreSQL service:")
        print("  sudo systemctl start postgresql")
        print("  sudo systemctl enable postgresql")
        return False
    
    # Create database
    print("\n3. Creating database...")
    if not create_database():
        print("❌ Failed to create database")
        return False
    
    # Test database connection
    print("\n4. Testing database connection...")
    if not test_database_connection():
        print("❌ Failed to connect to new database")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Database setup completed successfully!")
    print("\nNext steps:")
    print("1. cd backend")
    print("2. python manage.py migrate")
    print("3. python manage.py createsuperuser")
    print("4. python manage.py runserver")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
