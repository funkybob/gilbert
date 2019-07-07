from pathlib import Path

import pytest

from gilbert.site import Site


@pytest.fixture
def root():
	return Path(__file__).resolve().parent / 'root'


@pytest.fixture
def site(root):
	return Site(root)


def test_events(site, mocker):

	test_func = mocker.Mock()

	site.on('after-content', test_func)

	site.load_content()

	test_func.assert_called_once()