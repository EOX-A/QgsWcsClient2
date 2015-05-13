QgsWcsClient2
=============

A QGis WCS2.0/EO-WCS Plugin 

A tool to download (and subset in space and time) a series of raster data

The WCS 2.0/EO-WCS Client allows to specify an Area-Of-Interest and a Time-Of-Interest and then access/download the raster data (coverages) from OGC WCS-2.0 compliant servers.
Unlike WMS, WCS enables the access to the original data (and not just to portrayals).
The tool also handles the EO-WCS Application profile which allows to access/download a full time-series of coverages with just a few clicks. For multi-band EO-imagery the bands of interest can also be selected/sub-setted and their order in the output can be chosen.
The downloaded coverages are directly loaded as layers into QGIS

Requirements: This tool requires the python lxml-module to be pre-installed. 

