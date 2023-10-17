from equia.models import CalculationComposition, FlashCalculationInput


def test_flash_input_mapped():
    body = {
        "accessKey": "",
        "temperature": 445,
        "pressure": 20,
        "components": [
            {"mass": 0.78},
            {"mass": 0.02},
            {"mass": 0.20}
        ],
        "flashType": "Fixed Temperature/Pressure",
        "fluidId": "9E9ABAD5-C6CA-427F-B5E7-15AB3F7CF076",
        "units": {
            "temperature": {
                "in": "Kelvin",
                "out": "Kelvin"
            },
            "pressure": {
                "in": "Bar",
                "out": "Bar"
            },
            "composition": {
                "in": "Massfraction",
                "out": "Massfraction"
            },
            "enthalpy": {
                "in": "kJ/Kg",
                "out": "kJ/Kg"
            },
            "entropy": {
                "in": "kJ/(Kg Kelvin)",
                "out": "kJ/(Kg Kelvin)"
            }
        }
    }
    input = FlashCalculationInput.from_dict(body)

    assert input.fluidid == "9E9ABAD5-C6CA-427F-B5E7-15AB3F7CF076"
    assert input.temperature == 445
    assert input.pressure == 20
    assert input.flashtype == "Fixed Temperature/Pressure"
    assert len(input.components) == 3


def test_composition_mapped():
    body = {"mass": 0.78}
    input = CalculationComposition.from_dict(body)

    assert input.mass == 0.78
