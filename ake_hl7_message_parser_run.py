import json
from ake_hl7_message_parser import *
from ake_hl7_message_cerner_true_dictionary import *

from unittest import TestCase # Using unittest.TestCase for more comprehensive testing

# Segment -> Field -> Component -> Subcomponent

# message = """MSH|731^Ahmed&Kamal&ELSaman|$PID|||A100035537|"""
# message = """MSH|731^Ahmed&Kamal&ELSaman|||A100035537|"""

# message = """|1||123456^^^HOSP^MR~789012^^^CLINIC^PI||Doe^John^A&Junior||19800101|M"""

#^~\& # Normal\R\Value~Abnormal\T\Value
message = """MSH|^~\\&|AppA|FacA|AppB|FacB|202508231630||ADT^A01|MSG123|P|2.5
PID|1||123456^^^HOSP^MR~789012^^^CLINIC^PI||Doe^John^A&Junior||19800101|M
OBX|1|TX|TEST^BloodTest||Normal\R\Value~Abnormal\T\Value|N"""

message = """MSH|^~\&|12747|12747|CRELIO|CRELIO|20240529153012||ORM^O01|Q106013102T122699578||2.3||||||8859/1
PID|1|999999999^^^RRL MRN^MRN|999999999^^^RRL MRN^MRN||ZZZTEST^RRLM^||19880809|Male||National||||||||99999999999^^^RRL FIN^FIN
NBR|9999999999||||||0|||Saudi
PV1|1|Outpatient|RRL^^^RRL^^Ambulatory(s)^RRL||||DEMOPHYSVASCSURG^Physician^Vascular^Cerner^^MD^^^External Id^Personnel^^^External Identifier~11724009^Physician^Vascular^Cerner^^MD^^^PROVIDER_MESSAGING^Personnel^^^Messaging|||Laboratory|||||||DEMOPHYSVASCSURG^Physician^Vascular^Cerner^^MD^^^External Id^Personnel^^^External Identifier~11724009^Physician^Vascular^Cerner^^MD^^^PROVIDER_MESSAGING^Personnel^^^Messaging|Laboratory||Self Pay|||||||||||||||||||RRL||Active|||20240529134900
ORC|SC|309901965^HNAM_ORDERID|||In-Lab||||20240529153000|SYSTEMSYSTEM^SYSTEM^SYSTEM^Cerner^^^^^External Id^Personnel^^^External Identifier||3332057^Bolous^Medhat^Cerner^^^^^PROVIDER_MESSAGING^Personnel^^^Messaging~CERNERDRMEDGROUP10^Bolous^Medhat^Cerner^^^^^External Id^Personnel^^^External Identifier|||20240529153010||||SYSTEMSYSTEM^SYSTEM^SYSTEM^Cerner^^^^^External Id^Personnel^^^External Identifier
OBR|1|309901965^HNAM_ORDERID||350020^F11 Buckwheat|||20240529152400|||CERNERCERN473^Bhat^Rohit^Cerner^^^^^External Id^Personnel^^^External Identifier~11648100^Bhat^Rohit^Cerner^^^^^PROVIDER_MESSAGING^Personnel^^^Messaging|O|||20240529152400|Blood&Blood^^^^^Venous Draw|3332057^Bolous^Medhat^Cerner^^^^^PROVIDER_MESSAGING^Personnel^^^Messaging~CERNERDRMEDGROUP10^Bolous^Medhat^Cerner^^^^^External Id^Personnel^^^External Identifier||||000112024150000004^HNA_ACCN~4531502^HNA_ACCNID||20240529153010||General Lab|||1^^0^20240529152400^^RT~^^^^^RT - Routine|||||||||20240529152400||||||||||Laboratory^Laboratory^^Immunology^Immunology|aa&bb^cc&dd~ee&ff^gg&hh|abc1&abc2&abc3|xyz1~xyz2~xyz3"""

# message = """|1||123456^^^HOSP^MR~789012^^^CLINIC^PI||Doe^John^A&Junior||19800101|M""" # PID

# 
message = """MSH|^~\&|A&A^B&B~C&^&D~E&E^F&|ABC1&ABC2~ABC3&ABC4~ABC5&ABC6|xyz1^xyz2^xyz3~xyz4^xyz6^xyz6
PID|XYZ
PID|123
PID|xyz1~xyz2~xyz3"""

class AKEDict(dict): pass
hl7_dictionary = AKEDict() # {}

parser(hl7_dictionary, message)
hl7_dictionary_pretty_string = str(json.dumps(hl7_dictionary, indent='\t'))
print(hl7_dictionary_pretty_string)

# assert hl7_dictionary == hl7_message_cerner_true_dictionary
# TestCase().assertEqual(hl7_dictionary, hl7_message_cerner_true_dictionary)
# TestCase().assertDictEqual(hl7_dictionary, hl7_message_cerner_true_dictionary)

class CernerHL7MessageTest(TestCase):
	def run(self):
		# with self.assertRaises(AssertionError):
		#     self.assertDictEqual(hl7_dictionary, hl7_message_cerner_true_dictionary)
		self.maxDiff = None
		self.assertDictEqual(hl7_dictionary, hl7_message_cerner_true_dictionary)

cerner_hl7_message_test = CernerHL7MessageTest()
# cerner_hl7_message_test.run()

# print(hl7_dictionary['PID']['F3'][1]['C0'])
# print(hl7_dictionary['PID']['F5']['C2']['SC1'])

# import timeit
# t = timeit.timeit(
#     stmt=lambda: parser(hl7_dictionary, message),
#     number=100000  # how many times to run
# )

# print(f"Execution time: {t:.6f} seconds")

# fhir_dictionary = {
# 	"MRN": [hl7_dictionary['PID']['F3'][0]['C0'], hl7_dictionary['PID']['F3'][1]['C0']]

# }

# print(fhir_dictionary)

# https://github.com/microsoft/FHIR-Converter/blob/main/docs/HL7v2-templates.md
# https://chatgpt.com/share/68abbfa5-fc08-800c-9627-e4456c1d962d # whole chat
# https://chatgpt.com/s/t_68ab2c5b2c1c8191a6b19638e9c5edcb # design HL7 Engine
# https://chatgpt.com/s/t_68ab2c69d71c8191a7371d2eaa4bdfae # what is MLLP
# https://chatgpt.com/s/t_68ab2ca027b48191b64cbe673af4a048 # design HL7 Engine with MLLP
# https://chatgpt.com/s/t_68ab2cd08fc081918ce5aa763569beb6 # MLLP client and server in python
# https://chatgpt.com/s/t_68aba56fe7e88191adb6db6721d8ccfd # format and semantic escape characters

# python3 hl7_message_parser_dichir.py
# https://chatgpt.com/share/68af5d7c-7460-800c-afaa-00bacc51f615 # design HL7 integration in python from python packages