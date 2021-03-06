'''
Created on Oct 14, 2014

@author: hijungshin
'''

import meanshift
import numpy as np
from visualobjects import VisualObject
import sys
import util
import panorama_object
import cv2
from scipy.signal import argrelextrema



def meanshift_visobjs(list_of_visobjs, ctlx, cbrx, ctly, cbry, cstart, cend, w, h, nframes, bandwidth=None):
    data = []
    for visobj in list_of_visobjs:
        x = ctlx * visobj.tlx + cbrx * visobj.brx
        y = ctly * visobj.tly + cbry * visobj.bry
        fid = cstart*visobj.start_fid + cend*visobj.end_fid
        
        data.append((x*w, y*h, fid*nframes))
        
    labels, cluster_centers = meanshift.cluster(np.array(data), bandwidth=bandwidth)
        
    return labels, cluster_centers

def cluster_by_line_seeds(list_of_objs, seeds):
    data = []
    for visobj in list_of_objs:
        data.append((0, 0.5*visobj.tly + 0.5*visobj.bry))
    labels, cluster_centers = meanshift.cluster_with_seeds(np.array(data), seeds)
    
    labels_unique = np.unique(labels)
    n_clusters = len(labels_unique)
    print '# lines:', n_clusters    
    lineobjs = [[] for i in range(0, n_clusters)]
    for i in range(0, len(list_of_objs)):
        lineobjs[labels[i]].append(list_of_objs[i])
    
    return lineobjs
        
def cluster_by_line(list_of_objs, hbandwidth):   
    labels, cluster_centers = meanshift_visobjs(list_of_objs, 0, 0, 0, 1.0, 0, 0.0, 1.0, 1.0, 1.0, bandwidth=hbandwidth) 
    labels_unique = np.unique(labels)
    n_clusters = len(labels_unique)
    
    print '# lines:', n_clusters    
    lineobjs = [[] for i in range(0, n_clusters)]
    for i in range(0, len(list_of_objs)):
        lineobjs[labels[i]].append(list_of_objs[i])
    
    return lineobjs

def get_line_labels(list_of_objs, hbandwidth):
    labels, cluster_centers = meanshift_visobjs(list_of_objs, 0, 0, 0, 1.0, 0, 0.0, 1.0, 1.0, 1.0, bandwidth=hbandwidth) 
    return labels
    

def cluster_by_time(list_of_objs, tbandwidth):
    labels, cluster_centers = meanshift_visobjs(list_of_objs, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, tbandwidth) 
    labels_unique = np.unique(labels)
    n_clusters = len(labels_unique)
    print '# time clusters:', n_clusters    
    timeobjs = [[] for i in range(0, n_clusters)]
    for i in range(0, len(list_of_objs)):
        timeobjs[labels[i]].append(list_of_objs[i])
    
    return timeobjs
    

def get_labeled_objs(list_of_clusters):
    label = 0
    labels = []
    list_of_objs = []
    nclusters = len(list_of_clusters)
    for i in range(0, nclusters):
        cluster = list_of_clusters[i]
        for c in cluster:
            list_of_objs.append(c)
            labels.append(label)
        label += 1
    return list_of_objs, labels

def is_cut(prevobj, curobj, time_thres, line_thres):
    if (curobj.start_fid == prevobj.start_fid):
        return False
    if (curobj.start_fid - prevobj.end_fid > time_thres):
        return True
    else:
        False
#     if (abs(curobj.bry - prevobj.bry) < line_thres):
#         return False
#     return True

def line_cluster_with_seeds_main():
    objdir = sys.argv[1]
    panoramapath = sys.argv[2]
    img_objs = VisualObject.objs_from_file(None, objdir)
    panorama = cv2.imread(panoramapath)
    line_ys = VisualObject.area_projection_function(img_objs, objdir, panorama)
    line_ys = util.smooth(line_ys, window_len=100)
    maxys = argrelextrema(line_ys, np.greater)
    print maxys
    seeds = []
    for y in maxys[0]:
        print y
        seeds.append((0,y))
    lineobjs = cluster_by_line_seeds(img_objs, np.array(seeds))
    
    list_of_objs, labels = get_labeled_objs(lineobjs)
    line_cluster = panorama_object.draw_clusters(panorama, list_of_objs, labels)
    util.saveimage(line_cluster, objdir, "line_cluster.png")
    util.showimages([line_cluster], "line cluster")
    


def line_cluster_main():
    objdir = sys.argv[1]
    panoramapath = sys.argv[2]
    img_objs = VisualObject.objs_from_file(None, objdir)
    panorama = cv2.imread(panoramapath)
   
    timeobjs = cluster_by_line(img_objs, 3*VisualObject.avg_height(img_objs))
    nlines = len(timeobjs)
    
    list_of_objs, labels = get_labeled_objs(timeobjs)
    line_cluster = panorama_object.draw_clusters(panorama, list_of_objs, labels)
    util.showimages([line_cluster], "line cluster")
    

def cluster_wth_threshold(list_of_objs, timethres, linethres, objdir):
    if len(list_of_objs) == 0:
        return None
    prevobj = list_of_objs[0]
    clusterobjs = []
    clusterobjs.append(prevobj)
    new_imgobjs = []
    for i in range(1, len(list_of_objs)):
        curobj = list_of_objs[i]
        if (is_cut(prevobj, curobj, timethres, linethres)):
            objgroup = VisualObject.group(clusterobjs, objdir)
            new_imgobjs.append(objgroup)
            clusterobjs = []
#             util.showimages([objgroup.img], 'objgroup')
        clusterobjs.append(curobj)
        prevobj = curobj
        
    objgroup = VisualObject.group(clusterobjs, objdir)    
    new_imgobjs.append(objgroup)
    return new_imgobjs

if __name__ == "__main__":
    
    
    line_cluster_with_seeds_main()
    
    
    