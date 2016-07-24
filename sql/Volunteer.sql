CREATE TABLE Volunteer (
	employeeId integer,
	PRIMARY KEY (employeeId),
	FOREIGN KEY (employeeId) REFERENCES Worker.employeeId
);