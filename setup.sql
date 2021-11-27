CREATE DATABASE vend;
USE vend;

CREATE TABLE LOCATIONS(
    ID INT AUTO_INCREMENT PRIMARY KEY,
    DESCRIPTION VARCHAR(100) NOT NULL,
    LATITUDE DOUBLE NOT NULL,
    LONGITUDE DOUBLE NOT NULL
);

CREATE TABLE MACHINES(
    ID INT AUTO_INCREMENT PRIMARY KEY,
    LOCATIONID INT NOT NULL,
    SPECIFICLOCATION VARCHAR(45) NOT NULL,
    FOREIGN KEY (LOCATIONID) REFERENCES LOCATIONS(ID)
);

CREATE TABLE ITEMS(
    ID INT AUTO_INCREMENT PRIMARY KEY,
    NAME VARCHAR(45) NOT NULL,
    DESCRIPTION VARCHAR(100) NOT NULL
);

CREATE TABLE STOCKED_ITEMS(
    ID INT AUTO_INCREMENT PRIMARY KEY,
    MACHINEID INT NOT NULL,
    ITEMID INT NOT NULL,
    TIMESTAMP TIMESTAMP(6) NOT NULL,
    CERTAINTY INT NOT NULL,
    TAG VARCHAR(30) NOT NULL,
    FOREIGN KEY (ITEMID) REFERENCES ITEMS(ID),
    FOREIGN KEY (MACHINEID) REFERENCES MACHINES(ID)
);