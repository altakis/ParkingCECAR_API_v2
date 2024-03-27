# for python 2: use mock.patch from `pip install mock`.
from unittest.mock import patch
from uuid import UUID

import pytest
from api.models import Detection
from api.tasks import background_detection

# Happy path tests


@pytest.mark.parametrize(
    "id_ref, data",
    [
        (
            UUID("00000000-0000-0000-0000-000000000000"),
            {"src_file": "image1.jpg"},
        ),  # Regular UUID
        (
            UUID("ffffffff-ffff-ffff-ffff-ffffffffffff"),
            {"src_file": "image2.png"},
        ),  # Max UUID value
    ],
    ids=["Regular UUID", "Max UUID value"],
)
def test_background_detection_happy_path(id_ref, data):
    # Act
    background_detection(id_ref, data)

    # Assert
    # Assertions on result


# Edge case tests


@pytest.mark.parametrize(
    "id_ref",
    [
        (UUID("00000000-0000-0000-0000-000000000001")),  # Version 1 UUID
        (UUID("00000000-0000-0000-0000-000000000010")),  # Version 10 UUID
    ],
    ids=["Version 1 UUID", "Version 10 UUID"],
)
def test_background_detection_uuid_edge_cases(id_ref):
    # Act
    background_detection(id_ref, {"src_file": "image.jpg"})

    # Assert
    # Assertions on result


# Error case tests


@pytest.mark.parametrize(
    "id_ref, data",
    [
        (None, {"src_file": "image.jpg"}),  # Null id_ref
        ("not-a-uuid", {"src_file": "image.jpg"}),  # Invalid UUID string
        (UUID("00000000-0000-0000-0000-000000000000"), {}),  # Missing src_file
    ],
    ids=["Null id_ref", "Invalid UUID string", "Missing src_file"],
)
def test_background_detection_error_cases(id_ref, data):
    with pytest.raises(Exception):
        background_detection(id_ref, data)
