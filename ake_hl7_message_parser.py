from hl7_standard_versions.hl7_v2_3 import *
#================================================================================
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

	# segment_schema = hl7_v2_3[segment_code]['ake_segment']

	for position in range(start, len(message)):
		try:
			char = message[position]
			# field_code = f"{segment_code}.{fields_count}"
			# component_code = f"{field_code}.{components_count}"
			# subcomponents_code = f"{component_code}.{subcomponents_count}"
			if char == '|': # match |: dictionary[F0] = None # start_delimiter: | # position != start and position - start < 2
				if start_delimiter == '|': # | | close a previous single value field and start new field
					field = segment[fields_count] = message[start:position]
				elif start_delimiter == '^': # ^ | close a single value component and start new field
					field[components_count] = message[start:position]
				elif start_delimiter == '&': # & | close an always single value subcomponent and start new field
					field[components_count][subcomponents_count] = message[start:position]
				elif start_delimiter == '~': # ~ | close a single value repitition and start new field
					field.append(message[start:position])
				elif start_delimiter == new_segment_delimiter: # create segment
					segment_code = message[start:position]
					segment = {}
					if segment_code in hl7_message_dictionary:
						if type(hl7_message_dictionary[segment_code]) == dict:
							hl7_message_dictionary[segment_code] = [hl7_message_dictionary[segment_code]]
						hl7_message_dictionary[segment_code].append(segment)
					else:
						hl7_message_dictionary[segment_code] = segment
					# segment_schema = hl7_v2_3[segment_code]['ake_segment']
				#-----last will be written to field
				tree = segment
				# nodeType = segment_code
				count = fields_count
				#----------
				start_delimiter = '|'
				start = position + 1
				fields_count += 1
				components_count = 1
				subcomponents_count = 1
				composedField = False

				# field_code = f"{segment_code}.{fields_count}"
				# print(field_code)
				# if field_code in segment_schema['ake_fields']:
				# 	field_schema = segment_schema['ake_fields'][field_code]
				# 	fieldName = field_schema['name']
				# 	print(fieldName)
			#----------------------------------------
			elif char == '^':
				if start_delimiter == '|': # | ^ convert a single value field to field with components
					field = segment[fields_count] = {}
					composedField = True
					field[components_count] = message[start:position]
				elif start_delimiter == '^': # ^ ^ close a previous single value component and start a new component
					field[components_count] = message[start:position]
				elif start_delimiter == '&': # & ^ close an always single value subcomponent and start a new component
					field[components_count][subcomponents_count] = message[start:position]
				elif start_delimiter == '~': # ~ ^ close the last component in repitition and start a new component in a new repitition # current repitition has compoenents so the previous one
					field[components_count] = message[start:position]
				#-----last will be written to compoent
				tree = field
				# nodeType = field_code
				count = components_count
				#----------
				start = position + 1
				start_delimiter = '^'
				components_count += 1
				subcomponents_count = 1
				composedComponent = False
			#----------------------------------------
			elif char == '&':
				if start_delimiter == '|': # | & convert a single value field to field with components and make first component in the field to component with subcomponents
					field = segment[fields_count] = {}
					field[components_count] = {}
					composedField = True
					composedComponent = True
				elif start_delimiter == '^': # ^ & convert a single value component to component with subcomponents
					field[components_count] = {}
					composedComponent = True
				# elif start_delimiter == '&': # it & & will works automatically because the next uncommented line # ex.: |abc1~abc2~abc3|
					# field[components_count][subcomponents_count] = message[start:position]
				# elif start_delimiter == '~': # ~ & it will works automatically because the next uncommented line # ex.: |aa&bb^cc&dd~ee&ff^gg&hh|
					# field[components_count][subcomponents_count] = message[start:position]
				field[components_count][subcomponents_count] = message[start:position]
				#-----last will be written to subcompoent
				tree = field[components_count]
				# nodeType = component_code
				count = subcomponents_count
				#----------
				start = position + 1
				start_delimiter = '&'
				subcomponents_count += 1
			#----------------------------------------
			elif char == '~': # convert field to multi values list 'repitions'
				if start_delimiter == '^': # convert field with components to list of repetition with components
					field[components_count] = message[start:position]
					if not (type(segment[fields_count]) == list):
						segment[fields_count] = [segment[fields_count]]
					segment[fields_count].append({})
					lastFieldIndex = len(segment[fields_count]) - 1
					field = segment[fields_count][lastFieldIndex]
				elif start_delimiter == '|': # convert field from single values to multiple values
					field = segment[fields_count] = [message[start:position]] # first repetition in the field
				elif start_delimiter == '&':
					field[components_count][subcomponents_count] = message[start:position]
					if not (type(segment[fields_count]) == list):
						segment[fields_count] = [segment[fields_count]]
					segment[fields_count].append({1: {}})
					lastFieldIndex = len(segment[fields_count]) - 1
					field = segment[fields_count][lastFieldIndex]
				elif start_delimiter == '~':
					segment[fields_count].append(message[start:position])
				#-----last will be written to repitition
				tree = field
				#----------
				components_count = 1
				subcomponents_count = 1
				start = position + 1
				start_delimiter = '~'
			#----------------------------------------
			elif char == new_segment_delimiter:
				if type(tree) is list:
					tree.append(message[start:position]) # start delimiter will always be ~ with list tree
				else: # if start delimiter is | ^ &
					# tree[f"{nodeType}.{count+1}"] = message[start:position]
					tree[count+1] = message[start:position]
				fields_count = 0
				components_count = 1
				subcomponents_count = 1
				repitition_count = 1
				start = position + 1
				start_delimiter = new_segment_delimiter
		except Exception as e:
			hl7_dictionary_pretty_string = str(json.dumps(hl7_dictionary, indent='\t'))
			print(hl7_dictionary_pretty_string)
			print(f"break at: {segment_code}: {position}: {char}: {message[position-1]}{message[position]}{message[position+1]}")
			print(e)
			exit
	
	# uncommitted char
	if type(tree) is list: # start delimiter will always be ~ with list tree
		tree.append(message[start:position+1])
	else:  # if start delimiter is | ^ &
		# tree[f"{nodeType}.{count+1}"] = message[start:position+1]
		tree[count+1] = message[start:position+1]

#================================================================================
# https://github.com/microsoft/FHIR-Converter/blob/main/docs/HL7v2-templates.md
# https://chatgpt.com/share/68abbfa5-fc08-800c-9627-e4456c1d962d # whole chat
# https://chatgpt.com/s/t_68ab2c5b2c1c8191a6b19638e9c5edcb # design HL7 Engine
# https://chatgpt.com/s/t_68ab2c69d71c8191a7371d2eaa4bdfae # what is MLLP
# https://chatgpt.com/s/t_68ab2ca027b48191b64cbe673af4a048 # design HL7 Engine with MLLP
# https://chatgpt.com/s/t_68ab2cd08fc081918ce5aa763569beb6 # MLLP client and server in python
# https://chatgpt.com/s/t_68aba56fe7e88191adb6db6721d8ccfd # format and semantic escape characters

# https://chatgpt.com/share/68af5d7c-7460-800c-afaa-00bacc51f615 # design HL7 integration in python from python packages
#================================================================================
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