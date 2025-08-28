# In HL7 v2.x messages, delimiters are special characters that separate parts of the message (segments, fields, components, etc.).
# They are defined at the very beginning of the message, in the MSH (Message Header) segment:

# Segment delimiter: Carriage return (\r, ASCII 13).
# 	Each segment (MSH, PID, OBR, etc.) ends with a carriage return.
# Field delimiter: | (pipe).
# 	Separates fields in a segment.
# Component delimiter: ^ (caret).
# 	Separates components within a field.
# Subcomponent delimiter: & (ampersand).
# 	Separates subcomponents within a component.
# Repetition delimiter: ~ (tilde).
# 	Used when a field can repeat values.
# Escape character: \ (backslash).
# 	Used to escape special characters inside fields.
# ====================
# message = """MSH|731^Ahmed&Kamal&ELSaman|$PID|||A100035537|"""
message = """MSH|731^Ahmed&Kamal&ELSaman|||A100035537|"""
# message = """
# MSH|^~\&|AppA|FacA|AppB|FacB|202508231630||ADT^A01|MSG123|P|2.5
# PID|1||123456^^^HOSP^MR~789012^^^CLINIC^PI||Doe^John^A&Junior||19800101|M
# OBX|1|TX|TEST^BloodTest||Normal\R\Value~Abnormal\T\Value|N
# """

#00: start
#03: |
#08: ^
#14: &
#20: &
#28: |
#29: $
#33: |

separators = {
	"|": "^&", 
	"^": "&"
}

doc = {}
length = len(message)

class AKE:
	pos = 0

def subField(message, i, length, delimiter, doc, segment, parentField):
	field = None
	fieldPosition = 1
	for pos in range(i, length):
		ch = message[pos]
		#print(ch, pos)
		pos += 1
		if(ch == "^"):
			#new field
			parentField[fieldPosition] = field
			fieldPosition += 1
			field = None
		elif(ch == "|"):
			parentField[fieldPosition] = field
			return pos
		elif(ch == "&"):
			pass
		elif(ch == "$"):
			segmentCode = message[pos:pos+3]
			segment = doc[segmentCode] = {}
		else:
			try: field += ch
			except: field = ch

def field(message, i, length, delimiter, doc, segment):
	field = None
	fieldPosition = 0
	for pos in range(i, length):
		ch = message[pos]
		#print(ch, pos)
		pos += 1
		if(ch == "|"):
			#new field
			segment[fieldPosition] = field
			fieldPosition += 1
			field = None
		elif(ch in ["^"]):
			_field = segment[fieldPosition] = {0: field}
			pos = subField(message, pos, length, delimiter, doc, segment, _field)
			fieldPosition += 1
			field = None
		elif(ch == "$"):
			segmentCode = message[pos:pos+3]
			segment = doc[segmentCode] = {}
		else:
			try: field += ch
			except: field = ch

segment = doc["MSH"] = {}
field(message, 0, length, "|", doc, segment)
print(doc)
#add to field

#why segment and field are different ?
#Because their delimiter will be treated diffrently
#resulting in two different outcomes
#$ : create new object (segment)
#| : create new field