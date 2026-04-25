from typing import Literal

# Default node dimensions (width, height) matching Unity prefabs - for full serialization format
NODE_SIZES = {
    "String": (256, 64),
    "Float": (256, 64),
    "Color": (256, 64),
    "Country": (256, 64),
    "Bool": (256, 64),
    "ModularCarController": (192, 160),
    "UniformModularCarProperties": (192, 288),
    "Spherecast": (256, 64),
    "CarRaycasts": (192, 160),
    "HitInfo": (256, 64),
    "ParkingGetFloat": (320, 64),
    "ParkingGetBool": (320, 64),
    "ParkingGetTransform": (320, 64),
    "DemoDerbyGetTransform": (320, 64),
    "DemoDerbyGetCar": (320, 64),
    "GetCarPart": (320, 64),
    "CarInfo": (192, 224),
    "Autosteer": (192, 160),
    "Autothrottle": (192, 160),
    "GetCarFromTransform": (256, 64),
    "ConstructSurvivalProperties": (192, 288),
    "ConstructVector3": (256, 160),
    "CompareFloats": (256, 160),
    "CompareBool": (256, 160),
    "SurvivalGetFloat": (320, 64),
    "SurvivalGetBool": (320, 64),
    "SurvivalState": (256, 64),
    "ConditionalSetSurvivalState": (256, 288),
    "ConditionalSetSurvivalEmote": (256, 288),
    "SurvivalAutoPosition": (256, 64),
    "SurvivalEmote": (256, 64),
    "SurvivalController": (192, 160),
    "Relay": (32, 32),
    "AddFloats": (256, 64),
    "SubtractFloats": (256, 64),
    "MultiplyFloats": (256, 64),
    "DivideFloats": (256, 64),
    "Not": (256, 64),
    "Modulo": (256, 64),
    "Operation": (256, 64),
    "GetVariable": (256, 64),
    "SetVariable": (256, 64),
    "IsNull": (256, 64),
    "Region": (256, 224),
}
DEFAULT_NODE_SIZE = (256, 64)

# Node types that serialize size/color per NodeTypeDataSO (e.g. Region has user-resizable dimensions)
SERIALIZE_SIZE_DELTA_NODES = {"Region"}
SERIALIZE_COLOR_NODES = {"Region"}

# Default colors matching Unity (RGBA 0-1)
DEFAULT_NODE_COLOR = {"r": 0.21960784494876862, "g": 0.21960784494876862, "b": 0.21960784494876862, "a": 1}
DEFAULT_CONNECTION_COLOR = {"r": 0.98, "g": 0.94, "b": 0.84, "a": 1}
CAP_COLOR = {"r": 1, "g": 0.81, "b": 0.3, "a": 1}

outputs = {
    "AddVector3": "Vector3",
    "AddFloats": float,
    "Bool": bool,
    "ClampFloat": float,
    "Color": float,
    "UniformModularCarProperties": None,
    "ModularCarController": None,
    "ConstructVector3": "Vector3",
    "CompareBool": bool,
    "CompareFloats": bool,
    "ConditionalSetFloatV2": float,
    "ConditionalSetVector3": "Vector3",
    "ConstructSlimeProperties": None,
    "SlimeController": None,
    "Spherecast": "Spherecast",
    "CarRaycasts": "RaycastHit",
    "HitInfo": "Any",
    "Country": "Country",
    "CrossProduct": "Vector3",
    "Debug": None,
    "DebugDrawLine": None,
    "DebugDrawDisc": None,
    "Distance": float,
    "DivideFloats": float,
    "DotProduct": float,
    "Float": float,
    "VolleyballGetBool": bool,
    "VolleyballGetFloat": float,
    "VolleyballGetTransform": "Transform",
    "SlimeGetVector3": "Vector3",
    "Magnitude": float,
    "Modulo": float,
    "MultiplyFloats": float,
    "Not": bool,
    "Normalize": "Vector3",
    "Operation": float,
    "RelativePosition": "Vector3",
    "RandomFloat": float,
    "ScaleVector3": "Vector3",
    "Vector3Split": float,
    "Stat": "Stat",
    "String": str,
    "SubtractFloats": float,
    "SubtractVector3": "Vector3",
    "ConditionalSetBool": bool,
    "ConditionalSetSurvivalEmote": "SurvivalEmote",
    "ConditionalSetSurvivalState": "SurvivalState",
    "ConstructSurvivalProperties": None,
    "GetVariable": "Any",
    "IsNull": bool,
    "Keypress": bool,
    "Region": None,
    "Relay": "Any",
    "SetVariable": None,
    "SurvivalAutoPosition": "Vector3",
    "SurvivalController": None,
    "SurvivalEmote": "SurvivalEmote",
    "SurvivalGetBool": bool,
    "SurvivalGetFloat": float,
    "SurvivalGetTransform": "Transform",
    "SurvivalState": "SurvivalState",
    "TimePlot": None,
    "ParkingGetFloat": float,
    "ParkingGetBool": bool,
    "ParkingGetTransform": "Transform",
    "DemoDerbyGetTransform": "Transform",
    "DemoDerbyGetCar": "Car",
    "GetCarPart": "Transform",
    "CarInfo": "Vector3",
    "Autosteer": float,
    "Autothrottle": float,
    "GetCarFromTransform": "Car",
}

ports = {
    "AddVector3": [
        {"id": "Vector31", "polarity": 0},
        {"id": "Vector32", "polarity": 0},
        {"id": "Vector31", "polarity": 1}
    ],
    "AddFloats": [
        {"id": "Float1", "polarity": 1},
        {"id": "Float2", "polarity": 0},
        {"id": "Float1", "polarity": 0}
    ],
    "Bool": [
        {"id": "Bool1", "polarity": 1}
    ],
    "ClampFloat": [
        {"id": "Float3", "polarity": 0},
        {"id": "Float1", "polarity": 1},
        {"id": "Float2", "polarity": 0},
        {"id": "Float1", "polarity": 0}
    ],
    "Color": [
        {"id": "Color1", "polarity": 1}
    ],
    "ConstructVector3": [
        {"id": "Vector31", "polarity": 1},
        {"id": "Float3", "polarity": 0},
        {"id": "Float1", "polarity": 0},
        {"id": "Float2", "polarity": 0}
    ],
    "CompareBool": [
        {"id": "Bool1", "polarity": 1},
        {"id": "Bool2", "polarity": 0},
        {"id": "Bool1", "polarity": 0}
    ],
    "CompareFloats": [
        {"id": "Bool1", "polarity": 1},
        {"id": "Float1", "polarity": 0},
        {"id": "Float2", "polarity": 0}
    ],
    "ConditionalSetFloatV2": [
        {"id": "Float1", "polarity": 0},
        {"id": "Float2", "polarity": 0},
        {"id": "Float1", "polarity": 1},
        {"id": "Bool1", "polarity": 0}
    ],
    "ConditionalSetVector3": [
        {"id": "Bool1", "polarity": 0},
        {"id": "Vector31", "polarity": 0},
        {"id": "Vector32", "polarity": 0},
        {"id": "Vector31", "polarity": 1}
    ],
    "ConstructSlimeProperties": [
        {"id": "String1", "polarity": 0},
        {"id": "Color1", "polarity": 0},
        {"id": "Country1", "polarity": 0},
        {"id": "Stat1", "polarity": 0},
        {"id": "Stat2", "polarity": 0},
        {"id": "Stat3", "polarity": 0}
    ],
    "SlimeController": [
        {"id": "Bool1", "polarity": 0},
        {"id": "Vector31", "polarity": 0}
    ],
    "Country": [
        {"id": "Country1", "polarity": 1}
    ],
    "CrossProduct": [
        {"id": "Vector32", "polarity": 0},
        {"id": "Vector31", "polarity": 0},
        {"id": "Vector3", "polarity": 1}
    ],
    "Debug": [
        {"id": "Any1", "polarity": 0}
    ],
    "DebugDrawLine": [
        {"id": "Vector31", "polarity": 0},
        {"id": "Vector32", "polarity": 0},
        {"id": "Float1", "polarity": 0},
        {"id": "Color1", "polarity": 0}
    ],
    "DebugDrawDisc": [
        {"id": "Float1", "polarity": 0},
        {"id": "Color1", "polarity": 0},
        {"id": "Vector31", "polarity": 0},
        {"id": "Float2", "polarity": 0}
    ],
    "Distance": [
        {"id": "Vector32", "polarity": 0},
        {"id": "Float1", "polarity": 1},
        {"id": "Vector31", "polarity": 0}
    ],
    "DivideFloats": [
        {"id": "Float1", "polarity": 1},
        {"id": "Float2", "polarity": 0},
        {"id": "Float1", "polarity": 0}
    ],
    "DotProduct": [
        {"id": "Vector31", "polarity": 0},
        {"id": "Vector32", "polarity": 0},
        {"id": "Float1", "polarity": 1}
    ],
    "Float": [
        {"id": "Float1", "polarity": 1}
    ],
    "VolleyballGetBool": [
        {"id": "Bool1", "polarity": 1}
    ],
    "VolleyballGetFloat": [
        {"id": "Float1", "polarity": 1}
    ],
    "VolleyballGetTransform": [
        {"id": "Transform1", "polarity": 1}
    ],
    "SlimeGetVector3": [
        {"id": "Vector31", "polarity": 1}
    ],
    "Magnitude": [
        {"id": "Vector31", "polarity": 0},
        {"id": "Float1", "polarity": 1}
    ],
    "Modulo": [
        {"id": "Float1", "polarity": 0},
        {"id": "Float2", "polarity": 0},
        {"id": "Float1", "polarity": 1}
    ],
    "MultiplyFloats": [
        {"id": "Float1", "polarity": 1},
        {"id": "Float2", "polarity": 0},
        {"id": "Float1", "polarity": 0}
    ],
    "Not": [
        {"id": "Bool1", "polarity": 1},
        {"id": "Bool1", "polarity": 0}
    ],
    "Normalize": [
        {"id": "Vector31", "polarity": 0},
        {"id": "Vector31", "polarity": 1}
    ],
    "Operation": [
        {"id": "Float1", "polarity": 1},
        {"id": "Float1", "polarity": 0}
    ],
    "RelativePosition": [
        {"id": "Transform1", "polarity": 0},
        {"id": "Vector31", "polarity": 1}
    ],
    "RandomFloat": [
        {"id": "Float1", "polarity": 0},
        {"id": "Float1", "polarity": 1},
        {"id": "Float2", "polarity": 0}
    ],
    "ScaleVector3": [
        {"id": "Float1", "polarity": 0},
        {"id": "Vector31", "polarity": 1},
        {"id": "Vector31", "polarity": 0}
    ],
    "Vector3Split": [
        {"id": "Vector31", "polarity": 0},
        {"id": "Float1", "polarity": 1},
        {"id": "Float2", "polarity": 1},
        {"id": "Float3", "polarity": 1}
    ],
    "Stat": [
        {"id": "Stat1", "polarity": 1}
    ],
    "String": [
        {"id": "String1", "polarity": 1}
    ],
    "SubtractFloats": [
        {"id": "Float2", "polarity": 0},
        {"id": "Float1", "polarity": 0},
        {"id": "Float1", "polarity": 1}
    ],
    "SubtractVector3": [
        {"id": "Vector31", "polarity": 0},
        {"id": "Vector31", "polarity": 1},
        {"id": "Vector32", "polarity": 0}
    ],
    "ConditionalSetBool": [
        {"id": "Bool1", "polarity": 0},
        {"id": "Bool2", "polarity": 0},
        {"id": "Bool3", "polarity": 0},
        {"id": "Bool1", "polarity": 1}
    ],
    "ConditionalSetSurvivalEmote": [
        {"id": "Bool1", "polarity": 0},
        {"id": "SurvivalEmote1", "polarity": 0},
        {"id": "SurvivalEmote2", "polarity": 0},
        {"id": "SurvivalEmote1", "polarity": 1}
    ],
    "ConditionalSetSurvivalState": [
        {"id": "Bool1", "polarity": 0},
        {"id": "SurvivalState1", "polarity": 0},
        {"id": "SurvivalState2", "polarity": 0},
        {"id": "SurvivalState1", "polarity": 1}
    ],
    "ConstructSurvivalProperties": [
        {"id": "String1", "polarity": 0},
        {"id": "Country1", "polarity": 0},
        {"id": "Color1", "polarity": 0},
        {"id": "Float1", "polarity": 0},
        {"id": "Float2", "polarity": 0},
        {"id": "Color2", "polarity": 0},
        {"id": "Float3", "polarity": 0},
        {"id": "String2", "polarity": 0}
    ],
    "GetVariable": [
        {"id": "Any1", "polarity": 1}
    ],
    "IsNull": [
        {"id": "Any1", "polarity": 0},
        {"id": "Bool1", "polarity": 1}
    ],
    "Keypress": [
        {"id": "Bool1", "polarity": 1}
    ],
    "Region": [],
    "Relay": [
        {"id": "Any1", "polarity": 0},
        {"id": "Any1", "polarity": 1}
    ],
    "SetVariable": [
        {"id": "Any1", "polarity": 0}
    ],
    "SurvivalAutoPosition": [
        {"id": "SurvivalState1", "polarity": 0},
        {"id": "Vector31", "polarity": 1}
    ],
    "SurvivalController": [
        {"id": "Vector31", "polarity": 0},
        {"id": "SurvivalState1", "polarity": 0},
        {"id": "Bool1", "polarity": 0},
        {"id": "SurvivalEmote1", "polarity": 0}
    ],
    "SurvivalEmote": [
        {"id": "SurvivalEmote1", "polarity": 1}
    ],
    "SurvivalGetBool": [
        {"id": "Bool1", "polarity": 1}
    ],
    "SurvivalGetFloat": [
        {"id": "Float1", "polarity": 1}
    ],
    "SurvivalGetTransform": [
        {"id": "Transform1", "polarity": 1}
    ],
    "SurvivalState": [
        {"id": "SurvivalState1", "polarity": 1}
    ],
    "TimePlot": [
        {"id": "String1", "polarity": 0},
        {"id": "Color1", "polarity": 0},
        {"id": "String2", "polarity": 0},
        {"id": "Float1", "polarity": 0}
    ],
    "ModularCarController": [
        {"id": "Float1", "polarity": 0},
        {"id": "Float2", "polarity": 0},
        {"id": "Float3", "polarity": 0},
    ],
    "UniformModularCarProperties": [
        {"id": "String1", "polarity": 0},
        {"id": "Country1", "polarity": 0},
        {"id": "Color1", "polarity": 0},
        {"id": "Float1", "polarity": 0},
        {"id": "Float2", "polarity": 0},
        {"id": "Color2", "polarity": 0},
        {"id": "Float3", "polarity": 0},
        {"id": "Color3", "polarity": 0},
        {"id": "String2", "polarity": 0},
    ],
    "Spherecast": [
        {"id": "Float1", "polarity": 0},
        {"id": "Float2", "polarity": 0},
        {"id": "Spherecast1", "polarity": 1},
    ],
    "CarRaycasts": [
        {"id": "Spherecast1", "polarity": 0},
        {"id": "RaycastHit1", "polarity": 1},
        {"id": "RaycastHit2", "polarity": 1},
        {"id": "RaycastHit3", "polarity": 1},
        {"id": "RaycastHit4", "polarity": 1},
        {"id": "RaycastHit5", "polarity": 1},
        {"id": "RaycastHit6", "polarity": 1},
        {"id": "RaycastHit7", "polarity": 1},
        {"id": "RaycastHit8", "polarity": 1},
    ],
    "HitInfo": [
        {"id": "RaycastHit1", "polarity": 0},
        {"id": "Bool1", "polarity": 1},
        {"id": "Float1", "polarity": 1},
    ],
    "ParkingGetFloat": [{"id": "Float1", "polarity": 1}],
    "ParkingGetBool": [{"id": "Bool1", "polarity": 1}],
    "ParkingGetTransform": [{"id": "Transform1", "polarity": 1}],
    "DemoDerbyGetTransform": [{"id": "Transform1", "polarity": 1}],
    "DemoDerbyGetCar": [
        {"id": "Float1", "polarity": 0},
        {"id": "Car1", "polarity": 1},
    ],
    "GetCarPart": [
        {"id": "Car1", "polarity": 0},
        {"id": "Transform1", "polarity": 1},
        {"id": "Float1", "polarity": 1},
    ],
    "CarInfo": [
        {"id": "Car1", "polarity": 0},
        {"id": "Transform1", "polarity": 1},
        {"id": "Vector31", "polarity": 1},
        {"id": "Bool1", "polarity": 1},
        {"id": "Bool2", "polarity": 1},
        {"id": "Float1", "polarity": 1},
        {"id": "Float2", "polarity": 1},
    ],
    "Autosteer": [
        {"id": "Vector31", "polarity": 0},
        {"id": "Float1", "polarity": 1},
    ],
    "Autothrottle": [
        {"id": "Vector31", "polarity": 0},
        {"id": "Float1", "polarity": 0},
        {"id": "Float1", "polarity": 1},
    ],
    "GetCarFromTransform": [
        {"id": "Transform1", "polarity": 0},
        {"id": "Car1", "polarity": 1},
    ],
}

colorNames = Literal[
    "Auburn",
    "Black",
    "Blonde",
    "Blue",
    "Brown",
    "Dark Brown",
    "Dark Green",
    "Green",
    "Hot Pink",
    "Light Blue",
    "Light Grey",
    "Medium Grey",
    "Orange",
    "Pink",
    "Purple",
    "Red",
    "Tan",
    "White",
    "Yellow",
]
countryNames = Literal[
    "Unknown",
    "Afghanistan",
    "Albania",
    "Algeria",
    "Andorra",
    "Angola",
    "Argentina",
    "Armenia",
    "Australia",
    "Austria",
    "Azerbaijan",
    "Bahamas",
    "Bahrain",
    "Bangladesh",
    "Barbados",
    "Belarus",
    "Belgium",
    "Bermuda",
    "Bohemia",
    "Botswana",
    "Brazil",
    "Bulgaria",
    "Burkina Faso",
    "Burundi",
    "Cameroon",
    "Canada",
    "Chile",
    "China",
    "Colombia",
    "Costa Rica",
    "Croatia",
    "Cuba",
    "Cyprus",
    "Czechia",
    "Côte d'Ivoire",
    "Denmark",
    "Djibouti",
    "Dominican Republic",
    "DR Congo",
    "Ecuador",
    "Egypt",
    "Eritrea",
    "Estonia",
    "Ethiopia",
    "Fiji",
    "Finland",
    "France",
    "Gabon",
    "Georgia",
    "Germany",
    "Ghana",
    "Greece",
    "Grenada",
    "Guatemala",
    "Guyana",
    "Haiti",
    "Hong Kong",
    "Hungary",
    "Iceland",
    "India",
    "Indonesia",
    "Iran",
    "Iraq",
    "Ireland",
    "Israel",
    "Italy",
    "Jamaica",
    "Japan",
    "Jordan",
    "Kazakhstan",
    "Kenya",
    "Kosovo",
    "Kuwait",
    "Kyrgyzstan",
    "Latvia",
    "Lebanon",
    "Lithuania",
    "Luxembourg",
    "Malaysia",
    "Mauritius",
    "Mexico",
    "Moldova",
    "Mongolia",
    "Montenegro",
    "Morocco",
    "Mozambique",
    "Myanmar",
    "Namibia",
    "Netherlands",
    "New Zealand",
    "Niger",
    "Nigera",
    "North Korea",
    "North Macedonia",
    "Norway",
    "Oman",
    "Pakistan",
    "Palestine",
    "Panama",
    "Paraguay",
    "Peru",
    "Philippines",
    "Poland",
    "Portugal",
    "Puerto Rico",
    "Qatar",
    "Romania",
    "Russia",
    "Samoa",
    "San Marino",
    "Saudi Arabia",
    "Scotland",
    "Senegal",
    "Serbia",
    "Singapore",
    "Slovakia",
    "Slovenia",
    "Somolia",
    "South Africa",
    "South Korea",
    "Spain",
    "Sri Lanka",
    "Sudan",
    "Suriname",
    "Sweden",
    "Switzerland",
    "Syria",
    "Taiwan",
    "Tajikistan",
    "Tanzania",
    "Thailand",
    "Togo",
    "Tonga",
    "Trinidad and Tobago",
    "Tunisia",
    "Turkey",
    "Turkmenistan",
    "Uganda",
    "Ukraine",
    "United Arab Emirates",
    "United Kingdom",
    "United States of America",
    "Uruguay",
    "Uzbekistan",
    "Venezuela",
    "Vietnam",
    "Virgin Islands",
    "Yemen",
    "Zambia",
    "Zimbabwe",
]
