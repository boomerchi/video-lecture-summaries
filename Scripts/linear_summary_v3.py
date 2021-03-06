'''
Created on Jan 14, 2015

@author: hijungshin
'''

import sys
import lecturevisual
import util
from writehtml import WriteHtml
import os
import process_aligned_json as pjson

if __name__ == "__main__":
    videopath = sys.argv[1]
    panoramapath = sys.argv[2]
    objdir = sys.argv[3]
    scriptpath = sys.argv[4]
    title = sys.argv[5]
    
    [panorama, list_of_linegroups, list_of_sublines, list_of_stcstrokes, 
     list_of_strokes, list_of_chars] = lecturevisual.getvisuals(videopath, panoramapath, 
                                                                objdir, scriptpath)
     
    list_of_words = pjson.get_words(scriptpath)
    list_of_stcs = pjson.get_sentences(list_of_words)
    
     
    html = WriteHtml(objdir + "/linear_summary_v3_user_study.html", "Linear Summary with Context", stylesheet ="../Mainpage/summaries_v3.css")
    
    html.writestring("<iframe src=\"https://docs.google.com/forms/d/1rK79iFrErHIx-0jZHZQaIvOP_kwCZs4oaloe3WPX0xI/viewform?embedded=true\" width=\"780\" height=\"900\" frameborder=\"0\" marginheight=\"0\" marginwidth=\"0\">Loading...</iframe>")
    
    html.writestring("<h3>The first figure following the title shows a panoramic view of the entire lecture board. The following note presents figures and transcript in the order they appear in the lecture. The RIGHT figure shows the line that is being discussed, and the LEFT figure shows that line in the context of the panorama.</h3>")
    html.writestring("<h1>%s</h1><br>"%title)
    html.figure(panoramapath, width = "98%")
    
    figdir = objdir + "/linear_summary_v3_figures"
    if not os.path.exists(os.path.abspath(figdir)):
        os.makedirs(os.path.abspath(figdir))
    
    cur_stc_id = 0
    
    for subline in list_of_sublines:
        if (len(subline.list_of_stcstrokes) > 0):
            start_stc_id = subline.list_of_stcstrokes[0].stc_id
            if (start_stc_id > cur_stc_id):
                html.opendiv(idstring="wrapper")
                html.opendiv(idstring="c0")
                for i in range(cur_stc_id, start_stc_id):
                    print 'c00' , i 
                    html.write_list_of_words(list_of_stcs[i])
                cur_stc_id = start_stc_id
                html.closediv()
                html.closediv()
        
        html.opendiv(idstring="wrapper")
        
        pline = lecturevisual.panorama_lines(panorama, [subline.linegroup])
        pline_filename = "panorama_line_%i_%i.png"%(subline.line_id, subline.sub_line_id)
        util.saveimage(pline, figdir, pline_filename)
        
        html.opendiv(idstring="c1")
        html.image(figdir + "/" + pline_filename)
        html.closediv()
        
        html.opendiv(idstring="c2")
        html.image(subline.obj_in_line.imgpath)
        html.closediv()
        
        html.opendiv(idstring="c3")
        if (len(subline.list_of_stcstrokes) > 0):
            start_stc_id = subline.list_of_stcstrokes[0].stc_id
            end_stc_id = subline.list_of_stcstrokes[-1].stc_id
            for i in range(cur_stc_id, (end_stc_id+1)):
                print 'c3' , i 
                html.write_list_of_words(list_of_stcs[i])
            html.closediv()
            cur_stc_id = end_stc_id +1
        html.closediv()
    
    if (cur_stc_id < len(list_of_stcs) -1):
        html.opendiv(idstring="wrapper")
        html.opendiv(idstring="c0")
        for i in range(cur_stc_id, len(list_of_stcs)):
            print 'c10' , i 
            html.write_list_of_words(list_of_stcs[i])
        html.closediv()
        html.closediv()
    
    html.writestring("<p><!-- pagebreak --></p> ")
    html.writestring("<iframe src=\"https://docs.google.com/forms/d/1tWKK9LXFuqx3-dyu26wBOLD_m9EVoWMu8braJ2vEBA0/viewform?embedded=true\" width=\"780\" height=\"1280\" frameborder=\"0\" marginheight=\"0\" marginwidth=\"0\">Loading...</iframe>")
    
    html.closehtml()