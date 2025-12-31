"""
Fixtures模块

@author Test Engineer
@date 2025/01/01
"""

from .api_fixture import APIFixtures, api_fixtures
from .data_fixture import DataFixtures, data_fixtures
from .ui_fixture import UIFixtures, ui_fixtures

__all__ = [
    "APIFixtures",
    "api_fixtures",
    "DataFixtures",
    "data_fixtures",
    "UIFixtures",
    "ui_fixtures"
]
