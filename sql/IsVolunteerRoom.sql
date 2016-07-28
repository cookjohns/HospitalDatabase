drop table if exists IsVolunteerRoom;

CREATE TABLE IsVolunteerRoom (
   roomDescription varchar(30),
   FOREIGN KEY (roomDescription) REFERENCES Room (roomDescription),
   PRIMARY KEY (roomDescription)
);
