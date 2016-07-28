drop table if exists WorksIn; 

CREATE TABLE WorksIn (
   employeeID integer,
   roomNumber integer,
   PRIMARY KEY (employeeID, roomNumber),
   FOREIGN KEY (employeeID) REFERENCES Volunteer (employeeID),
   FOREIGN KEY (roomNumber) REFERENCES Room (roomNumber)
);
