
from conf_tools.utils.friendly_paths import friendly_path
from conf_tools.utils.indent_string import indent
from yc1304.s00_videos.fcpx_index_dir import fcpx_frac_time, get_info_for_file
import datetime
import os
from conf_tools.utils.locate_files import locate_files

# <?xml version="1.0" encoding="UTF-8" standalone="no"?>
# <!DOCTYPE fcpxml>
# <fcpxml version="1.2">
#   <project name="unicornA_base1_20130411201427-all">
#       
#         <!-- Project Resources -->
#         <resources>
#             <projectRef id="unicornA_base1_20130411201427" name="MyEvent"/>
#             <asset projectRef="unicornA_base1_20130411201427" 
#                    id="unicornA_base1_2013-04-11-20-14-27.cam_eye_right" 
#                   src="unicornA_base1_2013-04-11-20-14-27.cam_eye_right.mp4"/>
#             <asset projectRef="unicornA_base1_20130411201427" 
#                    id="unicornA_base1_2013-04-11-20-14-27.cam_back" 
#                   src="unicornA_base1_2013-04-11-20-14-27.cam_back.mp4"/>
#             <format id="large" frameDuration="1001/30000s" width="1920" height="1080"/>
#         </resources>
# 
#         <!-- Project Story Elements -->
#         <sequence format="large">
#             <spine>
#                 <clip duration="10s">
#                     <video ref="unicornA_base1_2013-04-11-20-14-27.cam_eye_right" duration="5s"/>
# 
#                     <clip lane="2" offset="1s" duration="10s">
#                     <video ref="unicornA_base1_2013-04-11-20-14-27.cam_back" duration="5s"/>
#                     </clip>
#                 </clip>
#             </spine>
#         </sequence>
#     </project>
# </fcpxml>

def create_project_for_fcpx(dirname, pattern, project_filename=None, project_name=None, event_name=None):
    """ Creates an index Event for final cut pro X """
    if project_filename is None:
        project_filename = os.path.join(dirname, 'project.fcpxml')

    if project_name is None:
        project_name = os.path.basename(dirname) + '-project'
                        
    filenames = list(locate_files(dirname, pattern))
    videos = [get_info_for_file(f, project_filename) for f in filenames]
        
    xml = fcpx_get_xml_project(videos, project_name, event_name)

    with open(project_filename, 'w') as f:
        f.write(xml.strip())

    print('written %s' % friendly_path(project_filename))
    

def fcpx_get_xml_project(videos, project_name, event_name): 
    videos = list(videos)
    assets = fcpx_get_xml_project_resources(videos, event_name)
    clips = fcpx_get_xml_project_clips(videos)

    template = """
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE fcpxml>
<fcpxml version="1.2">
<project name="{name}">
  <resources>
{assets}
  </resources>        
{clips}
</project>
</fcpxml>
    """
    assets = indent(assets, ' ' * 12)
    clips = indent(clips, ' ' * 8)
    s = template.format(name=project_name,
                        assets=assets,
                        clips=clips)
    return s


#
#             <projectRef id="unicornA_base1_20130411201427" name="MyEvent"/>
#             <asset projectRef="unicornA_base1_20130411201427" 
#                    id="unicornA_base1_2013-04-11-20-14-27.cam_eye_right" 
#                   src="unicornA_base1_2013-04-11-20-14-27.cam_eye_right.mp4"/>
#             <asset projectRef="unicornA_base1_20130411201427" 
#                    id="unicornA_base1_2013-04-11-20-14-27.cam_back" 
#                   src="unicornA_base1_2013-04-11-20-14-27.cam_back.mp4"/>
#             <format id="large" frameDuration="1001/30000s" width="1920" height="1080"/>
#         


def fcpx_get_xml_project_resources(videos, event):
    s = ""
    s += '<format id="large" name="FFVideoFormat1080p30"/>'
    s += '<projectRef id="{event}" name="{event}"/>\n'.format(event=event)
    
    def make_asset(v):
        t = '<asset projectRef="{event}" id="{id_video}" src="{filename}"/>'
        d = dict(event=event, id_video=v['id_video'], filename=v['filename'])
        return t.format(**d)
        
    s += "\n".join(map(make_asset, videos))
    
    return s
    
def fcpx_get_xml_project_clips(videos):
    def tw(t):
        return str(datetime.datetime.fromtimestamp(t))
                                         
    s = ''
    s += '<sequence format="large"><spine>\n'
    total_duration = max(v['length'] for v in videos)
    t0 = min(v['timestamp'] for v in videos)
    s += '<gap duration="{duration}">'.format(duration=fcpx_frac_time(total_duration))
    i = 0
    s += '<!-- t0 = %s -->' % t0
    for v in videos:
        i += 1
        cols = 3
        gx, gy = (i - 1) % cols, (i - 1) / cols 
        px = 30 * gx
        py = 30 * gy
        position = '%f %f' % (px, py)
        scale = '0.2 0.2'
        offset = v['timestamp'] - t0
        s += '<!-- timestamp = %s offset = %s -->' % (tw(v['timestamp']), offset)
        s += """
        <clip offset="{offset}" lane="{lane}" name="{name}" duration="{duration}">
            <adjust-transform position="{position}" scale="{scale}"/>
            <video  ref="{name}" duration="{duration}"/>
        </clip>
""".format(name=v['id_video'], lane=i, duration=fcpx_frac_time(v['length']),
           offset=fcpx_frac_time(offset), scale=scale, position=position)
    s += '</gap>'
    s += '</spine></sequence>'
#             <spine>
#                 <clip duration="10s">
#                     <video ref="unicornA_base1_2013-04-11-20-14-27.cam_eye_right" duration="5s"/>
# 
#                     <clip lane="2" offset="1s" duration="10s">
#                     <video ref="unicornA_base1_2013-04-11-20-14-27.cam_back" duration="5s"/>
#                     </clip>
#                 </clip>
#             </spine>
#         </sequence>
    return s
