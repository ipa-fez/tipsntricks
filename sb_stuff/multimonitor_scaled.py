#!/usr/bin/env python
import subprocess

def enablescreen(output, scale, w, h):
    internal_w = 3000
    internal_h = 2000
    external_fb_h = int(scale * h)
    external_fb_w = int(scale * w)
    fb_h = max(internal_h, external_fb_h)
    pos = internal_w + (output - 1) * external_fb_w
    fb_w = internal_w  + output * external_fb_w
    cmd = ['xrandr', '--output', 'DP1-{:d}'.format(output), '--scale', '{}x{}'.format(scale, scale), '--mode', '{:d}x{:d}'.format(w, h),
        '--fb', '{:d}x{:d}'.format(fb_w, fb_h), '--pos', '{:d}x0'.format(pos)]
    subprocess.call(cmd)
    #print " ".join(cmd)


scale = 1.3
w = 1920
h = 1080

enablescreen(1, scale, w, h)
enablescreen(2, scale, w, h)
