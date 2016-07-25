drop table if exists Discharges; 

CREATE TABLE Discharges (
   adminID integer,
   patientID integer NOT NULL,
   date datetime NOT NULL,
   PRIMARY KEY (adminID, patientID),
   FOREIGN KEY (adminID) REFERENCES Admin (employeeID),
   FOREIGN KEY (patientID) REFERENCES Patient (patientID)
);
