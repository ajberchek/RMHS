SELECT *
  FROM House as H
  WHERE 3 > (SELECT avg(CR.c_dangerLevel) 
              FROM CrimeRating as CR 
              WHERE CR.c_location = H.h_location);
