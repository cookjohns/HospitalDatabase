drop table if exists Room;

CREATE TABLE Room (
   roomNumber integer,
   roomDescription varchar(30),
   volunteerRoom bit,
   PRIMARY KEY (roomNumber),
   FOREIGN KEY (employeeID) REFERENCES Worker (employeeID)
);
