from travel_assistant.schemas import AttractionSearchInput
from travel_assistant.tools import normalize_attraction_results


def test_normalize_attraction_results_caps_and_shapes_output():
    raw_results = [
        {
            "title": "Art Institute of Chicago - Tickets and Hours",
            "body": "Major museum with modern and classic collections in downtown Chicago.",
            "href": "https://example.com/art-institute",
        },
        {
            "title": "Chicago Riverwalk | Official Guide",
            "body": "Scenic waterfront promenade with architecture views and dining.",
            "href": "https://example.com/riverwalk",
        },
        {
            "title": "Duplicate Riverwalk",
            "body": "Should be skipped because the URL repeats.",
            "href": "https://example.com/riverwalk",
        },
    ]
    search_input = AttractionSearchInput(
        destination="Chicago",
        interests=["architecture", "walking"],
        max_results=2,
    )

    output = normalize_attraction_results(search_input, raw_results)

    assert output.destination == "Chicago"
    assert len(output.attractions) == 2
    assert output.attractions[0].name == "Art Institute of Chicago"
    assert output.attractions[0].estimated_cost == "Paid or ticketed"
    assert output.attractions[1].estimated_cost == "Usually free"
    assert output.attractions[1].source_url == "https://example.com/riverwalk"
    assert output.notes
