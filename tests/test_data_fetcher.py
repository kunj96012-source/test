import pandas as pd
import pytest
from unittest.mock import patch, MagicMock

# Assuming function name will be: fetch_data()
# You will implement this later in data_fetcher.py
from so_challenge import data_fetcher


def mock_api_response():
    """Mock API response data"""
    return {
        "items": [
            {"creation_date": 1609459200},  # Jan 2021
            {"creation_date": 1609459200},
            {"creation_date": 1612137600},  # Feb 2021
        ]
    }


@patch("so_challenge.data_fetcher.requests.get")
def test_successful_data_fetch(mock_get, tmp_path):
    """Test successful API fetch returns correct DataFrame"""
    
    mock_response = MagicMock()
    mock_response.json.return_value = mock_api_response()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    df = data_fetcher.fetch_data(cache_path=tmp_path / "data.csv")

    assert isinstance(df, pd.DataFrame)
    assert "year_month" in df.columns
    assert "question_count" in df.columns
    assert len(df) > 0


@patch("so_challenge.data_fetcher.requests.get")
def test_cache_usage(mock_get, tmp_path):
    """Test cached data is used instead of API call"""

    # Create fake cached file
    cache_file = tmp_path / "data.csv"
    sample_df = pd.DataFrame({
        "year_month": pd.to_datetime(["2021-01"]),
        "question_count": [10]
    })
    sample_df.to_csv(cache_file, index=False)

    df = data_fetcher.fetch_data(cache_path=cache_file)

    # API should NOT be called
    mock_get.assert_not_called()

    assert len(df) == 1
    assert df.iloc[0]["question_count"] == 10


@patch("so_challenge.data_fetcher.requests.get")
def test_retry_on_failure(mock_get, tmp_path):
    """Test retry logic on network failure"""

    # First 2 calls fail, 3rd succeeds
    mock_get.side_effect = [
        Exception("Network error"),
        Exception("Network error"),
        MagicMock(
            status_code=200,
            json=lambda: mock_api_response()
        )
    ]

    df = data_fetcher.fetch_data(cache_path=tmp_path / "data.csv")

    assert mock_get.call_count == 3
    assert isinstance(df, pd.DataFrame)