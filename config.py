# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QgsWcsClient2
                                 A QGIS plugin
 A OGC WCS 2.0/EO-WCS Client
                             -------------------
        begin                : 2014-06-26
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

# some global setttings
settings = {}

#configured server listing (srv_list)
import os, pickle
global srv_list

plugin_dir = os.path.dirname(os.path.realpath(__file__))


    # read the sever names/urls from a file
def read_srv_list():
    insrvlst = os.path.join(plugin_dir, 'config_srvlist.pkl')
    fo = open(insrvlst, 'rb')
    sl = pickle.load(fo)
    fo.close()
    return sl


srv_list = read_srv_list()
