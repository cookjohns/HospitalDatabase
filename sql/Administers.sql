drop table if exists Administers; 

create table Administers (
   timeAdministered datetime,
   adminID integer,
   PRIMARY KEY (timeAdministered, adminID),
   FOREIGN KEY (employeeID) REFERENCES Worker (employeeID)
);

