from .wallmartclass import Wallmart
from .validation import Validation
from .main import WallMartTemplate

indexmap = {
    "Sr.No": 1,
    "Artical": 2,
    "Article Description": [3, 4],
    "HSN": 5,
    "EAN": 6,
    "Quantity Ordered": 7,
    "UOM": 8,
    "Pack": 9,
    "MRP": 10,
    "Cost": 11,
    "Line Cost Excl Tax": 12,
    "Tax Details": [13, 14, 15],
}

validation1 = {
    "Artical": r"^#\d{5}$",
    "EAN": r"^#\d{13}$",
    "Cost": r"[+-]?[0-9]+\.[0-9]+",
    "MRP": r"^\d+(\.\d{2})?\/EA$",
}

errortypes = {
    1: {
        "initialerrorpoint": "Article Description",
        "errortype": "formetting",
        "identificationprams": {"validation": r"^#\d\+\#\+[A-Z ]+$"},
    },
    2: {
        "initialerrorpoint": "Article Description",
        "errortype": "formetting",
        "identificationprams": {
            "validation": r"^#[A-Z ]+?[0-9]?[A-Z]?[0-9][A-Z]?\+\#\+[0-9]+$"
        },
    },
    3: {
        "initialerrorpoint": "Article Description",
        "errortype": "formetting",
        "identificationprams": {
            "validation": r"^#[A-Z ]+?[0-9]?[A-Z]?[0-9][0-9 ][0-9][A-Z]?\+\#\+[0-9]+$"
        },
    },
    4: {
        "initialerrorpoint": "MRP",
        "errortype": "formetting",
        "identificationprams": {"validation": r"^\d+(\.\d{2})?/$"},
    },
    5: {
        "initialerrorpoint": "Article Description",
        "errortype": "formetting",
        "identificationprams": {"validation": r"^\d#\d{5}$"},
    },
    6: {
        "initialerrorpoint": "Article Description",
        "errortype": "formetting",
        "identificationprams": {"validation": r"^#\d{8}#\d{13}$"},
    },
    7: {
        "initialerrorpoint": "HSN",
        "errortype": "formetting",
        "identificationprams": {"validation": r"^\d$"},
    },
    8: {
        "initialerrorpoint": "MRP",
        "errortype": "formetting",
        "identificationprams": {
            "validation": r"^[0-9]+\.[0-9]{2}\/[A-Z]{2}[0-9]+\.[0-9]{2}$"
        },
    },
    9: {
        "initialerrorpoint": "Article Description",
        "errortype": "formetting",
        "identificationprams": {"validation": r"#\d\+\#\d{13}\+"},
    },
    10: {
        "initialerrorpoint": "Article Description",
        "errortype": "formetting",
        "identificationprams": {"validation": r"^#\d\+\#[A-Z ]+$"},
    },
    11: {
        "initialerrorpoint": "Line Cost Excl Tax",
        "errortype": "formetting",
        "identificationprams": {"validation": r"^\d+\.\d{2} IN$"},
    },
    12: {
        "initialerrorpoint": "Article Description",
        "errortype": "formetting",
        "identificationprams": {"validation": r"^#\d\+\#[A-Z ]+$"},
    },
    13: {
        "initialerrorpoint": "Cost",
        "errortype": "formetting",
        "identificationprams": {"validation": r"^\d{4}\.\d{2}$"},
    },
}

subset = [
    "EAN",
    "Artical",
    "HSN",
    "Pack",
    "PURCHASE ORDER NO",
    "Total Amount incl tax",
    "Quantity Ordered",
    "Pack",
]

import json

fixtures = None


__all__ = [
    "fixtures",
    "subset",
    "errortypes",
    "validation1",
    "indexmap",
    "Wallmart",
    "Validation",
    "WallMartTemplate",
]
