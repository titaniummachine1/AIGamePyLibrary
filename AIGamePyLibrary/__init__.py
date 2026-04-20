"""
AIGamePyLibrary - thin alias for the AIGameLibrary package.

The GitHub repo is named ``AIGamePyLibrary`` but the canonical importable
package is ``AIGameLibrary`` (no "Py"). This shim exists so that scripts
written by LLMs that pattern-match on the repo name still work:

    from AIGamePyLibrary import *           # OK (re-exports AIGameLibrary)
    from AIGamePyLibrary import Distance    # OK
    import AIGamePyLibrary                  # OK

This is a graph-builder library, NOT a runtime SDK. There is no ``sim``
object and no tick loop. See the README's "How this library works" and
"Common LLM mistakes" sections before writing code.
"""

from AIGameLibrary import *  # noqa: F401,F403
from AIGameLibrary import nodes as _nodes  # noqa: F401
from AIGameLibrary import customNodes as _customNodes  # noqa: F401

__all__ = [name for name in dir(_nodes) if not name.startswith("_")] + [
    name for name in dir(_customNodes) if not name.startswith("_")
]
