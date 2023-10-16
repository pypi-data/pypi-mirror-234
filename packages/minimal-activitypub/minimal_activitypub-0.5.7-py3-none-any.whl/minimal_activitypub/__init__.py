"""Package 'minimal_activitypub' level definitions."""
import sys
from typing import Any
from typing import Dict
from typing import Final

__version__: Final[str] = "0.5.7"
__display_name__: Final[str] = "Minimal-ActivityPub"
__package_name__: Final[str] = __display_name__.lower()
USER_AGENT: Final[
    str
] = f"{__display_name__}_v{__version__}_Python_{sys.version.split()[0]}"

Status = Dict[str, Any]
