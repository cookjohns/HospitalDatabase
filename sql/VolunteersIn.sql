drop table if exists VolunteersIn; 

CREATE TABLE VolunteersIn (
   employeeID integer,
   roomNumber integer
   PRIMARY KEY (employeeID, roomNumber),
   FOREIGN KEY (employeeID) REFERENCES Staff (employeeID),
   FOREIGN KEY (roomNumber) REFERENCES Room (roomNumber)
);
