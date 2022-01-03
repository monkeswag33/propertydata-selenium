from main import wcad, bcad, fmv, init_programs
import pytest

driver, client = init_programs()
houses = {
    'b': [
        "700 San Pedro",
        "702 San Pedro",
        "704 San Pedro",
        "706 San Pedro",
        "800 San Pedro",
        "802 San Pedro"
    ],
    'w': [
        "103 Axis Deer TRL",
        "105 Orchard WAY",
        "107 Orchard WAY",
        "116 Sylvan ST",
        "118 Brown ST",
        "118 Wegstrom ST",
        "128 Flinn ST",
        "212 Cloud RD",
        "302 Quail CIR",
        "313 Ross ST",
        "403 Kates WAY",
        "6018 Andross CT",
        "900 Stewart DR"
    ]
}

@pytest.mark.parametrize("house", houses['b'])
def test_bcad(house):
    assessed_appraised_value = {
        'assessed_value': None,
        'appraised_value': None,
        'tax': None
    }
    bcad(driver, house, assessed_appraised_value, 5)
    assert None not in assessed_appraised_value.values()

@pytest.mark.parametrize("house", houses['w'])
def test_wcad(house):
    assessed_appraised_value = {
        'assessed_value': None,
        'appraised_value': None,
        'tax': None
    }
    wcad(driver, house, assessed_appraised_value, 5)
    assert None not in assessed_appraised_value.values()

@pytest.mark.parametrize("house", houses['w'])
def test_fmv(house):
    response = client.search(house + ' Hutto')
    url = response['payload']['exactMatch']['url']
    initial_info = client.initial_info(url)['payload']
    avm_details = client.avm_details(initial_info['propertyId'], initial_info['listingId'])
    assert avm_details