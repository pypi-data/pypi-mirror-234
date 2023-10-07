from dataclasses import dataclass

from nicknames import NickNamer


@dataclass
class RuleOption:
    nick_namer: NickNamer
