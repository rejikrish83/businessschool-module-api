# test_QueryBuilder.py

from datetime import datetime
from utility.QueryBuilder import QueryBuilder
import pytest
from datetime import datetime
from unittest.mock import MagicMock
@pytest.fixture
def mock_db_utility(monkeypatch):
    mock_instance = MagicMock()
    monkeypatch.setattr('utility.QueryBuilder.QueryBuilder', lambda *args, **kwargs: mock_instance)  # Adjust this import path
    return mock_instance
def test_queryForKpiData():
    # Replace these with your actual test data
    date_str = "2023-12-01"
    student_id = "your_student_id"
    role = "your_role"

    # Create a datetime object from the date string
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    # Create an instance of the QueryBuilder
    query_builder = QueryBuilder()

    # Act
    # Call the queryForKpiData method
    pipeline = query_builder.queryForKpiData(date_obj, student_id, role)

    # Assert
    # Ensure that the subQuery is called with the correct parameters
    query_builder.buildKpiDataSubQuery.assert_called_once_with(role, student_id)

    # Ensure that the pipeline is constructed correctly
    assert len(pipeline) == 8  # Adjust the count based on your actual pipeline
    assert pipeline[0] == mock_db_utility.buildKpiDataSubQuery.return_value
    # Add more assertions based on the structure of your pipeline

    # You can add more specific assertions based on your pipeline structure

    # ...
@pytest.fixture
def query_builder():
    # You might need to adjust this based on your actual implementation
    return QueryBuilder()

def test_buildModuleQuery(query_builder):
    # Mock data for testing
    student_id = "123"

    # Execute the method under test
    result = query_builder.buildModuleQuery(student_id)

    # Add your assertions here based on the expected result
    assert isinstance(result, list)

def test_buildKpiTypeQuery(query_builder):
    # Execute the method under test
    result = query_builder.buildKpiTypeQuery()

    # Add your assertions here based on the expected result
    assert isinstance(result, list)
    # Add more assertions as needed

