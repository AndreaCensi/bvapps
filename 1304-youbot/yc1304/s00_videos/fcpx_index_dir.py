from conf_tools.utils.locate_files import locate_files
from procgraph.utils.calling_ext_program import system_cmd_result, CmdException
from procgraph.utils.friendly_paths import friendly_path
from procgraph.utils.strings import indent
from procgraph_mplayer.conversions import pg_video_info
import os
from procgraph_mplayer.conversions.video_convert import pg_video_convert


def create_event_for_fcpx(dirname, pattern, event_filename=None, event_name=None):
    """ Creates an index Event for final cut pro X """
    if event_filename is None:
        event_filename = os.path.join(dirname, 'event.fcpxml')

    if event_name is None:
        event_name = os.path.basename(dirname) + '-event' 
                
    filenames = list(locate_files(dirname, pattern))
    videos = [get_info_for_file(f, event_filename) for f in filenames]
        
    xml_index = fcpx_get_xml_event(videos, event_name)

    with open(event_filename, 'w') as f:
        f.write(xml_index.strip())

    print('written %s' % friendly_path(event_filename))


def fcpx_frac_time(t):
    units = 30000
    num = int(t * units)
    den = units
    return '%d/%ds' % (num, den)

    
def fcpx_get_xml_clip(video):
    duration = fcpx_frac_time(video['length'])

    v = dict(name=video['id_video'], duration=duration, format=video['id_format'])
    return """
      <clip name="{name}"  duration='{duration}' format="{format}">
          <video ref="{name}"  duration='{duration}'>
          </video>
      </clip>
    """.format(**v)
  
def fcpx_get_xml_event(videos, project_name): 
    videos = list(videos)
    assets = fcpx_get_xml_assets(videos)
    clips = fcpx_get_xml_clips(videos)

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

    


def fcpx_get_xml_assets(videos):
    return "\n".join(fcpx_get_xml_asset(v) for v in videos)

def fcpx_get_xml_asset(video):
    id_format = video['id_format']
    xml_format = fcpx_get_xml_format(id_format, video)
    xml_metadata = fcpx_get_xml_metadata(video['metadata'])
    xml_asset = \
"""
<asset id="{id_video}" src="{src}">
{metadata}
</asset>
""".format(metadata=indent(xml_metadata, ' ' * 4),
           id_video=video['id_video'], src=video['filename'])
           
    return xml_format + '\n' + xml_asset
 
  
def fcpx_get_xml_format(id_format, video):
    # fps = video['fps'] 
    
    t = '<format id="{id_format}" frameDuration="{frameDuration}" width="{width}" height="{height}"/>'
    
    frameDuration = '1001/30000s'  # XXX
    values = dict(frameDuration=frameDuration,
                  id_format=id_format,
                  width=video['width'],
                  height=video['height'])
    return t.format(**values)
    
    
    
def fcpx_get_xml_metadata(md):
    def fcpx_get_md(k, v):
        return '<md key="com.apple.proapps.custom.%s" value=%r/>' % (k, v)  
    mds = ['  ' + fcpx_get_md(k.lower(), v) for k, v in md.items()]
    s = '<metadata>\n' + '\n'.join(mds) + '\n</metadata>'
    return s

 
def fcpx_get_xml_clips(videos):
    return "\n\n".join(fcpx_get_xml_clip(v) for v in videos)

def recode_to_mp4(v, v_mp4):
    cmds = ['ffmpeg', '-y', '-i', v, '-vcodec', 'copy', v_mp4]

    try:
        system_cmd_result('.', cmds,
                  display_stdout=False,
                  display_stderr=False,
                  raise_on_error=True,
                  capture_keyboard_interrupt=False)
    except CmdException:
        raise
    
    
def get_info_for_file(v, index_filename):
    """ 
        v: video
        index_filename: used to create relative paths
        
    """
    v_mov = os.path.splitext(v)[0] + '.mov'
    if not os.path.exists(v_mov):
        print('Creating Final Cut friendly file:\n<- %s\n-> %s' % (friendly_path(v), friendly_path(v_mov)))
        pg_video_convert(v, v_mov,
                         vcodec='prores',
                         vcodec_params={'profile': 3})
        # convert_to_mov_prores(v, v_mov, profile=2, quiet=False)
    
    #         v_mp4 = os.path.splitext(v)[0] + '.mp4'
    #         if not os.path.exists(v_mp4):
    #             recode_to_mp4(v, v_mp4)
    
    T = os.path.getmtime(v)
    os.utime(v_mov, (T, T))
       
    rel_filename = os.path.relpath(v_mov, os.path.dirname(index_filename))
    id_video = os.path.splitext(os.path.basename(v))[0]
    id_format = id_video + '_format'
    
    info = pg_video_info(v)
    
    info['filename'] = rel_filename
    info['id_video'] = id_video
    info['id_format'] = id_format
    info['filename_abs'] = v_mov
    
    return info
