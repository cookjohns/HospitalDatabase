drop table if exists Administers; 

CREATE TABLE Administers (
   timeAdministered datetime,
   adminID integer,
   PRIMARY KEY (timeAdministered, adminID),
   FOREIGN KEY (employeeID) REFERENCES Worker (employeeID)
);
