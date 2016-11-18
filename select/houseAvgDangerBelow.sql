SELECT *
  FROM House as H
  WHERE 3 > (SELECT avg(dangerLevel) 
              FROM CrimeRating as CR 
              WHERE CR.c_location = H.h_location);
