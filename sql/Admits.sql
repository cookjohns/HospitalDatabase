drop table if exists Admits; 

CREATE TABLE Admits (
   employeeID integer,
   patientID integer,
   timeAdmitted datetime,
   PRIMARY KEY (patientID, employeeID),
   FOREIGN KEY (employeeID) REFERENCES Worker (employeeID),
   FOREIGN KEY (patientID) REFERENCES Patient (patientID)
);
