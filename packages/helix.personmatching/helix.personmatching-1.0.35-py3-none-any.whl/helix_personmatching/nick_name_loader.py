from importlib.resources import path
from typing import Set, Dict

# noinspection PyProtectedMember
from nicknames import default_lookup, _lookup_from_csv


class NickNameLoader:
    @staticmethod
    def load_nick_names() -> Dict[str, Set[str]]:
        with path(__package__, "nick_name_overrides.csv") as f:
            nickname_overrides: Dict[str, Set[str]] = _lookup_from_csv(f)
            nickname_lookup: Dict[str, Set[str]] = default_lookup()
            # now add the overrides
            for key, value in nickname_overrides.items():
                if key in nickname_lookup:
                    nickname_lookup[key] = nickname_lookup[key] | value
                else:
                    nickname_lookup[key] = value
            return nickname_lookup
