drop table if exists Doctor;

CREATE TABLE Doctor (
	employeeId integer,
	consultingPrivilege byte,
	PRIMARY KEY (employeeId),
	FOREIGN KEY (employeeId) REFERENCES Worker.employeeId
);
