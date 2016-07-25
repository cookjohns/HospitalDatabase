drop table if exists Technician;

CREATE TABLE Technician (
	employeeId integer,
	PRIMARY KEY (employeeID),
	FOREIGN KEY (employeeID) REFERENCES Worker.employeeID
);
