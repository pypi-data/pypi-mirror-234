import pytest
import requests_mock

# Replace with the actual module name
from seali.config import CONF, PATH
from seali.requests.project import create, delete, download_edafile, download_lyp

BASE_URL = CONF.url
TEST_PROJECT_NAME = "test_project"


def test_create_success() -> None:
    with requests_mock.Mocker() as m:
        # Mocking a successful post request
        m.post(f"{BASE_URL}/project", status_code=201)
        file_path = PATH.test_data / "sample_reticle.gds"
        response = create(file=file_path, base_url=BASE_URL)
        assert response.status_code == 201


def test_delete_success() -> None:
    with requests_mock.Mocker() as m:
        # Mocking a successful delete request
        m.delete(f"{BASE_URL}/project/{TEST_PROJECT_NAME}", status_code=204)
        response = delete(project_name=TEST_PROJECT_NAME, base_url=BASE_URL)
        assert response.status_code == 204


def test_download_gds_success() -> None:
    with requests_mock.Mocker() as m:
        # Mocking a successful get request
        m.get(f"{BASE_URL}/project/{TEST_PROJECT_NAME}", status_code=200, text="data")
        response = download_edafile(project_name=TEST_PROJECT_NAME, base_url=BASE_URL)
        assert response.status_code == 200
        assert response.text == "data"


@pytest.mark.skip(reason="Not implemented yet in server side")
def test_download_lyp_success() -> None:
    with requests_mock.Mocker() as m:
        # Mocking a successful get request
        m.get(f"{BASE_URL}/project/{TEST_PROJECT_NAME}", status_code=200, text="data")
        response = download_lyp(project_name=TEST_PROJECT_NAME, base_url=BASE_URL)
        assert response.status_code == 200
        assert response.text == "data"
