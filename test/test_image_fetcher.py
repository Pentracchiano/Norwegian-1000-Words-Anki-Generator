import pytest
from src.image_fetcher import fetch_image, Image
from unittest.mock import Mock, patch


def test_fetch_image_handles_throttle():
    # Yeah, could use more abstractions here, but that's fine
    reset_time = "1"
    first_response = Mock()
    first_response.status_code = 429
    first_response.headers = {"X-RateLimit-Reset": reset_time}
    second_response = Mock()
    second_response.status_code = 200
    second_response.json.return_value = {"hits": [{"webformatURL": "https://example.com/image.jpg"}]}
    third_response = Mock()
    third_response.status_code = 200
    third_response.content = "image data"

    with (patch("requests.get", side_effect=[first_response, second_response, third_response]) as mock_get,
        patch("time.sleep") as mock_sleep):
        image = fetch_image("Beautiful Norway Fjord", retry_on_throttle=True)
        assert image.data == "image data"
        assert "pixabay" in image.attribution.lower()
        assert mock_sleep.call_args_list[0][0][0] > int(reset_time)
        assert mock_get.call_count == 3
    

def test_fetch_image():
    response = Mock()
    response.status_code = 200
    response.json.return_value = {"hits": [{"webformatURL": "https://example.com/image.jpg"}]}
    response.content = "image data"

    with patch("requests.get", return_value=response) as mock_get:
        image = fetch_image("Beautiful Norway Fjord")
        assert image.data == "image data"
        assert "pixabay" in image.attribution.lower()
        assert mock_get.call_count == 2


def test_fetch_image_fails_on_nonhandled_throttle():
    response = Mock()
    response.status_code = 429
    response.headers = {"X-RateLimit-Reset": "1"}

    with patch("requests.get", return_value=response) as mock_get:
        with pytest.raises(Exception):
            fetch_image("Beautiful Norway Fjord", retry_on_throttle=False)
        assert mock_get.call_count == 1