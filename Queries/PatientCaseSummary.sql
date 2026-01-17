-- Patient Case Summary - For BrCa AI Portal

SELECT TOP 1 PatientName, Gender, Age, Convert(varchar(10),Date_of_Registration, 103) as Date_of_Registration, Age_at_Diagnosis 
FROM PatientIDnReg WHERE BCNo='Z-2216'
ORDER BY CreationDate DESC

SELECT TOP 1 Convert(varchar(10),FollowUpDate,103) as FollowUpDate, DiseaseStatus, 
FollowUpNo, TimeBWRegAndLastFollowUp FROM vwFollowUp WHERE BCNo='Z-2216'
ORDER BY FollowUpNo DESC

SELECT TOP 1 * FROM Investigations WHERE BCNo='Z-2216'
ORDER BY FollowUpNo DESC

SELECT TOP 1 CONVERT(VARCHAR(10),SurgeryDateRight,101) AS 'SurgeryDateRight',Lesion1, Lesion2, TumorSizeLesion1, 
TumorSizeLesion2, HistologicalTypeLesion1, HistologicalTypeLesion2, HistologicalGradeLesion1,HistologicalGradeLesion2,
BrSurgeryProcRight, BrSurgeryProcLeft, SentinalLymphNodeRemovedRightLesion1, SentinalLymphNodeRemovedLeftLesion1, 
SentinalLymphNodeInvolvedRightLesion1, SentinalLymphNodeInvolvedLeftLesion1, AxillaryLymphNodeRemovedRightLesion1, 
AxillaryLymphNodeRemovedLeftLesion1, AxillaryLymphNodeInvolvedRightLesion1, AxillaryLymphNodeInvolvedLeftLesion1,
CONVERT(VARCHAR(10),SurgeryDateLeft,101) AS 'SurgeryDateLeft',Ki67LeftFrom,Ki67LeftTo,Ki67RightFrom,Ki67RightTo,
Cerb2Her2NeuLeft,Cerb2Her2NeuRight,EstrogenReceptorsLeft,EstrogenReceptorsRight,ProgesteroneReceptorsLeft,
ProgesteroneReceptorsRight,FISHRight,FISHLeft,LuminalSubTypeLeft,LuminalSubTypeRight,Ki67PostOpFromRight,
Ki67PostOpToRight, Ki67PostOpFromLeft, Ki67PostOpToLeft FROM Surgery WHERE BCNo='Z-2216'
ORDER BY CreationDate DESC

SELECT TOP 1 FinalHistopathologicalDiagnosis FROM ClinicalDiagnosis WHERE BCNo='Z-2216'
AND FinalHistopathologicalDiagnosis <> '-- SELECT --' 
ORDER BY CreationDate DESC

SELECT TOP 1 T,N,M,Stage,MetastatisLocation FROM ClinicalDiagnosis WHERE BCNo='Z-2216'
ORDER BY CreationDate DESC

SELECT TOP 1 LymphoVascularInvasionLesion1,LymphoVascularInvasionLesion2,LymphoVascularInvasionLesion3,
LymphoVascularInvasionLesion4,SentinalLymphnodeIdentified,SentinalLymphnodeBiopsyMetastasisFound 
FROM Surgery WHERE BCNo='Z-2216'
ORDER BY CreationDate DESC

SELECT TOP 1 BrLumpRightLargeWidth,BrLumpRightLargeHeight,BrLumpLeftLargeWidth,BrLumpLeftLargeHeight FROM Examination WHERE BCNo='Z-2216'
ORDER BY CreationDate DESC

SELECT  TOP 1 Modality='Chemo',EpisodeNo AS ChemoEpisodeNo,TreatmentType 
AS ChemoTreatmentType,CONVERT(varchar(10), DateOfStart,101) as 'ChemoDateOfStart', 
CONVERT(varchar(10),DateOfEnd,101) as 'ChemoDateOfEnd',AdverseEvents AS ChemoAdverseEvents,Regimen as ChemoRegimen, 
FollowedWith as ChemoFollowedWith, TherapyCompleted as ChemoTherapyCompleted 
FROM ChemoTherapy WHERE BCNo='Z-2216' ORDER BY CreationDate DESC

SELECT TOP 1 Modality='Radio',EpisodeNo AS RadioEpisodeNo,TreatmentType AS RadioTreatmentType, 
CONVERT(varchar(10), DateOfStart,101) as 'RadioDateOfStart',CONVERT(varchar(10),DateOfEnd,101) as 'RadioDateOfEnd', 
AdverseEvents AS RadioAdverseEvents, FollowedWith as RadioFollowedWith,TherapyCompleted as RadioTherapyCompleted 
FROM RadioTherapy WHERE BCNo='Z-2216'  ORDER BY CreationDate DESC

SELECT TOP 1 Modality='Hormonal',EpisodeNo AS HormonalEpisodeNo,TreatmentType 
                    AS HormonalTreatmentType,CONVERT(varchar(10), DateOfStart,101) as 'HormonalDateOfStart',
                    CONVERT(varchar(10),DateOfEnd,101) as 'HormonalDateOfEnd',AdverseEvents AS HormonalAdverseEvents,
                    Regimen as HormonalRegimen, FollowedWith as HormonalFollowedWith,TherapyCompleted as 
                    HormonalTherapyCompleted FROM HormonalTherapy WHERE BCNo='Z-2216'  ORDER BY CreationDate DESC

SELECT TOP 1 Modality='Targeted',EpisodeNo AS TargetedEpisodeNo,TreatmentType 
                    AS TargetedTreatmentType,CONVERT(varchar(10), DateOfStart,101) as 'TargetedDateOfStart',
                    CONVERT(varchar(10),DateOfEnd,101) as 'TargetedDateOfEnd',AdverseEvents AS TargetedAdverseEvents,
                    Regimen as TargetedRegimen, FollowedWith as TargetedFollowedWith, 
                    TherapyCompleted as TargetedTherapyCompleted FROM TargetedTherapy WHERE BCNo='Z-2216' ORDER BY CreationDate DESC