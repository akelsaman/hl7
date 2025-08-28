import json

# will search for delimiter | ^ &
# if the current character match any of the delimiters will create new field in the dictionary with right mapped name according to the matched delimiters
#     | F1
#     ^ C1
#     & SC1
#     ~ F1 will be converted to list
# recurse to itself with the dictionary path, key, message_position, current_delimiter, rest_of_the_delimiters
# if matched any of the rest of the delimiters recurse to it again if not 

# or just create machine stated field, component, subcomponent, repitition

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
OBR|1|309901965^HNAM_ORDERID||350020^F11 Buckwheat|||20240529152400|||CERNERCERN473^Bhat^Rohit^Cerner^^^^^External Id^Personnel^^^External Identifier~11648100^Bhat^Rohit^Cerner^^^^^PROVIDER_MESSAGING^Personnel^^^Messaging|O|||20240529152400|Blood&Blood^^^^^Venous Draw|3332057^Bolous^Medhat^Cerner^^^^^PROVIDER_MESSAGING^Personnel^^^Messaging~CERNERDRMEDGROUP10^Bolous^Medhat^Cerner^^^^^External Id^Personnel^^^External Identifier||||000112024150000004^HNA_ACCN~4531502^HNA_ACCNID||20240529153010||General Lab|||1^^0^20240529152400^^RT~^^^^^RT - Routine|||||||||20240529152400||||||||||Laboratory^Laboratory^^Immunology^Immunology|aa&bb^cc&dd~ee&ff^gg&hh|ABC1~ABC2"""

# message = """|1||123456^^^HOSP^MR~789012^^^CLINIC^PI||Doe^John^A&Junior||19800101|M""" # PID


# start = 0, position = 0
# 
# --- position += 1
# match |: dictionary[F0] = message[start:position] # '' #start_delimiter: |
# --- position += 1
# find 1: pass
# --- position += 1
# match |:
#   dictionary[F1] = message[start:position] # 1 #start_delimiter: |
# --- position += 1
# match |:
#	dictionary[F2] = message[start:position] # '' #start_delimiter: |
# --- position += 1
# find 1: pass
# --- position += 1
# find 2: pass
# --- position += 1
# find 3: pass
# --- position += 1
# find 4: pass
# --- position += 1
# find 5: pass
# --- position += 1
# find 6: pass
# --- position += 1
# match ^: 
#	dictionary[F2] = {}
#	dictionary[F2][C0] = message[start:position] # 123456 #start_delimiter: |
# --- position += 1
# match ^:
#	dictionary[F2][C1] = message[start:position] # '' #start_delimiter: ^
# match ^:
#	dictionary[F2][C2] = message[start:position] # '' #start_delimiter: ^
# --- position += 1
# find H: pass
# --- position += 1
# find O: pass
# --- position += 1
# find S: pass
# --- position += 1
# find P: pass
# --- position += 1
# match ^:
#	dictionary[F2][C3] = message[start:position] # HOSP #start_delimiter: ^
# --- position += 1
# find M: pass
# --- position += 1
# find R: pass
# --- position += 1
# match ~:
#	dictionary[F2] = [dictionary[F2]]
#	dictionary[F2][1] = {}
# --- position += 1
# find 7: pass
# --- position += 1
# find 8: pass
# --- position += 1
# find 9: pass
# --- position += 1
# find 0: pass
# --- position += 1
# find 1: pass
# --- position += 1
# find 2: pass
# --- position += 1
# match ^:
#	dictionary[F2][1][C0] = message[start:position] # 789012 #start_delimiter: ~
#	dictionary[F2][1][C1] = None
# --- position += 1
# match ^:
#	dictionary[F2][1][C2] = message[start:position] # '' #start_delimiter: ^
#	dictionary[F2][1][C3] = None
# --- position += 1
# find C: pass
# --- position += 1
# find L: pass
# --- position += 1
# find I: pass
# --- position += 1
# find N: pass
# --- position += 1
# find C: pass
# --- position += 1
# match ^:
#	dictionary[F2][1][C3] = message[start:position] # CLINC #start_delimiter: ^
#	dictionary[F2][1][C4] = None
# --- position += 1
# find P: pass
# --- position += 1
# find I: pass
# --- position += 1
# match |:
#	dictionary[F2][1][C4] = message[start:position] # PI #start_delimiter: ^
#	dictionary[F3] = None
# --- position += 1
# match |:
#	dictionary[F4] = message[start:position] # '' #start_delimiter: |
# --- position += 1
# ...

# \r   (ASCII 13, hex 0x0D)

# message = """MSH|^~\&|AA^BB~CC^DD~EE^FF|ABC"""

hl7_dictionary = {}

def setCurrent(tree, node, value):
	tree[node] = value
	return (tree, node)

def parser(hl7_message_dictionary, message, segment_code="MSH"):
	start = 8
	new_segment_delimiter = '\n'  # new_segment_delimiter
	start_delimiter = '|'
	fields_count = 1
	components_count = 1
	subcomponents_count = 1
	repitition_count = 1
	segment = hl7_message_dictionary[segment_code] = {}
	field = None
	composedField = False
	composedComponent = False
	tree = None
	node = None
	count = None
	for position in range(start, len(message)):
		try:
			char = message[position]
			if char == '|': # match |: dictionary[F0] = None # start_delimiter: | # position != start and position - start < 2
				if start_delimiter == '|': # | | close a previous single value field and start new field
					field = segment[f"F{fields_count}"] = message[start:position]
				elif start_delimiter == '^': # ^ | close a single value component and start new field
					field[f"C{components_count}"] = message[start:position]
				elif start_delimiter == '&': # & | close an always single value subcomponent and start new field
					field[f"C{components_count}"][f"SC{subcomponents_count}"] = message[start:position]
				elif start_delimiter == '~': # ~ | close a single value repitition and start new field
					field.append(message[start:position])
				elif start_delimiter == new_segment_delimiter: # create segment
					segment_code = message[start:position]
					segment = hl7_message_dictionary[segment_code] = {}
				#-----last will be written to field
				tree = segment
				nodeType = "F"
				count = fields_count
				#----------
				start_delimiter = '|'
				start = position + 1
				fields_count += 1
				components_count = 1
				subcomponents_count = 1
				composedField = False
			elif char == '^':
				if start_delimiter == '|': # | ^ convert a single value field to field with components
					field = segment[f"F{fields_count}"] = {}
					composedField = True
					field[f"C{components_count}"] = message[start:position]
				elif start_delimiter == '^': # ^ ^ close a previous single value component and start a new component
					field[f"C{components_count}"] = message[start:position]
				elif start_delimiter == '&': # & ^ close an always single value subcomponent and start a new component
					field[f"C{components_count}"][f"SC{subcomponents_count}"] = message[start:position]
				elif start_delimiter == '~': # ~ ^ close the last component in repitition and start a new component in a new repitition # current repitition has compoenents so the previous one
					field[f"C{components_count}"] = message[start:position]
				#-----last will be written to compoent
				tree = field
				nodeType = "C"
				count = components_count
				#----------
				start = position + 1
				start_delimiter = '^'
				components_count += 1
				subcomponents_count = 1
				composedComponent = False
			elif char == '&':
				if start_delimiter == '|': # | & convert a single value field to field with components and make first component in the field to component with subcomponents
					field = segment[f"F{fields_count}"] = {}
					field[f"C{components_count}"] = {}
					composedField = True
					composedComponent = True
				elif start_delimiter == '^': # ^ & convert a single value component to component with subcomponents
					field[f"C{components_count}"] = {}
					composedComponent = True
				# elif start_delimiter == '&': # it & & will works automatically because the next uncommented line
				# 	pass
				# elif start_delimiter == '~': # ~ & it will works automatically because the next uncommented line # |aa&bb^cc&dd~ee&ff^gg&hh|
					# field[f"C{components_count}"][f"SC{subcomponents_count}"] = message[start:position]
					# pass
				field[f"C{components_count}"][f"SC{subcomponents_count}"] = message[start:position]
				#-----last will be written to subcompoent
				tree = field[f"C{components_count}"]
				nodeType = "SC"
				count = subcomponents_count
				#----------
				start = position + 1
				start_delimiter = '&'
				subcomponents_count += 1
			elif char == '~': # convert field to multi values list 'repitions'
				if start_delimiter == '^': # convert field with components to list of repetition with components
					field[f"C{components_count}"] = message[start:position]
					if not (type(segment[f"F{fields_count}"]) == list):
						segment[f"F{fields_count}"] = [segment[f"F{fields_count}"]]
					segment[f"F{fields_count}"].append({})
					lastFieldIndex = len(segment[f"F{fields_count}"]) - 1
					field = segment[f"F{fields_count}"][lastFieldIndex]
				elif start_delimiter == '|': # convert field from single values to multiple values
					field = segment[f"F{fields_count}"] = [message[start:position]] # first repetition in the field
				elif start_delimiter == '&':
					field[f"C{components_count}"][f"SC{subcomponents_count}"] = message[start:position]
					if not (type(segment[f"F{fields_count}"]) == list):
						segment[f"F{fields_count}"] = [segment[f"F{fields_count}"]]
					segment[f"F{fields_count}"].append({"C1": {}})
					field = segment[f"F{fields_count}"][lastFieldIndex]
				elif start_delimiter == '~':
					pass
				#-----last will be written to repitition
				tree = field
				#----------
				components_count = 1
				subcomponents_count = 1
				start = position + 1
				start_delimiter = '~'
			elif char == new_segment_delimiter:
				start_delimiter = new_segment_delimiter
				# field = segment[f"F{fields_count}"] = message[start:position]
				# if type(tree) is list:
				# 	tree.append({"C0": message[start:position]})
				# else:
				# 	tree[f"{nodeType}{count+1}"] = message[start:position]
				tree[f"{nodeType}{count+1}"] = message[start:position]
				fields_count = 0
				components_count = 1
				subcomponents_count = 1
				repitition_count = 1
				start = position + 1
		except Exception as e:
			hl7_dictionary_pretty_string = str(json.dumps(hl7_dictionary, indent='\t'))
			print(hl7_dictionary_pretty_string)
			print(f"break at: {segment_code}: {position}: {char}")
			print(e)
			break
	# field = segment[f"F{fields_count}"] = message[start:] # uncommitted char
	# tree[f"{nodeType}{count+1}"] = message[start:]
	if type(tree) is list:
		tree.append(message[start:position])
	else:
		tree[f"{nodeType}{count+1}"] = message[start:position]

# match ~:
#	dictionary[F2] = [dictionary[F2]]
#	dictionary[F2][1] = {}
		
# import timeit
# t = timeit.timeit(
#     stmt=lambda: parser(hl7_dictionary, message),
#     number=10000  # how many times to run
# )

parser(hl7_dictionary, message)
hl7_dictionary_pretty_string = str(json.dumps(hl7_dictionary, indent='\t'))
print(hl7_dictionary_pretty_string)

# print(hl7_dictionary['PID']['F3'][1]['C0'])
# print(hl7_dictionary['PID']['F5']['C2']['SC1'])

# print(f"Execution time: {t:.6f} seconds")


# sada elbalad
# 3
# 4
# 5

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