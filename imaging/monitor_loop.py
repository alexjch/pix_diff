import os
import shutil
import glob
from .detector import VideoMonitor
from .draw_bbox import draw_bbox

IN_PATH = None
OUT_PATH = None
DEFAULT_IMAGE_EXT = None
CHANGE_THRESHOLD = 3

defaults = {
    "in": IN_PATH,
    "out": OUT_PATH,
    "img_ext": "jpg"
}

vid_monitor = VideoMonitor()


def store(in_f, out_f):
    shutil.copyfile(in_f, out_f)


def remove(fn):
    if os.path.exists(fn):
        print("removing: {}".format(fn))
        os.unlink(fn)


def process_frame(frame, out=OUT_PATH):
    print('processing {}'.format(frame))
    change, bbox = vid_monitor.has_change(frame)
    if change is True:
        # Store
        print('saving {}'.format(frame))
        out_file = os.path.join(out, os.path.basename(frame))
        # Create path if it does not exists
        if os.path.exists(os.path.dirname(out_file)) is False:
            os.makedirs(os.path.dirname(out_file))
        store(frame, out_file)
        # Draw rectangle
        _ = draw_bbox(out_file, bbox)
        remove(out_file)
    return change


def process_frames(conf=defaults):
    img_ext = conf.get('img_ext')
    in_path = conf.get('in_frames')
    out_path = conf.get('out_frames')
    frames = glob.glob(os.path.join(in_path, "*.{}".format(img_ext)))
    if len(frames) < 2:
        return
    background = frames[0]
    frames = frames[1:]
    vid_monitor.background = background
    change_count = 0
    # Process frames
    for frame in frames:
        if process_frame(frame, out=out_path) is True:
            pass
        else:
            change_count += 1
            if change_count == CHANGE_THRESHOLD:
                change_count = 0
                # Update background
                vid_monitor.background = frame
