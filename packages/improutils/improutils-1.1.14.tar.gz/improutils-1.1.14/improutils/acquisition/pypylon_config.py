# Configuration PyPylon Viewer to load features for RGB Matrix Camera
VIEWER_CONFIG_RGB_MATRIX = {
    "features": [
        {
            "name": "GainRaw",
            "type": "int",
            "step": 1,
        },
        {
            "name": "Height",
            "type": "int",
            "unit": "px",
            "step": 2,
        },
        {
            "name": "Width",
            "type": "int",
            "unit": "px",
            "step": 2,
        },
        {
            "name": "CenterX",
            "type": "bool",
        },
        {
            "name": "CenterY",
            "type": "bool",

        },
        {
            "name": "OffsetX",
            "type": "int",
            "dependency": {"CenterX": False},
            "unit": "px",
            "step": 2,
        },
        {
            "name": "OffsetY",
            "type": "int",
            "dependency": {"CenterY": False},
            "unit": "px",
            "step": 2,
        },
        {
            "name": "AcquisitionFrameRateAbs",
            "type": "int",
            "unit": "fps",
            "dependency": {"AcquisitionFrameRateEnable": True},
            "value": 30,
            "max": 150,
            "min": 1,
        },
        {
            "name": "AcquisitionFrameRateEnable",
            "type": "bool",
        },
        {
            "name": "ExposureAuto",
            "type": "choice_text",
            "options": ["Off", "Once", "Continuous"],
            "style": {"button_width": "90px"}
        },
        {
            "name": "ExposureTimeAbs",
            "type": "int",
            "dependency": {"ExposureAuto": "Off"},
            "unit": "μs",
            "step": 100,
            "max": 35000,
            "min": 500,
        },
        {
            "name": "BalanceWhiteAuto",
            "type": "choice_text",
            "options": ["Off", "Once", "Continuous"],
            "style": {"button_width": "90px"}
        },
    ],
    "features_layout": [
        ("Height", "Width"),
        ("OffsetX", "CenterX"),
        ("OffsetY", "CenterY"),
        ("ExposureAuto", "ExposureTimeAbs"),
        ("AcquisitionFrameRateAbs", "AcquisitionFrameRateEnable"),
        ("BalanceWhiteAuto", "GainRaw")
    ],
    "actions_layout": [
        ("StatusLabel"),
        ("SaveConfig", "LoadConfig", "ContinuousShot", "SingleShot"),
        ("UserSet")
    ],
    "default_user_set": "UserSet3",
}

# Configuration PyPylon Viewer to load features for Monochromatic Matrix Camera
VIEWER_CONFIG_MONO_MATRIX = {
    "features": [
        {
            "name": "GainRaw",
            "type": "int",
            "step": 1,
        },
        {
            "name": "Height",
            "type": "int",
            "unit": "px",
            "step": 2,
        },
        {
            "name": "Width",
            "type": "int",
            "unit": "px",
            "step": 2,
        },
        {
            "name": "CenterX",
            "type": "bool",
        },
        {
            "name": "CenterY",
            "type": "bool",

        },
        {
            "name": "OffsetX",
            "type": "int",
            "dependency": {"CenterX": False},
            "unit": "px",
            "step": 2,
        },
        {
            "name": "OffsetY",
            "type": "int",
            "dependency": {"CenterY": False},
            "unit": "px",
            "step": 2,
        },
        {
            "name": "AcquisitionFrameRateAbs",
            "type": "int",
            "unit": "fps",
            "dependency": {"AcquisitionFrameRateEnable": True},
            "value": 30,
            "max": 150,
            "min": 1,
        },
        {
            "name": "AcquisitionFrameRateEnable",
            "type": "bool",
        },
        {
            "name": "ExposureAuto",
            "type": "choice_text",
            "options": ["Off", "Once", "Continuous"],
            "style": {"button_width": "90px"}
        },
        {
            "name": "ExposureTimeAbs",
            "type": "int",
            "dependency": {"ExposureAuto": "Off"},
            "unit": "μs",
            "step": 500,
            "max": 35000,
            "min": 500,
        },
    ],
    "features_layout": [
        ("Height", "Width"),
        ("OffsetX", "CenterX"),
        ("OffsetY", "CenterY"),
        ("ExposureTimeAbs", "ExposureAuto"),
        ("AcquisitionFrameRateAbs", "AcquisitionFrameRateEnable"),
        ("GainRaw")
    ],
    "actions_layout": [
        ("StatusLabel"),
        ("SaveConfig", "LoadConfig", "ContinuousShot", "SingleShot"),
        ("UserSet")
    ],
    "default_user_set": "UserSet3",
}

# Configuration PyPylon Viewer to load features for Monochromatic Line Scan Camera
VIEWER_CONFIG_MONO_LINE = {
    "features": [
        {
            "name": "GainRaw",
            "type": "int",
            "step": 1,
        },
        {
            "name": "Height",
            "type": "int",
            "unit": "px",
            "step": 2,
        },
        {
            "name": "Width",
            "type": "int",
            "unit": "px",
            "step": 2,
        },
        {
            "name": "CenterX",
            "type": "bool",
        },
        {
            "name": "OffsetX",
            "type": "int",
            "dependency": {"CenterX": False},
            "unit": "px",
            "step": 2,
        },
        {
            "name": "AcquisitionLineRateAbs",
            "type": "int",
            "max": 5000,
            "min": 100,
            "step": 100,
        },
        {
            "name": "ExposureAuto",
            "type": "choice_text",
            "options": ["Off", "Once", "Continuous"],
            "style": {"button_width": "90px"}
        },
        {
            "name": "ExposureTimeAbs",
            "type": "int",
            "dependency": {"ExposureAuto": "Off"},
            "unit": "μs",
            "step": 500,
            "max": 35000,
            "min": 500,
        },
    ],
    "features_layout": [
        ("Height", "Width"),
        ("OffsetX", "CenterX"),
        ("ExposureTimeAbs", "ExposureAuto"),
        ("AcquisitionLineRateAbs", "GainRaw")
    ],
    "actions_layout": [
        ("StatusLabel"),
        ("SaveConfig", "LoadConfig", "ContinuousShot", "SingleShot"),
        ("UserSet")
    ],
    "default_user_set": "UserSet3",
}

# Configuration PyPylon Viewer to load features for Monochromatic Matrix Camera with pericentric lens
VIEWER_CONFIG_MONO_MATRIX_PERICENTRIC = {
    "features": [
        {
            "name": "Gain",
            "type": "int",
            "unit": "dB",
            "step": 1,
        },
        {
            "name": "Height",
            "type": "int",
            "unit": "px",
            "step": 2,
            "value": 1270
        },
        {
            "name": "Width",
            "type": "int",
            "unit": "px",
            "step": 2,
            "value": 1344
        },
        {
            "name": "OffsetX",
            "type": "int",
            "unit": "px",
            "step": 2,
            "value": 608
        },
        {
            "name": "OffsetY",
            "type": "int",
            "unit": "px",
            "step": 2,
            "value": 418
        },
        {
            "name": "ExposureTime",
            "type": "int",
            "max": 35000,
            "min": 90,
            "step": 30,
            "value": 1500,
            "unit": "μs",
        },
    ],
    "features_layout": [
        ("Height", "Width"),
        ("OffsetX", "OffsetY"),
        ("Gain", "ExposureTime"),
    ],
    "actions_layout": [
        ("StatusLabel"),
        ("SaveConfig", "LoadConfig", "ContinuousShot", "SingleShot"),
        ("UserSet")
    ],
    "default_user_set": "UserSet3",
}
