""" module:: test.tests_security_access
    :platform: Posix
    :synopsis: Tests for module socketcan_uds.security_access
    author:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""
import pytest

from socketcan_uds.security_access import seed_to_key
from random import randbytes, randint

KNOWN_SEED_KEYS_MASKS = {
    "DUZ": {
        "EDC17": {
            1: {'mask': 0x47D86C0F,
                'shifts': 35},
            3: {'mask': 0x391B0809,
                'shifts': 35},
            7: {'mask': 0x2F2815B3,
                'shifts': 35},
            9: {'mask': 0x6B9364DF,
                'shifts': 35},
            11: {'mask': 0x1FB70ACE,
                 'shifts': 35},
            13: {'mask': 0x2C0848D5,
                 'shifts': 35},
            15: {'mask': 0x281D42F6,
                 'shifts': 35},
            17: {'mask': 0x7D9C036F,
                 'shifts': 35},
            19: {'mask': 0x5BDF37D8,
                 'shifts': 35},
            21: {'mask': 0x4D7A625A,
                 'shifts': 35},
            23: {'mask': 0x409E62E7,
                 'shifts': 35},
            25: {'mask': 0x302D4DA2,
                 'shifts': 35},
        },
        "EDC16_EDC7": {
            1: {'mask': 0x00112233,
                'shifts': 35},
            3: {'mask': 0x11223344,
                'shifts': 35},
            7: {'mask': 0x22334455,
                'shifts': 35},
            9: {'mask': 0x33445566,
                'shifts': 35},
            11: {'mask': 0x55667788,
                 'shifts': 35},
            13: {'mask': 0x66778899,
                 'shifts': 35},
            15: {'mask': 0x778899AA,
                 'shifts': 35},
            17: {'mask': 0x8899AABB,
                 'shifts': 35},
            19: {'mask': 0x99AABBCC,
                 'shifts': 35},
        }
    },
    "FPT": {
        "EDC17": {
            3: {'mask': 0x0B16212C,
                'shifts': 35},
            # LEVEL 25:
            # Possible Mask 4B7AAE01
            # Possible Mask 54991BB2
            # Possible Mask 64162746
            # Possible Mask 7DBBDE97
            # Possible Mask 8DACCBFE
            # Possible Mask A92D6B1A
            # Possible Mask D61D34E5
            # Possible Mask FED5966B
        }
    }
}


class TestSecurityAccess:

    def test_seed_to_key_w_bytes(self):
        seed = randbytes(4)
        key = seed_to_key(seed)
        assert key
        assert isinstance(key, bytes)

    def test_seed_to_key_w_integer(self):
        seed = randint(0, 0xFFFFFFFF)
        key = seed_to_key(seed)
        assert key
        assert isinstance(key, int)

    def test_seed_to_key_w_unhandled_type(self):
        seed = "key"
        with pytest.raises(ValueError):
            seed_to_key(seed)

    def test_all_known_seed_keys(self):
        for oem, ecus in KNOWN_SEED_KEYS_MASKS.items():
            for ecu, seca_levels in ecus.items():
                for seca_level, seca_contents in seca_levels.items():
                    seed = randint(0, 0xFFFFFFFF)
                    key = seed_to_key(seed=seed,
                                      mask=seca_contents.get("mask"),
                                      shifts=seca_contents.get("shifts"))
                    assert key
