/****** Script for SelectTopNRows command from SSMS  ******/
-- Find duplicate BCNo values
SELECT BCNo, COUNT(*) AS DuplicateCount
FROM PatientIDnReg
GROUP BY BCNo
HAVING COUNT(*) > 1
ORDER BY DuplicateCount DESC;


