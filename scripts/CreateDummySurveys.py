from InteractiveDB.models import SurveyTable

def AddSurvey(id,date,theme,subthemeEnglish,subthemeFrench,surveyWeek):
    survey = SurveyTable()
    survey.qualtricsSurveyID = id
    survey.releaseDate = date
    survey.surveyTheme = theme
    survey.surveysubThemeEnglish = subthemeEnglish
    survey.surveysubThemeFrench = subthemeFrench
    survey.surveyWeek = surveyWeek

    survey.save()

def run(*args):
    
    AddSurvey('SV_aYnUZN7y2nQhXJc','2022-12-07','CHA','Current issues & challenges','Enjeux et défis actuels','Y1W01') 
    AddSurvey('SV_0eMEVIZkeSbKyjk','2022-12-14','CHA','Current issues & challenges','Enjeux et défis actuels','Y1W02')
    AddSurvey('SV_4PKhCR2n0Hw6xbo','2023-01-04','OTH','Looking Ahead/Planning for the Future',"Regarder vers l'avenir / Planifier l'avenir",'Y1W03') 
    AddSurvey('SV_8D2MdCYlLUZqu22','2023-01-11','GOV','HR & Staffing','RH et dotation','Y1W04')
    AddSurvey('SV_0SqKvaglCv3ophA','2023-01-18','EDI','Populations Served','Populations desservies','Y1W05')
    AddSurvey('SV_3agBieQhc6t7d2K','2023-01-25','FUN','Relationships with donors','Relations avec les donateurs','Y1W06')
    AddSurvey('SV_dhjlzfTnCj7mwT4','2023-02-01','GOV','Volunteers','Bénévoles','Y1W07')
    AddSurvey('SV_1RnShmHTBkbGhCu','2023-02-08','COL','Collaboration within the sector','Collaboration au sein du secteur','Y1W08') 
    AddSurvey('SV_cSUrXPI6VggGvEq','2023-02-15','POL','Advocacy efforts','Efforts de plaidoyer','Y1W09')
    AddSurvey('SV_42rjmguCfnl7s7s','2023-02-22','EDI','Working with Indigenous Communities','Travailler avec les communautés autochtones','Y1W10')
    AddSurvey('SV_6nk4KaDYWIazwSq','2023-03-01','GOV','HR & Staffing','RH et dotation','Y1W11')
    AddSurvey('SV_9Kpc8ttIoJCDwhg','2023-03-08','OTH','Impact & evaluation','Impact et évaluation','Y1W12')
    AddSurvey('SV_4ONclMGWEiBoZFk','2023-03-15','FUN','Funder requirements','Exigences du bailleur de fonds','Y1W13')
    AddSurvey('SV_29xoxQFVl4Rladg','2023-03-22','OTH','Artificial Intelligence','Intelligence Artificielle','Y1W14') 
    AddSurvey('SV_55fMnaZIQKk86ZE','2023-03-29','CHA','Inflation','Inflation','Y1W15') 
    AddSurvey('SV_1QRGU5FIfrMVtKm','2023-04-05','CHA','Board of Directors',"Conseil d'administration",'Y1W16')
    AddSurvey('SV_6DTO78p2MVG52g6','2023-04-12','GOV','Mental health challenges within the sector','Les défis de santé mentale dans le secteur','Y1W17')
    AddSurvey('SV_cPlOlLZZhtASd5I','2023-04-19','COL','Service collaboration & integration','Collaboration et intégration des services','Y1W18')
    AddSurvey('SV_8CzGXW2wXTMn9gq','2023-04-26','POL','Policy concerns,Required Government support,etc.','Préoccupations politiques, soutien gouvernemental requis, etc.','Y1W19')
    AddSurvey('SV_0lJ2ddSC0PnAQPI','2023-05-03','CHA','COVID-19','COVID 19','Y1W20')
    AddSurvey('SV_bqKBmSENlLRWNWm','2023-05-10','FUN','Financial health','Santé financière','Y1W21')
    AddSurvey('SV_1ziHebaCSozfbRc','2023-05-17','EDI','Gender in the sector','Genre dans le secteur','Y1W22')
    AddSurvey('SV_8emOMKK68Ne2JIW','2023-05-24','GOV','Leadership Requirements','Exigences en matière de leadership','Y1W23')
    AddSurvey('SV_e3fX4mMxLUEMXS6','2023-05-31','OTH','Climate change','Changement climatique','Y1W24')
    AddSurvey('SV_dbY9Vbg47dMKEwS','2023-06-07','GOV','Communications and marketing','Communication et marketing','Y1W25')
    AddSurvey('SV_cVfK6cKOue4VZgW','2023-06-14','FUN','Donor behavior and preferences','Comportement et préférences des donateurs','Y1W26')
    AddSurvey('SV_bC479yMxWekXnWS','2023-06-21','GOV','Volunteer engagement','Engagement des bénévoles','Y1W27')
    AddSurvey('SV_bycpZWVyBjTlmSO','2023-06-28','POL','Impact of Government funding on the sector','Impact du financement gouvernemental sur le secteur','Y1W28')
    AddSurvey('SV_0xsnw9eASP8WJYW','2023-07-05','CHA','Digital Transformation / Technological advancements','Transformation numérique / Avancées technologiques','Y1W29')
    AddSurvey('SV_3L4rLLzhPt3qx7g','2023-07-12','CHA','Increased Demand and Service Delivery','Augmentation de la demande et de la prestation de services','Y1W30')
    AddSurvey('SV_5zn42gF56T58USy','2023-07-19','EDI','Accessibility and Inclusion','Accessibilité et inclusion','Y1W31')
    AddSurvey('SV_9M0uIJ9LMYqpxoq','2023-08-09','FUN','Sustainability and Diversification of Funding Sources','Durabilité et diversification des sources de financement','Y1W32')
    AddSurvey('SV_e2P2IrTSf2X8TXM','2023-08-16','POL','Regulation & Management of the Sector','Régulation & Gestion du Secteur','Y1W33')
    AddSurvey('SV_88GOnUxCevOzQ3k','2023-08-23','COL','Cross-Disciplinary Collaboration','Collaboration interdisciplinaire','Y1W34')
    AddSurvey('SV_3rsdcxWqQGmNCWa','2023-08-30','GOV','Accountability strategies','Stratégies de responsabilisation','Y1W35')
    AddSurvey('SV_0MPnoTzRsHwMWvY','2023-09-06','EDI','Organizational culture','Culture organisationnelle','Y1W36')
    AddSurvey('SV_2fB85PBzkIEX8mW','2023-09-13','CHA','Tech and Data Security','Sécurité technologique et des données','Y1W37')
    AddSurvey('SV_8eM0qAI5kTQDpX0','2023-09-20','GOV','Long-term Sustainability','Durabilité à long terme','Y1W38')
    AddSurvey('SV_5vjKtSXRopYShUi','2023-09-27','OTH','Public Perception and Trust','Perception et confiance du public','Y1W39')