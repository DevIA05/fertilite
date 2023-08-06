CREATE DATABASE mydatabase;
USE mydatabase;

CREATE TABLE fertilite (
    Season VARCHAR(255),
    Age INT,
    Childish_diseases VARCHAR(255),
    Accident_or_serious_trauma VARCHAR(255),
    Surgical_intervention VARCHAR(255),
    High_fevers_in_the_last_year VARCHAR(255),
    Frequency_of_alcohol_consumption VARCHAR(255),
    Smoking_habit VARCHAR(255),
    Number_of_hours_spent_sitting_per_day INT,
    Diagnosis VARCHAR(255)
);

LOAD DATA INFILE '/var/lib/mysql-files/fertility.csv'
INTO TABLE mydatabase.fertilite
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

