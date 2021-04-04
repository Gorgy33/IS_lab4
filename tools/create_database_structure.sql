CREATE TYPE "ROLES" AS ENUM (
    'ADMIN',
    'USER'
);

CREATE TABLE "users" (
  "id" SERIAL UNIQUE,
  "password_hash" VARCHAR,
  "login" VARCHAR,
  "role" "ROLES",
  "nickname" VARCHAR
);

CREATE TABLE "common" (
    "field" VARCHAR,
    "value" VARCHAR
);

INSERT INTO common VALUES ('SECRET_KEY', 'SECRET KEY');

CREATE TABLE "notes" (
  "id" SERIAL UNIQUE,
  "text" VARCHAR,
  "author" VARCHAR
);
