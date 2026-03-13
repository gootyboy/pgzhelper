"""Main runner for pgzhelper. Use pgzhelper.pgzhelper_run.go() instead of pgzhelper._runner.go()."""

from ._core import *
from ._core import _screen, _update_fps, _draw_fps, _init, _camera, _on_mouse_down_fps, _on_mouse_move_fps, _on_mouse_up_fps

def go() -> None:
    """Runs the pgzero script."""
    global _draw_fps, _screen, _update_fps
    caller_frame = sys._getframe(1)
    caller_globals = caller_frame.f_globals

    if '__main__' in caller_globals['__name__']:
        functions = {}
        for name, obj in caller_globals.items():
            if inspect.isfunction(obj) and obj.__module__ == caller_globals['__name__']:
                functions[name] = obj

        def tdraw() -> None:
            """The temporary draw function to be injected into the user's file."""
            _init(screen)
            if 'draw' in functions:
                functions['draw']()
            if _camera.is_camera_loaded():
                _camera.camera_draw_func(_screen)
            if _draw_fps:
                time.sleep(1 / _draw_fps)

        def ton_mouse_down(pos: tuple[int, int], button: PGZeroMouse) -> None:
            """
            The temporary on_mouse_down function to be injected into the user's file.

            :param pos: The position of the click.
            :param button: The button pressed.
            """
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
            if _on_mouse_down_fps:
                time.sleep(1 / _on_mouse_down_fps)

        def ton_mouse_move(pos: tuple[int, int]) -> None:
            """
            The temporary on_mouse_move function to be injected into the user's file.

            :param pos: The currentb position of the mouse.
            """
            if 'on_mouse_move' in functions:
                func = functions['on_mouse_move']
                sig = inspect.signature(func)
                para_len = len(sig.parameters)
                if para_len == 0:
                    functions['on_mouse_move']()
                else:
                    functions['on_mouse_move'](pos)
            if _on_mouse_move_fps:
                time.sleep(1 / _on_mouse_move_fps)

        def ton_mouse_up(pos: tuple[int, int], button: PGZeroMouse):
            """
            The temporary on_mouse_up function to be injected into the user's file.

            :param pos: The position of the release.
            :param button: The button released.
            """
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
            if _on_mouse_up_fps:
                time.sleep(1 / _on_mouse_up_fps)

        def tupdate() -> None:
            """The temporary update function to be injected into the user's file."""
            if 'update' in functions:
                functions['update']()
            if _update_fps:
                time.sleep(1 / _update_fps)
            if _camera.is_camera_loaded():
                _camera.camera_update_func()
            if _update_fps:
                time.sleep(1 / _update_fps)
        
        def ton_quit() -> None:
            """The temporary on_quit function to be injected into the user's file."""
            if 'on_quit' in functions:
                functions['on_quit']()
            if _camera.is_camera_loaded():
                _camera.camera_on_quit_func()

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
