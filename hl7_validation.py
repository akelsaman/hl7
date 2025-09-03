from hl7_standard_versions.hl7_v2_3 import *

for segment in hl7_v2_3:
    # print(hl7_v2_3[segment]['ake_segment']['longName'])
    fields = hl7_v2_3[segment]['ake_segment']['ake_fields']
    for field in fields:
        id = fields[field]['id']
        name = fields[field]['name']
        print(f"{id}: {name}")
    # hl7_v2_3[segment]['ake_segment']