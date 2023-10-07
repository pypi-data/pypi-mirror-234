from typing import Any, Dict, Optional

from helix_personmatching.mergers.merge_config import MergeConfig

CLIENT_EXTENSION_URL = "https://www.icanbwell.com/client"


class PracticeMerger:
    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def merge(
        self,
        *,
        row: Dict[str, Any],
        config: Optional[MergeConfig],
        graph: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        return row
