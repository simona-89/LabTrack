from file_manager import extract_report_date_time, extract_hemoglobin_data


def test_extract_report_date_time():
    # Test with a valid date
    text = "This is a test... 2024.05.11 12:00... if 1st ctach is 2024-05-11 12:00 continue on..."
    assert extract_report_date_time(text) == "2024-05-11 12:00"

    # Test with an invalid date
    text = "This is a test string with no date..."
    assert extract_report_date_time(text) is None

    # Test with an invalid date
    text = "This is an e.g. of one case if regex not followed-2024-05-11  12:00-more space"
    assert extract_report_date_time(text) is None


def test_extract_hemoglobin_data_extraction_of_parameter_result():
    # Test when valid text & parameter result
    text = "2024-05-11 \n Hemoglobin, HGB,\n...   120 117 – 150"
    result = extract_hemoglobin_data(text)
    assert result["result"] == 120.0

    # Test when parameter result do not exist
    text = "Can you find HGB result somwhere in this text?"
    result = extract_hemoglobin_data(text)
    assert result["result"] is None


def test_extract_hemoglobin_data_extraction_of_levels():
    # Test when match_result valid and levels follow regex
    text = "HGB 120 nuo 117 - 150"
    result = extract_hemoglobin_data(text)
    assert result["levels from lab."] == "117.0 - 150.0"

    # Test when match_result valid, levels is first found
    text = "HGB 120 nuo 117 - 150 and there is something within 120 - 145"
    result = extract_hemoglobin_data(text)
    assert result["levels from lab."] == "117.0 - 150.0"

    # Test when match_result valid, but any levels for match_valid
    text = "HGB 120, Ferritin 120, \n"
    result = extract_hemoglobin_data(text)
    assert result["levels from lab."] is None


def test_extract_hemoglobin_data_extraction_of_date():
    # Test when valid text & date before the parameter result
    text = "2024-05-11 \n HB 120 117 – 150"
    result = extract_hemoglobin_data(text)
    assert result["analysed on"] == "2024-05-11"

    # Test when date patterns valid, but need to extract last one
    text = "2024-05-10... 2024-05-11 .\n. 2024-05-12 ... 2024.05.11... HB 120 117 – 150"
    result = extract_hemoglobin_data(text)
    assert result["analysed on"] == "2024.05.11"

    # Test when date is missing
    text = "HB, 120 117 – 150"
    result = extract_hemoglobin_data(text)
    assert result["analysed on"] is None

    # Test when date is after match_result start (until parameter was found)
    text = "HB 120 117 – 150 2024.05.11... 2024-05-11"
    result = extract_hemoglobin_data(text)
    assert result["analysed on"] is None
