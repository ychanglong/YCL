import os
import datetime
import pandas as pd

today = datetime.date.today()

now = datetime.datetime.now()

# sender = "CI-Service-Center-Suzhou@cn.bosch.com"
sender = "jared.ma@cn.bosch.com"
# sender = "johnson.qian@cn.bosch.com"
# recipient = "CICriticalIncidentReport@bcn.bosch.com"
recipient = "jared.ma@cn.bosch.com"
# recipient = "johnson.qian@cn.bosch.com"

body = """
<body>
<p style="font-family:Arial;font-size:13px">Dear Madam or Sir,<br><br>
Please find attached "Daily Report of Critical SMT Tickets". <br><br>
Mit freundlichen Grüßen/ Kind regards, <br><br>
<strong>BD Critical Ticket Ownership (BD/ISA-GOC7)</strong> <br>
Tel: +4971181192929 <br>
Mail: CI-Service-Center-Suzhou@cn.bosch.com</p>
</body>
"""

body_no_results = """
<body>
<p style="font-family:Arial;font-size:13px">Dear Madam or Sir,<br><br>
There is no critical ticket during this period of time. <br><br>
Mit freundlichen Grüßen/ Kind regards, <br><br>
<strong>BD Critical Ticket Ownership (BD/ISA-GOC7)</strong> <br>
Tel: +4971181192929 <br>
Mail: CI-Service-Center-Suzhou@cn.bosch.com</p>
</body>
"""


def get_date():
    if today.isoweekday() in range(2, 6):
        time_period = today - datetime.timedelta(days=1)
        subject_timestamp = time_period.strftime("%d.%m.%Y")
        attachment = f"Tagesbericht_j{time_period.strftime('%Y%m%d')}.xlsx"
        return time_period.strftime("%d.%m.%Y"), subject_timestamp, attachment
    if today.strftime("%A") == "Monday":
        time_period = today - datetime.timedelta(days=3)
        subject_timestamp = f"{time_period.strftime('%d.%m.%Y')}-{today.strftime('%d.%m.%Y')}"
        attachment = f"Tagesbericht_j{time_period.strftime('%Y%m%d')}bis{today.strftime('%m%d')}.xlsx"
        return time_period.strftime("%d.%m.%Y"), subject_timestamp, attachment


time_period, subject_timestamp, attachment = get_date()

if now.strftime("%H") == "13":
    subject = f"Daily Report of Critical SMT Tickets <{subject_timestamp}> (Draft Version)"
else:
    subject = f"Daily Report of Critical SMT Tickets <{subject_timestamp}>"

df_summary = pd.DataFrame(
    {
        "SMT Critical Incidents": [
            "",
            "All critical Incidents created within date selected.",
            "",
            "Submit Date From (dd.mm.yyyy)",
            "Submit Date Till (dd.mm.yyyy)",
            "Last Refresh Date",
        ],
        "": ["","","", time_period, today.strftime("%d.%m.%Y"), now.strftime("%d.%m.%Y %H:%M")],
    }
)

hostname = 'rb0orarac29.de.bosch.com'
service_name = 'ASH372.de.bosch.com'
username = 'OSR4_CN_READ'
password = 'OSR4_CN_READ_945'
port = 38000
stmt = f"""
        SELECT 
        DISTINCT
        A.INCIDENT_NUMBER AS "Incident ID",
        A.SUBMITED_DATE AS "Created Date(UTC+0)",
        (SELECT 
                TO_CHAR(TRUNC(C.DOWN_TIME/3600),'FM0999') || ':' ||
                TO_CHAR(TRUNC(MOD(C.DOWN_TIME,3600)/60),'FM00') 
        FROM TRANSLATION.VW_INC_DOWN_TIME C WHERE A.INCIDENT_NUMBER=C.INCIDENT_NUMBER) AS "Down Time (hhh:mi)",
        A.DESCRIPTION AS Summary,
		A.RESOLUTION AS Resolution,
        A.STATUS AS Status,
        A.SITE AS Site,
        A.CUSTOMERCOMPANY AS "Customer Company",
        A.FIRST_SOLVED_COMPANY AS "Support Group Company",
        A.FIRST_SOLVED_ORGANIZATION AS "Support Group Organization",
        A.FIRST_SOLVED_GROUP AS "Assigned Group",
        A.PRODUCT_CATEGORIZATION_TIER_1 AS "Product Categorization Tier 1",
        A.PRODUCT_CATEGORIZATION_TIER_2 AS "Product Categorization Tier 2",
        A.PRODUCT_CATEGORIZATION_TIER_3 AS "Product Categorization Tier 3",
        A.RESOLUTION_PROD_CATEGORY_TIER1,
        A.RESOLUTION_PROD_CATEGORY_TIER2,
        A.RESOLUTION_PROD_CATEGORY_TIER3,
        A.SERVICE AS Service,
        A.CI,
        (SELECT 
                LISTAGG(F.RELATEDCONFIGURATIONITEMS,', ') WITHIN GROUP(ORDER BY F.INCIDENT_NUMBER)
        FROM TRANSLATION.VW_INC_RELATED_CONFIGITEMS F WHERE A.INCIDENT_NUMBER=F.INCIDENT_NUMBER GROUP BY F.INCIDENT_NUMBER)AS Relatedconfigurationitems,
        TO_CHAR(trunc((( A.FIRST_SOLVED_DATE - A.REPORTED_DATE)*24*60*60)/3600),'FM0999') || ':' ||
        TO_CHAR(ROUND(MOD((( A.FIRST_SOLVED_DATE - A.REPORTED_DATE)*24*60*60),3600)/60),'FM00') 
        AS "Resolving time (hhhh:mm)",
        LISTAGG(B.PROBLEM_ID,'; ') 
        WITHIN GROUP (ORDER BY B.INCIDENT_ID) OVER (PARTITION BY B.INCIDENT_ID) AS "Related Problem ID"
        FROM TRANSLATION.VW_HPD_HELP_DSK_BASIC_CRITICAL A FULL OUTER JOIN TRANSLATION.VW_INC_PBM_RELATIONSHIP_BASIC B
        ON A.INCIDENT_NUMBER=B.INCIDENT_ID
        WHERE A.WAS_CRITICAL='yes' 
        AND (A.SUBMITED_DATE BETWEEN TO_DATE ('{time_period} 00:00:00', 'dd.mm.yyyy hh24:mi:ss') AND TO_DATE ('{today.strftime("%d.%m.%Y")} 06:00:00', 'dd.mm.yyyy hh24:mi:ss')+ 1)
        AND A.PRIORITY='Critical' 
        and A.IS_CHILD <> 'YES'
        AND UPPER(substr(A.DESCRIPTION,0,2)) <> 'T5'
        order by A.SUBMITED_DATE ASC
        """
