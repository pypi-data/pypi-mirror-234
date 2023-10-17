import pytest
from notifypy import Notify
from bbpp.modules.service.bitbucket import BitBucket


def test_bitbucket_init(mocker):
    config = mocker.Mock()
    bb = BitBucket(config=config)
    assert bb.config == config
    assert bb.ENDPOINT == 'https://api.bitbucket.org/2.0'
    assert type(bb.notifier_service) == Notify


@pytest.mark.asyncio
async def test_get_first_repo(mocker, httpx_mock):
    config = mocker.Mock()
    config.auth = ('test', 'pass')

    bb = BitBucket(config=config)
    httpx_mock.add_response(json={'size': 1, 'pagelen': 1})
    r = await bb._get_first_repo()
    assert type(r) == dict
    assert r == {'size': 1, 'pagelen': 1}


@pytest.mark.asyncio
async def test_get_all_pages(mocker, httpx_mock):
    config = mocker.Mock()
    config.auth = ('test', 'pass')

    bb = BitBucket(config=config)
    httpx_mock.add_response(json={'values': [{'name': 'test'}]})
    httpx_mock.add_response(json={'values': [{'name': 'test2'}]})
    r = await bb._get_all_pages(pages=2)
    assert type(r) == list
    assert r == [
        {'values': [{'name': 'test'}]},
        {'values': [{'name': 'test2'}]},
    ]


def test_parse_repos(mocker):
    bb = BitBucket(config=mocker.Mock())
    output = {'values': [{'name': 'test'}, {'name': 'test2'}]}
    r = bb.parse_repos(output)
    assert list(r) == ['test', 'test2']
