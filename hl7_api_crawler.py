import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
import json
from datetime import datetime

def get_segments():
	options = Options()
	options.add_argument("--headless")
	driver = webdriver.Chrome(options=options)

	url = "https://hl7-definition.caristix.com/v2/HL7v2.3/Segments"  # replace with your URL
	driver.get(url)

	# Find the virtual scroll container
	viewport = driver.find_element(By.CSS_SELECTOR, "cdk-virtual-scroll-viewport")

	links = set()
	last_count = 0

	# https://chatgpt.com/s/t_68acf0348a30819185feb868e0bf717e # how it works
	while True:
		# Collect currently visible links
		anchors = viewport.find_elements(By.TAG_NAME, "a")
		for a in anchors:
			href = a.get_attribute("href")
			if href:
				links.add(href)

		# Scroll down inside the viewport
		driver.execute_script("arguments[0].scrollBy(0, 500);", viewport)
		time.sleep(1)  # allow new items to load

		# Stop when no new links are found
		if len(links) == last_count:
			break
		last_count = len(links)

	print("Total links found:", len(links))
	for link in links:
		print(link)

	driver.quit()

# get_segments()
#================================================================================
# https://chatgpt.com/s/t_68acef5720388191ab357ea1880766cd # if authentication needed

headers = {
	"User-Agent": "Mozilla/5.0",  # mimic browser if needed
	"Accept": "application/json"
}

def call_api(url):
	response = requests.get(url, headers=headers)

	if response.status_code == 200:
		data = response.json()  # parse JSON directly
		return data
	else:
		print("Error:", response.status_code)

# data = call_api("https://hl7-definition.caristix.com/v2-api/1/HL7v2.3/Segments")
# print("Items:", data)
#----------------------------------------
def writeToPythonFile(data, timestamp, pattern="hl7"):
	# # tickets = tickets.replace('[]', 'None')
	# tickets = tickets.replace('null', 'None')
	# tickets = tickets.replace('true', 'True')
	# tickets = tickets.replace('false', 'False')

	f = open(f'{pattern}_{timestamp}.py', 'a')
	f.write(data)
	f.close()
#----------------------------------------
visited_fields = {}
def getField(fieldName):
	field = call_api(f"{fieldsURL}/{fieldName}")

	if field:
		if "id" in field:
			if "fields" in field:
				if( type(field["fields"]) == list):
					pass
				else:
					writeToPythonFile(f"Error: {fieldName}: fields is not a list.\n", "log", pattern=hl7_version)
					return field
			else:
				writeToPythonFile(f"Error: {fieldName}: fields is not exists.\n", "log", pattern=hl7_version)
				return field
		else:
			writeToPythonFile(f"Error: {fieldName}: id field is not exists.\n", "log", pattern=hl7_version)
			return field
	else:
		writeToPythonFile(f"Error: {fieldName}: is None.\n", "log", pattern=hl7_version)
		return field

	id = field['id']
	fields = field['fields']
	field['ake_fields'] = {}
	for subField in fields:
		subFieldID = subField['id']
		print(f"{id}: {subFieldID}")
		writeToPythonFile(f"{id}: {subFieldID}\n", "log", pattern=hl7_version)
		if subFieldID == id or subFieldID in visited_fields:
			writeToPythonFile(f"Error: {subFieldID}: Infinite recursive/Self referencing.\n", "log", pattern=hl7_version)
			break
		else:
			field['ake_fields'][subFieldID] = getField(subFieldID)
			visited_fields[subFieldID] = None
	return field
# data = getField('PID.4')
# # print(data)
# writeToPythonFile(data)
#----------------------------------------
def getSegment(segment):
	print(segment)
	segment = call_api(f"{segmentsURL}/{segment}")
	fields = segment['fields']
	segment['ake_fields'] = {}
	for field in fields:
		fieldID = field['id']
		segment['ake_fields'][fieldID] = getField(fieldID)
	return segment

# data = getSegment('PID')
# # print(data)
# writeToPythonFile(data)
#----------------------------------------
hl7_version = "2.5"
segmentIndex = 0
#----------------------------------------
# url = "https://hl7-definition.caristix.com/v2-api/1/HL7v2.3/Segments/PID"
# url = "https://hl7-definition.caristix.com/v2-api/1/HL7v2.3/Fields/PID.4.1"
fieldsURL = f"https://hl7-definition.caristix.com/v2-api/1/HL7v{hl7_version}/Fields"
segmentsURL = f"https://hl7-definition.caristix.com/v2-api/1/HL7v{hl7_version}/Segments"
#----------------------------------------
# segments = [
# 	{'id': 'MSH'}, 
# 	{'id': 'MSA'}
# ]
timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

segments = call_api(segmentsURL)
segments = segments[segmentIndex:]
for segment in segments:
	segmentID = segment['id']
	segment['ake_segment'] = getSegment(segmentID)
	segment = json.dumps(segment, indent='\t')
	segment = str(segment)
	writeToPythonFile(f'"{segmentID}": {segment}, \n', timestamp, pattern=f"hl7_v{hl7_version}")
	print(segmentIndex)
	segmentIndex += 1
#================================================================================
# https://chatgpt.com/s/t_68acef9fff148191a83a468f22159768 # write to parquet table
#================================================================================
# field = {'id': 'PID.4', 'type': 'Field', 'position': 'PID.4', 'name': 'Alternate Patient ID', 'length': 20, 'usage': 'O', 'rpt': '*', 'dataType': 'CX', 'dataTypeName': 'Extended Composite ID With Check Digit', 'tableId': None, 'tableName': None, 'description': 'This field contains the alternate, temporary, or pending optional patient identifier to be used if needed  - or additional  numbers that may be required to identify a patient.  This field may be used to convey multiple patient IDs when more than one exist for a patient. Possible contents might include a visit number, a visit date, or a Social Security Number', 'sample': '', 'fields': []}
# component = {'id': 'PID.4.4', 'type': 'Component', 'position': 'PID.4.4', 'length': 0, 'dataType': 'HD', 'dataTypeName': 'Hierarchic Designator', 'usage': 'O', 'rpt': '1', 'tableId': None, 'tableName': None, 'name': 'Assigning Authority', 'description': 'The assigning authority is a unique name of the system that creates the data.  It is an HD data type.  It is equivalent to the application ID of the placer or filler order number (see Chapter 4).  Assigning authorities are unique across a given HL7 implementation. '}
# component = {'id': 'PID.4.4', 'type': 'Component', 'position': 'PID.4.4', 'name': 'Assigning Authority', 'length': 0, 'usage': 'O', 'rpt': '1', 'dataType': 'HD', 'dataTypeName': 'Hierarchic Designator', 'tableId': None, 'tableName': None, 'description': 'The assigning authority is a unique name of the system that creates the data.  It is an HD data type.  It is equivalent to the application ID of the placer or filler order number (see Chapter 4).  Assigning authorities are unique across a given HL7 implementation. ', 'sample': '', 'fields': []}

# Field attributes:
# ['id', 'type', 'position', 'name', 'length', 'usage', 'rpt', 'dataType', 'dataTypeName', 'tableId', 'tableName', 'description', 'sample', 'fields']
# Component attributes:
# ['id', 'type', 'position', 'length', 'dataType', 'dataTypeName', 'usage', 'rpt', 'tableId', 'tableName', 'name', 'description']
#================================================================================