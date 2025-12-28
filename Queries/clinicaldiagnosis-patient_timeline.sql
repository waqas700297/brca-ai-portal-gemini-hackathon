WITH LatestVisit AS (
    SELECT 
        BCNo, 
        MAX(CreationDate) AS MaxCreationDate
    FROM 
        dbo.ClinicalDiagnosis
    --WHERE 
    --    isFollowUp IS NOT NULL 
    --    AND VisitNo IS NOT NULL
    GROUP BY 
        BCNo, VisitNo
)
SELECT 
    CD.BCNo, 
    CD.isFollowUp, 
    CD.CaBrFNAC, 
    CD.VisitNo, 
    CD.FirstClinicalDiagnosiis, 
    CD.FirstDiagnosisDate, 
    CD.FinalClinicalDiagnosis, 
    CD.FinalDiagnosisDate, 
    CD.FinalHistopathologicalDiagnosis, 
    CD.FinalHistoDiagnosisDate, 
    CD.PostingDate, 
    CD.DiseaseRecurred, 
    CD.DiseaseStatus, 
    CD.Comments, 
    CD.CreationDate, 
    CD.UserID, 
    CD.UserIP, 
    CD.CurrentTNM, 
    CD.TNMDate, 
    CD.T, 
    CD.N, 
    CD.M, 
    CD.Stage, 
    CD.PregOrLact, 
    CD.MetastatisLocation
FROM 
    dbo.ClinicalDiagnosis CD
INNER JOIN 
    LatestVisit LV
ON 
    CD.BCNo = LV.BCNo 
    AND CD.CreationDate = LV.MaxCreationDate
ORDER BY 
    CD.BCNo, VisitNo ASC;