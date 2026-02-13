from .pyscreen import *

def go(): 
    global draw_frames_per_second
    caller_frame = sys._getframe(1)
    caller_globals = caller_frame.f_globals

    if '__main__' in caller_globals['__name__']:
        functions = {}
        for name, obj in caller_globals.items():
            if inspect.isfunction(obj) and obj.__module__ == caller_globals['__name__']:
                functions[name] = obj

        def tdraw():
            if 'draw' in functions:
                functions['draw']()
            if pgz_camera.is_camera_loaded():
                pgz_camera.camera_draw_func(pgzero_screen)
            if draw_frames_per_second:
                time.sleep(1 / draw_frames_per_second)

        def ton_mouse_down(pos, button):
            if 'on_mouse_down' in functions:
                func = functions['on_mouse_down']
                sig = inspect.signature(func)
                para_len = len(sig.parameters)
                if para_len == 0:
                    functions['on_mouse_down']()
                elif para_len == 1:
                    functions['on_mouse_down'](pos)
                else:
                    functions['on_mouse_down'](pos, button)

        def ton_mouse_move(pos):
            global width_increase, height_increase
            if 'on_mouse_move' in functions:
                func = functions['on_mouse_move']
                sig = inspect.signature(func)
                para_len = len(sig.parameters)
                if para_len == 0:
                    functions['on_mouse_move']()
                else:
                    functions['on_mouse_move'](pos)

        def ton_mouse_up(pos, button):
            if 'on_mouse_up' in functions:
                func = functions['on_mouse_up']
                sig = inspect.signature(func)
                para_len = len(sig.parameters)
                if para_len == 0:
                    functions['on_mouse_up']()
                elif para_len == 1:
                    functions['on_mouse_up'](pos)
                else:
                    functions['on_mouse_up'](pos, button)

        def tupdate():
            if 'update' in functions:
                functions['update']()
            if update_frames_per_second:
                time.sleep(1 / update_frames_per_second)
            if pgz_camera.is_camera_loaded():
                pgz_camera.camera_update_func()
        
        def ton_quit():
            if 'on_quit' in functions:
                functions['on_quit']()
            if pgz_camera.is_camera_loaded():
                pgz_camera.camera_on_quit_func()

        caller_globals['draw'] = tdraw
        caller_globals['on_mouse_down'] = ton_mouse_down
        caller_globals["on_mouse_move"] = ton_mouse_move
        caller_globals["on_mouse_up"] = ton_mouse_up
        caller_globals['on_mouse_down'] = ton_mouse_down
        caller_globals["on_mouse_move"] = ton_mouse_move
        caller_globals["on_mouse_up"] = ton_mouse_up
        caller_globals['update'] = tupdate
        caller_globals['on_quit'] = ton_quit
        import pgzrun
        pgzrun.go()