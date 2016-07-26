drop table if exists AssignedTo;

CREATE TABLE AssignedTo (
   doctorID integer,
   patientID integer,
   FOREIGN KEY (doctorID) references Doctor (employeeID),
   FOREIGN KEY (patientID) references Admits (patientID),
   PRIMARY KEY (doctorID, patientID)
);
