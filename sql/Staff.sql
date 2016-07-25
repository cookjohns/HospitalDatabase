CREATE TABLE Staff (
	employeeId integer,
	PRIMARY KEY (employeeId),
	FOREIGN KEY (employeeId) REFERENCES Worker.employeeId
);