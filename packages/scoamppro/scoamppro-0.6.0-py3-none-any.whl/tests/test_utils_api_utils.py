import pytest
from unittest.mock import Mock

from scoamp.utils.api_utils import (save_auth, load_auth, switch_env)
from scoamp.utils.error import *

@pytest.fixture(scope='function')
def fake_auth_file(tmp_path, mocker):
    env = tmp_path / 'env.json'
    mocker.patch('scoamp.utils.api_utils.ENV_PATH', env)
    return  env


def test_auth_save_load(fake_auth_file):
    with pytest.raises(NotLoginError):
        load_auth()
    
    env_name1 = 'env1'
    ep1 = 'https://a.cn'
    ak1 = 'a111'
    sk1 = 's111'

    save_auth(env_name1, ep1, ak1, sk1)
    auth1 = load_auth(env_name1)
    assert auth1.endpoint == ep1
    assert auth1.access_key == ak1
    assert auth1.secret_key == sk1
    assert load_auth() == auth1
    with pytest.raises(NotLoginError):
        load_auth('xxx')

    env_name2 = 'env2'
    ep2 = 'https://b.cn'
    ak2 = 'a222'
    sk2 = 's222'

    save_auth(env_name2, ep2, ak2, sk2)
    auth2 = load_auth(env_name2)
    assert auth2.endpoint == ep2
    assert auth2.access_key == ak2
    assert auth2.secret_key == sk2
    assert load_auth() == auth2
 
    # switch env 
    switch_env(env_name1)
    assert load_auth() == auth1
    assert load_auth(env_name2) == auth2

    # override
    env_name3 = env_name2
    ep3 = 'https://c.cn'
    ak3 = 'a333'
    sk3 = 's333'
    save_auth(env_name3, ep3, ak3, sk3)
    auth3 = load_auth(env_name2)
    assert auth3.endpoint == ep3
    assert auth3.access_key == ak3
    assert auth3.secret_key == sk3
    assert load_auth() == auth3
 
