drop table if exists TreatmentGiver; 

create table TreatmentGiver (   
   employeeID serial,   
   FOREIGN KEY (employeeID) REFERENCES Worker (employeeID)
);