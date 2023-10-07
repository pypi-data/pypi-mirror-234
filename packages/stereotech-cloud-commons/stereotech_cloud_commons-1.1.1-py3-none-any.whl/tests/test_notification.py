from configparser import ConfigParser
from typing import Any
import pytest
from stereotech_cloud_commons.components.notification import NotificationService
from stereotech_cloud_commons.confighelper import ConfigHelper

def config_get(option: str, default: Any):
    return 'https://notification.stereotech.cloud'

@pytest.mark.asyncio
async def test_email_send(monkeypatch):
    monkeypatch.setattr(ConfigHelper, 'get', config_get)
    monkeypatch.setattr(ConfigParser, 'sections', {})
    service = NotificationService(ConfigHelper(None, ConfigParser(), None, None))
    result = await service.send_email('frylock3434@gmail.com')
    assert result is not None