import os

from .mock_search import mock as mock_search

ENABLED = os.getenv('ENABLE_MOCKING', 'false') == 'true'


def auto_mock():
    return enable_mock() if ENABLED else None


def enable_mock():
    """
    Mock calls to Hestia API using pre-loaded search results.
    """
    # apply mocks on search results
    mock_search()
