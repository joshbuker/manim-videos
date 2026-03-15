# Some ChatGPT vibe code, TODO: Rework into what I actually want.

from manim import *
import numpy as np

FRAME_MS = 20
SEP_MS = 0.3

CHANNEL_COLORS = [
    RED, ORANGE, YELLOW, GREEN,
    TEAL, BLUE, PURPLE, PINK
]

class PPMPacket(Scene):
    def construct(self):
        title = Text("PPM RF Packet Example").to_edge(UP)
        self.play(Write(title))

        # Time axis
        axis = NumberLine(
            x_range=[0, 22, 2],
            length=12,
            include_numbers=True,
        )
        axis.shift(DOWN)

        axis_label = Text("Time (ms)").scale(0.5).next_to(axis, DOWN)

        self.play(Create(axis), FadeIn(axis_label))

        # Example channel pulse widths (ms)
        channels = [1.2, 1.5, 1.0, 1.8, 1.3, 1.6, 1.4, 1.7]

        x = 0
        pulses = VGroup()

        for i, width in enumerate(channels):
            pulse = Rectangle(
                width=width * 0.5,
                height=0.6
            ).move_to(axis.n2p(x + width/2) + UP)

            label = Text(f"Ch{i+1}").scale(0.4).next_to(pulse, UP)

            pulses.add(pulse, label)

            x += width + 0.4  # spacing between pulses

        self.play(LaggedStart(*[FadeIn(p) for p in pulses], lag_ratio=0.2))

        # Sync gap at end of frame
        sync = Brace(
            Line(axis.n2p(x), axis.n2p(22)),
            UP
        )
        sync_label = Text("Sync Gap").scale(0.5).next_to(sync, UP)

        self.play(GrowFromCenter(sync), Write(sync_label))

        self.wait(2)

class PPMSignal(Scene):

    def build_waveform(self, values):
        """
        values: list of channel pulse widths in ms
        returns a VMobject polyline representing waveform
        """

        points = []
        t = 0
        y_low = -1
        y_high = 1

        points.append([t, y_low, 0])

        for width in values:

            # separator low
            points.append([t, y_low, 0])
            t += SEP_MS
            points.append([t, y_low, 0])

            # rising edge
            points.append([t, y_high, 0])

            # pulse high
            t += width
            points.append([t, y_high, 0])

            # falling edge
            points.append([t, y_low, 0])

        # sync gap
        if t < FRAME_MS:
            points.append([FRAME_MS, y_low, 0])

        wave = VMobject()
        wave.set_points_as_corners([np.array(p) for p in points])

        return wave

    def construct(self):

        title = Text("PPM RF Frame").to_edge(UP)
        self.play(Write(title))

        # time axis
        axis = NumberLine(
            x_range=[0, FRAME_MS, 2],
            length=12,
            include_numbers=True
        )

        axis.shift(DOWN * 2)

        axis_label = Text("milliseconds").scale(0.5).next_to(axis, DOWN)

        self.play(Create(axis), FadeIn(axis_label))

        # initial channel widths
        channels = [1.2, 1.5, 1.0, 1.7, 1.3, 1.6, 1.4, 1.8]

        waveform = self.build_waveform(channels)
        waveform.scale(0.5)
        waveform.move_to(axis.get_center() + UP)

        self.play(Create(waveform), run_time=3)

        # channel labels
        labels = VGroup()

        t = 0

        for i, width in enumerate(channels):

            mid = t + SEP_MS + width / 2

            label = Text(f"Ch {i+1}", font_size=24, color=CHANNEL_COLORS[i])
            label.move_to(axis.n2p(mid) + UP * 2)

            labels.add(label)

            t += SEP_MS + width

        self.play(LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.1))

        # demonstrate stick movement (pulse change)

        new_channels = [1.8, 1.1, 1.6, 1.2, 1.5, 1.3, 1.9, 1.4]

        new_wave = self.build_waveform(new_channels)
        new_wave.scale(0.5)
        new_wave.move_to(axis.get_center() + UP)

        self.wait(1)

        self.play(
            Transform(waveform, new_wave),
            run_time=2
        )

        # highlight sync gap

        total = sum(new_channels) + len(new_channels) * SEP_MS
        sync_start = total

        sync_line = Line(
            axis.n2p(sync_start),
            axis.n2p(FRAME_MS),
            color=WHITE
        )

        brace = Brace(sync_line, UP)
        brace_text = Text("Sync Gap", font_size=28).next_to(brace, UP)

        self.play(Create(brace), Write(brace_text))

        self.wait(2)

        # looping frame visualization

        loop_arrow = CurvedArrow(
            waveform.get_right(),
            waveform.get_left(),
            angle=TAU/3
        )

        loop_text = Text("Frame repeats (~50 Hz)", font_size=28)
        loop_text.next_to(loop_arrow, UP)

        self.play(Create(loop_arrow), Write(loop_text))

        self.wait(3)

class JoystickPPM(Scene):

    def build_wave(self, widths):

        points = []
        t = 0
        y_low = -1
        y_high = 1

        points.append([t, y_low, 0])

        for w in widths:

            # separator
            points.append([t, y_low, 0])
            t += SEP_MS
            points.append([t, y_low, 0])

            # rise
            points.append([t, y_high, 0])

            # pulse
            t += w
            points.append([t, y_high, 0])

            # fall
            points.append([t, y_low, 0])

        points.append([FRAME_MS, y_low, 0])

        wave = VMobject()
        wave.set_points_as_corners([np.array(p) for p in points])

        return wave


    def construct(self):

        title = Text("Joystick → PPM RF Frame").to_edge(UP)
        self.play(Write(title))


        # ----------------------------
        # Joystick
        # ----------------------------

        base = Circle(radius=1.5)
        knob = Dot(radius=0.15, color=YELLOW)

        joystick = VGroup(base, knob)
        joystick.shift(LEFT*4)

        self.play(Create(base), FadeIn(knob))

        x_tracker = ValueTracker(0)
        y_tracker = ValueTracker(0)

        knob.add_updater(
            lambda m: m.move_to(
                base.get_center()
                + RIGHT*x_tracker.get_value()
                + UP*y_tracker.get_value()
            )
        )

        x_label = Text("Roll", font_size=24).next_to(base, DOWN)
        y_label = Text("Pitch", font_size=24).next_to(base, LEFT)

        self.play(FadeIn(x_label), FadeIn(y_label))


        # ----------------------------
        # Axis / waveform area
        # ----------------------------

        axis = NumberLine(
            x_range=[0, FRAME_MS, 2],
            length=10,
            include_numbers=True
        )

        axis.shift(RIGHT*3 + DOWN*2)

        axis_label = Text("ms", font_size=24).next_to(axis, DOWN)

        self.play(Create(axis), FadeIn(axis_label))


        # ----------------------------
        # Channel pulse trackers
        # ----------------------------

        ch1 = ValueTracker(1.5)
        ch2 = ValueTracker(1.5)

        def update_channels():

            roll = x_tracker.get_value()
            pitch = y_tracker.get_value()

            ch1.set_value(1.5 + roll*0.5)
            ch2.set_value(1.5 + pitch*0.5)

            widths = [
                ch1.get_value(),
                ch2.get_value(),
                1.5, 1.5, 1.5, 1.5
            ]

            wave = self.build_wave(widths)

            wave.scale(0.45)
            wave.move_to(axis.get_center()+UP)

            return wave

        waveform = always_redraw(update_channels)

        self.play(Create(waveform), run_time=2)


        # ----------------------------
        # Pulse width measurement
        # ----------------------------

        brace = always_redraw(
            lambda:
            BraceBetweenPoints(
                axis.n2p(SEP_MS),
                axis.n2p(SEP_MS + ch1.get_value()),
                UP
            )
        )

        label = always_redraw(
            lambda:
            Text(
                f"{int(ch1.get_value()*1000)} µs",
                font_size=24
            ).next_to(brace, UP)
        )

        self.play(Create(brace), FadeIn(label))


        # ----------------------------
        # Move joystick to show mapping
        # ----------------------------

        self.play(x_tracker.animate.set_value(1), run_time=2)
        self.play(x_tracker.animate.set_value(-1), run_time=2)
        self.play(x_tracker.animate.set_value(0), run_time=2)

        self.play(y_tracker.animate.set_value(1), run_time=2)
        self.play(y_tracker.animate.set_value(-1), run_time=2)
        self.play(y_tracker.animate.set_value(0), run_time=2)


        # ----------------------------
        # Sync gap highlight
        # ----------------------------

        sync_start = 12

        sync_line = Line(
            axis.n2p(sync_start),
            axis.n2p(FRAME_MS)
        )

        sync_brace = Brace(sync_line, UP)
        sync_text = Text("Sync Gap", font_size=24).next_to(sync_brace, UP)

        self.play(Create(sync_brace), Write(sync_text))

        self.wait(3)