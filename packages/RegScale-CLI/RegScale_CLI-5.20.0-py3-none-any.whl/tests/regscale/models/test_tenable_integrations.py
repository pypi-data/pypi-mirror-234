import json
from unittest.mock import MagicMock, patch

import pytest

from regscale.models.integration_models.nessus import NessusReport
from regscale.models.integration_models.tenable import TenableIOAsset


@pytest.fixture
def new_assets():
    with open("./tests/test_data/ten_assets.json", "r") as f:
        dat = json.load(f)
    assets = [TenableIOAsset(**a) for a in dat]
    return assets


@pytest.fixture
def new_vulns():
    with open("./tests/test_data/ten_vulns.json", "r") as f:
        dat = json.load(f)
    vulns = [NessusReport(**v) for v in dat]
    return vulns


@patch("regscale.core.app.application.Application")
@patch("regscale.models.integration_models.tenable.TenableIOAsset.sync_to_regscale")
def test_fetch_assets(mock_app, new_assets):
    # Call the fetch_assets function
    assets = new_assets
    app = mock_app
    with patch.object(TenableIOAsset, "sync_to_regscale") as mock_sync:
        mock_sync(app=app, assets=assets, ssp_id=2)

        # Check that the sync_to_regscale method was called with the correct arguments
        mock_sync.assert_called_once_with(app=app, assets=assets, ssp_id=2)


@patch("regscale.models.integration_models.nessus.NessusReport.sync_to_regscale")
def test_sync_nessus_reports(mock_sync):
    # Create some mock NessusReport objects to pass to the sync_nessus_reports function
    report1 = MagicMock(spec=NessusReport)
    report2 = MagicMock(spec=NessusReport)

    # Call the sync_nessus_reports function with the mock objects
    mock_sync([report1, report2], 123)

    # Check that the sync_to_regscale method was called with the expected arguments
    mock_sync.assert_called_once_with([report1, report2], 123)
