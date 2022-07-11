from manim import *
from manim_presentation import Slide
import random

MEMBER = GREEN
POSSIBLE = BLUE
EXCLUDED = RED


class DashedArrow(Arrow, DashedLine):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class VRPIntro(Slide):

    def construct(self):
        # introduction
        text = MarkupText(f"From <span fgcolor='{BLUE}'>TSP</span>\nto Vehicle Routing Problems (<span fgcolor='{BLUE}'>VRP</span>)")
        coords = [
            np.array([-4.25, 0.75, 0]),
            np.array([-1.75, 2.75, 0]),
            np.array([-1.25, 1.25, 0]),
            np.array([-1, -0.5, 0]),
            np.array([2, 2.5, 0]),
            np.array([1.75, 1, 0]),
            np.array([3.25, -0.75, 0]),
            np.array([2.5, -2, 0]),
            np.array([4.75, 1, 0]),
        ]
        dots = [Dot(i) for i in coords]
        dot_group = VGroup(*dots)
        VGroup(text, dot_group).arrange(DOWN)
        self.play(FadeIn(text))
        self.pause()
        self.play(*[FadeIn(dot) for dot in dots])
        self.pause()
        self.wait()

        # successor model


class SequenceOtherWork(Slide):

    def construct(self):
        # mention insertion graph and partial order scheduling

        # mention cplex
        pass


class Sequences(Slide):

    def construct(self):

        # coordinates for the dots
        coords = [
            np.array([-4.25, 0.75, 0]),
            np.array([-1.75, 2.75, 0]),
            np.array([-1.25, 1.25, 0]),
            np.array([-1, -0.5, 0]),  # last member
            np.array([2, 2.5, 0]),
            np.array([1.75, 1, 0]),
            np.array([3.25, -0.75, 0]),  # last possible
            np.array([2.5, -2, 0]),
            np.array([4.75, 1, 0]),
        ]
        # draw the dots
        dots = [Dot(i, radius=0.16) for i in coords]
        self.play(*[FadeIn(dot) for dot in dots])
        self.pause()
        # partition of the nodes
        members = [0, 1, 2, 3]
        possible = [4, 5, 6]
        insertions = {
            4: [1, 2, 3],
            5: [1, 2, 3, 4],
            6: [1, 2, 3, 4, 5],
        }
        excluded = [7, 8]

        members_group = VGroup(*[dots[i] for i in members])
        excluded_group = VGroup(*[dots[i] for i in excluded])
        possible_group = VGroup(*[dots[i] for i in possible])
        # nodes that will be set as members
        self.play(members_group.animate.set_color(MEMBER))
        self.pause()

        # ordering for the members
        successors = [Arrow(i.get_center(), j.get_center(), color=MEMBER) for i, j in zip(members_group, members_group[1:])]
        # successors_group = VGroup(*successors)
        animations = [GrowArrow(succ) for succ in successors]
        self.play(AnimationGroup(*animations, lag_ratio=0.25))
        self.pause()

        # excluded nodes
        self.play(excluded_group.animate.set_color(EXCLUDED))
        self.pause()

        # possible nodes
        self.play(possible_group.animate.set_color(POSSIBLE))
        self.pause()
        # predecessors for the nodes
        insertions_arrows = {
            node:
                [DashedArrow(start=dots[pred].get_center(), end=dots[node].get_center(), dashed_ratio=0.4, dash_length=0.15, color=POSSIBLE) for pred in v]
            for node, v in insertions.items()
        }
        # make the arrows grow
        arrows_list = [arrow for k, v in insertions_arrows.items() for arrow in v]
        random.shuffle(arrows_list)
        animations_list = [GrowArrow(arrow) for arrow in arrows_list]
        self.play(AnimationGroup(*animations_list, lag_ratio=0.2))

        self.pause()
        self.wait()


class TransitionTimeConstraint(Slide):

    def construct(self):
        pass


class OtherConstraints(Slide):

    def construct(self):
        pass


class SearchProcedure(Slide):

    def construct(self):
        pass


class MultipleProblems(Slide):

    def construct(self):
        pass


class Perspectives(Slide):

    def construct(self):
        pass


class Conclusion(Slide):

    def construct(self):
        pass

