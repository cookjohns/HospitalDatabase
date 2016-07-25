drop table if exists Administers; 

CREATE TABLE Administers (
   timeAdministered datetime,
   treatmentGiverID integer,
   patientID integer,
   PRIMARY KEY (timeAdministered, treatmentGiverID),
   FOREIGN KEY (treatmentGiverID) REFERENCES TreatmentGiver(treatmentGiverID),
   FOREIGN KEY (patientID) REFERENCES Patient(patientID)
);
