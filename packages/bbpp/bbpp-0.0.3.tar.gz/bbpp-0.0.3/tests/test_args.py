from pytest import raises

from bbpp.modules.service.argparser import ArgParser


def test_argparser_selects_pipeline():
    args = ArgParser.parse(['-r', 'test'])
    assert args.repository == 'test'


def test_argparser_config_requires_username_and_password():
    with raises(SystemExit, match=r'2'):
        ArgParser.parse(['config'])


def test_argparser_config_all_params():
    args = ArgParser.parse(
        [
            'config',
            '-u',
            'test',
            '-p',
            'testpwd',
            '-s',
            'test.wav',
            '-w',
            'test',
        ]
    )
    assert args.username == 'test'
    assert args.password == 'testpwd'
    assert args.sound == 'test.wav'
    assert args.workspace == 'test'
