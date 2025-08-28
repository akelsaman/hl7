class HL7Subcomponent(str):
    pass


class HL7Component(list):
    """A component holds subcomponents."""
    def __repr__(self):
        return f"Comp({super().__repr__()})"


class HL7Repetition(list):
    """A repetition holds components."""
    def __repr__(self):
        return f"Rep({super().__repr__()})"


class HL7Field(list):
    """A field holds repetitions."""
    def __repr__(self):
        return f"Field({super().__repr__()})"


class HL7Segment(list):
    """A segment holds fields."""
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __repr__(self):
        return f"Segment({self.name}, {super().__repr__()})"


class HL7Message(list):
    """The HL7 message holds segments."""
    def __repr__(self):
        return f"Message({super().__repr__()})"


# ---------- Parser (O(n) scanner) ----------
def parse_hl7(raw: str) -> HL7Message:
    msg = HL7Message()

    segment = None
    field = HL7Field()
    rep = HL7Repetition()
    comp = HL7Component()
    buf = []

    def flush_sub():
        nonlocal buf, comp
        if buf or not comp:
            comp.append(HL7Subcomponent("".join(buf)))
        buf = []

    def flush_comp():
        nonlocal comp, rep
        flush_sub()
        rep.append(comp)
        comp = HL7Component()

    def flush_rep():
        nonlocal rep, field
        flush_comp()
        field.append(rep)
        rep = HL7Repetition()

    def flush_field():
        nonlocal field, segment
        flush_rep()
        segment.append(field)
        field = HL7Field()

    def flush_segment():
        nonlocal segment, msg
        flush_field()
        msg.append(segment)

    for ch in raw:
        if ch == "|":
            flush_field()
        elif ch == "~":
            flush_rep()
        elif ch == "^":
            flush_comp()
        elif ch == "&":
            flush_sub()
        elif ch == "\n":
            flush_segment()
            segment = None
        else:
            buf.append(ch)
            # initialize segment name (first field)
            if segment is None and len(buf) == 3:
                segment = HL7Segment("".join(buf))
                buf = []

    # flush at end
    if segment:
        flush_segment()

    return msg

# raw = "MSH|^~\\&|App1|Fac1\rPID|1||12345^^^HOSP^MR||Doe^John^A&Robert"
# raw = """MSH|^~\\&|1||123456^^^HOSP^MR~789012^^^CLINIC^PI||Doe^John^A&Junior||19800101|M"""
raw = """MSH|^~\\&|AppA|FacA|AppB|FacB|202508231630||ADT^A01|MSG123|P|2.5
PID|1||123456^^^HOSP^MR~789012^^^CLINIC^PI||Doe^John^A&Junior||19800101|M
OBX|1|TX|TEST^BloodTest||Normal\R\Value~Abnormal\T\Value|N"""

raw = """MSH|^~\&|12747|12747|CRELIO|CRELIO|20240529153012||ORM^O01|Q106013102T122699578||2.3||||||8859/1
PID|1|999999999^^^RRL MRN^MRN|999999999^^^RRL MRN^MRN||ZZZTEST^RRLM^||19880809|Male||National||||||||99999999999^^^RRL FIN^FIN
NBR|9999999999||||||0|||Saudi
PV1|1|Outpatient|RRL^^^RRL^^Ambulatory(s)^RRL||||DEMOPHYSVASCSURG^Physician^Vascular^Cerner^^MD^^^External Id^Personnel^^^External Identifier~11724009^Physician^Vascular^Cerner^^MD^^^PROVIDER_MESSAGING^Personnel^^^Messaging|||Laboratory|||||||DEMOPHYSVASCSURG^Physician^Vascular^Cerner^^MD^^^External Id^Personnel^^^External Identifier~11724009^Physician^Vascular^Cerner^^MD^^^PROVIDER_MESSAGING^Personnel^^^Messaging|Laboratory||Self Pay|||||||||||||||||||RRL||Active|||20240529134900
ORC|SC|309901965^HNAM_ORDERID|||In-Lab||||20240529153000|SYSTEMSYSTEM^SYSTEM^SYSTEM^Cerner^^^^^External Id^Personnel^^^External Identifier||3332057^Bolous^Medhat^Cerner^^^^^PROVIDER_MESSAGING^Personnel^^^Messaging~CERNERDRMEDGROUP10^Bolous^Medhat^Cerner^^^^^External Id^Personnel^^^External Identifier|||20240529153010||||SYSTEMSYSTEM^SYSTEM^SYSTEM^Cerner^^^^^External Id^Personnel^^^External Identifier
OBR|1|309901965^HNAM_ORDERID||350020^F11 Buckwheat|||20240529152400|||CERNERCERN473^Bhat^Rohit^Cerner^^^^^External Id^Personnel^^^External Identifier~11648100^Bhat^Rohit^Cerner^^^^^PROVIDER_MESSAGING^Personnel^^^Messaging|O|||20240529152400|Blood&Blood^^^^^Venous Draw|3332057^Bolous^Medhat^Cerner^^^^^PROVIDER_MESSAGING^Personnel^^^Messaging~CERNERDRMEDGROUP10^Bolous^Medhat^Cerner^^^^^External Id^Personnel^^^External Identifier||||000112024150000004^HNA_ACCN~4531502^HNA_ACCNID||20240529153010||General Lab|||1^^0^20240529152400^^RT~^^^^^RT - Routine|||||||||20240529152400||||||||||Laboratory^Laboratory^^Immunology^Immunology"""

# msg = parse_hl7(raw)
		
import timeit
t = timeit.timeit(
    stmt=lambda: parse_hl7(raw),
    number=10000  # how many times to run
)
print(f"Execution time: {t:.6f} seconds")

msg = parse_hl7(raw)
# Print parsed tree
print(msg)

# python3 chatgpt_parser.py