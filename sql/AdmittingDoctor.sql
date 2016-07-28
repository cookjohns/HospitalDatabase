drop table if exists AdmittingDoctor;

CREATE TABLE AdmittingDoctor (
   employeeID integer,
   FOREIGN KEY (employeeID) REFERENCES Doctor (employeeID),
   PRIMARY KEY (employeeID)
);
