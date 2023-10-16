import sys
import os
import json
from typing import Generator, Any, Dict, List

# Add the project's root directory to the Python path
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, project_root)

import pytest, requests
from preloader import Preloader
from unittest.mock import patch, Mock
from requests.models import Response

# Define the path to the external mock XML file
MOCK_XML_FILE_MAIN = os.path.join(
    os.path.dirname(__file__), "mocks", "mock_sitemap_main.xml"
)
MOCK_XML_FILE_MAIN_ERROR = os.path.join(
    os.path.dirname(__file__), "mocks", "mock_sitemap_main_error.xml"
)
MOCK_XML_FILE_SUB1 = os.path.join(
    os.path.dirname(__file__), "mocks", "mock_sitemap_sub1.xml"
)
MOCK_XML_FILE_SUB2 = os.path.join(
    os.path.dirname(__file__), "mocks", "mock_sitemap_sub2.xml"
)
MOCK_XML_FILE_SUB_ERROR = os.path.join(
    os.path.dirname(__file__), "mocks", "mock_sitemap_sub_error.xml"
)
MOCK_PAGE = os.path.join(os.path.dirname(__file__), "mocks", "page.html")


@pytest.fixture
def mock_requests_get() -> Generator[Mock, None, None]:
    """Mock requests.get to return our own XML file for each URL"""

    def custom_get(url: str, *args: Any, **kwargs: Any) -> Response:
        response = requests.Response()
        if url == "https://example.com/sitemap.xml":
            response.status_code = 200
            with open(MOCK_XML_FILE_MAIN, "rb") as mock_file:
                response._content = mock_file.read()
        elif url == "https://example.com/sitemap_error.xml":
            response.status_code = 200
            with open(MOCK_XML_FILE_MAIN_ERROR, "rb") as mock_file:
                response._content = mock_file.read()
        elif url == "https://example.com/sitemap_sub1.xml":
            response.status_code = 200
            with open(MOCK_XML_FILE_SUB1, "rb") as mock_file:
                response._content = mock_file.read()
        elif url == "https://example.com/sitemap_sub2.xml":
            response.status_code = 200
            with open(MOCK_XML_FILE_SUB2, "rb") as mock_file:
                response._content = mock_file.read()
        elif url == "https://example.com/sitemap_sub_error.xml":
            response.status_code = 200
            with open(MOCK_XML_FILE_SUB_ERROR, "rb") as mock_file:
                response._content = mock_file.read()
        elif (
            url == "https://example.com/page1.html"
            or url == "https://example.com/page2.html"
            or url == "https://example.com/page3.html"
            or url == "https://example.com/page4.html"
            or url == "https://example.com/page5.html"
            or url == "https://example.com/page6.html"
        ):
            response.status_code = 200
            with open(MOCK_PAGE, "rb") as mock_file:
                response._content = mock_file.read()
        else:
            response.status_code = 404
        return response

    with patch("requests.get", side_effect=custom_get) as mock_get:
        yield mock_get


def test_mock_ok(mock_requests_get: Generator[Any, None, None]) -> None:
    """Test that the mock is returning the file content"""
    response = requests.get("https://example.com/sitemap.xml")
    assert response.status_code == 200
    with open(MOCK_XML_FILE_MAIN, "rb") as file:
        expected_content = file.read()
    assert response.content == expected_content


def test_mock_fail(mock_requests_get: Generator[Any, None, None]) -> None:
    """Test that the mock is returning 404 for other URLs"""
    response = requests.get("https://example.com/other.xml")
    assert response.status_code == 404


def test_value_error(mock_requests_get: Generator[Any, None, None]) -> None:
    with pytest.raises(ValueError) as exc_info:
        Preloader("https://example.com/sitemap.xml", depth=0)
    assert str(exc_info.value) == "depth must be greater than 1"


def test_preloader_fetch_level_1(mock_requests_get: Generator[Any, None, None]) -> None:
    """Test a 1 level sitemap"""
    preloader = Preloader("https://example.com/sitemap.xml", depth=1)
    assert len(preloader.page_urls) == 2
    assert len(preloader.sitemap_urls) == 0


def test_preloader_level_2(mock_requests_get: Generator[Any, None, None]) -> None:
    """Test a 2 levels sitemap"""
    preloader = Preloader("https://example.com/sitemap.xml", depth=2)
    assert preloader.sitemap_url == "https://example.com/sitemap.xml"
    assert len(preloader.page_urls) == 6
    assert len(preloader.sitemap_urls) == 2


def test_preloader_level_3(mock_requests_get: Generator[Any, None, None]) -> None:
    """Test a 3 levels sitemap"""
    preloader = Preloader("https://example.com/sitemap.xml", depth=3)
    assert preloader.sitemap_url == "https://example.com/sitemap.xml"
    assert len(preloader.page_urls) == 0
    assert len(preloader.sitemap_urls) == 8


def test_fetch_all_pages(mock_requests_get: Generator[Any, None, None]) -> None:
    """Test that the preloader can fetch all pages from a sitemap"""
    preloader = Preloader("https://example.com/sitemap.xml", depth=2)
    assert len(preloader.page_urls) == 6
    preloader.fetch_pages()
    assert len(preloader.finished_pages) == 6
    assert len(preloader.page_urls) == 0
    assert len(preloader.sitemap_urls) == 2


def test_fetch_pages_batch(mock_requests_get: Generator[Any, None, None]) -> None:
    """Test that the preloader can fetch pages in batches"""
    preloader = Preloader("https://example.com/sitemap.xml", depth=2)
    assert len(preloader.page_urls) == 6
    preloader.fetch_pages(3)
    assert len(preloader.finished_pages) == 3
    assert len(preloader.page_urls) == 3
    preloader.fetch_pages(3)
    assert len(preloader.finished_pages) == 6
    assert len(preloader.page_urls) == 0


def test_fetch_sitemap_with_error_page(
    mock_requests_get: Generator[Any, None, None]
) -> None:
    """
    Test that the preloader can handle a sitemap with iteams returning an error page
    """
    preloader = Preloader("https://example.com/sitemap_error.xml", depth=2)
    assert len(preloader.sitemap_urls) == 1
    assert len(preloader.failed_urls) == 1
    assert len(preloader.page_urls) == 3
    preloader.fetch_pages()
    assert len(preloader.failed_urls[404]) == 3


def test_serialize(mock_requests_get: Generator[Any, None, None]) -> None:
    """
    Test that the preloader can serialize the results
    """
    preloader = Preloader("https://example.com/sitemap.xml", depth=2)
    preloader.fetch_pages()
    serialized: Dict[str, Any] = preloader.to_dict()
    assert serialized["sitemap_url"] == "https://example.com/sitemap.xml"
    assert len(serialized["page_urls"]) == 0
    assert len(serialized["sitemap_urls"]) == 2
    assert len(serialized["failed_urls"]) == 0
    assert len(serialized["finished_pages"]) == 6


def test_json(mock_requests_get: Generator[Any, None, None]) -> None:
    """
    Test that the preloader can serialize the results
    """
    preloader = Preloader("https://example.com/sitemap.xml", depth=2)
    preloader.fetch_pages()
    preloader_json: str = preloader.json()
    preloader_dict: Dict[str, Any] = json.loads(preloader_json)
    assert preloader_dict["sitemap_url"] == "https://example.com/sitemap.xml"
    assert len(preloader_dict["page_urls"]) == 0
    assert len(preloader_dict["sitemap_urls"]) == 2
    assert len(preloader_dict["failed_urls"]) == 0
    assert len(preloader_dict["finished_pages"]) == 6


if __name__ == "__main__":
    pytest.main()
