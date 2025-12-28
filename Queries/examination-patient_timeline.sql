WITH LatestExamination AS (
    SELECT 
        BCNo, 
        MAX(CreationDate) AS MaxCreationDate
    FROM 
        dbo.Examination
    --WHERE 
    --    isFollowUp IS NOT NULL 
    --    AND visitNo IS NOT NULL
    GROUP BY 
        BCNo
)
SELECT 
    E.BCNo, 
    E.isFollowUp, 
    E.visitNo, 
    E.Exam_Date, 
    E.IsRightBrLumpMultiCentric, 
    E.IsLeftBrLumpMultiCentric, 
    E.BrLumpRightLargeWidth, 
    E.BrLumpRightLargeHeight, 
    E.BrLumpLeftLargeWidth, 
    E.BrLumpLeftLargeHeight, 
    E.BrLumpRightLargeStatus, 
    E.BrLumpRightLargePosition, 
    E.BrLumpLeftLargeStatus, 
    E.BrLumpLeftLargePosition, 
    E.BrLumpRightSmallWidth, 
    E.BrLumpRightSmallHeight, 
    E.BrLumpLeftSmallWidth, 
    E.BrLumpLeftSmallHeight, 
    E.BrLumpRightSmallStatus, 
    E.BrLumpRightSmallPosition, 
    E.BrLumpLeftSmallStatus, 
    E.BrLumpLeftSmallPosition, 
    E.BrLumpNotes, 
    E.AbdominalFinding, 
    E.AbdominalNotes, 
    E.LymphNodeRightCervicalStatus, 
    E.LymphNodeRightSupraclavicular, 
    E.LymphNodeRightAxillaryStatus, 
    E.LymphNodeRightInguinal, 
    E.LymphNodeLeftCervicalStatus, 
    E.LymphNodeLeftSupraclavicular, 
    E.LymphNodeLeftAxillaryStatus, 
    E.LymphNodeLeftInguinal, 
    E.LympNodeNotes, 
    E.CurrentTNM, 
    E.TNMDate, 
    E.T, 
    E.N, 
    E.M, 
    E.ZoneRightLarger, 
    E.ZoneLeftLarger, 
    E.ClockRightLarger, 
    E.ClockLeftLarger, 
    E.QuadrantRightLarger, 
    E.QuadrantLeftLarger, 
    E.ZoneRightSmaller, 
    E.ZoneLeftSmaller, 
    E.ClockRightSmaller, 
    E.ClockLeftSmaller, 
    E.QuadrantRightSmaller, 
    E.QuadrantLeftSmaller, 
    E.CreationDate, 
    E.UserID, 
    E.UserIP, 
    E.FollowUpNo, 
    E.LymphNodeRightAxillary, 
    E.LymphNodeLeftAxillary
FROM 
    dbo.Examination E
INNER JOIN 
    LatestExamination LE
ON 
    E.BCNo = LE.BCNo 
    AND E.CreationDate = LE.MaxCreationDate
ORDER BY 
    E.BCNo, VisitNo ASC;