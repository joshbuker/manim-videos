from manim import *

class SquareToCircle(Scene):
  def construct(self):
    circle = Circle()  # create a circle
    circle.set_fill(PINK, opacity=0.5)  # set color and transparency

    square = Square()  # create a square
    square.rotate(PI / 4)  # rotate a certain amount

    self.play(Create(square))  # animate the creation of the square
    self.play(Transform(square, circle))  # interpolate the square into the circle
    self.play(FadeOut(square))  # fade out animation

class ToyExample(Scene):
  def construct(self):
    orange_square = Square(color=ORANGE, fill_opacity=0.5)
    blue_circle = Circle(color=BLUE, fill_opacity=0.5)
    self.add(orange_square)
    self.play(ReplacementTransform(orange_square, blue_circle, run_time=3))
    small_dot = Dot()
    small_dot.add_updater(lambda mob: mob.next_to(blue_circle, DOWN))
    self.play(Create(small_dot))
    self.play(blue_circle.animate.shift(RIGHT))
    self.wait()
    self.play(FadeOut(blue_circle, small_dot))
