drop table if exists Orders;

CREATE TABLE Orders (
   doctorID integer,
   patientID integer,
   treatmentGiverID,
   treatmentID,
   date datetime NOT NULL,
   FOREIGN KEY (doctorID, patientID) references AssignedTo (doctorID, patientID),
   FOREIGN KEY (treatmentGiverID, treatmentID) 
      references Administers (treamentGiverID, treatmentID),
   PRIMARY KEY (doctorID, patientID, treatmentID, treatmentGiverID)
);
