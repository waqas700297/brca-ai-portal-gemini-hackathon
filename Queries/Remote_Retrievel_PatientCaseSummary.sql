WITH BasePatient AS (
    SELECT p.*,
           ROW_NUMBER() OVER (PARTITION BY BCNo ORDER BY CreationDate DESC) AS rn
    FROM PatientIDnReg p
),
LatestFollowUp AS (
    SELECT BCNo,
           Convert(varchar(10), FollowUpDate, 103) AS FollowUpDate,
           DiseaseStatus, FollowUpNo, TimeBWRegAndLastFollowUp,
           ROW_NUMBER() OVER (PARTITION BY BCNo ORDER BY FollowUpNo DESC, CreationDate DESC) AS rn
    FROM vwFollowUp
),
LatestInvestigations AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY BCNo ORDER BY FollowUpNo DESC, CreationDate DESC) AS rn
    FROM Investigations
),
LatestSurgery AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY BCNo ORDER BY CreationDate DESC) AS rn
    FROM Surgery
),
LatestDiagnosis AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY BCNo ORDER BY CreationDate DESC) AS rn
    FROM ClinicalDiagnosis
),
LatestExam AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY BCNo ORDER BY CreationDate DESC) AS rn
    FROM Examination
),
LatestChemo AS (
    SELECT BCNo,
           EpisodeNo AS ChemoEpisodeNo, TreatmentType AS ChemoTreatmentType,
           CONVERT(varchar(10), DateOfStart, 101) AS ChemoDateOfStart,
           CONVERT(varchar(10), DateOfEnd, 101) AS ChemoDateOfEnd,
           AdverseEvents AS ChemoAdverseEvents, Regimen AS ChemoRegimen,
           FollowedWith AS ChemoFollowedWith, TherapyCompleted AS ChemoTherapyCompleted,
           ROW_NUMBER() OVER (PARTITION BY BCNo ORDER BY CreationDate DESC, EpisodeNo DESC) AS rn
    FROM ChemoTherapy
),
LatestRadio AS (
    SELECT BCNo,
           EpisodeNo AS RadioEpisodeNo, TreatmentType AS RadioTreatmentType,
           CONVERT(varchar(10), DateOfStart, 101) AS RadioDateOfStart,
           CONVERT(varchar(10), DateOfEnd, 101) AS RadioDateOfEnd,
           AdverseEvents AS RadioAdverseEvents, FollowedWith AS RadioFollowedWith,
           TherapyCompleted AS RadioTherapyCompleted,
           ROW_NUMBER() OVER (PARTITION BY BCNo ORDER BY CreationDate DESC, EpisodeNo DESC) AS rn
    FROM RadioTherapy
),
LatestHormonal AS (
    SELECT BCNo,
           EpisodeNo AS HormonalEpisodeNo, TreatmentType AS HormonalTreatmentType,
           CONVERT(varchar(10), DateOfStart, 101) AS HormonalDateOfStart,
           CONVERT(varchar(10), DateOfEnd, 101) AS HormonalDateOfEnd,
           AdverseEvents AS HormonalAdverseEvents, Regimen AS HormonalRegimen,
           FollowedWith AS HormonalFollowedWith, TherapyCompleted AS HormonalTherapyCompleted,
           ROW_NUMBER() OVER (PARTITION BY BCNo ORDER BY CreationDate DESC, EpisodeNo DESC) AS rn
    FROM HormonalTherapy
),
LatestTargeted AS (
    SELECT BCNo,
           EpisodeNo AS TargetedEpisodeNo, TreatmentType AS TargetedTreatmentType,
           CONVERT(varchar(10), DateOfStart, 101) AS TargetedDateOfStart,
           CONVERT(varchar(10), DateOfEnd, 101) AS TargetedDateOfEnd,
           AdverseEvents AS TargetedAdverseEvents, Regimen AS TargetedRegimen,
           FollowedWith AS TargetedFollowedWith, TherapyCompleted AS TargetedTherapyCompleted,
           ROW_NUMBER() OVER (PARTITION BY BCNo ORDER BY CreationDate DESC, EpisodeNo DESC) AS rn
    FROM TargetedTherapy
)
SELECT 
    p.PatientName, p.Gender, p.Age,
    CONVERT(varchar(10), p.Date_of_Registration, 103) AS Date_of_Registration,
    p.Age_at_Diagnosis,

    f.FollowUpDate, f.DiseaseStatus, f.FollowUpNo, f.TimeBWRegAndLastFollowUp,
    i.*, s.*, cd.*, e.*,
    c.ChemoEpisodeNo, c.ChemoTreatmentType, c.ChemoDateOfStart, c.ChemoDateOfEnd,
    c.ChemoAdverseEvents, c.ChemoRegimen, c.ChemoFollowedWith, c.ChemoTherapyCompleted,
    r.RadioEpisodeNo, r.RadioTreatmentType, r.RadioDateOfStart, r.RadioDateOfEnd,
    r.RadioAdverseEvents, r.RadioFollowedWith, r.RadioTherapyCompleted,
    h.HormonalEpisodeNo, h.HormonalTreatmentType, h.HormonalDateOfStart, h.HormonalDateOfEnd,
    h.HormonalAdverseEvents, h.HormonalRegimen, h.HormonalFollowedWith, h.HormonalTherapyCompleted,
    t.TargetedEpisodeNo, t.TargetedTreatmentType, t.TargetedDateOfStart, t.TargetedDateOfEnd,
    t.TargetedAdverseEvents, t.TargetedRegimen, t.TargetedFollowedWith, t.TargetedTherapyCompleted

FROM BasePatient p
LEFT JOIN LatestFollowUp f ON p.BCNo = f.BCNo AND f.rn = 1
LEFT JOIN LatestInvestigations i ON p.BCNo = i.BCNo AND i.rn = 1
LEFT JOIN LatestSurgery s ON p.BCNo = s.BCNo AND s.rn = 1
LEFT JOIN LatestDiagnosis cd ON p.BCNo = cd.BCNo AND cd.rn = 1
LEFT JOIN LatestExam e ON p.BCNo = e.BCNo AND e.rn = 1
LEFT JOIN LatestChemo c ON p.BCNo = c.BCNo AND c.rn = 1
LEFT JOIN LatestRadio r ON p.BCNo = r.BCNo AND r.rn = 1
LEFT JOIN LatestHormonal h ON p.BCNo = h.BCNo AND h.rn = 1
LEFT JOIN LatestTargeted t ON p.BCNo = t.BCNo AND t.rn = 1
WHERE p.rn = 1
  AND p.BCNo IN (SELECT DISTINCT BCNo from PatientIDnReg)
ORDER BY f.FollowUpNo DESC, p.CreationDate DESC;