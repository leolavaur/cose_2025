from pathlib import Path

from matplotlib import pyplot as plt
from matplotlib.backend_bases import register_backend
from matplotlib.backends.backend_pgf import FigureCanvasPgf
from matplotlib.figure import Figure

# Constants (configured for the CDB thesis template)
TEXTWIDTH = 6.30045  # in inches
PAGEWIDTH = 6.30045 + 1.17638 + 0.1384  # in inches


def init(style: str = "cdb.mplstyle"):
    # Make the interactive backend as PDF
    register_backend("pdf", FigureCanvasPgf)

    # Set the default style
    if (s := Path().cwd() / style).exists():
        plt.style.use(s.as_posix())
    elif (s := Path().cwd().parent / style).exists():
        plt.style.use(s.as_posix())
    else:
        print(f"Style file '{style}' not found.")


def newfig(
    format: float = 1.618 / 1,  # Golden ratio, can be 4/3, 16/9, etc.
    width: float = 1,  # % of \textwidth
    height: float | None = None,
    base_width: float = TEXTWIDTH,  # in inches
    base_height: float = TEXTWIDTH / 1.618,
    **kwargs,
) -> Figure:
    """Create a new figure with the appropriate size."""
    figwidth = base_width * width

    if height is not None:
        figheight = base_height * height
    else:
        figheight = figwidth / format

    # set constrained_layout to True by default
    kwargs["layout"] = kwargs.get("layout", "constrained")

    return plt.figure(figsize=(figwidth, figheight), **kwargs)
