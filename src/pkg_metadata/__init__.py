__version__ = "0.1"

FIELDS = [
    # (Name, Multiple-Use)
    ("Metadata-Version", False),
    ("Name", False),
    ("Version", False),
    ("Dynamic", True),
    ("Platform", True),
    ("Supported-Platform", True),
    ("Summary", False),
    ("Description", False),
    ("Description-Content-Type", False),
    ("Keywords", False),
    ("Home-page", False),
    ("Download-URL", False),
    ("Author", False),
    ("Author-email", False),
    ("Maintainer", False),
    ("Maintainer-email", False),
    ("License", False),
    ("Classifier", True),
    ("Requires-Dist", True),
    ("Requires-Python", False),
    ("Requires-External", True),
    ("Project-URL", True),
    ("Provides-Extra", True),
    ("Provides-Dist", True),
    ("Obsoletes-Dist", True),
]

def json_name(name):
    return name.lower().replace("-", "_")

@dataclass
class Metadata:
    def __init__(self):
        pass

    @classmethod
    def from_pkginfo(cls, msg):
        self = cls()
        for field, multi in FIELDS:
            if multi:
                val = msg.get_all(field)
            else:
                val = msg.get(field)

        # Special processing
        if field == "Keywords":
            if "," in val:
                val = [v.strip() for v in val.split(",")]
            else:
                val = val.split()

        # TODO: What if both description and payload are present?
        if field == "Description" and val is None:
            val = msg.get_payload()

        # Convert list to tuple for val? None handling?
        setattr(self, json_name(field)) = val

        return self

    @classmethod
    def from_json(cls, data):
        self = cls()
        for field, multi in FIELDS:
            name = json_name(field)
            if name in data:
                setattr(self, name, data[name])
        return self

    def to_pkginfo(self):
        msg = email.message.Message()
        for field, multi in FIELDS:
            val = getattr(self, json_name(field))

            # Special processing
            if field == "Keywords":
                val = ",".join(val)

            if field == "Description":
                msg.set_payload(val)
        
            if multi:
                for v in val:
                    msg[field] = v
            else:
                msg[field] = val

    def to_json(self):
        data = {}
        for field, multi in FIELDS:
            name = json_name(field)
            data[name] = getattr(self, name)

        return data
