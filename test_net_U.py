

import os, sys
import urllib2, socket
from xml.dom import minidom


outpath = "/home/schillerc/cs_pylib/wcs_qgis_plugin/QgsWcsClient2/"
out = "response.xml"
#req_base = select_url
req_base= [ "http://data.eox.at/instance00/ows?", "http://neso.cryoland.enveo.at/cryoland/ows?" ]
req_p1 = "service=wcs&request=GetCapabilities&sections=ServiceMetadata"


cnt=0
for uu in req_base:
    http_request = uu + req_p1
    print http_request
    
    outfile = outpath+'_U_'+str(cnt)+'_'+out
    print outfile

    try:
            # access the url
        request_handle = urllib2.urlopen(http_request)
    #            status = request_handle.code
            # read the content of the url
        result_xml = request_handle.read()

    except urllib2.URLError, url_ERROR:
        if hasattr(url_ERROR, 'reason'):
            print '\n', time.strftime("%Y-%m-%dT%H:%M:%S%Z"), "- ERROR:  Server not accessible -", url_ERROR.reason

            try:
                print url_ERROR.read(), '\n'
            except:
                pass

        elif hasattr(url_ERROR, 'code'):
            print time.strftime("%Y-%m-%dT%H:%M:%S%Z"), "- ERROR:  The server couldn\'t fulfill the request - Code returned:  ", url_ERROR.code, url_ERROR.read()
            err_msg = str(url_ERROR.code)+'--'+url_ERROR.read()
            print err_msg
    

    fo = open(outfile,"wb")
    fo.write(result_xml)
    fo.flush()
    fo.close()

    cnt += 1

