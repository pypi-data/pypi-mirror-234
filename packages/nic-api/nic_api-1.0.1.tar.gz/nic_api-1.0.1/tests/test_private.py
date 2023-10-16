"""Secret tests"""

from getpass import getpass
import json
import os

from oauthlib.oauth2.rfc6749.tokens import OAuth2Token

from nic_api import DnsApi
from nic_api import pprint
from nic_api.exceptions import ExpiredToken
from nic_api.models import (
    NSRecord,
    ARecord,
    AAAARecord,
    CNAMERecord,
    MXRecord,
    TXTRecord,
    SRVRecord,
    PTRRecord,
    DNAMERecord,
    HINFORecord,
    NAPTRRecord,
    RPRecord,
)


APP_LOGIN = "233031f0f85729067fba98e25f1dbd69"
APP_PASSWORD = "p5vduFX8uS8HRIj9ciOr15A0cr5S-BhoBVsyM7UuRaA"
DEFAULT_SERVICE = "DP2301147486"
DEFAULT_ZONE = "werylabs.tech"

TOKEN_CACHE_FILE = os.path.join(os.path.expanduser("~"), ".nic_api_token.json")


def test_add_print_rollback():
    api = DnsApi(APP_LOGIN, APP_PASSWORD, _load_token(), _save_token)
    api.default_service = DEFAULT_SERVICE
    api.default_zone = DEFAULT_ZONE
    records = [
        NSRecord(ns="dnsa.google.com.", name="@"),
        ARecord("1.1.1.1", name="foobar"),
        ARecord("8.8.8.8", name="тест-кириллицы".encode("idna").decode()),
        AAAARecord("cafe:dead:beef::1", name="foobar"),
        CNAMERecord("foo", name="bar"),
        MXRecord(50, "mx.foobar.ru", name="@"),
        TXTRecord("my name is Sergey", name="foobar"),
        TXTRecord("testing TTL", name="foobar", ttl=7200),
        SRVRecord(
            priority=0,
            weight=5,
            port=5060,
            target="sipserver.test.ru.",
            name="_sip._tcp",
        ),
        PTRRecord(ptr="1.0.168.192.in-addr.arpa."),
        DNAMERecord(dname="nic-api-test-2.com."),
        HINFORecord(hardware="IBM-PC/XT", os="OS/2"),
        NAPTRRecord(
            order=1,
            preference=100,
            flags="S",
            service="sip+D2U",
            replacement="_sip._udp.nic-api-test.com.",
        ),
        RPRecord(mbox="info.andrian.ninja.", txt="."),
    ]

    # Ensure there are no changes
    my_zones = [zone for zone in api.zones() if zone.name == DEFAULT_ZONE]
    assert len(my_zones) == 1 and not my_zones[0].has_changes

    # Add records
    added_records = api.add_record(records)

    assert added_records[2].idn_name == "тест-кириллицы"

    # Ensure changes are there
    my_zones = [zone for zone in api.zones() if zone.name == DEFAULT_ZONE]
    assert len(my_zones) == 1 and my_zones[0].has_changes

    try:
        all_records = api.records()
        for record in all_records:
            pprint(record)
    finally:
        api.rollback()

    # Ensure there are no changes again
    my_zones = [zone for zone in api.zones() if zone.name == DEFAULT_ZONE]
    assert len(my_zones) == 1 and not my_zones[0].has_changes


def test_add_delete_commit():
    api = DnsApi(APP_LOGIN, APP_PASSWORD, _load_token(), _save_token)
    api.default_service = DEFAULT_SERVICE
    api.default_zone = DEFAULT_ZONE

    # Ensure there are no changes
    my_zones = [zone for zone in api.zones() if zone.name == DEFAULT_ZONE]
    assert len(my_zones) == 1 and not my_zones[0].has_changes

    rec_1 = ARecord("1.1.1.1", name="foobar")
    added = api.add_record(rec_1)

    # Ensure changes are there
    my_zones = [zone for zone in api.zones() if zone.name == DEFAULT_ZONE]
    assert len(my_zones) == 1 and my_zones[0].has_changes

    api.delete_record(added[0].id)

    # Ensure changes are there
    my_zones = [zone for zone in api.zones() if zone.name == DEFAULT_ZONE]
    assert len(my_zones) == 1 and my_zones[0].has_changes

    api.commit()

    # Ensure there are no changes
    my_zones = [zone for zone in api.zones() if zone.name == DEFAULT_ZONE]
    assert len(my_zones) == 1 and not my_zones[0].has_changes


def _load_token():
    with open(TOKEN_CACHE_FILE, "r") as fp_token:
        token_data = json.load(fp_token)
    return OAuth2Token(token_data)


def _save_token(token):
    with open(TOKEN_CACHE_FILE, "w") as fp_token:
        json.dump(token, fp_token)


def main():
    api = None
    try:
        token = _load_token()
        api = DnsApi(APP_LOGIN, APP_PASSWORD, token, _save_token)
        services = api.services()
        print(services)
    except (ValueError, ExpiredToken) as exc_info:
        print(exc_info)
        username = input("Login: ")
        password = getpass("Password: ")
        if api is None:
            api = DnsApi(
                APP_LOGIN,
                APP_PASSWORD,
                token_updater_clb=_save_token,
            )
        api.get_token(username, password)
        services = api.services()
        print(services)


if __name__ == "__main__":
    main()
