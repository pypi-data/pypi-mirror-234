from pytest import raises

from bbpp.modules.service.config import Config


def test_config_calls_write_file(mocker):
    p = mocker.patch('builtins.open', mocker.mock_open())
    config = Config(username='test', password='pass', workspace='test')
    p.assert_called_once_with(config.config_file, 'w')
    p().write.assert_called_once_with(
        '{"username": "test", "password": "pass", "workspace": "test", "sound": "ping.wav"}'
    )


def test_config_calls_write_file_with_sound(mocker):
    p = mocker.patch('builtins.open', mocker.mock_open())
    config = Config(
        username='test', password='pass', workspace='test', sound='cars.wav'
    )
    p.assert_called_once_with(config.config_file, 'w')
    p().write.assert_called_once_with(
        '{"username": "test", "password": "pass", "workspace": "test", "sound": "cars.wav"}'
    )


def test_config_reads_file_if_not_username_and_password(mocker):
    mocker.patch('os.path.exists', return_value=True)
    p = mocker.patch(
        'builtins.open',
        mocker.mock_open(
            read_data='{"username": "test", "password": "pass", "workspace": "test", "sound": "cars.wav"}'
        ),
    )
    config = Config()
    p.assert_called_once_with(config.config_file, 'r')
    assert config.username == 'test'
    assert config.password == 'pass'
    assert config.workspace == 'test'
    assert config.sound == 'cars.wav'
    assert config.auth == ('test', 'pass')


def test_check_config_file_exists(mocker):
    p = mocker.patch('os.path.exists', return_value=True)
    r = mocker.patch(
        'builtins.open',
        mocker.mock_open(
            read_data='{"username": "test", "password": "pass", "workspace": "test", "sound": "cars.wav"}'
        ),
    )
    config = Config()
    p.assert_called_once_with(config.config_file)


def test_check_config_raises_value_error_if_no_configfile_present(mocker):
    mocker.patch('os.path.exists', return_value=False)
    with raises(ValueError, match=r'Cannot find config file,.*'):
        config = Config()
        config.check_config_file_exists()


def test_read_config_file_returns_dictionary(mocker):
    mocker.patch('os.path.exists', return_value=True)
    p = mocker.patch(
        'builtins.open',
        mocker.mock_open(
            read_data='{"username": "test", "password": "pass", "workspace": "test", "sound": "cars.wav"}'
        ),
    )
    config = Config()
    p.assert_called_once_with(config.config_file, 'r')
    assert config._read_config_file() == {
        'username': 'test',
        'password': 'pass',
        'workspace': 'test',
        'sound': 'cars.wav',
    }
