from manim import *


# class xx(Scene):
#     def construct(self):

#         # sc = Scene()

#         txt = Text("hello")


#         self.play(
#             Write(txt)
#         )

#         self.wait(2)

def xx():
    sc = Scene()
    txt = Text("hello")
    sc.play(
        Write(txt)
    )
    sc.wait(2)

xx()