DROP TABLE IF EXISTS users;



CREATE TABLE divar_raw(id VARCHAR(255),widgets VARCHAR,timestr VARCHAR);

CREATE TABLE divar_widget(id VARCHAR(255),token VARCHAR,creation_date VARCHAR);

CREATE TABLE divar_detail(id VARCHAR(255),title VARCHAR,type VARCHAR,text VARCHAR,geog geography(POINT,4326),detail_title VARCHAR); 

CREATE TABLE users(
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    user_email VARCHAR(255) UNIQUE NOT NULL,
    user_first_name VARCHAR(20) NOT NULL,
    user_last_name VARCHAR(20) NOT NULL,
    user_birthdate DATE NOT NULL,
    created_on TIMESTAMP NOT NULL,
    last_update TIMESTAMP
);

INSERT INTO users(
    username,
    user_email,
    user_first_name,
    user_last_name,
    user_birthdate,
    created_on,
    last_update
)
VALUES 
    ('cwenga','cwenga@carml.ai','carmel','wenga','1990-09-20',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP),
    ('smenguope','smenguope@carml.ai','suzie','menguope','1992-11-13',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP),
    ('cdiogni','cdiogni@carml.ai','christian','diogni','1992-10-13',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)