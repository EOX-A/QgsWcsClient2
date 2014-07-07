#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""
#------------------------------------------------------------------------------
# Name:  cmdline_wcs_client.py
#
#   Command Line interface to the general purpose WCS 2.0/EO-WCS Client (wcs_client.py):
#       This routine allows to use the  general purpose WCS 2.0/EO-WCS Client (wcs_client.py)
#       from the cmd-line. It importes the wcs_client (required) as a module.
#       It provieds extensive help information.
#
#   This WCS-Client provides the following functionality:
#         - GetCapabilities Request
#         - DescribeCoverage Request
#         - DescribeEOCoverageSet Request
#         - GetMap Request
#
#         - return responses
#         - download coverages
#         - download time-series of coverages
#
#   It allows users to specify:
#         + Server URL
#         + Area of Interest (subset)
#         + Time of Interest (time constrain)
#         + DatasetSeries or Coverage
#         + Rangesubsetting (eg. Bands)
#         + File-Format (image format) for downloads
#         + output CRS for downloads
#         + mediatype
#         + updateSequence
#         + containment
#         + section
#         + count
#         + interpolation
#         + size or resolution
#
#   Additional (non-standard parameters implemented:
#           + mask
#           + IDs_only (DescribeEOCoverageSet returns only CoverageIDs - to be used for immediate download)
#           + output (GetCoverage only - local location where downloaded files shall be written too)
#
#
#
# Name:        cmdline_wcs_client.py
# Project:     DeltaDREAM
# Author(s):   Christian Schiller <christian dot schiller at eox dot at>
##
#-------------------------------------------------------------------------------
# Copyright (C) 2014 EOX IT Services GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies of this Software or works derived from this Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#-------------------------------------------------------------------------------

"""

import sys

import argparse
    # wcs_client provides the WCS/EO-WCS functionality (required)
import wcs_client   # as wcsClient

global __version__
__version__ = '0.1'



#/************************************************************************/
#/*                              _get_cmdline()                           */
#/************************************************************************/
def _get_cmdline():
    """
        Handles the input from the cmd-line, extensive help, and usage information.
        It initiates some checks and reformatting of the input from the cmd-line
        It uses argparse() with submenus, providing the Mandatory and Optional parameter
        handling for each request type.
    """
   # print "I'm in "+sys._getframe().f_code.co_name

    #---------------
    class _reformat_outsize(argparse.Action):
        """
            reformats and sets the  size/resolution  parameter for the requested output-size
        """
        def __call__(self, cl_parser, namespace, values, option_string=None):
            out = ''
            label = values[1]
            if values[0].startswith('siz'):
                out = 'size='+label+'('+values[2]
            if values[0].startswith('res'):
                out = 'resolution='+label+'('+values[2]

            setattr(namespace, self.dest, out)

    #---------------
    class _chk_time(argparse.Action):
        """
            validates and reformats the received time input
        """
        def __call__(self, cl_parser, namespace, values, option_string=None):
            items = values.split(',')
            if len(values) < 1:
                raise argparse.ArgumentError
            else:
                out = ",".join(items)

            setattr(namespace, self.dest, out)

    #---------------
    class _chk_coord(argparse.Action):
        """
            checks and reformats the recieved coordinates and provides the corrcet Axis syntax
        """
        def __call__(self, cl_parser, namespace, values, option_string=None):
            print namespace
            if values[0].startswith('epsg'):
                crs = values[0].split(':')[1]
                label = values[1]
                coord = values[2].strip()
                out = label+','+'http://www.opengis.net/def/crs/EPSG/0/'+crs+'('+coord
            elif values[0].startswith('pix') or values[0].startswith('ori'):
                label = values[1]
                coord = values[2].strip()
                out = label+'('+coord
            else:
                print '\n', 'Input causing the Error: ', values
                raise argparse.ArgumentError

            setattr(namespace, self.dest, out)

    #---------------
    class _chk_mask(argparse.Action):
        """
            some simple checks of the recieved mask values (count, start=end , etc.)
        """
        def __call__(self, cl_parser, namespace, values, option_string=None):
            if values[0].startswith('epsg'):
                coord = values[1].split(',')
            else:
                coord = values[0].split(',')

            if  len(coord) % 2 is 0:
                if coord[0] == coord[-2] and coord[1] == coord[-1]:
                    if values[0].startswith('epsg'):
                        crs = values[0].split(':')[1]
                        out = crs+'('+",".join(coord)
                    else:
                        out = '4326('+",".join(coord)
                else:
                    raise ValueError('Provided Masking Polygon not closed')
            else:
                raise ValueError('Provided Mask coordinates are not given in pairs')


            setattr(namespace, self.dest, out)

    #---------------
    class _cnv2str(argparse.Action):
        """
            converts input received as  numbers/lists  to strings for further usage
        """
        def __call__(self, cl_parser, namespace, values, option_string=None):
            out = ",".join(values)
            setattr(namespace, self.dest, out)

    #---------------

       # workaround -> this is needed to handle negativ input values (eg. for coordinates)
        # otherwise argparser would interpret them as arguments
    for i, arg in enumerate(sys.argv):
        if (arg[0] == '-') and arg[1].isdigit():
            sys.argv[i] = ' '+arg

    #===============


        #  the argument parser sections
            # Common to all subparsers
    common_parser = argparse.ArgumentParser(add_help=False, version='%(prog)s'+':   '+ __version__)

    cl_parser = argparse.ArgumentParser(description='WCS 2.0.1/EO-WCS Client routine', parents=[common_parser])
    subparsers = cl_parser.add_subparsers(help='Requests', dest='request')


        # ==== GetCapabilities parameters
    getcap_parser = subparsers.add_parser('GetCapabilities', parents=[common_parser],
                        help='send a GetCapabilities request')

          # Mandatory parameters
    mandatory = getcap_parser.add_argument_group('Mandatory')
    mandatory.add_argument('-s', '--server_url', metavar='server_url', dest='server_url', action='store',
                         required=True, help='the SERVER URL to be contaced')

        # Optional parameters
    getcap_parser.add_argument('--updateSequence', metavar='[Date_of_Change]', dest='updateSequence', action='store',
                        help='to receive a new document only if it has changed since last requested (expressed in ISO-8601 e.g. 2007-04-05)')

    getcap_parser.add_argument('--sections', dest='sections', nargs='*', choices=['DatasetSeriesSummary', 'CoverageSummary', \
                        'Contents', 'ServiceIdentification', 'ServiceProvider', 'OperationsMetadata', 'Languages', 'All'],
                        help='request one or more section(s) of a Capabilities Document; NOTE: multiple sections need to \
                        be supplied within {};  [default=All]', action=_cnv2str)


        # ==== DescribeCoverage parameters
    desccov_parser = subparsers.add_parser('DescribeCoverage', parents=[common_parser],
                        help='send a DescribeCoverage request')

          # Mandatory parameters
    mandatory = desccov_parser.add_argument_group('Mandatory')

    mandatory.add_argument('-s', '--server_url', metavar='server_url', dest='server_url', action='store',
                         required=True, help='the SERVER URL which should be contaced')

    mandatory.add_argument('--coverageID', metavar='coverageID', required=True,
                        help='a valid ID of a Coverage or a StitchedMosaic')


        # ==== DescribeEOCoverageSet parameters
    desceocov_parser = subparsers.add_parser('DescribeEOCoverageSet', parents=[common_parser],
                        help='DescribeEOCoverageSet')

          # Mandatory parameters
    mandatory = desceocov_parser.add_argument_group('Mandatory')

    mandatory.add_argument('-s', '--server_url', metavar='server_url', dest='server_url', action='store',
                         required=True, help='the SERVER URL which should be contaced')

    mandatory.add_argument('--eoID', metavar='eoID', required=True,
                        help='a valid ID of a: DatasetSeries, Coverage, or StitchedMosaic ')

        # Optional parameters
    desceocov_parser.add_argument('--subset_lat', metavar='subset_lat', dest='subset_lat',
                        help='Allows to constrain the request in Lat-dimensions. \
                        The spatial constraint is always expressed in WGS84. ')

    desceocov_parser.add_argument('--subset_lon', metavar='subset_lon', dest='subset_lon',
                        help='Allows to constrain the request in Long-dimensions. \
                        The spatial constraint is always expressed in WGS84. ')

    desceocov_parser.add_argument('--subset_time', metavar='subset_Start, subset_End', action=_chk_time,
                        help='Allows to constrain the request in Time-dimensions. The temporal \
                        constraint is always expressed in ISO-8601 format and in the UTC time zone \
                        (e.g. -subset_time 2007-04-05T14:30Z,2007-04-07T23:59Z). ')

    desceocov_parser.add_argument('--containment', choices=['overlaps', 'contains'],
                        help='Allows to limit the spatial search results to either: overlaps (just touching) \
                        (=default) or contains (fully within)')

    desceocov_parser.add_argument('--count', metavar='count', help='Limits the maximum number of \
                        DatasetDescriptions returned')

    desceocov_parser.add_argument('--section', dest='section', choices=['DatasetSeriesSummary', 'CoverageSummary', 'All'],
                        nargs='+', help='request one or more section(s) of a DescribeEOCoverageSet Document; NOTE: multiple sections need to \
                        be supplied within {}; [default=All]', action=_cnv2str)

    desceocov_parser.add_argument('--IDs_only', dest='IDs_only', action='store_true', default=None, help='A non-standard parameter -\
                        which will provide only a listing of the available CoverageIDs; intended to be fed directly to a GetCoverage loop')


        # ==== GetCoverage parameters
    getcov_parser = subparsers.add_parser('GetCoverage', parents=[common_parser],
                        help='request a coverage for download')

          # Mandatory parameters
    mandatory = getcov_parser.add_argument_group('Mandatory')

    mandatory.add_argument('-s', '--server_url', metavar='server_url', dest='server_url', action='store',
                        required=True, help='the SERVER URL which should be contaced')

    mandatory.add_argument('--coverageID', metavar='coverageID', required=True, help='a valid coverageID')

    mandatory.add_argument('--format', choices=['tiff', 'jpeg', 'png', 'gif'],
                        required=True, help='requested format of coverage to be returned')

    mandatory.add_argument('-o', '--output', metavar='output', dest='output', action='store',
                        help='location where downloaded data shall be stored')

        # Optional parameters
    getcov_parser.add_argument('--subset_x', metavar='subset_x', action=_chk_coord, nargs=3,
                        help='Trimming of coverage in X-dimension (no slicing allowed!), \
                        Syntax: Coord-Type Axis-Label Coord,Coord; either in: pixel \
                        coordinates [use: pix x 400,200 ], coordinates without CRS (-> original projection) [use:  orig Long 12,14 ], \
                        or coordinates with CRS (-> reprojecting) [use:  epsg:4326 Long 17,17.4 ]')

    getcov_parser.add_argument('--subset_y', metavar='subset_y', action=_chk_coord, nargs=3,
                        help='Trimming of coverage in Y-dimension (no slicing allowed!), \
                        Syntax: Coord-Type Axis-Label Coord,Coord; either in: pixel \
                        coordinates [use: pix y 400,200 ], coordinates without CRS (-> original projection) [use:  orig Lat 12,14 ], \
                        or coordinates with CRS (-> reprojecting) [use:  epsg:4326 Lat 17,17.4 ]')

    getcov_parser.add_argument('--rangesubset', metavar='rangesubset', help='Subsetting in the range \
                        domain (e.g. Band-Subsetting, e.g. 3,2,1)')

    getcov_parser.add_argument('--outputcrs', metavar='outputcrs', type=int,
                        help='CRS for the requested output coverage, supplied as EPSG number [default=4326]. \
                        Example: --outputcrs 3035')

    getcov_parser.add_argument('--size_x', nargs='*', action=_reformat_outsize, metavar=('[size X 100 |', 'resolution Long 15 ]'),
                        help='Mutually exclusive, enter either: size & Axis-Label & integer dimension of \
                        the requested coverage or resolution & Axis-Label & the dimension of one pixel in X-Dimension')

    getcov_parser.add_argument('--size_y', nargs='*', action=_reformat_outsize, metavar=('[size Lat 100 |', 'resolution Y 15 ]'),
                        help='Mutually exclusive, enter either: size & Axis-Label & integer dimension of  \
                        the requested coverage or resolution & Axis-Label & dimension of one pixel in Y-Dimension')

    getcov_parser.add_argument('--interpolation', choices=['nearest', 'bilinear', 'average'],
                        help='Interpolation method to be used [default=nearest]')

    getcov_parser.add_argument('--mediatype', choices=['multipart/mixed'], nargs='?',
                        help='Coverage delivered directly as image file or enclosed in GML structure \
                        [default=parameter is not provided]')

    getcov_parser.add_argument('--mask', metavar='mask', action=_chk_mask, nargs='*',
                        help='Masking of coverage by polygon: define the polygon as a list of points \
                        (i.e. latitude and longitude values), e.g. lat1,lon1,lat2,lon2,...; make sure \
                        to close the polygon with the last pair of coordinates; CRS is optional; per default \
                        EPSG 4326 is assumed; use the subset parameter to crop the resulting coverage  \
                        Syntax:  epsg:xxxx lat1,lon1,lat2,lon2, lat3,lon3,lat1,lon1 \
                        epsg:4326 42,10,43,12,39,13,38,9,42,10')

        # parse the input and convert it into a dict
    input_params = cl_parser.parse_args().__dict__

    return input_params



#/************************************************************************/
#/*                               main()                                 */
#/************************************************************************/
def main():
    """
        Command Line interface to the general purpose WCS client (wcs_client.py) 
        for WCS 2.0/EO-WCS server access
        This cmd-line interface handles all functionalities as described in 
        the EOxServer ver.0.3 documentation 
        (http://eoxserver.org/doc/en/users/EO-WCS_request_parameters.html)
        It offers cmd-line execution of:
          - GetCapabilities Request
          - DescribeCoverage Request
          - DescribeEOCoverageSet Request
          - GetMap Request
    """
   # print "I'm in "+sys._getframe().f_code.co_name

        # get all parameters provided via cmd-line
    input_params = _get_cmdline()

        # execute the user selected Request-type
    if input_params.has_key('request'):
        to_call = input_params.get('request')

    wcs_call = wcs_client.wcsClient()

    exec "result = wcs_call."+to_call+"(input_params)"

    print result


if __name__ == "__main__":
    sys.exit(main())
