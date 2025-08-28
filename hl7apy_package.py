from hl7apy.parser import parse_message

# hl7 = open("hl7.txt", "r").read()
# msg = parse_message(hl7)
# print(msg.children)

# from hl7apy import set_default_version
# set_default_version("2.5")

# from hl7apy.core import Message
# m = Message("ADT_A01", version="2.5")

message = r"""MSH|^~\&|AppA|FacA|AppB|FacB|202508231630||ADT^A01|MSG123|P|2.5
PID|1||123456^^^HOSP^MR~789012^^^CLINIC^PI||Doe^John^A&Junior||19800101|M
OBX|1|TX|TEST^BloodTest||Normal\R\Value~Abnormal\T\Value|N"""

import timeit
t = timeit.timeit(
	stmt=lambda: parse_message(message, validation_level=None, find_groups=False),
	number=10000  # how many times to run
)
print(f"Execution time: {t:.6f} seconds")

# python3 hl7apy_package.py