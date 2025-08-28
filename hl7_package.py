import hl7
# h = hl7.parse(message)

message = """MSH|^~\\&|AppA|FacA|AppB|FacB|202508231630||ADT^A01|MSG123|P|2.5
PID|1||123456^^^HOSP^MR~789012^^^CLINIC^PI||Doe^John^A&Junior||19800101|M
OBX|1|TX|TEST^BloodTest||Normal\R\Value~Abnormal\T\Value|N"""

message = """MSH|^~\&|12747|12747|CRELIO|CRELIO|20240529153012||ORM^O01|Q106013102T122699578||2.3||||||8859/1
PID|1|999999999^^^RRL MRN^MRN|999999999^^^RRL MRN^MRN||ZZZTEST^RRLM^||19880809|Male||National||||||||99999999999^^^RRL FIN^FIN
NBR|9999999999||||||0|||Saudi
PV1|1|Outpatient|RRL^^^RRL^^Ambulatory(s)^RRL||||DEMOPHYSVASCSURG^Physician^Vascular^Cerner^^MD^^^External Id^Personnel^^^External Identifier~11724009^Physician^Vascular^Cerner^^MD^^^PROVIDER_MESSAGING^Personnel^^^Messaging|||Laboratory|||||||DEMOPHYSVASCSURG^Physician^Vascular^Cerner^^MD^^^External Id^Personnel^^^External Identifier~11724009^Physician^Vascular^Cerner^^MD^^^PROVIDER_MESSAGING^Personnel^^^Messaging|Laboratory||Self Pay|||||||||||||||||||RRL||Active|||20240529134900
ORC|SC|309901965^HNAM_ORDERID|||In-Lab||||20240529153000|SYSTEMSYSTEM^SYSTEM^SYSTEM^Cerner^^^^^External Id^Personnel^^^External Identifier||3332057^Bolous^Medhat^Cerner^^^^^PROVIDER_MESSAGING^Personnel^^^Messaging~CERNERDRMEDGROUP10^Bolous^Medhat^Cerner^^^^^External Id^Personnel^^^External Identifier|||20240529153010||||SYSTEMSYSTEM^SYSTEM^SYSTEM^Cerner^^^^^External Id^Personnel^^^External Identifier
OBR|1|309901965^HNAM_ORDERID||350020^F11 Buckwheat|||20240529152400|||CERNERCERN473^Bhat^Rohit^Cerner^^^^^External Id^Personnel^^^External Identifier~11648100^Bhat^Rohit^Cerner^^^^^PROVIDER_MESSAGING^Personnel^^^Messaging|O|||20240529152400|Blood&Blood^^^^^Venous Draw|3332057^Bolous^Medhat^Cerner^^^^^PROVIDER_MESSAGING^Personnel^^^Messaging~CERNERDRMEDGROUP10^Bolous^Medhat^Cerner^^^^^External Id^Personnel^^^External Identifier||||000112024150000004^HNA_ACCN~4531502^HNA_ACCNID||20240529153010||General Lab|||1^^0^20240529152400^^RT~^^^^^RT - Routine|||||||||20240529152400||||||||||Laboratory^Laboratory^^Immunology^Immunology"""


import timeit
t = timeit.timeit(
    stmt=lambda: hl7.parse(message),
    number=10000  # how many times to run
)
print(f"Execution time: {t:.6f} seconds")

# python3 hl7_package.py