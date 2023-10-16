from datetime import date

import pytest

from prelude_parser import parse_to_classes, parse_to_dict
from prelude_parser._prelude_parser import FileNotFoundError, InvalidFileTypeError, ParsingError


def test_parse_to_classes(test_file_1):
    result = parse_to_classes(test_file_1)
    assert len(result) == 2
    assert result[0].__name__ == "Communications"
    assert result[0].study_name == "PBS"
    assert result[0].site_name == "Some Site"
    assert result[0].site_id == 1681574834910
    assert result[0].patient_name == "ABC-001"
    assert result[0].patient_id == 1681574905819
    assert result[0].form_title == "Communications"
    assert result[0].base_form == "communications.form.name.communications"
    assert result[0].form_number is None
    assert result[0].form_group == "Communications"
    assert result[0].form_state == "In-Work"
    assert result[0].communications_made == "Yes"


def test_parse_to_classes_with_float(test_file_2):
    result = parse_to_classes(test_file_2)
    assert len(result) == 2
    assert result[0].__name__ == "Demographics"
    assert result[0].weight == 80.2
    assert result[0].dob == date(2020, 4, 15)


def test_parse_to_classes_i_form(test_file_3):
    result = parse_to_classes(test_file_3)
    assert len(result) == 3
    assert result[0].__name__ == "ICommunicationsDetails"
    assert result[0].study_name == "PBS"
    assert result[0].site_name == "Some Site"
    assert result[0].site_id == 1681574834910
    assert result[0].patient_name == "ABC-001"
    assert result[0].patient_id == 1681574905819
    assert result[0].form_title == "Communications"
    assert result[0].base_form == "communications.form.name.communications"
    assert result[0].form_number is None
    assert result[0].form_group == "Communications"
    assert result[0].form_state == "In-Work"
    assert result[0].i == 1
    assert result[0].contacted_by == "You"
    assert result[0].investigator == "Dr. Me"
    assert result[0].communication == "Some random talk"


def test_parse_to_classes_not_found_error():
    with pytest.raises(FileNotFoundError):
        parse_to_classes("bad.xml")


def test_parse_to_classes_invalid_file_type_error(tmp_path):
    bad = tmp_path / "bad.txt"
    bad.touch()
    with pytest.raises(InvalidFileTypeError):
        parse_to_classes(bad)


def test_parse_to_classes_parsing_error(tmp_path):
    bad = tmp_path / "bad.xml"
    bad.touch()
    with pytest.raises(ParsingError):
        parse_to_classes(bad)


def test_parse_to_classes_short_names(test_file_4):
    result = parse_to_classes(test_file_4, short_names=True)
    assert len(result) == 2
    assert result[0].__name__ == "Communications"
    assert result[0].studyname == "PBS"
    assert result[0].sitename == "Some Site"


def test_parse_to_dict(test_file_1):
    result = parse_to_dict(test_file_1)
    expected = {
        "communications": [
            {
                "base_form": "communications.form.name.communications",
                "communications_made": "Yes",
                "form_group": "Communications",
                "form_number": None,
                "form_state": "In-Work",
                "form_title": "Communications",
                "patient_id": 1681574905819,
                "patient_name": "ABC-001",
                "site_id": 1681574834910,
                "site_name": "Some Site",
                "study_name": "PBS",
            },
            {
                "base_form": "communications.form.name.communications",
                "communications_made": "Yes",
                "form_group": "Communications",
                "form_number": None,
                "form_state": "In-Work",
                "form_title": "Communications",
                "patient_id": 1681574994823,
                "patient_name": "ABC-002",
                "site_id": 1681574834910,
                "site_name": "Some Site",
                "study_name": "PBS",
            },
        ]
    }

    result["communications"] = [dict(sorted(x.items())) for x in result["communications"]]

    assert result == expected


def test_parse_to_dict_with_float(test_file_2):
    result = parse_to_dict(test_file_2)
    expected = {
        "demographics": [
            {
                "base_form": "day.0.form.name.demographics",
                "breed": "Labrador",
                "dob": date(2020, 4, 15),
                "first_name": "Imma",
                "form_group": "Day 0",
                "form_number": None,
                "form_state": "In-Work",
                "form_title": "Demographics",
                "gender": "Female Spayed",
                "last_name": "Dog",
                "patient_id": 1681574905819,
                "patient_name": "ABC-001",
                "screening_number": 1,
                "site_id": 1681574834910,
                "site_name": "Some Site",
                "site_type": "Live",
                "study_name": "PBS",
                "subject_id": "ABC-001",
                "visit_date": date(2023, 4, 15),
                "weight": 80.2,
            },
            {
                "base_form": "day.0.form.name.demographics",
                "breed": "Golden",
                "dob": date(2019, 4, 9),
                "first_name": "Arthur",
                "form_group": "Day 0",
                "form_number": None,
                "form_state": "In-Work",
                "form_title": "Demographics",
                "gender": "Male Neutered",
                "last_name": "Dent",
                "patient_id": 1681574994823,
                "patient_name": "ABC-002",
                "screening_number": 2,
                "site_id": 1681574834910,
                "site_name": "Some Site",
                "site_type": "Live",
                "study_name": "PBS",
                "subject_id": "ABC-002",
                "visit_date": date(2023, 4, 15),
                "weight": 40.5,
            },
        ]
    }

    result["demographics"] = [dict(sorted(x.items())) for x in result["demographics"]]

    assert result == expected


def test_parse_to_dict_i_form(test_file_3):
    result = parse_to_dict(test_file_3)
    expected = {
        "i_communications_details": [
            {
                "base_form": "communications.form.name.communications",
                "communication": "Some random talk",
                "contacted_by": "You",
                "form_group": "Communications",
                "form_number": None,
                "form_state": "In-Work",
                "form_title": "Communications",
                "i": 1,
                "investigator": "Dr. Me",
                "patient_id": 1681574905819,
                "patient_name": "ABC-001",
                "site_id": 1681574834910,
                "site_name": "Some Site",
                "study_name": "PBS",
            },
            {
                "base_form": "communications.form.name.communications",
                "communication": "We talked",
                "contacted_by": "Hi",
                "form_group": "Communications",
                "form_number": None,
                "form_state": "In-Work",
                "form_title": "Communications",
                "i": 1,
                "investigator": "There",
                "patient_id": 1681574994823,
                "patient_name": "ABC-002",
                "site_id": 1681574834910,
                "site_name": "Some Site",
                "study_name": "PBS",
            },
            {
                "base_form": "communications.form.name.communications",
                "communication": "We talked again",
                "contacted_by": "There",
                "i": 2,
                "investigator": "Hi",
                "form_group": "Communications",
                "form_number": None,
                "form_state": "In-Work",
                "form_title": "Communications",
                "patient_id": 1681574994823,
                "patient_name": "ABC-002",
                "site_id": 1681574834910,
                "site_name": "Some Site",
                "study_name": "PBS",
            },
        ]
    }

    result["i_communications_details"] = [
        dict(sorted(x.items())) for x in result["i_communications_details"]
    ]

    assert result == expected


def test_parse_to_dict_short_names(test_file_4):
    result = parse_to_dict(test_file_4, short_names=True)
    expected = {
        "communications": [
            {
                "sitename": "Some Site",
                "studyname": "PBS",
            },
            {
                "sitename": "Another Site",
                "studyname": "PBS",
            },
        ]
    }

    result["communications"] = [dict(sorted(x.items())) for x in result["communications"]]

    assert result == expected
