import scooby


class Report(scooby.Report):
    def __init__(self, additional=None, ncol=3, text_width=80, sort=False):
        """Initiate a scooby.Report instance."""

        # Mandatory packages.
        large_image_core = [
            "large_image",
            "large_image_source_rasterio",
            "cachetools",
            "PIL",
            "psutil",
            "numpy",
            "palettable",
        ]
        core = [
            "localtileserver",
            "flask",
            "flask_caching",
            "flask_cors",
            "flask_restx",
            "requests",
            "werkzeug",
            "click",
            "server_thread",
            "scooby",
        ] + large_image_core

        # Optional packages.
        optional = [
            "gunicorn",
            "pylibmc",
            "ipyleaflet",
            "jupyterlab",
            "jupyter_server_proxy",
            "traitlets",
            "shapely",
            "folium",
            "matplotlib",
            "colorcet",
            "cmocean",
            "large_image_source_gdal",
            "large_image_source_mapnik",
            "large_image_source_pil",
            "large_image_source_tiff",
            "large_image_converter",
            "tifftools",
            "pyvips",
            "pylibtiff",
            "osgeo.gdal",
            "pyproj",
        ]

        scooby.Report.__init__(
            self,
            additional=additional,
            core=core,
            optional=optional,
            ncol=ncol,
            text_width=text_width,
            sort=sort,
        )
