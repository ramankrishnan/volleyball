CREATE DATABASE volleyball_db;
CREATE USER volleyball_user WITH PASSWORD 'volleyball_pass';
GRANT ALL PRIVILEGES ON DATABASE volleyball_db TO volleyball_user;
\c volleyball_db;
GRANT ALL ON SCHEMA public TO volleyball_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO volleyball_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO volleyball_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO volleyball_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO volleyball_user;