# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QgsWcsClient2
                                 A QGIS plugin
 A OGC WCS 2.0/EO-WCS Client
                             -------------------
        begin                : 2014-06-26; 2017-04-10
        copyright            : (C) 2014 by Christian Schiller / EOX IT Services GmbH, Vienna, Austria
        email                : christian dot schiller at eox dot at
 ***************************************************************************/

/*********************************************************************************/
 *  The MIT License (MIT)                                                         *
 *                                                                                *
 *  Copyright (c) 2014 EOX IT Services GmbH                                       *
 *                                                                                *
 *  Permission is hereby granted, free of charge, to any person obtaining a copy  *
 *  of this software and associated documentation files (the "Software"), to deal *
 *  in the Software without restriction, including without limitation the rights  *
 *  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell     *
 *  copies of the Software, and to permit persons to whom the Software is         *
 *  furnished to do so, subject to the following conditions:                      *
 *                                                                                *
 *  The above copyright notice and this permission notice shall be included in    *
 *  all copies or substantial portions of the Software.                           *
 *                                                                                *
 *  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR    *
 *  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,      *
 *  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE   *
 *  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER        *
 *  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, *
 *  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE *
 *  SOFTWARE.                                                                     *
 *                                                                                *
 *********************************************************************************/
configuration for the QgsWcsClient2 plugin
"""
from __future__ import print_function

# some global setttings
settings = {}

#configured server listing (srv_list)
import os, pickle
global srv_list
global default_interpol

plugin_dir = os.path.dirname(os.path.realpath(__file__))

default_interpol = ['nearest (default)', 'bilinear', 'average (slow)']

    # read the sever names/urls from a file
def read_srv_list():
    insrvlst = os.path.join(plugin_dir, 'config_srvlist.pkl')
        # check if a 'config_srvlist.pkl already exists, if not create a default one
        # this prevents overwriting of user edited listings during update/re-installation
    if not os.path.isfile(insrvlst):
        chk_srvlist(insrvlst)

    fo = open(insrvlst, 'rb')
    sl = pickle.load(fo)
    fo.close()
    return sl


    # check if a insrvlst exists if not create a default one; this way we don't need to distribute a sepaerate file
    # and an already existing 'config_srvlist.pkl' doesn't get overwritten during the installation
def chk_srvlist(insrvlst):
    # fix_print_with_import
    print('Creating a default Server-list file')
    f = open(insrvlst,'w')
    # fix_print_with_import
    # fix_print_with_import
    print("(dp0", file=f)
    # fix_print_with_import
    # fix_print_with_import
    print("S'servers'", file=f)
    # fix_print_with_import
    # fix_print_with_import
    print("p1", file=f)
    # fix_print_with_import
    # fix_print_with_import
    print("(lp2", file=f)
    # fix_print_with_import
    # fix_print_with_import
    print("(lp3", file=f)
    # fix_print_with_import
    # fix_print_with_import
    print("VOGC: WCS 2.0/EO-WCS 1.0 - Reference Implemetation (EOxServer)", file=f)
    # fix_print_with_import
    # fix_print_with_import
    print("p4", file=f)
    # fix_print_with_import
    # fix_print_with_import
    print("aVhttp://ows.eox.at/cite/eoxserver/ows?", file=f)
    # fix_print_with_import
    # fix_print_with_import
    print("p5", file=f)
    # fix_print_with_import
    # fix_print_with_import
    print("aa(lp6", file=f)
    # fix_print_with_import
    # fix_print_with_import
    print("VOGC: WCS 2.0 - Reference Implementation (MapServer)", file=f)
    # fix_print_with_import
    # fix_print_with_import
    print("p7", file=f)
    # fix_print_with_import
    # fix_print_with_import
    print("aVhttp://ows.eox.at/cite/mapserver/ows?", file=f)
    # fix_print_with_import
    # fix_print_with_import
    print("p8", file=f)
    # fix_print_with_import
    # fix_print_with_import
    print("aas.", end=' ', file=f)
    f.close()


    # read the sever names/urls from a file
srv_list = read_srv_list()

