"""
TO-DO
"""

# To activate virtual environemnt
# For windows
# pupillabs\Scripts\activate
# For linux/mac
# source tutorial-env/bin/activate

tracking = False
debug = False
ip = "192.168.1.5"

# Variables
fix_size = 30
winCol = (-1,-1,-1)
# winCol = (0,0,0)
nMarkers = 4
side_pixels = 128
pad_width = int(side_pixels/8)

def translate_from_topLeft_to_center(screen_size, pos):
    x, y = pos
    translated_x = x - screen_size[0] / 2
    translated_y = screen_size[1] / 2 - y
    return (translated_x, translated_y)

def translate_from_topLeft_to_center(screen_size, pos):
    x, y = pos
    translated_x = x - screen_size[0] / 2
    translated_y = screen_size[1] / 2 - y
    return (translated_x, translated_y)

def translate_from_bottomLeft_to_center(screen_size, pos):
    x, y = pos
    translated_x = x - screen_size[0] / 2
    translated_y = y - screen_size[1] / 2
    return (translated_x, translated_y)

def norm2screen(screen_size, pos):
    x, y = pos
    screen_x = x * screen_size[0]
    screen_y = y * screen_size[1]
    return (screen_x, screen_y)

# Make markers
from pupil_labs.real_time_screen_gaze import marker_generator
...
"""
More markers will yield higher accuracy
Make 4 markers at least
"""
from matplotlib import pyplot as plt
import numpy as np

marker_pixels = {}
for marker_id in range(nMarkers):
    marker_pixels[marker_id] = marker_generator.generate_marker(marker_id=marker_id, side_pixels=side_pixels, flip_x=True)
    # Add white border to the markers
    marker_pixels[marker_id] = np.pad(marker_pixels[marker_id], pad_width=pad_width, mode='constant', constant_values=255)
    # print("\n\nMarker ID: ", marker_id, "\n", marker_pixels[marker_id])

marker_size = marker_pixels[0].shape[0]
print(f" Marker size: {marker_size}")

"""
Set up GazeMapper object
Requires calibration data for the scene camera
"""
from pupil_labs.realtime_api.simple import discover_one_device, Device
from pupil_labs.real_time_screen_gaze.gaze_mapper import GazeMapper
...

if tracking:
    device = discover_one_device()
    # hard code ip address for now
    device = Device(address=ip, port="8080")

    # check if device can be found
    if device is None:
        print("No device found.")
        raise SystemExit(-1)


    print(f"Phone IP address: {device.phone_ip}")
    print(f"Phone name: {device.phone_name}")
    print(f"Phone unique ID: {device.phone_id}")

    print(f"Battery level: {device.battery_level_percent}%")
    print(f"Battery state: {device.battery_state}")

    print(f"Free storage: {device.memory_num_free_bytes / 1024**3}GB")
    print(f"Storage level: {device.memory_state}")

    print(f"Connected glasses: SN {device.serial_number_glasses}")
    print(f"Connected scene camera: SN {device.serial_number_scene_cam}")

    calibration = device.get_calibration()
    print(f"\n\nCalibration data: {calibration}")
    gaze_mapper = GazeMapper(calibration)
    print(f"\n\nGazeMapper object: {gaze_mapper}")

"""
Call PsychoPy and start drawing
"""
from psychopy import core, event, visual
from psychopy.event import Mouse
from params import params
from drawStim import drawStim
from pupil_labs.realtime_api.simple import discover_one_device
import json
...
BS = {}
# env,param,stim,circLoc,win,deg,sequence = params(BS)
# Open a window
win = visual.Window(size = (800,600),fullscr=True, screen=1, units='pix', color=winCol) # external monitor
mouse = Mouse(visible=False, newPos=None,win=win)


# screen_size = (1440, 900) # MacBook Air M1
lumVal = win._getPixels(makeLum=True)
screen_size = lumVal.shape[1], lumVal.shape[0] # width, height
print(f"\n\nScreen size is: {screen_size}")
"""
Now that we have a GazeMapper object, we need to specify which AprilTag markers we're using 
and where they appear on the screen.
"""
# 0,0 is top left corner of screen, Puipil Labs coordinates
marker_verts = { # do not include white padding
    0: [ # marker id 0, top left corner
        (pad_width, pad_width), # Top left marker corner
        (pad_width+side_pixels, pad_width), # Top right
        (pad_width+side_pixels, pad_width+side_pixels), # Bottom right
        (pad_width, pad_width+side_pixels), # Bottom left
    ],
    1: [ # marker id 1, top right corner
        (screen_size[0]-pad_width-side_pixels, pad_width), # Top left marker corner
        (screen_size[0]-pad_width, pad_width), # Top right
        (screen_size[0]-pad_width, pad_width+side_pixels), # Bottom right
        (screen_size[0]-pad_width-side_pixels, pad_width+side_pixels), # Bottom left
    ],
    2: [ # marker id 2, bottom left corner
        (pad_width, screen_size[1]-pad_width-side_pixels), # Top left marker corner
        (pad_width+side_pixels, screen_size[1]-pad_width-side_pixels), # Top right
        (pad_width+side_pixels, screen_size[1]-pad_width), # Bottom right
        (pad_width, screen_size[1]-pad_width), # Bottom left
    ],
    3: [ # marker id 3, bottom right corner
        (screen_size[0]-pad_width-side_pixels, screen_size[1]-pad_width-side_pixels), # Top left marker corner
        (screen_size[0]-pad_width, screen_size[1]-pad_width-side_pixels), # Top right
        (screen_size[0]-pad_width, screen_size[1]-pad_width), # Bottom right
        (screen_size[0]-pad_width-side_pixels, screen_size[1]-pad_width), # Bottom left
    ],
}

# for id, verts in marker_verts.items():
#     print(f"\n\nMarker ID: {id}")
#     for vert in verts:
#         print(vert)

marker_pos = { # 0,0 is center of screen - PsychoPy coordinates
    0: [-screen_size[0]/2 + marker_size/2, screen_size[1]/2 - marker_size/2], # top left
    1: [screen_size[0]/2 - marker_size/2, screen_size[1]/2 - marker_size/2], # top right
    2: [-screen_size[0]/2 + marker_size/2, -screen_size[1]/2 + marker_size/2], # bottom left
    3: [screen_size[0]/2 - marker_size/2, -screen_size[1]/2 + marker_size/2] # bottom right
}


def drawStim(type, win=win, screen_size=screen_size, fix_col="white", marker_pos=marker_pos, marker_pixels=marker_pixels, marker_verts=marker_verts, fix_size=fix_size):
    if type == "fixation":
        # Draw fixation        
        fix_lw = 10
        line1 = visual.Line(win, start=[-fix_size,0], end=[fix_size,0], 
                            lineColor=fix_col, lineWidth=fix_lw)
        line2 = visual.Line(win, start=[0,-fix_size], end=[0,fix_size],
                            lineColor=fix_col, lineWidth=fix_lw)    
        line1.draw()
        line2.draw()

    if type == "marker":
        # Draw markers
        for marker_id, pos in marker_pos.items():
            image_np = marker_pixels[marker_id]
            # image_np = (image_np.astype(float) / 255.0) * 2 - 1 # convert to float in [-1,1], assuming image is 8-bit uint.
            image_np = (image_np.astype(float) / 255.0) - 1 # convert to float in [-1,0], assuming image is 8-bit uint.
            # print(np.unique(image_np))
            image_stim = visual.ImageStim(
                win,
                image=image_np,
                units="pix",
                size=(image_np.shape[1],
                    image_np.shape[0]),
                colorSpace="rgb",
                pos=pos
            )
            image_stim.draw()

    if type == "outline":
        # Draw red outlines according to marker_verts
        for marker_id, verts in marker_verts.items():
            line1 = visual.Line(win, start=translate_from_topLeft_to_center(screen_size, verts[0]), end=translate_from_topLeft_to_center(screen_size, verts[1]), lineColor="red", lineWidth=2)
            line2 = visual.Line(win, start=translate_from_topLeft_to_center(screen_size, verts[1]), end=translate_from_topLeft_to_center(screen_size, verts[2]), lineColor="red", lineWidth=2)
            line3 = visual.Line(win, start=translate_from_topLeft_to_center(screen_size, verts[2]), end=translate_from_topLeft_to_center(screen_size, verts[3]), lineColor="red", lineWidth=2)
            line4 = visual.Line(win, start=translate_from_topLeft_to_center(screen_size, verts[3]), end=translate_from_topLeft_to_center(screen_size, verts[0]), lineColor="red", lineWidth=2)
            line1.draw()
            line2.draw()
            line3.draw()
            line4.draw()
    
# while True loop to keep drawing and tracking
keepDrawing = True
gaze_data = []

fix_col="white"
# 1st frame
fr = 1
drawStim("fixation", fix_col=fix_col)
drawStim("marker")
if debug: drawStim("outline")
# print(f"frame {fr}")
win.flip()

# Get screen surface
if tracking:
    screen_surface = gaze_mapper.add_surface(
                                        marker_verts,
                                        screen_size
                                        )
    print(f"\nscreen surface uid: {screen_surface.uid}\n\n")
    print(f"\n\nscreen surface object: {screen_surface}\n\n")
    # device = discover_one_device(max_search_duration_seconds=10)
    # hard code ip address for now
    # device = Device(address=ip, port="8080")

while keepDrawing: 
    fr += 1
    drawStim("fixation", fix_col=fix_col)
    drawStim("marker")
    if debug: drawStim("outline")

    """
    With that, setup is complete and we're ready to start mapping gaze to the screen! 
    On each iteration of our main loop we'll grab a video frame from the scene camera 
    and gaze data from the Realtime API. We pass those along to our GazeMapper instance 
    for processing, and it returns our gaze positions mapped to screen coordinates.
    """   

    # draw circle object to show gaze position
    circle = visual.Circle(win, radius=10, edges='circle', units='pix', 
                            fillColor=None, lineColor='yellow', lineWidth=5)
    
    if tracking:
        # device = discover_one_device(max_search_duration_seconds=.01)
        # device = discover_one_device()
        # # hard code ip address for now
        device = Device(address=ip, port="8080")

        try:            
            frame, gaze = device.receive_matched_scene_video_frame_and_gaze()
            print(f"\nFrame {fr}: Gaze at {gaze.x}, {gaze.y}\n")
            result = gaze_mapper.process_frame(frame, gaze)
            for surface_gaze in result.mapped_gaze[screen_surface.uid]:
                print(f"\nFrame {fr}: Normalized mapped gaze at {surface_gaze.x}, {surface_gaze.y}\n")
                screen_gaze = norm2screen(screen_size, (surface_gaze.x, surface_gaze.y))
                print(f"\nFrame {fr}: Screen mapped gaze at {screen_gaze[0]}, {screen_gaze[1]}\n")
                translated_gaze = translate_from_bottomLeft_to_center(screen_size, screen_gaze)
                print(f"\nFrame {fr}: Translated screen mapped gaze at {translated_gaze[0]}, {translated_gaze[1]}\n")
                
                gaze_data.append({"x": translated_gaze[0], "y": translated_gaze[1]})
                circle.pos = translated_gaze
                circle.draw()
        except KeyboardInterrupt:
            pass
        # finally:
            # print("Stopping...")
            # device.close()  # explicitly stop auto-update

        """
        frame, gaze = device.receive_matched_scene_video_frame_and_gaze()
        result = gaze_mapper.process_frame(frame, gaze)
        for surface_gaze in result.mapped_gaze[screen_surface.uid]:
            print(f"Gaze at {surface_gaze.x}, {surface_gaze.y}")
            gaze_data.append({"x": surface_gaze.x, "y": surface_gaze.y})
            circle.pos = (surface_gaze.x, surface_gaze.y)
            circle.draw()
        """
    else:
        circle.pos = mouse.getPos()
        circle.draw()

    # Check if circle.pos is within a circle with radius=fix_size from the center of the screen
    if circle.pos[0]**2 + circle.pos[1]**2 <= (fix_size+20)**2:
        fix_col = "green"
    else:
        fix_col = "red"

    win.flip()

    # Exit loop if escape key is pressed
    a = event.getKeys(timeStamped=True)
    keys = [row[0] for row in a]
    # secs = [row[1] for row in a][-1]

    for key in keys:
        if key in ['escape', 'q']: 
            keepDrawing = False
            win.close()
            core.quit()
            with open("surface_gaze_data.json", "w") as file:
                json.dump(gaze_data, file)