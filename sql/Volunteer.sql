drop table if exists Volunteer;

CREATE TABLE Volunteer (
	employeeID integer,
	PRIMARY KEY (employeeID),
	FOREIGN KEY (employeeID) REFERENCES Worker.employeeID
);
