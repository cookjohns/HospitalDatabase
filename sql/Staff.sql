drop table if exists Staff;

CREATE TABLE Staff (
	employeeID integer,
	PRIMARY KEY (employeeID),
	FOREIGN KEY (employeeID) REFERENCES Worker(employeeID)
);
