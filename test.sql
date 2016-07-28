select roomNumber, firstName, lastName, timeAdmitted, patientID
from (admits as a join patientroom using(patientID)) join patient using (patientID)
where A.timeAdmitted > (select max(date)
   from discharges as c
   where a.patientID = c.patientID);
