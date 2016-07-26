drop table if exists Admin;

CREATE TABLE Admin (
	employeeID integer,
	PRIMARY KEY (employeeID),
	FOREIGN KEY (employeeID) REFERENCES Worker(employeeID)
);
