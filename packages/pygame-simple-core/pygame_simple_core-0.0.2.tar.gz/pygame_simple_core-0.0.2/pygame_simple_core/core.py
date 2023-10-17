import sys
import pygame as pg
from . import tools


class FpsDisplay():

    def __init__(
        self, clock, foreground, background, antialias, font, position,
        precision, visible
    ):
        self.clock = clock
        self.foreground = foreground
        self.background = background
        self.antialias = antialias
        self.font = tools.load_font(font)
        self.position = position
        self.precision = precision
        self.visible = visible

    @tools.default_screen
    def draw(self, screen=None):
        if self.visible:
            fps_value = self.clock.get_fps()
            fps_text = f'FPS: {fps_value:.{self.precision}f}'
            fps_surf = self.font.render(
                fps_text, self.antialias, self.foreground, self.background
            )
            fps_rect = fps_surf.get_rect()
            position_value = getattr(screen.get_rect(), self.position)
            setattr(fps_rect, self.position, position_value)

            screen.blit(fps_surf, fps_rect)


class ScheduledEvent():

    def __init__(self, core, repeat, interval, function, *args, **kwargs):
        self.core = core
        self.repeat = repeat
        self.start = pg.time.get_ticks()
        self.interval = interval
        self.function = lambda: function(*args, **kwargs)

    @property
    def target_time_reached(self):
        return pg.time.get_ticks() >= self.start + self.interval

    def call_function(self):
        if self.target_time_reached:
            self.function()

            if self.repeat:
                self.start = pg.time.get_ticks()
            else:
                self.quit()

    def quit(self):
        self.core.scheduled_events.remove(self)


class Core():
    """
    The main application core that manages the game loop and events.

    Args:
        size (tuple): The screen size (width, height).
        flags (int): Pygame screen flags.
        fps_foreground (tuple): The color for the FPS text (R, G, B).
        fps_background (tuple): The background color behind the FPS text (R, G, B).
        fps_antialias (bool): Enable antialiasing for text rendering.
        fps_font (str or list): Font settings for rendering the FPS text.
        fps_position (str): The position of the FPS display on the screen.
        fps_precision (int): The number of decimal places to display for FPS.
        fps_visible (bool): Whether the FPS display is initially visible.

    Methods:
        run():
            Starts the main game loop.
        set_interval(interval, function, *args, **kwargs):
            Schedules a repeating event.
        set_timeout(interval, function, *args, **kwargs):
            Schedules a one-time event.
        check_event(event):
            Handles Pygame events. Override to implement custom event handling.
        update():
            Updates the game/application state. Override to implement your logic.
        draw():
            Renders graphics to the screen. Override to create the visual aspect of your game.
        __exit__():
            Called when the Core instance is exiting. Override for cleanup or specific actions.
    """

    def __init__(
        self, size=(0, 0), flags=pg.FULLSCREEN | pg.SRCALPHA,
        fps_foreground=(255, 255, 0), fps_background=(0, 0, 0),
        fps_antialias=False, fps_font=[20, None], fps_position='topright',
        fps_precision=1, fps_visible=True
    ):
        pg.init()

        self.screen = pg.display.set_mode(size, flags)
        self.screen_rect = self.screen.get_rect()
        self.screen_color = (255, 255, 255)
        self.clock = pg.time.Clock()
        self.max_fps = 0
        self.fps_display = FpsDisplay(
            self.clock, fps_foreground, fps_background, fps_antialias,
            fps_font, fps_position, fps_precision, fps_visible
        )
        self.scheduled_events = []
        self.quit_keys = [27]
        self.running = True

    def run(self):
        while self.running:
            self._check_scheduled_events()
            self._check_quit_event()
            self.update()
            self._draw()
            self.clock.tick(self.max_fps)

        self.__exit__()

    def _check_scheduled_events(self):
        for event in self.scheduled_events:
            event.call_function()

    def _check_quit_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN \
                    and event.key in self.quit_keys:
                self.running = False
            else:
                self.check_event(event)

    def check_event(self, event):
        pass

    def update(self):
        pass

    def _draw(self):
        self.screen.fill(self.screen_color)
        self.draw()
        self.fps_display.draw()
        pg.display.flip()

    def draw(self):
        pass

    def __exit__(self):
        pass

    def set_interval(self, interval, function, *args, **kwargs):
        event = ScheduledEvent(
            self, True, interval, function, *args, **kwargs
        )

        self.scheduled_events.append(event)

        return event

    def set_timeout(self, interval, function, *args, **kwargs):
        event = ScheduledEvent(
            self, False, interval, function, *args, **kwargs
        )

        self.scheduled_events.append(event)

        return event
