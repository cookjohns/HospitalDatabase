drop table if exists Room;

CREATE TABLE Room (
   roomNumber integer,
   employeeID integer,
   roomDescription varchar(30),
   PRIMARY KEY (roomNumber),
   FOREIGN KEY (employeeID) REFERENCES Worker (employeeID)
);
