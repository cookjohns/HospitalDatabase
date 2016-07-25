drop table if exists Doctor;

CREATE TABLE Doctor (
	employeeID integer,
	consultingPrivilege byte,
	PRIMARY KEY (employeeID),
	FOREIGN KEY (employeeID) REFERENCES Worker.employeeID
);
