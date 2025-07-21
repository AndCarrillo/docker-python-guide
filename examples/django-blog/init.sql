-- Initialize the database with sample data
-- This script runs when the PostgreSQL container starts for the first time

-- Create additional database if needed
-- CREATE DATABASE blogdb_test;

-- Set up initial user permissions
GRANT ALL PRIVILEGES ON DATABASE blogdb TO bloguser;

-- You can add more initialization SQL here
-- For example, creating additional schemas, functions, etc.
