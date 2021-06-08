"""Implement the graphical user interface for the Logic Simulator.

Used in the Logic Simulator project to enable the user to run the simulation
or adjust the network properties.

**PEP 8 has been followed except for the linelength, which has been limited such that it is
easily visible on a full screen rather than following the 79 character limit.
This is, because in general it makes code more readable.**

Classes:
--------
MyGLCanvas - handles all canvas drawing operations.
Gui - configures the main window and all the widgets.
"""
from OpenGL.raw.GL.VERSION.GL_1_1 import GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT
import wx
import wx.glcanvas as wxcanvas
import time
import sys
import os
import math
import numpy as np
import io
from wx.core import HORIZONTAL
import wx.lib.scrolledpanel as scrolled
import wx.glcanvas as wxcanvas
from OpenGL import GL, GLUT, GLU
from error import Error

from names import Names
from devices import Devices
from network import Network
from monitors import Monitors
from scanner import Scanner
from parse import Parser



class MyGLCanvas2D(wxcanvas.GLCanvas):
    """Handle all drawing operations.

    This class contains functions for drawing onto the canvas. It
    also contains handlers for events relating to the canvas.

    Parameters

    ----------
    parent: parent window.
    devices: instance of the devices.Devices() class.
    monitors: instance of the monitors.Monitors() class.

    Public methods
    --------------
    init_gl(self): Configures the OpenGL context.

    render_value(self, values): Handles all drawing operations.

    render_empty(self): Draws empty canvas.

    on_paint(self, event): Handles the paint event.

    render_text(self, text, x_pos, y_pos): Handles text drawing
                                           operations.

    """

    def __init__(self, parent, devices, monitors, size):
        """Initialise.

        Initialise canvas properties and useful variables.
        """
        super().__init__(parent, size=size,
                         attribList=[wxcanvas.WX_GL_RGBA,
                                     wxcanvas.WX_GL_DOUBLEBUFFER,
                                     wxcanvas.WX_GL_DEPTH_SIZE, 16, 0])
                                     
        GLUT.glutInit()
        self.parent = parent
        self.init = False
        self.context = wxcanvas.GLContext(self)

        # Initialise variables for panning
        self.pan_x = 0
        self.pan_y = 0
        self.last_mouse_x = 0  # previous mouse x position
        self.last_mouse_y = 0  # previous mouse y position

        # Initialise variables for zooming
        self.zoom = 1

        # Bind events to the canvas
        self.Bind(wx.EVT_PAINT, self.on_paint)

    def init_gl(self):
        """Configure and initialise the OpenGL context.

        Set up all the drawing tools needed for openGL.
        """
        size = self.GetClientSize()
        self.SetCurrent(self.context)
        GL.glDrawBuffer(GL.GL_BACK)
        GL.glClearColor(1.0, 1.0, 1.0, 0.0)
        GL.glViewport(0, 0, size.width, size.height)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(0, size.width, 0, size.height, -1, 1)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        GL.glTranslated(self.pan_x, self.pan_y, 0.0)
        GL.glScaled(self.zoom, self.zoom, self.zoom)

    def render_value(self, values):
        """Draw a trace.

        Draw the trace of a signal value.
        """
        self.SetCurrent(self.context)
        if not self.init:
            # Configure the viewport, modelview and projection matrices
            self.init_gl()
            self.init = True

        # Clear everything
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        # Draw a sample signal trace
        GL.glColor3f(0.0, 0.0, 1.0)  # signal trace is blue
        GL.glBegin(GL.GL_LINE_STRIP)
        for i in range(len(values)):
            print("i is", i)
            x = (i * 20) + 10
            x_next = (i * 20) + 30
            if values[i] == 1:
                y = 25
            else:
                y = 0
            GL.glVertex2f(x, y)
            GL.glVertex2f(x_next, y)
        GL.glEnd()


        GL.glColor3f(0.5, 0.5, 0.0)
        GL.glColor3f(0.3, 0.5, 0.7)
        GL.glBegin(GL.GL_LINES)
        GL.glVertex2f(10.0,0.0)
        GL.glVertex2f(10.0, 35.0)
        GL.glEnd()
        GL.glColor3f(1.0, 0.7, 0.5)
        self.render_text("1", 0.0, 25.0)
        self.render_text("0", 0.0, 0.0)
        # We have been drawing to the back buffer, flush the graphics pipeline
        # and swap the back buffer to the front
        GL.glFlush()
        self.SwapBuffers()

    def render_empty(self):
        """Render empty canvas.

        Initialise an empty canvas.
        """
        self.SetCurrent(self.context)
        if not self.init:
            # Configure the viewport, modelview and projection matrices
            self.init_gl()
            self.init = True

        # Clear everything
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        # We have been drawing to the back buffer, flush the graphics pipeline
        # and swap the back buffer to the front
        GL.glFlush()
        self.SwapBuffers()

    def on_paint(self, event):
        """Handle the paint event.

        Define that on_paint self.render is called.
        """
        self.SetCurrent(self.context)
        if not self.init:
            # Configure the viewport, modelview and projection matrices
            self.init_gl()
            self.init = True

        size = self.GetClientSize()
        text = "".join(["Canvas redrawn on paint event, size is ",
                        str(size.width), ", ", str(size.height)])
        # self.render(text)
        self.parent.render()

    def render_text(self, text, x_pos, y_pos):
        """Handle text drawing operations.

        Writes text on canvas.
        """
        GL.glColor3f(0.0, 0.0, 0.0)  # text is black
        GL.glRasterPos2f(x_pos, y_pos)
        font = GLUT.GLUT_BITMAP_HELVETICA_12

        for character in text:
            if character == '\n':
                y_pos = y_pos - 20
                GL.glRasterPos2f(x_pos, y_pos)
            else:
                GLUT.glutBitmapCharacter(font, ord(character))



class MyGLCanvas3D(wxcanvas.GLCanvas):
    """Handle all drawing operations.

    This class contains functions for drawing onto the canvas. It
    also contains handlers for events relating to the canvas.

    Parameters

    ----------
    parent: parent window.
    devices: instance of the devices.Devices() class.
    monitors: instance of the monitors.Monitors() class.

    Public methods
    --------------
    init_gl(self): Configures the OpenGL context.

    render_value(self, values): Handles all drawing operations.

    render_empty(self): Draws empty canvas.

    on_paint(self, event): Handles the paint event.

    render_text(self, text, x_pos, y_pos): Handles text drawing
                                           operations.

    """

    def __init__(self, parent, devices, monitors, size):
        """Initialise canvas properties and useful variables."""
        super().__init__(parent, size=size,
                         attribList=[wxcanvas.WX_GL_RGBA,
                                     wxcanvas.WX_GL_DOUBLEBUFFER,
                                     wxcanvas.WX_GL_DEPTH_SIZE, 16, 0])
                                     
        GLUT.glutInit()
        self.parent = parent
        self.init = False
        self.context = wxcanvas.GLContext(self)
        

        # Constants for OpenGL materials and lights
        self.mat_diffuse = [0.0, 0.0, 0.0, 1.0]
        self.mat_no_specular = [0.0, 0.0, 0.0, 0.0]
        self.mat_no_shininess = [0.0]
        self.mat_specular = [0.5, 0.5, 0.5, 1.0]
        self.mat_shininess = [50.0]
        self.top_right = [1.0, 1.0, 1.0, 0.0]
        self.straight_on = [0.0, 0.0, 1.0, 0.0]
        self.no_ambient = [0.0, 0.0, 0.0, 1.0]
        self.dim_diffuse = [0.5, 0.5, 0.5, 1.0]
        self.bright_diffuse = [1.0, 1.0, 1.0, 1.0]
        self.med_diffuse = [0.75, 0.75, 0.75, 1.0]
        self.full_specular = [0.5, 0.5, 0.5, 1.0]
        self.no_specular = [0.0, 0.0, 0.0, 1.0]

        # Initialise variables for panning
        self.pan_x = 0
        self.pan_y = 0
        self.last_mouse_x = 0  # previous mouse x position
        self.last_mouse_y = 0  # previous mouse y position

        # Initialise the scene rotation matrix
        self.scene_rotate = np.identity(4, 'f')

        # Initialise variables for zooming
        self.zoom = 1

        # Offset between viewpoint and origin of the scene
        self.depth_offset = 1000

        # Bind events to the canvas
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse)

    def init_gl(self):
        """Configure and initialise the OpenGL context."""
        size = self.GetClientSize()
        self.SetCurrent(self.context)

        GL.glViewport(0, 0, size.width, size.height)

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective(45, size.width / size.height, 10, 10000)

        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()  # lights positioned relative to the viewer
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_AMBIENT, self.no_ambient)
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_DIFFUSE, self.med_diffuse)
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_SPECULAR, self.no_specular)
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, self.top_right)
        GL.glLightfv(GL.GL_LIGHT1, GL.GL_AMBIENT, self.no_ambient)
        GL.glLightfv(GL.GL_LIGHT1, GL.GL_DIFFUSE, self.dim_diffuse)
        GL.glLightfv(GL.GL_LIGHT1, GL.GL_SPECULAR, self.no_specular)
        GL.glLightfv(GL.GL_LIGHT1, GL.GL_POSITION, self.straight_on)

        GL.glMaterialfv(GL.GL_FRONT, GL.GL_SPECULAR, self.mat_specular)
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_SHININESS, self.mat_shininess)
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_AMBIENT_AND_DIFFUSE,
                        self.mat_diffuse)
        GL.glColorMaterial(GL.GL_FRONT, GL.GL_AMBIENT_AND_DIFFUSE)

        GL.glClearColor(1, 1, 1, 1)
        GL.glDepthFunc(GL.GL_LEQUAL)
        GL.glShadeModel(GL.GL_SMOOTH)
        GL.glDrawBuffer(GL.GL_BACK)
        GL.glCullFace(GL.GL_BACK)
        GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glEnable(GL.GL_CULL_FACE)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_LIGHTING)
        GL.glEnable(GL.GL_LIGHT0)
        GL.glEnable(GL.GL_LIGHT1)
        GL.glEnable(GL.GL_NORMALIZE)

        # Viewing transformation - set the viewpoint back from the scene
        GL.glTranslatef(0.0, 0.0, -self.depth_offset)

        # Modelling transformation - pan, zoom and rotate
        GL.glTranslatef(self.pan_x, self.pan_y, 0.0)
        GL.glMultMatrixf(self.scene_rotate)
        GL.glScalef(self.zoom, self.zoom, self.zoom)


    def render_value(self, values):
        """Draw a trace.

        Draw the trace of a signal value.
        """
        self.SetCurrent(self.context)
        if not self.init:
            # Configure the viewport, modelview and projection matrices
            self.init_gl()
            self.init = True

        # Clear everything
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        # Draw a sample signal trace
        GL.glColor3f(1.0, 0.7, 0.5)   # signal trace is beige
        list_length = len(values)
        for i in range(list_length):
                z = (i-list_length//2) * 300
                if values[i] == 0:
                    self.draw_cuboid(z, 150, 75, 15, "normal")
                else:
                    self.draw_cuboid(z, 150, 75, 165, "normal")
        
        GL.glColor3f(0.3, 0.5, 0.7)
        GL.glBegin(GL.GL_LINES)
        GL.glVertex3f(-list_length//2 * 300, 75.0,75.0)
        GL.glVertex3f(-list_length//2 * 300, 275.0, 75.0)
        GL.glEnd()
        #GL.glColor3f(1.0, 0.7, 0.5)
        self.render_text("1", -list_length//2 * 300, 225.0, 100.0)
        self.render_text("0", -list_length//2 * 300, 75.0, 100.0)
        # We have been drawing to the back buffer, flush the graphics pipeline
        # and swap the back buffer to the front
        GL.glFlush()
        self.SwapBuffers()

    def render(self):
        """Handle all drawing operations."""
        
        self.SetCurrent(self.context)
        if not self.init:
            # Configure the OpenGL rendering context
            self.init_gl()
            self.init = True

        # Clear everything
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        # Draw a sample signal trace, make sure its centre of gravity
        # is at the scene origin
        GL.glColor3f(1.0, 0.7, 0.5)  # signal trace is beige
        for i in range(3):
            if i == 0:
                GL.glColor3f(1.0, 0.7, 0.5)  # signal trace is beige
                orientation = "back"
            elif i ==2:
                 #GL.glColor3f(1, 0.5, 0.7)
                 orientation = "normal"
            else:
                #GL.glColor3f(0.3, 0.5, 0.7)
                orientation = "front"
            
            for i in range(-10, 10):
                z = i * 300
                if i % 2 == 0:
                    self.draw_cuboid(z, 150, 75, 15, orientation)
                else:
                    self.draw_cuboid(z, 150, 75, 165, orientation)

        GL.glColor3f(0, 0, 0)  # text is black
        self.render_text("D1.QBAR", 0, 0, 210)

        # We have been drawing to the back buffer, flush the graphics pipeline
        # and swap the back buffer to the front
        GL.glFlush()
        self.SwapBuffers()

    def draw_cuboid(self, x_pos, half_width, half_depth, height, orientation):
        """Draw a cuboid.

        Draw a cuboid at the specified position, with the specified
        dimensions.
        """

        verticies = (
            (x_pos + half_width, half_depth, half_depth),
            (x_pos - half_width, half_depth, half_depth),
            (x_pos - half_width, half_depth, -half_depth),
            (x_pos + half_width, half_depth, - half_depth),
            (x_pos + half_width, half_depth + height, half_depth),
            (x_pos + half_width, half_depth + height, - half_depth),
            (x_pos - half_width, half_depth + height, -half_depth),
            (x_pos - half_width, half_depth + height, half_depth),
        )

        faces = (
            (0, 1, 2, 3),
            (4, 5, 6, 7),
            (6, 5, 3, 2),
            (1, 0, 4, 7),
            (2, 1, 7, 6),
            (5, 4, 0, 3),
        )

        normals = (
            (0, -1, 0),
            (0, 1, 0),
            (0, 0, -1),
            (0, 0, 1),
            (-1, 0, 0),
            (1, 0, 0),
        )
        
        if orientation == "normal":
            GL.glBegin(GL.GL_QUADS)
            for normal, face in zip(normals, faces):
                GL.glNormal3fv(normal)
                for index in face:
                    GL.glVertex3fv(verticies[index])
            GL.glEnd()

        elif orientation == "back":
            mirror = ((1, 0, 0),(0, 0, 1),(0, -1, 0))
            new_verticies = [np.matmul(mirror, vertex) for vertex in verticies]
            #new_verticies = [[x, y-11, z-11] for [x, y, z] in new_verticies]
            new_normals = [np.matmul(mirror, vertex) for vertex in normals]
            GL.glBegin(GL.GL_QUADS)
            for normal, face in zip(new_normals, faces):
                GL.glNormal3fv(normal)
                for index in face:
                    GL.glVertex3fv(new_verticies[index])
            GL.glEnd()
        
        elif orientation == "front":
            mirror = ((1, 0, 0),(0, 0, -1),(0, 1, 0))
            new_verticies = [np.matmul(mirror, vertex) for vertex in verticies]
            #new_verticies = [[x, y-11, z+11] for [x, y, z] in new_verticies]
            new_normals = [np.matmul(mirror, vertex) for vertex in normals]
            GL.glBegin(GL.GL_QUADS)
            for normal, face in zip(new_normals, faces):
                GL.glNormal3fv(normal)
                for index in face:
                    GL.glVertex3fv(new_verticies[index])
            GL.glEnd()
        else:
            print("Sorry wronf orientation.")
            sys.exit()
        """
        GL.glColor3f(0.3, 0.5, 0.7)
        GL.glBegin(GL.GL_LINES)
        GL.glVertex3f(0.0,0.0, half_depth)
        GL.glVertex3f(0.0, 1.5* height, half_depth)
        GL.glEnd()
        GL.glColor3f(1.0, 0.7, 0.5)"""

    def on_paint(self, event):
        """Handle the paint event."""
        self.SetCurrent(self.context)
        if not self.init:
            # Configure the OpenGL rendering context
            self.init_gl()
            self.init = True

        size = self.GetClientSize()
        text = "".join(["Canvas redrawn on paint event, size is ",
                        str(size.width), ", ", str(size.height)])
        #self.render()
        self.parent.render()

    def on_size(self, event):
        """Handle the canvas resize event."""
        # Forces reconfiguration of the viewport, modelview and projection
        # matrices on the next paint event
        self.init = False

    def down_rotate(self, step):
        """Handle the downwards rotation."""
        self.SetCurrent(self.context)

        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        
        GL.glRotatef(90/step, 1, 0, 0)

        GL.glMultMatrixf(self.scene_rotate)
        GL.glGetFloatv(GL.GL_MODELVIEW_MATRIX, self.scene_rotate)

        self.init = False

        self.Refresh()  # triggers the paint event
        self.SwapBuffers()
        GL.glFlush()


    def on_down_rotate(self, event):
        """Handle the downwards rotation."""
        start_time = time.time()
        steps = 15
        k = 0

        while time.time() < start_time + 1:
            if steps*(time.time()-start_time)> k:
                self.rotate(steps, k+2)
                k += 1

    def on_up_rotate(self, event):
        """Handle upwards rotation event."""
        start_time = time.time()
        steps = 15
        k = 0

        while time.time() < start_time + 1:
            if steps*(time.time()-start_time)> k:
                self.rotate(steps, -(k+2))
                k += 1

    def rotate(self, steps, j):
        self.SetCurrent(self.context)
        GL.glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        GL.glPushMatrix()
        print("j is", j)
        GL.glRotatef(j*90/steps,1 ,0 , 0)
        self.render()
        GL.glPopMatrix()
        self.SwapBuffers()
        

    def on_mouse(self, event):
        """Handle mouse events."""
        self.SetCurrent(self.context)

        if event.ButtonDown():
            self.last_mouse_x = event.GetX()
            self.last_mouse_y = event.GetY()

        if event.Dragging():
            GL.glMatrixMode(GL.GL_MODELVIEW)
            GL.glLoadIdentity()
            x = event.GetX() - self.last_mouse_x
            y = event.GetY() - self.last_mouse_y
            if event.LeftIsDown():
                GL.glRotatef(math.sqrt((x * x) + (y * y)), y, x, 0)
                #GL.glRotatef(0, 0, (x + y), 1)
            if event.MiddleIsDown():
                GL.glRotatef(y, y, 0, 0)
            if event.RightIsDown():
                self.pan_x += x
                self.moved += x
                #self.pan_y -= y
            GL.glMultMatrixf(self.scene_rotate)
            GL.glGetFloatv(GL.GL_MODELVIEW_MATRIX, self.scene_rotate)
            self.last_mouse_x = event.GetX()
            self.last_mouse_y = event.GetY()
            self.init = False

        if event.GetWheelRotation() < 0:
            self.zoom *= (1.0 + (
                event.GetWheelRotation() / (20 * event.GetWheelDelta())))
            self.init = False

        if event.GetWheelRotation() > 0:
            self.zoom /= (1.0 - (
                event.GetWheelRotation() / (20 * event.GetWheelDelta())))
            self.init = False

        self.Refresh()  # triggers the paint event

    def render_text(self, text, x_pos, y_pos, z_pos):
        """Handle text drawing operations."""
        GL.glDisable(GL.GL_LIGHTING)
        GL.glRasterPos3f(x_pos, y_pos, z_pos)
        font = GLUT.GLUT_BITMAP_HELVETICA_10

        for character in text:
            if character == '\n':
                y_pos = y_pos - 20
                GL.glRasterPos3f(x_pos, y_pos, z_pos)
            else:
                GLUT.glutBitmapCharacter(font, ord(character))

        GL.glEnable(GL.GL_LIGHTING)


class SidePanel(wx.Panel):
    """SidePanel object is responsible for all runtime control in the GUI object.

    Parameters:
    ------
    parent: GUI object.
    scrolled_pabel: MonitorPanel object.
    ------
    Public Methods:
    ------
    read_name(self, name_string): Return the name ID of the current string if valid,
                                Return None if the current string is not a valid name string.

    read_signal_name(self): Return the device and port IDs of the current signal name.
                            Return None if either is invalid.

    on_add_monitor(self, event): Handle the event when the add monitor button is pressed, adds a MonitorItem.

    run_network(self, cycles): Run the network for the specified number of simulation cycles.
                                Return True if successful.

    on_update_signal(self, event): Set the specified switch to the specified signal level.

    on_remove_monitor(self, event): Event handler, removes monitor.

    on_remove_all_monitors(self, event): Event handler, removes all monitors.

    on_run_button(self, event): Event handler for when the user clicks the run
                                button.

    on_continue_button(self, event): Continue a previously run simulation.

    run_command(self): Run the simulation from scratch.

    on_text_box(self, event): Event handler for when the user enters text.
    on_combo_select(self, event): Handle event from selecting an event from the combobox dropdown menu

    """

    def __init__(self, parent, scrolled_panel) -> None:
        """Initialise SidePanel object, set up widgets.

        Create all the widgets, assign to sizers and initialise.
        """
        super().__init__(parent=parent)

        self.parent = parent
        self.scrolled_panel = scrolled_panel

        # Configure the widgets

        # control setting number of cycles
        self.text = wx.StaticText(self, wx.ID_ANY, "Cycles")
        self.spin = wx.SpinCtrl(self, wx.ID_ANY, "10")

        # run and continue buttons
        self.run_button = wx.Button(self, wx.ID_ANY, "Run")
        self.continue_button = wx.Button(self, wx.ID_ANY, "Continue")

        """Setting the value of a signal/ switch
        switch_box takes the value
        zero_button and one_button allow toggling between 0 and 1
        add_switch_executes the add button"""
        self.switch_box_text = wx.StaticText(self, wx.ID_ANY, "Set Switch")
        self.switch_box = wx.ComboBox(
            self, wx.ID_ANY, "Switch", choices=[
                self.parent.names.get_name_string(i) for i in self.parent.devices.find_devices(
                    self.parent.devices.SWITCH)])
        self.zero_button = wx.RadioButton(self, -1, "0", style=wx.RB_GROUP)
        self.one_button = wx.RadioButton(self, -1, "1")
        self.add_switch_button = wx.Button(self, -1, "Set")

        self.monitor_text = wx.StaticText(
            self, wx.ID_ANY, "Set outputs to monitor")
        # monitor_sizer
        all = [self.parent.names.get_name_string(
            i) for i in self.parent.devices.find_devices(None)]
        switches = [self.parent.names.get_name_string(
            i) for i in self.parent.devices.find_devices(self.parent.devices.SWITCH)]
        clocks = [self.parent.names.get_name_string(
            i) for i in self.parent.devices.find_devices(self.parent.devices.CLOCK)]
        choices = [i for i in all if i not in switches and i not in clocks]
        self.monitor_combobox = wx.ComboBox(
            self, wx.ID_ANY, "Select", choices=choices)
        self.add_monitor_button = wx.Button(self, wx.ID_ANY, "Add")

        self.remove_monitor_text = wx.StaticText(
            self, wx.ID_ANY, "Remove monitor")
        # remove_monitor_sizer
        self.remove_monitor_combobox = wx.ComboBox(
            self, wx.ID_ANY, "Select", choices=[
                item.name for item in self.scrolled_panel.item_list])
        self.remove_monitor_button = wx.Button(self, wx.ID_ANY, "Remove")
        self.remove_all_button = wx.Button(self, wx.ID_ANY, "Remove all")
        self.remove_all_button.SetForegroundColour('#ff1a1a')

        self.toggle_gui_text = wx.StaticText(
            self, wx.ID_ANY, "Change between 2D and 3D view mode")
        self.toggle_gui_button = wx.Button(self, wx.ID_ANY, "3D")

        # Bind events to widgets

        self.run_button.Bind(wx.EVT_BUTTON, self.on_run_button)
        self.continue_button.Bind(wx.EVT_BUTTON, self.on_continue_button)

        self.add_switch_button.Bind(wx.EVT_BUTTON, self.on_update_signal)

        self.add_monitor_button.Bind(wx.EVT_BUTTON, self.on_add_monitor)

        self.remove_monitor_button.Bind(wx.EVT_BUTTON, self.on_remove_monitor)
        self.remove_all_button.Bind(wx.EVT_BUTTON, self.on_remove_all_monitors)

        self.side_sizer = wx.BoxSizer(wx.VERTICAL)

        self.cycle_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.switch_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.monitor_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.remove_monitor_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.remove_monitor_subsizer = wx.BoxSizer(wx.VERTICAL)
        self.remove_monitor_bordersizer = wx.BoxSizer(wx.VERTICAL)
        self.binary_choice_sizer = wx.BoxSizer(wx.VERTICAL)

        self.side_sizer.SetMinSize(self.side_sizer.GetMinSize())
        self.side_sizer.Add(self.toggle_gui_text, 0, wx.ALL | wx.EXPAND, 5)
        self.side_sizer.Add(self.toggle_gui_button, 0, wx.ALL | wx.EXPAND, 5)
        self.side_sizer.Add(wx.StaticLine(self, -1), 0, wx.ALL | wx.EXPAND, 5)
        self.side_sizer.Add(self.cycle_sizer, 1, wx.ALL | wx.EXPAND, 0)
        self.side_sizer.Add(self.button_sizer, 1, wx.ALL | wx.EXPAND, 0)
        self.side_sizer.Add(wx.StaticLine(self, -1), 0, wx.ALL | wx.EXPAND, 5)
        self.side_sizer.Add(self.switch_box_text, 1, wx.ALIGN_CENTER, 0)
        self.side_sizer.Add(self.switch_sizer, 1, wx.EXPAND, 0)
        self.side_sizer.Add(wx.StaticLine(self, -1), 0, wx.ALL | wx.EXPAND, 5)
        self.side_sizer.Add(self.monitor_text, 1, wx.ALL | wx.ALIGN_CENTER, 0)
        self.side_sizer.Add(self.monitor_sizer, 1, wx.ALL | wx.EXPAND, 0)
        self.side_sizer.Add(wx.StaticLine(self, -1), 0, wx.ALL | wx.EXPAND, 5)
        self.side_sizer.Add(self.remove_monitor_text, 1,
                            wx.ALL | wx.ALIGN_CENTER, 5)
        self.side_sizer.Add(self.remove_monitor_sizer,
                            1, wx.ALL | wx.EXPAND, 0)

        self.cycle_sizer.Add(self.text, 1, wx.ALL | wx.ALIGN_CENTER, 5)
        self.cycle_sizer.Add(self.spin, 2, wx.ALL, 5)

        self.button_sizer.Add(self.run_button, 1, wx.ALL | wx.EXPAND, 5)
        self.button_sizer.Add(self.continue_button, 1, wx.ALL | wx.EXPAND, 5)

        self.switch_sizer.Add(self.switch_box, 1, wx.ALL, 5)
        self.switch_sizer.Add(self.binary_choice_sizer, 1, wx.ALL, 5)
        self.switch_sizer.Add(self.add_switch_button, 1, wx.ALL, 5)

        self.binary_choice_sizer.Add(self.zero_button, 0, wx.ALL, 0)
        self.binary_choice_sizer.Add(self.one_button, 0, wx.ALL, 0)

        self.monitor_sizer.Add(self.monitor_combobox, 1, wx.ALL, 5)
        self.monitor_sizer.Add(self.add_monitor_button, 1, wx.ALL, 5)

        self.remove_monitor_sizer.Add(
            self.remove_monitor_bordersizer,
            1,
            wx.RIGHT | wx.LEFT | wx.EXPAND,
            5)
        self.remove_monitor_sizer.Add(
            self.remove_monitor_subsizer, 1, wx.ALL, 5)

        self.remove_monitor_bordersizer.Add(
            self.remove_monitor_combobox, 0, wx.TOP | wx.BOTTOM | wx.EXPAND, 10)

        self.remove_monitor_subsizer.Add(
            self.remove_monitor_button, 0, wx.ALL | wx.EXPAND, 5)
        self.remove_monitor_subsizer.Add(
            self.remove_all_button, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(self.side_sizer)

    def read_name(self, name_string):
        """Return the name ID of the current string if valid.

        Return None if the current string is not a valid name string.
        """
        if name_string is None:
            return None
        else:
            name_id = self.parent.names.query(name_string)
        if name_id is None:
            print("Error! Unknown name.")
        return name_id

    def read_signal_name(self):
        """Return the device and port IDs of the current signal name.

        Return None if either is invalid.
        """
        device_id = self.read_name()
        if device_id is None:
            return None
        elif self.character == ".":
            port_id = self.read_name()
            if port_id is None:
                return None
        else:
            port_id = None
        return [device_id, port_id]

    def on_add_monitor(self, event):
        """Handle the event when the add monitor button is pressed, adds a MonitorItem.

        If no monitor is selected, do nothing.
        """
        monitor = self.monitor_combobox.GetValue()

        if monitor != "Select":
            self.remove_monitor_combobox.Append(monitor)
            self.scrolled_panel.add_monitor(monitor)

    def run_network(self, cycles):
        """Run the network for the specified number of simulation cycles.

        Return True if successful.
        """
        for _ in range(cycles):
            if self.parent.network.execute_network():
                self.parent.monitors.record_signals()
            else:
                print("Error! Network oscillating.")
                return False
        self.parent.monitors.display_signals()
        self.parent.scrolled_panel.render_children()
        return True

    def on_update_signal(self, event):
        """Set the specified switch to the specified signal level.

        Get Value from switch box and set switch to this.
        """
        name_string = self.switch_box.GetValue()
        switch_id = self.read_name(name_string)
        if switch_id is not None:
            if self.one_button.GetValue():
                switch_state = 1
            else:
                switch_state = 0
            if self.parent.devices.set_switch(switch_id, switch_state):
                print("Successfully set switch.")
            else:
                print("Error! Invalid switch.")

    def on_remove_monitor(self, event):
        """Handle the event when the remove monitor button is pressed.

        Remove the monitor.
        """
        self.remove_monitor_combobox.Clear()
        self.scrolled_panel.remove_monitor(self.remove_monitor_combobox.Value)
        for item in self.scrolled_panel.item_list:
            self.remove_monitor_combobox.Append(item.name)

    def on_remove_all_monitors(self, event):
        """Handle the event when removing all monitors.

        Remove all monitors.
        """
        self.scrolled_panel.remove_all_monitors()

    def on_run_button(self, event):
        """Handle the event when the user clicks the run button.

        Call cold_startuo and then run_network.
        """
        self.cycles_completed = 0
        cycles = self.spin.GetValue()
        self.parent.monitors.reset_monitors()
        print("".join(["Running for ", str(cycles), " cycles"]))
        self.parent.devices.cold_startup()
        if self.run_network(cycles):
            self.cycles_completed += cycles

    def on_continue_button(self, event):
        """Continue a previously run simulation.

        Run_network.
        """
        cycles = self.spin.GetValue()
        if cycles is not None:  # if the number of cycles provided is valid
            if self.cycles_completed == 0:
                print("Error! Nothing to continue. Run first.")
            elif self.run_network(cycles):
                self.cycles_completed += cycles

    def run_command(self):
        """Run the simulation from scratch.

        Do cold_startup and run_network.
        """
        self.cycles_completed = 0
        cycles = self.read_number(0, None)

        if cycles is not None:  # if the number of cycles provided is valid
            self.monitors.reset_monitors()
            print("".join(["Running for ", str(cycles), " cycles"]))
            self.devices.cold_startup()
            if self.run_network(cycles):
                self.cycles_completed += cycles

    def on_text_box(self, event):
        """Handle the event when the user enters text.

        Text response.
        """
        text_box_value = self.text_box.GetValue()
        text = "".join(["New text box value: ", text_box_value])
        self.canvas.render(text)

    def on_combo_select(self, event):
        """Handle event from selecting an event from the combobox dropdown menu.

        Render selected.
        """
        self.canvas.render("selected")


class MonitorPanel(scrolled.ScrolledPanel):
    """Scrolled Panel that contains all the monitor traces.

    Paramaters:

    parent: Gui passes an instance of itself.
    monitors: Instance of the Monitors class.
    devices: Instance of the Devices class.
    names: Instance of the Names class.

    Public Methods:
    render_children(self): Calls all MonitorItems render method.
    add_monitor(self, text): Add a MonitorItem with name text
    remove_monitor(self, text): Removes the MonitorItem with name text.
    remove_child(self, child): Removes a specific MonitorItem.
    remove_all_monitors(self): Removes all MonitorItems.

    """

    def __init__(self, parent, monitors, devices, names) -> None:
        """Set up the scrolled panel.

        Initialise MonitorItems from definition file.
        """
        scrolled.ScrolledPanel.__init__(self, parent, -1)
        self.SetupScrolling()
        self.parent = parent
        self.monitors = monitors
        self.devices = devices
        self.names = names

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.item_list = []

        for key, value in self.monitors.monitors_dictionary.items():
            self.item_list.append(
                MonitorItem3D(
                    self,
                    self.names.get_name_string(
                        key[0]),
                    self.monitors,
                    self.devices,
                    self.names))
            self.item_list[-1].SetBackgroundColour('#b0bcda')
            self.sizer.Add(self.item_list[-1], 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(self.sizer)


    def render_children(self):
        """Render sall MonitorItems.

        Remove children.
        """
        for child in self.item_list:
            child.render()

    def add_monitor(self, text):
        """Add a MonitorItem with name text.

        Call make_monitor.
        """
        [child_device_id, child_output_id] = self.devices.get_signal_ids(text)
        self.monitors.make_monitor(child_device_id, child_output_id)
        self.item_list.append(
            MonitorItem3D(
                self,
                text,
                self.monitors,
                self.devices,
                self.names))
        self.item_list[-1].SetBackgroundColour('#b0bcda')
        self.sizer.Add(self.item_list[-1], 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(self.sizer)
        self.sizer.Layout()
        self.SetupScrolling()

    def remove_monitor(self, text):
        """Remove a MonitorItem with name text.

        Call remove_monitor.
        """
        [child_device_id, child_output_id] = self.devices.get_signal_ids(text)
        self.monitors.remove_monitor(child_device_id, child_output_id)
        self.item_list = [item for item in self.item_list if item.name != text]
        for item in self.sizer.GetChildren():
            widget = item.GetWindow()
            if widget.name == text:
                self.sizer.Hide(widget)
                widget.Destroy()
        self.SetSizer(self.sizer)
        self.sizer.Layout()
        self.SetupScrolling()

    def remove_child(self, child):
        """Remove the MonitorItem child.

        Destroy self.
        """
        for element in self.sizer.GetChildren():
            if element.GetWindow() == child:
                self.sizer.Hide(child)
                child.Destroy()
                self.SetSizer(self.sizer)
                self.sizer.Layout()
                self.SetupScrolling()

    def remove_all_monitors(self):
        """Remove all MonitorItems.

        Destroy all.
        """
        for item in self.sizer.GetChildren():
            self.sizer.Hide(item.GetWindow())
            item.GetWindow().Destroy()
        self.SetSizer(self.sizer)
        self.sizer.Layout()
        self.SetupScrolling()


class MonitorItem(wx.Panel):
    """A single Panel that displays a monitor trace. Child of MonitorPanel.

    Paramaters:

    parent: MonitorPanel object.
    name: Name of the output to be monitored.
    monitors: Monitors object.
    devices: Devices object.
    names: Names object.

    Public Methods:

    on_remove_item(self, event): Event handler, handles when Remove is pressed,
                                destroys self.
    render(self): Calls the render_value method of the Canvaspanel object,
                    added to this widget, draws signal trace.

    """

    def __init__(self, parent, name, monitors, devices, names) -> None:
        """Initialise widget.

        Create a canvas object and all buttons.
        """
        super().__init__(parent=parent)
        self.parent = parent
        self.name = name
        self.names = names
        self.monitors = monitors
        self.devices = devices

        [self.device_id, self.output_id] = self.devices.get_signal_ids(
            self.name)

        self.name_text = wx.StaticText(
            self, wx.ID_ANY, label=self.name, size=(50, 50), style = wx.ALIGN_CENTER)
        fo = wx.Font(13, wx.MODERN, wx.NORMAL, wx.NORMAL, False)
        self.name_text.SetFont(fo)


    def on_remove_item(self, event):
        """Event handler.

        Destroy self widget.
        """
        self.parent.item_list = [
            item for item in self.parent.item_list if item.name != self.name]
        self.parent.parent.side_panel.remove_monitor_combobox.Clear()
        for item in self.parent.item_list:
            self.parent.parent.side_panel.remove_monitor_combobox.Append(
                item.name)
        self.parent.remove_child(self)

    def render(self):
        """Render signal trace on Canvaspanel object attached to MonitorItem.

        If DTYPE find outputID.
        """
        [self.device_id, self.output_id] = self.devices.get_signal_ids(
            self.name)
        if self.devices.get_device(self.device_id).device_kind == self.devices.D_TYPE:
            self.values = self.parent.monitors.monitors_dictionary[self.device_id, self.devices.dtype_output_ids[0]]
            self.canvas.render_value(self.values)
        else:
            self.values = self.parent.monitors.monitors_dictionary[self.device_id, self.output_id]
            self.canvas.render_value(self.values)


class MonitorItem3D(MonitorItem):
    """A single Panel that displays a monitor trace. Child of MonitorPanel.

    Paramaters:

    parent: MonitorPanel object.
    name: Name of the output to be monitored.
    monitors: Monitors object.
    devices: Devices object.
    names: Names object.

    Public Methods:

    on_remove_item(self, event): Event handler, handles when Remove is pressed,
                                destroys self.
    render(self): Calls the render_value method of the Canvaspanel object,
                    added to this widget, draws signal trace.

    """

    def __init__(self, parent, name, monitors, devices, names) -> None:
        """Initialise widget.

        Create a canvas object and all buttons.
        """
        super().__init__(parent=parent, name=name, monitors=monitors, devices=devices, names=names)
        
        self.canvas = MyGLCanvas3D(
            self, self.devices, self.monitors, size=(100, -1))


        self.switch_to_2d_button = wx.Button(self, wx.ID_ANY, "2D mode")
        self.next_trace_button = wx.Button(self, wx.ID_ANY, "Next trace")
        self.prev_trace_button = wx.Button(self, wx.ID_ANY, "Previous trace")
        self.remove_item = wx.Button(self, wx.ID_ANY, "Remove")
        
        self.remove_item.Bind(wx.EVT_BUTTON, self.on_remove_item)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.button_sizer = wx.GridSizer(rows=2, cols=2, hgap=0, vgap=0)

        self.sizer.Add(self.name_text, 1, wx.CENTER, 0)
        self.sizer.Add(self.canvas, 6, wx.EXPAND, 0)
        self.sizer.Add(self.button_sizer, 1, wx.ALIGN_CENTER, 0)

        self.button_sizer.Add(self.next_trace_button, 1, wx.EXPAND, 0)
        self.button_sizer.Add(self.prev_trace_button, 1, wx.EXPAND, 0)
        self.button_sizer.Add(self.switch_to_2d_button, 1, wx.EXPAND, 0)
        self.button_sizer.Add(self.remove_item, 1, wx.EXPAND, 0)

        self.Layout()
        self.SetSizer(self.sizer)



class MonitorItem2D(MonitorItem):
    """A single Panel that displays a monitor trace. Child of MonitorPanel.

    Paramaters:

    parent: MonitorPanel object.
    name: Name of the output to be monitored.
    monitors: Monitors object.
    devices: Devices object.
    names: Names object.

    Public Methods:

    on_remove_item(self, event): Event handler, handles when Remove is pressed,
                                destroys self.
    render(self): Calls the render_value method of the Canvaspanel object,
                    added to this widget, draws signal trace.

    """

    def __init__(self, parent, name, monitors, devices, names) -> None:
        """Initialise widget.

        Create a canvas object and all buttons.
        """
        super().__init__(parent=parent, name=name, monitors=monitors, devices=devices, names=names)
        
        self.canvas = MyGLCanvas(
            self, self.devices, self.monitors, size=(100, -1))


        self.switch_to_3d_button = wx.Button(self, wx.ID_ANY, "3D mode")
        self.remove_item = wx.Button(self, wx.ID_ANY, "Remove")
        

        self.remove_item.Bind(wx.EVT_BUTTON, self.on_remove_item)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.button_sizer = wx.BoxSizer(wx.VERTICAL)

        self.sizer.Add(self.name_text, 1, wx.CENTER, 0)
        self.sizer.Add(self.canvas, 4, wx.EXPAND, 0)
        self.sizer.Add(self.button_sizer, 1, wx.ALIGN_CENTER, 0)

        self.button_sizer.Add(self.switch_to_3d_button, 1, wx.EXPAND, 0)
        self.button_sizer.Add(self.remove_item, 1, wx.EXPAND, 0)

        self.Layout()
        self.SetSizer(self.sizer)


class MenuFrame(wx.Frame):
    """Main frame that opens when application is started.

    Allows loading and saving of files,
    allows editing of text and debugging features. Has a button to enter GUI.

    Parameters:
    ------
    parent: FrameManager object.
    title: title.
    ------
    Public Methods:
    ------
    closeWindow(self, event): Closes all frames, calls sys.exit.

    """

    def __init__(self, parent, title) -> None:
        """Set up frame.

        Instantiate all objects.
        """
        super().__init__(parent=None, title=title)
        self.parent = parent

        self.Bind(wx.EVT_CLOSE, self.closeWindow)
        self.file_panel = FilePanel(self)
        self.text_editor = TextEditor(self)
        self.error_panel = wx.TextCtrl(
            self, wx.ID_ANY, "", style=wx.TE_READONLY | wx.TE_MULTILINE)
        fo = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False)
        self.text_editor.SetFont(fo)
        self.error_panel.SetFont(fo)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.Add(self.file_panel, 1, wx.EXPAND, 0)
        main_sizer.Add(self.text_editor, 7, wx.EXPAND, 0)
        main_sizer.Add(self.error_panel, 2, wx.EXPAND, 0)

        self.SetSizeHints(600, 600)
        self.SetSizer(main_sizer)

    def closeWindow(self, event):
        """Close all frames.

        Shutdown everything.
        """
        sys.exit()


class FilePanel(wx.Panel):
    """Control Panel that has control buttons in the MenuFrame.

    Parameters:
    ------
    parent: Instance of the MenuFrame frame.
    ------
    Public Methods:
    ------
    on_open_file(self, event): Handles the event when the open file button is pressed,
                                opens FileDialog.
    on_gui_button(self, event): Handles the event when the enter GUI button is pressed,
                                calls FrameManagers show_gui method.
    on_save_file(self, event): Handles the event when the save file button is pressed,
                                calls FrameManagers save_file methods.

    """

    def __init__(self, parent) -> None:
        """Initialise FilePanel and widgets.

        Create all widgets and sizers.
        """
        super().__init__(parent=parent)
        self.parent = parent
        self.path = None

        search_file_button = wx.Button(self, wx.ID_ANY, "Search file")
        save_as_button = wx.Button(self, wx.ID_ANY, "Save as")
        gui_button = wx.Button(self, wx.ID_ANY, "Continue to GUI")

        search_file_button.Bind(wx.EVT_BUTTON, self.on_open_file)
        save_as_button.Bind(wx.EVT_BUTTON, self.on_save_file)
        gui_button.Bind(wx.EVT_BUTTON, self.on_gui_button)

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        main_sizer.Add(search_file_button, -1, wx.ALL , 5)
        main_sizer.Add(save_as_button, -1, wx.ALL, 5)
        main_sizer.Add(gui_button, -1, wx.ALL , 5)
        self.SetSizer(main_sizer)

    def on_open_file(self, event):
        """Open FileDialog.

        Let user select file and load in text from file.
        """
        self.currentDirectory = os.getcwd()
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=self.currentDirectory,
            defaultFile="",
            style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR
        )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            print("You chose the following file:")
        dlg.Destroy()
        print("Filepath is", path)
        if path is not None:
            print("setting text")
            self.parent.text_editor.set_text(path)
            self.parent.error_panel.SetValue("")
            try:
                """Open and return the file specified by path for reading"""
                with open(path, "r") as f:
                    self.parent.parent.content = f.read()
                    self.parent.parent.file = io.StringIO(
                        self.parent.parent.content)
            except IOError:
                print("error, can't find or open file")
                sys.exit()
            self.path = path

    def on_gui_button(self, event):
        """Attempt to go to gui, call parser.

        If it fails display error.
        """
        self.parent.parent.show_gui(self.path)

    def on_save_file(self, event):
        """Open save menu.

        Let user save file.
        """
        self.parent.parent.save_file(self)


class TextEditor(wx.Panel):
    """Text Editor Panel that stores file text and allows users to edit said text before parsing.

    Parameters:
    ------
    parent: MenuFrame object.
    ------
    Public Methods:
    ------
    set_text(self, path): Sets text.

    """

    def __init__(self, parent) -> None:
        """Create text control widget.

        Holds the file content.
        """
        super().__init__(parent=parent)
        self.file = None
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.text = wx.TextCtrl(self, 1, style=wx.TE_MULTILINE)
        main_sizer.Add(self.text, -1, wx.EXPAND, 0)
        self.SetSizer(main_sizer)

    def set_text(self, path):
        """Set text.

        Set the file to the textbox.
        """
        try:
            """Open and return the file specified by path for reading"""
            with open(path) as f:
                content = f.readlines()
            self.text.SetValue("".join(content))
        except IOError:
            print("error, can't find or open file")
            sys.exit()


class GuiControlPanel(wx.Panel):
    """Control panel that handles switching back to menu frame, saving and help button.

    Parameters:
    ------
    parent: passes an instance of the GUI class
    size: passes size
    ------
    Public Methods:
    ------
    on_return_button(self, event): event handler for the return_button, shows menu, hides gui
    on_save_file(self, event): event handler for the save_as button, opens save menu.

    """

    def __init__(self, parent, size) -> None:
        """Initialise widgets and layout.

        Create widgets and sizers.
        """
        super().__init__(parent=parent, size=size)

        self.parent = parent
        self.path = None

        self.return_button = wx.Button(self, wx.ID_ANY, "Back to text editor")
        self.save_as_button = wx.Button(self, wx.ID_ANY, "Save as")
        self.help_button = wx.Button(self, wx.ID_ANY, "Help")

        self.return_button.Bind(wx.EVT_BUTTON, self.on_return_button)
        self.save_as_button.Bind(wx.EVT_BUTTON, self.on_save_file)

        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.main_sizer.Add(self.return_button, 1, wx.ALL, 5)
        self.main_sizer.Add(self.save_as_button, 1, wx.ALL, 5)
        self.main_sizer.Add(self.help_button, 1, wx.ALL, 5)

        self.SetSizer(self.main_sizer)

    def on_return_button(self, event):
        """Call the FrameManager show_menu method, hide gui, show menu.

        Toggle between frames.
        """
        self.parent.parent.show_menu()

    def on_save_file(self, event):
        """Call the FrameManager save_file method, open file saving menu.

        Call FrameManager.save_file.
        """
        self.parent.parent.save_file(self)


class Gui(wx.Frame):
    """Configure the main window and all the widgets.

    This class provides a graphical user interface for the Logic Simulator and
    enables the user to change the circuit properties and run simulations.

    Parameters
    ----------
    title: title of the window.

    Public methods
    --------------

    closeWindow(self, event): Closes all frames

    """

    def __init__(self, parent, title, names, devices, network, monitors):
        """Initialise widgets and layout.

        Create widgets and sizers.
        """
        super().__init__(parent=None, title=title, size=(800, 600))

        self.parent = parent
        self.Bind(wx.EVT_CLOSE, self.closeWindow)

        self.names = names
        self.devices = devices
        self.network = network
        self.monitors = monitors

        self.cycles_completed = 0  # number of simulation cycles completed

        self.character = ""  # current character
        self.line = ""  # current string entered by the user
        self.cursor = 0  # cursor position

        # Canvas for drawing signals
        self.scrolled_panel = MonitorPanel(
            self, self.monitors, self.devices, self.names)
        self.scrolled_panel.SetupScrolling()
        # Control side_panel
        self.side_panel = SidePanel(self, self.scrolled_panel)
        self.gui_control = GuiControlPanel(self, size=(-1, 75))

        # Configure sizers for layout
        self.top_level_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.top_level_sizer.Add(self.gui_control, 1, wx.EXPAND, 0)
        self.top_level_sizer.Add(self.main_sizer, 10, wx.EXPAND, 0)

        self.main_sizer.Add(self.scrolled_panel, 8, wx.EXPAND | wx.ALL, 5)
        self.main_sizer.Add(self.side_panel, 1, wx.ALL, 5)

        self.SetSizeHints(600, 600)
        self.SetSizer(self.top_level_sizer)

    def closeWindow(self, event):
        """Close all frames.

        Shutdown everything.
        """
        sys.exit()


class FrameManager:
    """Manage the two main frames for the GUI and starting menu, including showing and hiding frames.

    Paramaters:
    ------
    title: title of the Logic simulator
    ------
    Public methods:
    ------
    show_gui(self, path): Shows the gui, creates objects for devices, monitors, network.

    process_content(self): Reads in text_field and passes the text to parser, parsese and handles errors.

    show_menu(self): Shows menu, hides gui.

    save_file(self, button): Opens file saving menu.

    """

    def __init__(self, title):
        """Launch app.

        Create MenuFrame.
        """
        self.title = title
        self.app = wx.App()
        self.menu = MenuFrame(self, title)
        self.menu.Show()
        self.app.MainLoop()

    def show_gui(self, path):
        """Show the gui.

        Create objects for devices, monitors, network.
        """
        self.path = path
        if self.menu.text_editor.text is not None:
            self.names = Names()
            self.devices = Devices(self.names)
            self.network = Network(self.names, self.devices)
            self.monitors = Monitors(self.names, self.devices, self.network)

            self.process_content()

        else:
            print("Please choose a file first!")

    def process_content(self):
        """Read in text_field and pass the text to parser, parse and handle errors.

        Process all the key backend logic.
        """
        self.content = self.menu.text_editor.text.GetValue()
        self.file = io.StringIO(self.content)
        self.scanner = Scanner(self.path, self.file, self.names)
        self.parser = Parser(
            self.names,
            self.devices,
            self.network,
            self.monitors,
            self.scanner)

        if self.parser.parse_network():
            print("parsing")
            self.gui = Gui(
                self,
                self.title,
                self.names,
                self.devices,
                self.network,
                self.monitors)
            self.menu.Hide()
            self.gui.Show()
            self.gui.path = self.path
            self.menu.error_panel.SetValue("")
        else:
            error = Error.gui_report_error(self.scanner)
            Error.print_error(self.scanner)
            print("Sorry, can't parse network.")
            self.menu.error_panel.SetValue(error)

    def show_menu(self):
        """Show menu.

        Hide gui.
        """
        self.menu.Show()
        self.gui.Hide()

    def save_file(self, button):
        """Open file saving menu.

        Allows saving of file to txt file.
        """
        self.content = self.menu.text_editor.text.GetValue()
        self.file = io.StringIO(self.content)
        print("content", self.content)
        self.currentDirectory = os.getcwd()
        dlg = wx.FileDialog(
            button, message="Save file as ...",
            defaultDir=self.currentDirectory,
            defaultFile="", style=wx.FD_SAVE
        )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            print(f"You chose the following filename: {path}")
            with open(path, "w") as file:
                file.write(self.content)
        dlg.Destroy()
