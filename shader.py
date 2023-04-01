from ursina import *

water_shader = Shader(name='water_shader', language=Shader.GLSL, fragment='''
#version 130
uniform vec4 p3d_ColorScale;
in vec2 uv;
out vec4 result;




uniform sampler2D p3d_Texture0;
uniform float time;

uniform vec4 dark_color;
uniform vec4 light_color;

uniform float s;
uniform float mod;
uniform float mod2;
uniform float mody;

void main() {



    
    
    vec4 a = texture(p3d_Texture0, uv + vec2(time*mody, time*mody));
    vec4 b = texture(p3d_Texture0, uv + vec2(time*mod, time*mod-.025));
    vec4 c = (a + b) * s;

    result = texture(p3d_Texture0, uv + c.xy) * c;
    result.a = 1.0;

    result = mix(dark_color, light_color, result.r*mod2);
}

''',
default_input = {
  'dark_color' : color.black,
  'light_color' : color.white,
  "s" : .5,
  "mod" : .5,
  "mod2" : 0,
  "mody" : .1,
}
)