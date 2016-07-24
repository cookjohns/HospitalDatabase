CREATE TABLE Admin (
	employeeId integer,
	PRIMARY KEY (employeeId),
	FOREIGN KEY (employeeId) REFERENCES Worker.employeeId
);