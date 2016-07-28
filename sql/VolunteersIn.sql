drop table if exists VolunteersIn; 

CREATE TABLE VolunteersIn (
   employeeID integer,
   roomNumber integer,
   dayOfWeek varchar(10),
   PRIMARY KEY (employeeID, roomNumber),
   FOREIGN KEY (employeeID) REFERENCES Volunteer (employeeID),
   FOREIGN KEY (roomNumber) REFERENCES Room (roomNumber)
);
