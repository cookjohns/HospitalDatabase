drop table if exists TreatmentGiver; 

CREATE TABLE TreatmentGiver (   
   employeeID serial,   
   FOREIGN KEY (employeeID) REFERENCES Worker (employeeID)
);
