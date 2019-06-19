import pytest

import ns1.rest.ipam

try:  # Python 3.3 +
    import unittest.mock as mock
except ImportError:
    import mock


def Any():
    class Any():
        def __eq__(self, other):
            return True
    return Any()


@pytest.fixture
def reservation_config(config):
    config.loadFromDict({
        'endpoint': 'api.nsone.net',
        'default_key': 'test1',
        'keys': {
            'test1': {
                'key': 'key-1',
                'desc': 'test key number 1',
                'writeLock': True
            }
        }
    })
    return config


def test_rest_reservation_list(reservation_config):
    z = ns1.rest.ipam.Reservations(reservation_config)
    z._make_request = mock.MagicMock()
    z.list(1)
    z._make_request.assert_called_once_with('GET',
                                            'dhcp/scopegroup/1/reservations',
                                            callback=None,
                                            errback=None)


@pytest.mark.parametrize('scopegroup_id, address_id, url',
                         [(1, 2,
                           'dhcp/scopegroup/1/reservations')])
def test_rest_reservation_retrieve(reservation_config, scopegroup_id,
                                   address_id, url):
    z = ns1.rest.ipam.Reservations(reservation_config)
    z._make_request = mock.MagicMock()
    z.retrieve(scopegroup_id, address_id)
    z._make_request.assert_called_once_with('GET',
                                            url,
                                            callback=None,
                                            errback=None)


@pytest.mark.parametrize('scopegroup_id, address_id, mac, url',
                         [(1, 2, '12:34:56:78:90:ab',
                           'dhcp/scopegroup/1/reservations')])
def test_rest_reservation_create(reservation_config, scopegroup_id,
                                 address_id, mac, url):
    z = ns1.rest.ipam.Reservations(reservation_config)
    z._make_request = mock.MagicMock()

    z.create(scopegroup_id, address_id, mac=mac)
    z._make_request.assert_called_once_with('POST',
                                            url,
                                            callback=Any(),
                                            errback=None,
                                            body={"address_id": address_id,
                                                  "mac": mac})


@pytest.mark.parametrize('scopegroup_id, address_id, url',
                         [(1, 2,
                           'dhcp/scopegroup/1/reservations?address_id=2')])
def test_rest_reservation_delete(reservation_config, scopegroup_id,
                                 address_id, url):
    z = ns1.rest.ipam.Reservations(reservation_config)
    z._make_request = mock.MagicMock()
    z.delete(scopegroup_id, address_id)
    z._make_request.assert_called_once_with('DELETE',
                                            url,
                                            callback=None,
                                            errback=None)