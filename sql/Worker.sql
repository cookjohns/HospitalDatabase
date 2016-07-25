drop table if exists Worker;

CREATE TABLE Worker (
	employeeID integer,
	firstName varchar(20) NOT NULL,
	lastName varchar(20) NOT NULL,
	salary integer NOT NULL,
	hireDate datetime NOT NULL,
	PRIMARY KEY (employeeID)
);
