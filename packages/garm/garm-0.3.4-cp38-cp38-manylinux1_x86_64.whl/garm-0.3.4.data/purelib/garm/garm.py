import ctypes
import os
import platform

path = os.path.dirname(os.path.realpath(__file__))
pf = platform.system();

if pf == 'Windows':
    lib = ctypes.cdll.LoadLibrary("%s/lib/libcgarm.dll"%path)
elif pf == 'Linux':
    lib = ctypes.CDLL("%s/lib/libcgarm.so"%path)
else:
    lib = ctypes.CDLL("%s/lib/libcgarm.dylib"%path)

def convert(*args):
    lib.setup()

    args_array = (ctypes.POINTER(ctypes.c_char) * (len(args)+1))()

    enc_arg = "garm".encode('utf8')
    args_array[0] = ctypes.create_string_buffer(enc_arg)

    for i, arg in enumerate(args):
        enc_arg = arg.encode('utf-8')
        args_array[i+1] = ctypes.create_string_buffer(enc_arg)

    lib.garm(len(args)+1, args_array)

    lib.tear_down()

#if __name__ == '__main__':
#    garm('bar.mk3d', 'bar.usdz')
#    garm('PendulumY.urdf', 'afo.glb', 'PendulumY.garm')
