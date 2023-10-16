from collections.abc import Iterable
import json
import logging
from typing import Any, List, Union

from localtileserver.tiler.palettes import get_palette_by_name

logger = logging.getLogger(__name__)


def reformat_style_query_parameters(args: dict):
    out = {}
    for k, v in args.items():
        name = k.split(".")[0]
        if name in out:
            out[name].append(v)
        else:
            out.setdefault(name, [v])
    # If not multiple, remove list
    for k, v in out.items():
        if len(v) == 1:
            out[k] = v[0]
    return out


def make_single_band_style(
    band: int,
    vmin: Union[int, float] = None,
    vmax: Union[int, float] = None,
    palette: Union[str, List[str]] = None,
    nodata: Union[int, float] = None,
    scheme: str = None,
    n_colors: int = 255,
):
    style = None
    if isinstance(band, (int, str)):
        band = int(band)
        # Check for 0-index:
        if band == 0:
            raise ValueError("0 is an invalid band index. Bands start at 1.")
        style = {"band": band}
        if vmin is not None:
            style["min"] = vmin
        if vmax is not None:
            style["max"] = vmax
        if nodata is not None:
            style["nodata"] = float(nodata)
        if palette:
            if isinstance(palette, str):
                style["palette"] = get_palette_by_name(palette, n_colors=n_colors)
            else:
                # TODO: check contents to make sure its a list of valid HEX colors
                style["palette"] = palette
        if scheme is not None:
            style["scheme"] = scheme
    return style


def safe_get(obj: Any, index: int):
    if isinstance(obj, (list, tuple)):
        try:
            return obj[index]
        except (TypeError, IndexError):
            return None
    return obj


def make_style(
    band: Union[int, List[int]],
    palette: Union[str, List[str]] = None,
    vmin: Union[Union[float, int], List[Union[float, int]]] = None,
    vmax: Union[Union[float, int], List[Union[float, int]]] = None,
    nodata: Union[Union[float, int], List[Union[float, int]]] = None,
    scheme: Union[str, List[str]] = None,
    n_colors: int = 255,
):
    style = None
    # Handle when user sets min/max/etc. but forgot band. Default to 1
    if not band and any(v is not None for v in [vmin, vmax, palette, nodata]):
        band = 1
    elif band == 0:
        return

    if isinstance(band, (int, str)):
        # Handle viewing single band
        style = make_single_band_style(
            band,
            vmin=vmin,
            vmax=vmax,
            palette=palette,
            nodata=nodata,
            scheme=scheme,
            n_colors=n_colors,
        )
    elif isinstance(band, Iterable):
        # Handle viewing multiple bands together
        style = {"bands": []}
        if palette is None and len(band) == 3:
            # Handle setting RGB by default
            palette = ["r", "g", "b"]
        for i, b in enumerate(band):
            vmi = safe_get(vmin, i)
            vma = safe_get(vmax, i)
            p = safe_get(palette, i)
            nod = safe_get(nodata, i)
            style["bands"].append(
                make_single_band_style(b, vmin=vmi, vmax=vma, palette=p, nodata=nod, scheme=scheme),
            )
    # Return JSON encoded
    if style:
        return json.dumps(style)
