hl7Message = """MSH||DXCEM|A1|OHCAPPL|A1|20230320143118||ORM^O01|147626918|P|2.4|||AL||
PID|||A100035537||ابوزيد احمد رضوان^ابراهيم^||19600621000000|M||||||||||A100035537|26006210300119|||||||EGP^EGYPTIAN||EGP||N
PV1||OP|DN^Dentistry^^^A1^O|AC|||P00022^Dr Iman Saleh|||DN|||||||^||102726290001|UHIN|||||||||||||||||||A1|||||20230320132536|
ORC|NW|TROP00000904192|44540698|TROP00000904192|IP|D|1^^^^20230320142928^^P||20230320143116|P00022||P00022^Dr Iman Saleh|||20230320142928|OS|A1|MOBILE|||A1|~~~|~~~
OBR|1|TROP00000904192!1|44540698|TPDN0133^Root Canal Treatment For Anterior Teeth|R|20230320143116|20230320142928|||||||||P00022^Dr Iman Saleh||OS|||||||||1^^^20230320142928^20230320142928^R||||||||||||^
DG1|1|ICD11|DA09.0|DA09.0 Pulpitis|20230320143116|PD|||||||||
"""

# segments = []
# fields = []
# def analyzer(message):
# 	_segment = {}
# 	_field = {}
# 	segment = ""
# 	field = ""
# 	for ch in message:
# 		if ch == "\n":
# 			segments.append(segment)
# 			segment = ""
# 		else:
# 			segment += ch
# 			if(ch == "|"):
# 				fields.append(field)
# 				field = ""
# 			else:
# 				field += ch


# analyzer(hl7Message)
# for segment in segments:
# 	print(segment)

# for field in fields:
# 	print(field)


separators ={
    "|": None, 
	"^": None, 
	"~": None, 
	"&": None, 
	"\\": None
}
msg = {}

def analyzer(message, pos, length):
	currentSegmentPosition = 0
	currentFieldPosition = 0
	currentSubFieldPosition = 0
	currentSegment = msg[currentSegmentPosition] = {}
	field = ""
	for pos in range(pos, length):
		ch = message[pos]
		if ch == "|":
			currentSegment[currentFieldPosition] = field
			currentFieldPosition += 1
			field = ""
		# if ch == "^":
		# 	currentSegment[currentFieldPosition] = {}
		# 	currentFieldPosition += 1
		# 	field = ""
		elif ch == "\r\n":
			currentSegment[currentFieldPosition] = field
			currentFieldPosition = 0
			field = ""
			currentSegmentPosition += 1
			currentSegment = msg[currentSegmentPosition] = {}
		else:
			field += ch

length = len(hl7Message)
analyzer(hl7Message, 0, length)

import json
pretty = json.dumps(msg, indent=4)
print(pretty)

separators = {
	# "": "\n", 
	# "\n": "|",
	"": "$", 
	"$": "|",
	"|": "^", 
	"^": "&", 
	"&": None
}

class AKE:
	pos = 0
	startPos = 0
	
# def piece(message, length, end_delimiter):
# 	block = {}
# 	field = ""
# 	fieldPosition = 0
# 	delimiter = separators[end_delimiter]
# 	sub_delimiter = separators[delimiter]
# 	#for pos in range(pos, length):
# 	while(AKE.pos < length):
# 		ch = message[AKE.pos]
# 		#print(AKE.pos, ch)
# 		AKE.pos += 1
# 		if(ch == sub_delimiter):
# 			AKE.pos = AKE.startPos
# 			block[fieldPosition] = piece(message, length, delimiter)
# 			field = ""
# 			fieldPosition += 1
# 		elif(ch == end_delimiter):
# 			block[fieldPosition] = field
# 			return block
# 		elif(ch == delimiter):
# 			AKE.startPos = AKE.pos
# 			block[fieldPosition] = field
# 			fieldPosition += 1
# 			field = ""
# 		else:
# 			field += ch
# 			#print(field)
# 	print(block)
# 	return block

# def piece(message, length, delimiter, end_delimiters):
# 	block = {}
# 	field = ""
# 	fieldPosition = 0
# 	sub_delimiter = separators[delimiter]
# 	#for pos in range(pos, length):
# 	while(AKE.pos < length):
# 		ch = message[AKE.pos]
# 		#print(AKE.pos, ch)
# 		AKE.pos += 1
# 		if(ch == sub_delimiter):
# 			AKE.pos = AKE.startPos
# 			_end_delimiters = end_delimiters + [delimiter]
# 			block[fieldPosition] = piece(message, length, sub_delimiter, _end_delimiters)
# 			field = ""
# 			fieldPosition += 1
# 		elif(ch in end_delimiters):
# 			block[fieldPosition] = field
# 			return block
# 		elif(ch == delimiter):
# 			AKE.startPos = AKE.pos
# 			block[fieldPosition] = field
# 			fieldPosition += 1
# 			field = ""
# 		else:
# 			field += ch
# 			#print(field)
# 	print(block)
# 	return block

def piece(message, length, delimiter):
	block = {}
	field = ""
	fieldPosition = 0
	sub_delimiter = separators[delimiter]
	#for pos in range(pos, length):
	while(AKE.pos < length):
		ch = message[AKE.pos]
		#print(AKE.pos, ch)
		AKE.pos += 1
		if(ch == sub_delimiter):
			AKE.pos = AKE.startPos
			_end_delimiters = end_delimiters + [delimiter]
			block[fieldPosition] = piece(message, length, sub_delimiter)
			field = ""
			fieldPosition += 1
		elif(ch in end_delimiters):
			block[fieldPosition] = field
			return block
		elif(ch == delimiter):
			AKE.startPos = AKE.pos
			block[fieldPosition] = field
			fieldPosition += 1
			field = ""
		else:
			field += ch
			#print(field)
	print(block)
	return block

aaa = """MSH|DXCEM|A1|OHCAPPL|A1|20230320143118||ORM^O01|147626918|P|2.4|||AL||"""
#block = piece(aaa, len(aaa), "\n")
hl7Message = """MSH|731^Ahmed&Kamal&ELSaman|$PID|||A100035537|"""
block = piece(hl7Message, len(hl7Message), "$", ["$"])

pretty = json.dumps(block, indent=4)
print(pretty)

#start analyzer
#new segment
#new field(message, pos, segment)
#new subField(message, pos, field)
#if ch  in ["|", "\r"]: return pos
#else: keep field

#start analyzer
#if $: new field
#if |: sub field

hl7Message = """MSH|731^Ahmed&Kamal&ELSaman|$PID|||A100035537|"""

#00: start
#03: |
#08: ^
#14: &
#20: &
#28: |
#29: $
#33: |

