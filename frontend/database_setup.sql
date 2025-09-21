-- PostgreSQL Database Setup Script for Alumni Management Platform
-- This script creates the database and user for the project

-- Create database
CREATE DATABASE alumni_platform;

-- Create user (optional, can use default postgres user)
-- CREATE USER alumni_user WITH PASSWORD 'alumni_password';
-- GRANT ALL PRIVILEGES ON DATABASE alumni_platform TO alumni_user;

-- Connect to the database
\c alumni_platform;

-- Create extensions that might be needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "unaccent";

-- Set timezone
SET timezone = 'UTC';

-- Create a schema for the application (optional)
-- CREATE SCHEMA IF NOT EXISTS alumni_schema;
-- SET search_path TO alumni_schema, public;

-- Grant permissions (if using custom user)
-- GRANT ALL ON SCHEMA public TO alumni_user;
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO alumni_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO alumni_user;

-- Display database information
SELECT 
    datname as "Database Name",
    datowner as "Owner",
    encoding as "Encoding",
    datcollate as "Collate",
    datctype as "Ctype"
FROM pg_database 
WHERE datname = 'alumni_platform';

-- Show current database
SELECT current_database(), current_user, version();
