#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""
#------------------------------------------------------------------------------
# Name:  wcs_client.py
#
#   General purpose WCS 2.0/EO-WCS Client:
#       The routine is inteded to be imported as modules.
#       If cmd-line usage is desired the cmdline_wcs_client.py will provide it.
#       The documentation of the modules functionality is provided as doc-strings.
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
# Name:        wcs_client.py
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
from __future__ import print_function

from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import object
import sys
import os
import time, datetime
import urllib.request, urllib.error, urllib.parse, socket
#from xml.dom import minidom
from lxml import etree

global __version__
__version__ = '0.1'

    # check for OS Platform and set the Directory-Separator to be used
global dsep
dsep = os.sep

    # sets the url where epsg CRSs are defined/referenced
global crs_url
crs_url = 'http://www.opengis.net/def/crs/EPSG/0/'


    # sets a storage location in case the user doesn't provide one (to be on the save side) - eg. for error msgs.
global temp_storage
temp_storage = None
try_dir = ['TMP', 'TEMP', 'HOME', 'USER']
for elem in try_dir:
    temp_storage = os.getenv(elem)
    if temp_storage != None:
        break

if temp_storage is None:
    cur_dir = os.getcwd()
    temp_storage = cur_dir # +'/tmp'




#/************************************************************************/
#/*                              wcsClient()                             */
#/************************************************************************/

class wcsClient(object):
    """
        General purpose WCS client for WCS 2.0/EO-WCS server access.
        This client provides all functionalities as described in the EOxServer ver.0.3
        documentation (http://eoxserver.org/doc/en/users/EO-WCS_request_parameters.html).
        It offers:
          - GetCapabilities Request
          - DescribeCoverage Request
          - DescribeEOCoverageSet Request
          - GetMap Request
        It therefore provides the receipt of
            - GetCapabilities response XML documents
            - DescribeCoverage response XML documents
            - DescribeEOCoverageSet response XML documents
            - download coverages using GetCoverage request
            - download time-series of coverages using the combination of
              DescribeEOCoverageSet and GetCoverage requests
         It allows the users to specify:
            + Server URL
            + Area of Interest (subset)
            + Time of Interest (time constrain)
            + DatasetSeries or Coverage
            + Rangesubsetting (eg. Bands)
            + File-Format (image format) for downloads
            + output CRS for downloads
            + mediatype
            + updateSequence
            + containment
            + section
            + count
            + interpolation
            + size or resolution

         Aadditional (non-standard) parameters implemented:
            + mask
            + IDs_only (DescribeEOCoverageSet returns only CoverageIDs - to be
              used for immediate download)
            + output (GetCoverage only - local location where downloaded files
              shall be written too)

        Detailed description of parameters associated with each Request are
        porvided with the respective request
    """
        # default timeout for all sockets (in case a requests hangs)
    _timeout = 180
    socket.setdefaulttimeout(_timeout)



    def __init__(self):
        pass


    #/************************************************************************/
    #/*                       _valid_time_wrapper()                           */
    #/************************************************************************/

    def _valid_time_wrapper(self, indate_list):
        """
           Wrapper function to _validate_date(),it handles the looping through
           multiple input date values
           It test if the provided date value(s) are a valid dates and are formated in ISO-8601 format
           The function  _validate_date() performs the actual testing, but this
           is not intended to be called directly
           Input:  a 1 or 2-element list of ISO-8601 formated dates
           Returns:  a 2-element list of ISO-8601 formated dates
           Error:  if either, date is not valid or not in ISO-8601 format
        """
       # print "I'm in "+sys._getframe().f_code.co_name

        outdate = []
        for d in indate_list:
            outdate.append(self._validate_date(d))

            # add one day to get correct responses from WCS Servers
        if len(outdate) < 2:
            fyear = int(outdate[0][0:4])
            fmonth = int(outdate[0][5:7])
            fday = int(outdate[0][8:10])
            time_stamp = datetime.datetime(day=fday, month=fmonth, year=fyear)
            difference = time_stamp+datetime.timedelta(days=1)
            to_date = '%.4d-%.2d-%.2d' %  (difference.year, difference.month, difference.day)
            outdate.append(to_date)

        return outdate

    #/************************************************************************/
    #/*                          _validate_date()                            */
    #/************************************************************************/

    def _validate_date(self, indate):
        """
            Performs testing of the supplied date values (checks formats, validity, etc.)
            private function of _valid_time_wrapper(), which only handles the looping.
            _validate_date() is not intended to be called directly, only through the
            _valid_time_wrapper() function.
        """
       # print "I'm in "+sys._getframe().f_code.co_name

        if indate.endswith('Z'):
            testdate = indate[:-1]
        else:
            testdate = indate
            if len(indate) == 16 or len(indate) == 19:
                indate = indate+'Z'


        dateformat = ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M", "%Y-%m-%dT%H", "%Y-%m-%dT", "%Y-%m-%d"]

        dformat = dateformat.__iter__()
        cnt = next(dformat)
        while True:
            try:
                time.strptime(testdate, cnt)
                return indate
            except ValueError:
                try:
                    cnt = next(dformat)
                except StopIteration:
                    raise ValueError("Could not parse date - either date not valid or date not in ISO-8601 format : ", testdate)


    #/************************************************************************/
    #/*                           _set_base_request()                        */
    #/************************************************************************/
    def _set_base_request(self):
        """
            Returns the basic url components for any valid WCS request
        """
      #  print "I'm in "+sys._getframe().f_code.co_name

        base_request = {'service': 'service=WCS'}

        return base_request

    #/************************************************************************/
    #/*                            _set_base_cap()                           */
    #/************************************************************************/
    def _set_base_cap(self):
        """
            Returns the basic url components for a valid GetCapabilities request
        """
       # print "I'm in "+sys._getframe().f_code.co_name

        base_cap = {'request': '&request=',
            'server_url': '',
            'updateSequence': '&updateSequence=',
            'sections' :'&sections='}

        return base_cap


    #/************************************************************************/
    #/*                            _set_base_desccov()                       */
    #/************************************************************************/
    def _set_base_desccov(self):
        """
            Returns the basic urls components for a valid DescribeCoverage Request
        """
      #  print "I'm in "+sys._getframe().f_code.co_name

        base_desccov = {'version': '&version=',
            'request': '&request=',
            'server_url': '',
            'coverageID': '&coverageID='}

        return base_desccov


    #/************************************************************************/
    #/*                             _set_set_base_desceocovset()              */
    #/************************************************************************/
    def _set_base_desceocoverageset(self):
        """
            Returns the basic urls components for a valid DescribeEOCoverageSet Request
        """
       # print "I'm in "+sys._getframe().f_code.co_name

        base_desceocoverageset = {'version': '&version=',
            'request': '&request=',
            'server_url': '',
            'eoID': '&eoID=',
#            'subset_lon': '&subset=Long,'+crs_url+'4326(', #@@
#            'subset_lat': '&subset=Lat,'+crs_url+'4326(',  #@@
            'subset_lon': '&subset=Long(',
            'subset_lat': '&subset=Lat(',
            'subset_time': '&subset=phenomenonTime(%22',
            'containment': '&containment=',
            'sections': '&sections=',
            'count': '&count=',
            'IDs_only': False}

        #print "base_desceocoverageset", base_desceocoverageset
        return base_desceocoverageset


    #/************************************************************************/
    #/*                             _set_base_getcov()                        */
    #/************************************************************************/
    def _set_base_getcov(self):
        """
           Rreturns the basic urls components for a GetCoverage Request
        """
      #  print "I'm in "+sys._getframe().f_code.co_name

        getcov_dict = {'version': '&version=',
            'request': '&request=',
            'server_url': '',
            'coverageID': '&coverageid=',
            'format': '&format=',
            'subset_x': '&subset=',
            'subset_y': '&subset=',
            'rangesubset': '&rangesubset=',
            'outputcrs': '&outputcrs='+crs_url,
            'interpolation': '&interpolation=',     #@@
#            'interpolation': '&interpolation=nearest-neighbour',  #@@
            'mediatype': '&mediatype=',
            'mask': '&mask=polygon,'+crs_url,
            'size_x': '&',
            'size_y': '&',
            'output': None}

        return getcov_dict


    #/************************************************************************/
    #/*                           GetCapabilities()                          */
    #/************************************************************************/
    def GetCapabilities(self, input_params):
        """
            Creates a GetCapabilitiy request url based on the input_parameters
            and executes the request.
            The input_parameters have to be supplied as a dictionary.
            Input:
                Mandatory Parameters to be provided:
                    Request:      GetCapabilities
                    server_url:   Server URL to be accessed
                Optional prameters:
                    updateSequence:   Receive a new document only if it has changed since last
                        requested (expressed in ISO-8601 date format e.g. 2007-04-05)
                    sections:         Request one or more section(s) of a Capabilities Document
                        possible sections: [ DatasetSeriesSummary, CoverageSummary, Content, ServiceMetadata,
                        ServiceIdentification, ServiceProvider, OperationsMetadata, Languages, All ]
            Example:
                input_params= {'request': 'GetCapabilities',
                               'server_url': 'http://some.where.org/ows?' ,
                               'updateSequence': '2007-04-05',
                               'sections' : 'CoverageSummary' }
            Returns:  XML GetCapabilities resonse
        """
       # print "I'm in "+sys._getframe().f_code.co_name

        if 'updateSequence' in input_params and input_params['updateSequence'] is not None:
            res_in = self._valid_time_wrapper(list(input_params.get('updateSequence').split(',')))
            input_params['updateSequence'] = ','.join(res_in)

        procedure_dict = self._set_base_cap()
        http_request = self._create_request(input_params, procedure_dict)
        result_xml = wcsClient._execute_xml_request(self, http_request)

        return result_xml


    #/************************************************************************/
    #/*                           DescribeCoverage()                         */
    #/************************************************************************/
    def DescribeCoverage(self, input_params):
        """
            Creates a DescribeCoverage request url based on the input_parameters
            and executes the request.
            The input_parameters have to be supplied as a dictionary.
            Input:
                Mandatory Parameters to be provided:
                    Request:      DescribeCoverage
                    server_url:   Server URL to be accessed
                    coverageID:   one valid ID of a [ Coverage | StitchedMosaic ]
                Optional prameters:
                    None
            Example:
                input_params={'request': 'DescribeCoverage',
                               'server_url': 'http://some.where.org/ows?' ,
                               'coverageID': 'some_Coverage_ID_yxyxyx_yxyxyx' }
            Returns:   XML DescribeCoverage response
        """
      #  print "I'm in "+sys._getframe().f_code.co_name

        procedure_dict = self._set_base_desccov()

        http_request = self._create_request(input_params, procedure_dict)
        result_xml = wcsClient._execute_xml_request(self, http_request)

        return result_xml


    #/************************************************************************/
    #/*                          DescribeEOCoverageSet()                     */
    #/************************************************************************/
    def DescribeEOCoverageSet(self, input_params):
        """
            Creates a DescribeEOCoverageSet request url based on the input_parameters
            and executes the request.
            The input_parameters have to be supplied as a dictionary.
            Input:
                Mandatory Parameters to be provided:
                    Request:      DescribeEOCoverageSet;
                    server_url:   Server URL to be accessed;
                    eoID:         One valid ID of a: [ DatasetSeries | Coverage | StitchedMosaic ]
                Optional Parameters:
                    subset_lat:   Allows to constrain the request in Lat-dimensions. \
                                  The spatial constraint is always expressed in WGS84
                    subset_lon:   Allows to constrain the request in Long-dimensions. \
                                  The spatial constraint is always expressed in WGS84.
                    subset_time:  Allows to constrain the request in Time-dimensions. The temporal \
                                  constraint is always expressed in ISO-8601 format and in the UTC  \
                                  time zone (e.g. subset_time 2007-04-05T14:30:00Z,2007-04-07T23:59Z).
                    containment:  Allows to limits the spatial search results. \
                                  [ overlaps (just touching)(=default) | contains (fully within) ]
                    count:        Limits the maximum number of DatasetDescriptions returned
                    sections:      Request one or more section(s) of a DescribeEOCoverageSet Document;
                                  possible sections: [ DatasetSeriesDescription, CoverageDescription, All ]
                Non-standard Parameters implemented:
                    IDs_only:     Will provide only a listing of the available CoverageIDs;
                                  intended to feed results directly to a GetCoverage request loop [ True | False ]
            Example:
                input_params={'request': 'DescribeEOCoverageSet',
                              'server_url': 'http://some.where.org/ows?' ,
                              'eoID':  'some_ID_of_coverage_or_datasetseries_or_stitchedmosaic'
                              'subset_lon': '-2.7,-2.6'
                              'subset_lat': '47.6,47.7'
                              'subset_time':'2013-06-16,2013-07-01T23:59Z'
                              'IDs_only': True }
            Returns:    XML DescribeEOCoverageSet response  or  only a list of available coverageIDs
        """
       # print "I'm in "+sys._getframe().f_code.co_name

            # validate that the provided date/time stings are in ISO8601
        if 'subset_time' in input_params and input_params['subset_time'] is not None:
            res_in = self._valid_time_wrapper(list(input_params.get('subset_time').split(',')))
            input_params['subset_time'] = ','.join(res_in)

        procedure_dict = self._set_base_desceocoverageset()
        http_request = self._create_request(input_params, procedure_dict)

        if 'IDs_only' in input_params and input_params['IDs_only'] == True:
            result_list, axis_labels, offered_crs = wcsClient._execute_xml_request(self, http_request, IDs_only=True)
            return result_list, axis_labels, offered_crs
        else:
            result_list = wcsClient._execute_xml_request(self, http_request)
            return result_list


    #/************************************************************************/
    #/*                              GetCoverage()                           */
    #/************************************************************************/

    def GetCoverage(self, input_params, use_wcs_GCo_call):
        """
            Creates a GetCoverage request url based on the input_parameters
            and executes the request.
            The input_parameters have to be supplied as a dictionary.
            Input:
                Mandatory Parameters to be provided:
                    Request:      DescribeEOCoverageSet;
                    server_url:   Server URL to be accessed;
                    coverageID:   A valid coverageID
                    format:       Requested format of coverage to be returned, (e.g. tiff, jpeg, png, gif)
                                  but depends on offering of the server
                Non-standard Parameter implemented (Mandatory):
                    output:      Location where downloaded data shall be stored
                                 (defaulting to: global variable temp_storage, which will get set to
                                 the available environmental variables [ TMP | TEMP | HOME | USER | current_directory ] )
                Optional Parameters:
                    subset_x:    Trimming of coverage in X-dimension (no slicing allowed!),
                                 Syntax: Coord-Type Axis-Label Coord,Coord;
                                 either in: pixel coordinates [use: pix x 400,200 ], coordinates without
                                 CRS (-> original projection) [use:  orig Long 12,14 ], or coordinates
                                 with CRS (-> reprojecting) [use:  epsg:4326 Long 17,17.4 ]
                    subset_y:    Trimming of coverage in y-dimension (no slicing allowed!),
                                 Syntax: Coord-Type Axis-Label Coord,Coord;
                                 either in: pixel coordinates [use: pix x 400,200 ], coordinates without
                                 CRS (-> original projection) [use:  orig Long 12,14 ], or coordinates
                                 with CRS (-> reprojecting) [use:  epsg:4326 Long 17,17.4 ]
                    rangesubset: Subsetting in the range domain (e.g. Band-Subsetting, e.g. 3,2,1)
                    outputcrs:   CRS for the requested output coverage, supplied as EPSG number (default=4326)
                    size_x:      Mutually exclusive, enter either: size & Axis-Label & integer dimension of
                                 the requested coverage or resolution & Axis-Label & the dimension of one pixel
                                 in X-Dimension e.g.[size X 800 | resolution Long 15 ]
                    size_y:      Mutually exclusive, enter either: size & Axis-Label & integer dimension of
                                 the requested coverage or resolution & Axis-Label & the dimension of one pixel
                                 in Y-Dimension e.g.[size Y 320 | resolution Lat 55 ]
                    interpolation: Interpolation method to be used (default=nearest), ['nearest | bilinear | average]
                    mediatype:   Coverage delivered directly as an image file or enclosed inside a GML structure.
                                 parameter either [ not present (=default) | multipart/related ]
                Non-standard Parameter implemented (optional):
                    mask:        Masking of coverage by polygon: define the polygon as a list of points
                                 (i.e. latitude and longitude values), e.g. lat1,lon1,lat2,lon2,...; make sure
                                 to close the polygon with the last pair of coordinates; CRS is optional; per default
                                 EPSG 4326 is assumed; use the subset parameter to crop the resulting coverage
                                 Syntax:  epsg:xxxx lat1,lon1,lat2,lon2, lat3,lon3,lat1,lon1
                                 e.g.  epsg:4326 42,10,43,12,39,13,38,9,42,10'
        """
      #  print "I'm in "+sys._getframe().f_code.co_name

            # provide the same functionality for input as for the cmd-line
            # (to get around the url-notation for input)
        if 'subset_x' in input_params and input_params['subset_x'] is not None and input_params['subset_x'].startswith('epsg') :
            crs = input_params['subset_x'].split(':')[1].split(' ')[0]
            label = input_params['subset_x'].split(':')[1].split(' ')[1]
            coord = input_params['subset_x'].split(':')[1].split(' ')[2]
#            out = label+','+crs_url+crs+'('+coord   #@@
            out = label+'('+coord
            input_params['subset_x'] = out
        elif 'subset_x' in input_params and input_params['subset_x'] is not None and (input_params['subset_x'].startswith('pix') or input_params['subset_x'].startswith('ori')):
            label = input_params['subset_x'].split(' ')[1]
            coord = input_params['subset_x'].split(' ')[2]
            out = label+'('+coord
            input_params['subset_x'] = out
        else:
            pass

        if 'subset_y' in input_params and input_params['subset_y'] is not None and input_params['subset_y'].startswith('epsg'):
            crs = input_params['subset_y'].split(':')[1].split(' ')[0]
            label = input_params['subset_y'].split(':')[1].split(' ')[1]
            coord = input_params['subset_y'].split(':')[1].split(' ')[2]
#            out = label+','+crs_url+crs+'('+coord  #@@
            out = label+'('+coord
            input_params['subset_y'] = out
        elif 'subset_y' in input_params and input_params['subset_y'] is not None and (input_params['subset_y'].startswith('pix') or input_params['subset_y'].startswith('ori')):
            label = input_params['subset_y'].split(' ')[1]
            coord = input_params['subset_y'].split(' ')[2]
            out = label+'('+coord
            input_params['subset_y'] = out
        else:
            pass


        if 'size_x' in input_params and input_params['size_x'] is not None:
            if input_params['size_x'].startswith('siz'):
                out = "size="+input_params['size_x'].split(" ")[1]+"("+input_params['size_x'].split(" ")[2]
                input_params['size_x'] = out
            elif input_params['size_x'].startswith('res'):
                out = "resolution="+input_params['size_x'].split(" ")[1]+"("+input_params['size_x'].split(" ")[2]
                input_params['size_x'] = out

        if 'size_y' in input_params and input_params['size_y'] is not None:
            if input_params['size_y'].startswith('siz'):
                out = "size="+input_params['size_y'].split(" ")[1]+"("+input_params['size_y'].split(" ")[2]
                input_params['size_y'] = out
            elif input_params['size_y'].startswith('res'):
                out = "resolution="+input_params['size_y'].split(" ")[1]+"("+input_params['size_y'].split(" ")[2]
                input_params['size_y'] = out


        procedure_dict = self._set_base_getcov()
        http_request = self._create_request(input_params, procedure_dict)

        result = wcsClient._execute_getcov_request(self, http_request, input_params)

        return result


    #/************************************************************************/
    #/*                             parse_xml()                              */
    #/************************************************************************/
    def _parse_xml(self, in_xml):
        """
            Function to parse the request results of a DescribeEOCoverageSet
            and extract all available CoveragesIDs.
            This function is used when the the  IDs_only  parameter is supplied.
            Return:  List of available coverageIDs
        """
        join_xml = ''.join(in_xml)
        tree = etree.fromstring(join_xml)
        try:
            tag_ids = tree.xpath("wcs:CoverageDescriptions/wcs:CoverageDescription/wcs:CoverageId/text()", namespaces=tree.nsmap)
            #print tag_ids
        except etree.XPathEvalError:
            raise IndexError

        axis_labels = tree.xpath("wcs:CoverageDescriptions/wcs:CoverageDescription/gml:boundedBy/gml:Envelope/@axisLabels|wcs:CoverageDescriptions/wcs:CoverageDescription/gml:boundedBy/gml:EnvelopeWithTimePeriod/@axisLabels", namespaces=tree.nsmap)
        #print 'AxisLabels: ', type(axis_labels),len(axis_labels), axis_labels
        axis_labels = axis_labels[0].encode().split(" ")
        #print axis_labels
        offered_crs = tree.xpath("wcs:CoverageDescriptions/wcs:CoverageDescription/gml:boundedBy/gml:Envelope/@srsName|wcs:CoverageDescriptions/wcs:CoverageDescription/gml:boundedBy/gml:EnvelopeWithTimePeriod/@srsName", namespaces=tree.nsmap)
        offered_crs = os.path.basename(offered_crs[0])
        #print offered_crs
        if len(axis_labels) == 0:
            axis_labels = ["", ""]
        if len(offered_crs) == 0:
            offered_crs = '4326'

        return tag_ids, axis_labels[0:2], offered_crs


    #/************************************************************************/
    #/*                         _execute_xml_request()                       */
    #/************************************************************************/
    def _execute_xml_request(self, http_request, IDs_only=False):
        """
            Executes the GetCapabilities, DescribeCoverage, DescribeEOCoverageSet
            requests based on the generate http_url
            Returns:  either XML response document  or  a list of coverageIDs
            Output: prints out the submitted http_request  or Error_XML in case of failure
        """
      #  print "I'm in "+sys._getframe().f_code.co_name
        # fix_print_with_import
        # fix_print_with_import
        print('REQUEST: ',http_request)  #@@

        try:
                # create a request object,
            request_handle = urllib.request.Request(http_request, headers={'User-Agent': 'Python-urllib/2.7,QgsWcsClient-plugin'})
            response = urllib.request.urlopen(request_handle)
            xml_result = response.read()
            status = response.code
            #headers = response.headers.dict
            #print 'HEADERS ', headers
            #print 'XML-ResponseStatus: ', status



                # extract only the CoverageIDs and provide them as a list for further usage
            if IDs_only == True:
                try:
                    cids, axis_labels, offered_crs = self._parse_xml(xml_result)
    #                request_handle.close()
                    return cids, axis_labels, offered_crs
                except IndexError:
                    raise IndexError
            else:
                return xml_result

        except urllib.error.URLError as url_ERROR:
            if hasattr(url_ERROR, 'reason'):
                # fix_print_with_import
                print('\n', time.strftime("%Y-%m-%dT%H:%M:%S%Z"), "- ERROR:  Server not accessible -" , url_ERROR.reason)
                err_msg=['ERROR', url_ERROR.read()]
                return err_msg

                try:
                    # fix_print_with_import
                    print(url_ERROR.read(), '\n')

                except:
                    pass

            elif hasattr(url_ERROR, 'code'):
                # fix_print_with_import
                print(time.strftime("%Y-%m-%dT%H:%M:%S%Z"), "- ERROR:  The server couldn\'t fulfill the request - Code returned:  ", url_ERROR.code, url_ERROR.read())
                err_msg = str(url_ERROR.code)+'--'+url_ERROR.read()
                return err_msg

        return


    #/************************************************************************/
    #/*                     _execute_getcov_request()                        */
    #/************************************************************************/

    def _execute_getcov_request(self, http_request, input_params):
        """
            Executes the GetCoverage request based on the generated http_url and stores
            the receved/downloaded coverages in the defined  output location.
            The filenames are set to the coverageIDs (with extension according to requested file type)
            plus the the current date and time. This timestamp is added to avoid accidently overwriting of
            received coverages having the same coverageID but a differerent extend (AOI) (i.e.
            multiple subsets of the same coverage).

            Output: prints out the submitted http_request
                    stores the received datasets
                    saves Error-XML (-> access_error_"TimeStamp".xml) at output location (in case of failure)
            Returns:  HttpCode (if success)
        """
       # print "I'm in "+sys._getframe().f_code.co_name
        # fix_print_with_import
        # fix_print_with_import
        print('REQUEST:', http_request)

        now = time.strftime('_%Y%m%dT%H%M%S')

            # set some common extension to a more 'useful' type
        if input_params['format'].find('/') != -1:
            out_format_ext = os.path.basename(input_params['format'])
            if out_format_ext == "tiff":
                out_format_ext = "tif"
            elif out_format_ext == "x-netcdf":
                out_format_ext = "nc"
            elif out_format_ext == "jpeg":
                out_format_ext = "jpg"
            elif out_format_ext == "x-hdf":
                out_format_ext = "hdf"
            elif out_format_ext.startswith("gml"):
                out_format_ext = "gml"
        else:
            out_format_ext = input_params['format']


        out_coverageID = input_params['coverageID']+now+'.'+out_format_ext  # input_params['format']

        if 'output' in input_params and input_params['output'] is not None:
            outfile = input_params['output']+dsep+out_coverageID
        else:
            outfile = temp_storage+dsep+out_coverageID

            # fix_print_with_import
            # fix_print_with_import
            print('REQUEST-GetCov: ',http_request)  #@@

        try:
            request_handle = urllib.request.Request(http_request, headers={'User-Agent': 'Python-urllib/2.7,QgsWcsClient-plugin'})
            response = urllib.request.urlopen(request_handle)
            result = response.read()
            status = response.code
            #headers = response.headers.dict
            #print 'HEADERS ', headers
            #print 'GCov-Status: ', status

            try:
                file_getcov = open(outfile, 'w+b')
                file_getcov.write(result)
                file_getcov.flush()
                os.fsync(file_getcov.fileno())
                file_getcov.close()
                return status


            except IOError as xxx_todo_changeme:
                (errno, strerror) = xxx_todo_changeme.args
                # fix_print_with_import
                print("I/O error({0}): {1}".format(errno, strerror))
            except:
                # fix_print_with_import
                print("Unexpected error:", sys.exc_info()[0])
                raise


        except urllib.error.URLError as url_ERROR:
            if hasattr(url_ERROR, 'reason'):
                # fix_print_with_import
                print('\n', time.strftime("%Y-%m-%dT%H:%M:%S%Z"), "- ERROR:  Server not accessible -", url_ERROR.reason)
                    # write out the servers return msg
                errfile = outfile.rpartition(dsep)[0]+dsep+'access_error'+now+'.xml'
                access_err = open(errfile, 'w+b')
                access_err.write(url_ERROR.read())
                access_err.flush()
                access_err.close()
            elif hasattr(url_ERROR, 'code'):
                # fix_print_with_import
                print(time.strftime("%Y-%m-%dT%H:%M:%S%Z"), "- ERROR:  The server couldn\'t fulfill the request - Code returned:  ", url_ERROR.code, url_ERROR.read())
                err_msg = str(url_ERROR.code)+'--'+url_ERROR.read()
                return err_msg
        except TypeError:
            pass

        return #status


    #/************************************************************************/
    #/*                              _merge_dicts()                           */
    #/************************************************************************/
    def _merge_dicts(self, input_params, procedure_dict):
        """
            Merge and harmonize the input_params-dict with the required request-dict
            e.g. the base_getcov-dict
        """
        #print "I'm in "+sys._getframe().f_code.co_name

        request_dict = {}
        for k, v in input_params.items():
            #print 'TTTT: ',  k,' -- ',v
                # make sure there is always a version set
            if k == 'version' and (v == '' or v == None):
                v = '2.0.0'
                # skip all keys with None or True values
            if v == None or v == True:
                continue

                # create the request-dictionary but ensure there are no whitespaces left
                # (which got inserted for argparse() to handle negativ input values correctly)
            request_dict[k] = str(procedure_dict[k])+str(v).strip()

            # get the basic request settings
        base_request = self._set_base_request()
        request_dict.update(base_request)

        return request_dict



    #/************************************************************************/
    #/*                               _create_request()                      */
    #/************************************************************************/
    def _create_request(self, input_params, procedure_dict):
        """
            Create the http-request according to the user selected Request-type
        """
      #  print "I'm in "+sys._getframe().f_code.co_name

        request_dict = self._merge_dicts(input_params, procedure_dict)
        #print 'Request_Dict: ', request_dict  #@@

            # this doesn't look so nice, but this way I can control the order within the generated request
        http_request = ''
        if 'server_url' in request_dict:
            http_request = http_request+request_dict.get('server_url')
        if 'service' in request_dict:
            http_request = http_request+request_dict.get('service')
        if 'version' in request_dict:
            http_request = http_request+request_dict.get('version')
        if 'request' in request_dict:
            http_request = http_request+request_dict.get('request')
        if 'coverageID' in request_dict:
            http_request = http_request+request_dict.get('coverageID')
        if 'subset_x' in request_dict:
            http_request = http_request+request_dict.get('subset_x')+')'
        if 'subset_y' in request_dict:
            http_request = http_request+request_dict.get('subset_y')+')'
        if 'format' in request_dict:
            http_request = http_request+request_dict.get('format')
        if 'rangesubset' in request_dict:
            http_request = http_request+request_dict.get('rangesubset')
        if 'outputcrs' in request_dict:
            http_request = http_request+request_dict.get('outputcrs')
        if 'interpolation' in request_dict:
            http_request = http_request+request_dict.get('interpolation')
        if 'mediatype' in request_dict:
            http_request = http_request+request_dict.get('mediatype')
        if 'size_x' in request_dict:
            http_request = http_request+request_dict.get('size_x')+')'
        if 'size_y' in request_dict:
            http_request = http_request+request_dict.get('size_y')+')'
        if 'mask' in request_dict:
            http_request = http_request+request_dict.get('mask')+')'
        if 'updateSequence' in request_dict:
            http_request = http_request+request_dict.get('updateSequence')
        if 'sections' in request_dict:
            http_request = http_request+request_dict.get('sections')
        if 'eoID' in request_dict:
            http_request = http_request+request_dict.get('eoID')
        if 'subset_lat' in request_dict:
            http_request = http_request+request_dict.get('subset_lat')+')'
        if 'subset_lon' in request_dict:
            http_request = http_request+request_dict.get('subset_lon')+')'
        if 'subset_time' in request_dict:
            http_request = http_request+request_dict.get('subset_time').split(',')[0] \
                +'%22,%22'+request_dict.get('subset_time').split(',')[1]+'%22)'
        if 'containment' in request_dict:
            http_request = http_request+request_dict.get('containment')
        if 'section' in request_dict:
            http_request = http_request+request_dict.get('section')
        if 'count' in request_dict:
            http_request = http_request+request_dict.get('count')


        return http_request


#/************************************************************************/
# /*            END OF:        wcs_Client()                              */
#/************************************************************************/




