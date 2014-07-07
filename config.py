# configuration for the QgsWcsClient2 plugin

# for some global setttings 
settings = {}

#configured server listing (srv_list)
import os, pickle
global srv_list
#srv_list= {}


plugin_dir = os.path.dirname(os.path.realpath(__file__))

#def __init__(self):
    #global srv_list
    #srv_list = read_srv_list()
    

    # read the sever names/urls from a file
def read_srv_list():
    #plugloc = os.path.realpath(os.path.curdir)
    insrvlst = os.path.join(plugin_dir,'config_srvlist.pkl')
    fo = open(insrvlst, 'rb')
    sl = pickle.load(fo)
    fo.close()
    return sl

#def get_plugindir():
    #plugin_dir = os.path.dirname(__file__)
    #os.path.dirname(os.path.realpath(__file__))
    #print __file__
    #print plugin_dir



srv_list = read_srv_list()
