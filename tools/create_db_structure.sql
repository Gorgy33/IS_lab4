CREATE TYPE "ROLES" as enum (
    'ADMIN',
    'USER'
    );
CREATE TABLE "users" (
    "id" serial unique,
    "password" varchar,
    "login" varchar,
    "role" "ROLES"
);