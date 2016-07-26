drop table if exists Administers; 

CREATE TABLE Administers (
   timeAdministered datetime NOT NULL,
   treatmentGiverID integer,
   treatmentID integer,
   patientID integer,
   PRIMARY KEY (treatmentID, treatmentGiverID, patientID),
   FOREIGN KEY (treatmentGiverID) REFERENCES TreatmentGiver(treatmentGiverID),
   FOREIGN KEY (patientID) REFERENCES Patient(patientID),
   FOREIGN KEY (treatmentID) REFERENCES Treatment(treatmentID)
);
