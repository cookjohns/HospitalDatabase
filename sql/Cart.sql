drop table if exists Cart;

CREATE TABLE Cart (
   cartNumber integer,
   employeeID integer,
   cartDescription varchar(30),
   volunteerCart bit,
   PRIMARY KEY (cartNumber),
   FOREIGN KEY (employeeID) REFERENCES Worker (employeeID)
);
