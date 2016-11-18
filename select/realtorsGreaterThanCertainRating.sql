SELECT R.r_realtorKey,compiledRVs.avgRating
FROM Realtor as R,(SELECT avg(rv_rating) as avgRating,rv_realtorKey 
                    FROM Reviews GROUP BY rv_realtorKey) as compiledRVs
WHERE R.r_realtorKey = compiledRVs.rv_realtorkey
AND compiledRVs.avgRating > 3.0
