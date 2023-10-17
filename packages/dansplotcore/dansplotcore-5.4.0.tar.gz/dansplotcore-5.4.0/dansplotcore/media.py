#===== imports =====#
from .vector_text import Texter

import pyglet
from pyglet import gl

import ctypes

#===== consts =====#
vert_shader_src = b'''\
uniform vec2 uOrigin;
uniform vec2 uZoom;

attribute vec2 aPosition;
attribute vec4 aColor;

varying vec4 vColor;

void main() {
    gl_Position = vec4(
        (aPosition.x - uOrigin.x) * uZoom.x,
        (aPosition.y - uOrigin.y) * uZoom.y,
        0.0,
        1.0
    );
    vColor = aColor;
}
'''

frag_shader_src = b'''\
varying vec4 vColor;

void main() {
    gl_FragColor = vColor;
}
'''

#===== helpers =====#
def compile_shader(type_, src):
    shader = gl.glCreateShader(type_)
    gl.glShaderSource(
        shader,
        1,
        ctypes.cast(
            ctypes.pointer(ctypes.pointer(ctypes.create_string_buffer(src))),
            ctypes.POINTER(ctypes.POINTER(ctypes.c_char)),
        ),
        ctypes.byref(ctypes.c_int(len(src) + 1)),
    )
    gl.glCompileShader(shader)
    status = ctypes.c_int(0)
    gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS, ctypes.byref(status))
    if not status.value:
        log = ctypes.create_string_buffer(4096)
        gl.glGetShaderInfoLog(shader, len(log), None, log)
        raise Exception('Error compiling shader: ' + log.value.decode('utf8'))
    return shader

#===== file-scope =====#
class F:
    program = None
    locations = {}
    window = None
    origin = [0, 0]
    zoom = [1, 1]

#===== interfaces =====#
class Buffer:
    def __init__(self):
        self.data = []
        self.draws = []
        self.buffer = gl.GLuint()
        gl.glGenBuffers(1, self.buffer)

    def __len__(self):
        return len(self.data) // 6

    def add(self, x, y, r, g, b, a):
        self.data.extend([x, y, r, g, b, a])

    def add_vertices(self, vertices):
        for v in self.vertices:
            self.add(v)

    def add_data(self, data):
        self.data.extend(data)

    def prep(self, usage):
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.buffer)
        gl.glBufferData(
            gl.GL_ARRAY_BUFFER,
            len(self.data)*4,
            (gl.GLfloat * len(self.data))(*self.data),
            getattr(gl, f'GL_{usage.upper()}_DRAW'),
        )

    def draw(self):
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.buffer);
        gl.glVertexAttribPointer(F.locations['aPosition'], 2, gl.GL_FLOAT, gl.GL_FALSE, 6 * 4, 0 * 4);
        gl.glVertexAttribPointer(F.locations['aColor'   ], 4, gl.GL_FLOAT, gl.GL_FALSE, 6 * 4, 2 * 4);
        for mode, first, count in self.draws:
            gl.glDrawArrays(getattr(gl, f'GL_{mode.upper()}'), first, count)

def init(w, h, title):
    # window
    F.window = pyglet.window.Window(
        width=w,
        height=h,
        caption=title,
        resizable=True,
        vsync=True,
    )
    # shader
    F.program = gl.glCreateProgram()
    gl.glAttachShader(F.program, compile_shader(gl.GL_VERTEX_SHADER, vert_shader_src))
    gl.glAttachShader(F.program, compile_shader(gl.GL_FRAGMENT_SHADER, frag_shader_src))
    gl.glLinkProgram(F.program)
    # uniforms
    F.locations['uOrigin'] = gl.glGetUniformLocation(F.program, b'uOrigin')
    F.locations['uZoom'  ] = gl.glGetUniformLocation(F.program, b'uZoom')
    # attributes
    F.locations['aPosition'] = gl.glGetAttribLocation(F.program, b'aPosition')
    F.locations['aColor'   ] = gl.glGetAttribLocation(F.program, b'aColor')
    gl.glEnableVertexAttribArray(F.locations['aPosition'])
    gl.glEnableVertexAttribArray(F.locations['aColor'])

def view_set(x, y, w, h):
    F.origin = [x + w/2, y + h/2]
    F.zoom = [2/w, 2/h]

def width():
    return F.window.width

def height():
    return F.window.height

def capture():
    pyglet.image.get_buffer_manager().get_color_buffer().save('plot.png')

def clear():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

def set_callbacks(
    mouse_drag=None,
    mouse_scroll=None,
    key_press=None,
    draw=None,
):
    @F.window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        mouse_drag(dx, dy)

    @F.window.event
    def on_mouse_scroll(x, y, scroll_x, scroll_y):
        mouse_scroll(x, y, scroll_y)

    @F.window.event
    def on_key_press(symbol, modifiers):
        if 32 <= symbol < 127:
            key = chr(symbol)
        else:
            key = {
                pyglet.window.key.LEFT  : 'Left',
                pyglet.window.key.RIGHT : 'Right',
                pyglet.window.key.UP    : 'Up',
                pyglet.window.key.DOWN  : 'Down',
                pyglet.window.key.SPACE : 'Space',
                pyglet.window.key.RETURN: 'Return',
            }.get(symbol)
        if key: key_press(key)

    @F.window.event
    def on_draw():
        gl.glUseProgram(F.program)
        gl.glUniform2f(F.locations['uOrigin'], *F.origin)
        gl.glUniform2f(F.locations['uZoom'  ], *F.zoom)
        draw()

def run():
    gl.glEnable(gl.GL_BLEND);
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA);
    pyglet.app.run()
