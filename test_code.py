from main import Searcher
import pytest

searcher = Searcher()
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
    searcher.bcad(house)
    assert None not in searcher.assessed_appraised_tax.values()
    searcher.reset_data()

@pytest.mark.parametrize("house", houses['w'])
def test_wcad(house):
    searcher.wcad(house)
    assert None not in searcher.assessed_appraised_tax.values()
    searcher.reset_data()

@pytest.mark.parametrize("house", houses['w'])
def test_fmv(house):
    searcher.get_fmv(house)
    assert None not in searcher.fmv
    searcher.reset_data()