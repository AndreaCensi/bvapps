#!/usr/bin/env python
import sys, os

def main():
    files = sys.argv[1:]
    if not files:
        raise Exception('No files specified')
    stream = sys.stdout
    print_header(stream)

    for f in files:
        base = os.path.basename(f)
        print_video(stream, base)
        
    print_footer(stream)
    stream.flush()
    
def print_video(s, basename):
    rid =os.path.splitext(basename)[0]
    rid =  rid.replace('join-exz1sb-', '')
    rid =  rid.replace('join-exz1no-', '')
    
    s.write('<div id="%s" class="video-div">\n' % rid)
    s.write('<h2>%s</h2>\n' % rid)
    src=basename
    s.write(
    """
    <video controls="controls">
      <source src="%s" type="video/mp4" />
      Your browser does not support the video tag.
      <a href="%s">Download the MP4 file.</a>
    </video>
    """ % (src, src))
    s.write('</div>\n')
    
def print_header(s):
    s.write("""<html><head>Vehicles video</head>
    <link rel="stylesheet" href="style.css" type="text/css"/>
    <body>""")

def print_footer(s):
    s.write("""</body>\n</html>\n""")

if __name__ == '__main__':
    main()