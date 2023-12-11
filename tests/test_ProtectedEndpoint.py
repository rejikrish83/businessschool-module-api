import pytest
from fastapi import HTTPException
from endpoints.ProtectedEndpoint import get_kpi_data

# Assuming DATE_FORMAT is defined in your main_module or config
DATE_FORMAT = "%Y-%m-%d"

@pytest.mark.asyncio
async def test_get_kpi_data_valid_date_format():
    # Your setup code, if needed
    student_id = "your_student_id"
    date_str = "2023-12-01"
    role = "your_role"

    # Call the asynchronous method
    result = await get_kpi_data(student_id, date_str, role)

    # Your assertions
    assert result is not None
    # Add more assertions based on the expected behavior

@pytest.mark.asyncio
async def test_get_kpi_data_invalid_date_format():
    # Your setup code, if needed
    student_id = "your_student_id"
    date_str = "invalid_date_format"
    role = "your_role"

    # Call the asynchronous method and expect an HTTPException
    with pytest.raises(HTTPException) as exc_info:
        await get_kpi_data(student_id, date_str, role)

    # Your assertions for the exception
    assert exc_info.value.status_code == 400
    assert "Invalid date format" in exc_info.value.detail

# You can add more test cases as needed
