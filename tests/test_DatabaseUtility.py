

import pytest
from unittest.mock import MagicMock
from database.DatabaseUtility import DatabaseUtility

@pytest.fixture
def mock_mongo_client(monkeypatch):
    # Create a MagicMock object to replace MongoClient
    mock_client = MagicMock()

    # Patch MongoClient to return the mock_client
    monkeypatch.setattr('database.DatabaseUtility.MongoClient', mock_client)  # Adjust this import path

    return mock_client

# Write a test using the mock_mongo_client fixture
def test_database_connection(mock_mongo_client):
    # Arrange
    # Create an instance of DatabaseUtility
    db_utility = DatabaseUtility("mock_uri", "mock_db")

    # Act
    # Call the dataBaseConnection method
    db = db_utility.dataBaseConnection()

    # Assert
    # Ensure that MongoClient was called with the expected URI
    mock_mongo_client.assert_called_once_with("mock_uri")
    # Ensure that the returned value is the mocked database
    assert db == mock_mongo_client.return_value["mock_db"]