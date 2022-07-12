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
        text_tsp_to_vrp = MarkupText(f"From <span fgcolor='{BLUE}'>TSP</span>\nto Vehicle Routing Problems (<span fgcolor='{BLUE}'>VRP</span>)")
        text_successor = MarkupText("Successor model", color=BLUE)
        text_group = VGroup(text_tsp_to_vrp, text_successor).arrange(DOWN, center=False, aligned_edge=LEFT).to_corner(UP + LEFT)
        coords = [
            np.array([-4.25, 0.75, 0]),
            np.array([-1.75, 2.75, 0]),
            np.array([-1.25, 1.25, 0]),
            np.array([-1, -0.5, 0]),
            np.array([2, 2.5, 0]),
            np.array([1.75, 1, 0]),
            np.array([3.25, -0.75, 0]),
            np.array([2.5, -2, 0]),
            np.array([1.5, 0, 0]),
        ]
        dots = [Dot(i) for i in coords]
        dot_group = VGroup(*dots)
        VGroup(text_group, dot_group).arrange(DOWN)
        self.play(FadeIn(text_tsp_to_vrp))
        self.pause()
        self.play(*[FadeIn(dot) for dot in dots])
        self.pause()
        # example of path between the nodes
        ordering = [0, 1, 4, 5, 8, 6, 7, 3, 2]
        arrows = [Arrow(dots[i], dots[j], color=BLUE) for i, j in zip(ordering, ordering[1:] + [0])]
        arrows_animations = [GrowArrow(arrow) for arrow in arrows]
        self.play(AnimationGroup(*arrows_animations, lag_ratio=.2))
        self.pause()
        # remove the path and add new path for 2 vehicles
        ordering_1 = [0, 1, 4, 5, 2]
        ordering_2 = [0, 3, 7, 6, 8]
        self.play(AnimationGroup(*[FadeOut(arrow) for arrow in arrows]))
        arrows_1 = [Arrow(dots[i], dots[j], color=PURPLE) for i, j in zip(ordering_1, ordering_1[1:] + [0])]
        arrows_2 = [Arrow(dots[i], dots[j], color=TEAL) for i, j in zip(ordering_2, ordering_2[1:] + [0])]
        self.play(AnimationGroup(*[GrowArrow(arrow) for arrow in arrows_1], lag_ratio=.2))
        self.play(AnimationGroup(*[GrowArrow(arrow) for arrow in arrows_2], lag_ratio=.2))
        self.pause()

        # add time window on top of nodes: values between [0..99]
        tws = [
            [0, 99],
            [5, 15],
            [80, 99],
            [0, 30],
            [25, 60],
            [70, 80],
            [60, 70],
            [40, 50],
            [60, 99],
        ]
        # a time window is simply a red rectangle for the invalid time, a green for the valid time and a red again
        tw_animation_list = []
        tw_group_list = []
        height = 0.1
        for i, dot in enumerate(dots):
            tw = tws[i]
            lengths = ([0] + tw + [99])
            l = [(j-i)/100 for i, j in zip(lengths, lengths[1:])]
            before = Rectangle(color=RED, fill_opacity=1, width=l[0], height=height, stroke_width=0)
            during = Rectangle(color=GREEN, fill_opacity=1, width=l[1], height=height, stroke_width=0)
            after = Rectangle(color=RED, fill_opacity=1, width=l[2], height=height, stroke_width=0)
            group = VGroup(before, during, after).arrange(RIGHT, buff=0).next_to(dot, UP)
            tw_group_list.append(group)
            animation = GrowFromPoint(group, dot)
            tw_animation_list.append(animation)
        self.play(AnimationGroup(*tw_animation_list))
        self.pause()
        self.play(AnimationGroup(*[ShrinkToCenter(tw) for tw in tw_group_list]))
        self.pause()


        # transform the nodes into arrows pointing upwards or downwards, if pickup or drop
        self.play(AnimationGroup(*[FadeOut(dot) for dot in dots[1:]]))
        pickups = [1, 4, 3, 6]
        drops = [2, 5, 7, 8]
        request_colors = [GREEN, BLUE, RED, GOLD]
        images_height = height * 4
        pickup_img = [
            ImageMobject("res/restaurant_red.png").scale_to_fit_height(images_height),
            ImageMobject("res/restaurant_green.png").scale_to_fit_height(images_height),
            ImageMobject("res/restaurant_blue.png").scale_to_fit_height(images_height),
            ImageMobject("res/restaurant_gold.png").scale_to_fit_height(images_height),
        ]
        drop_img = [
            ImageMobject("res/house_red.png").scale_to_fit_height(images_height),
            ImageMobject("res/house_green.png").scale_to_fit_height(images_height),
            ImageMobject("res/house_blue.png").scale_to_fit_height(images_height),
            ImageMobject("res/house_gold.png").scale_to_fit_height(images_height),
        ]
        for i, pickup in enumerate(pickups):
            img = pickup_img[i]
            img.move_to(dots[pickup])
        for i, drop in enumerate(drops):
            img = drop_img[i]
            img.move_to(dots[drop])
        self.play(AnimationGroup(*[FadeIn(img) for img in pickup_img + drop_img]))

        self.pause()
        self.play(AnimationGroup(*[FadeOut(img) for img in pickup_img + drop_img]))
        self.play(AnimationGroup(*[FadeIn(dot) for dot in dots[1:]]))
        self.pause()

        # successor model
        # remove arrows
        self.play(AnimationGroup(*[FadeOut(arrow) for arrow in arrows_1 + arrows_2]))
        self.play(FadeIn(text_successor))
        self.pause()
        bounding_boxes = [
            SurroundingRectangle(dots[0], color=BLUE),
            SurroundingRectangle(dots[1], color=GREEN),
            SurroundingRectangle(dots[2], color=GREEN),
            SurroundingRectangle(dots[3], color=GREEN),
        ]
        self.play(AnimationGroup(*[Create(box) for box in bounding_boxes], lag_ratio=0.2))
        self.wait(1)
        successor_candidates = [
            DashedArrow(start=dots[0], end=dots[1], dashed_ratio=0.4, dash_length=0.15),
            DashedArrow(start=dots[0], end=dots[2], dashed_ratio=0.4, dash_length=0.15),
            DashedArrow(start=dots[0], end=dots[3], dashed_ratio=0.4, dash_length=0.15),
        ]
        self.play(AnimationGroup(*[GrowArrow(arrow) for arrow in successor_candidates], lag_ratio=.2))
        self.pause()
        self.play(AnimationGroup(*[successor_candidates[1].animate.set_color(RED), successor_candidates[2].animate.set_color(RED)]))
        self.pause()
        self.play(AnimationGroup(*([FadeOut(successor_candidates[1]), FadeOut(successor_candidates[2])] + [FadeOut(box) for box in bounding_boxes])))
        correct_succ = Arrow(dots[0], dots[1])
        self.play(AnimationGroup(*[FadeIn(correct_succ), correct_succ.animate.set_color(BLUE)]))
        self.play(FadeOut(successor_candidates[0]))
        self.pause()
        self.wait()

        # drawbacks of the successor model
        self.play(AnimationGroup(*[FadeOut(text_tsp_to_vrp), FadeOut(correct_succ)]))
        self.play(text_successor.animate.to_corner(UP + LEFT))
        blist1 = Tex("1. Prevent insertions heuristics")
        annex_1 = Tex(r"$\rightarrow$ Some kind of LNS")
        blist2 = Tex("2. Represent optional visits")
        annex_2 = Tex(r"$\rightarrow$ Fake vehicle")
        successor_group = VGroup(text_successor,
                                 VGroup(blist1, annex_1).arrange(RIGHT),
                                 VGroup(blist2, annex_2).arrange(RIGHT)
                                 ).arrange(DOWN, center=False, aligned_edge=LEFT)
        self.pause()
        # drawback 1: insertion heuristics
        self.play(FadeIn(blist1))
        partial_ordering = [0, 1, 4, 5, 2]
        partial_route = [Arrow(dots[i], dots[j], color=BLUE) for i, j in zip(partial_ordering, partial_ordering[1:] + [0])]
        self.play(AnimationGroup(*[GrowArrow(arrow) for arrow in partial_route], lag_ratio=.2))
        self.pause()
        self.play(FadeOut(partial_route[3]))
        partial_route.remove(partial_route[3])
        detour = [Arrow(dots[5], dots[8], color=BLUE), Arrow(dots[8], dots[2], color=BLUE)]
        self.play(AnimationGroup(*[GrowArrow(detour[0]), GrowArrow(detour[1])], lag_ratio=.2))
        self.play(FadeIn(annex_1))
        self.pause()
        # drawback 2: exclusion
        self.play(AnimationGroup(*[FadeOut(arrow) for arrow in partial_route + detour]))
        optional = [8, 6, 7, 3]
        self.play(AnimationGroup(*[dots[i].animate.set_color(ORANGE) for i in optional]))
        self.play(FadeIn(blist2))
        center = (sum(dots[i].get_x() for i in optional) / len(optional), sum(dots[i].get_y() for i in optional) / len(optional), 0)
        question_mark = Text("?", color=ORANGE).move_to(center)
        self.play(Write(question_mark))
        self.pause()
        visited = [0, 1, 4, 5, 8, 2]
        excluded = [6, 7, 3]
        visited_arrows = [Arrow(dots[i], dots[j], color=BLUE) for i, j in zip(visited, visited[1:] + [0])]
        excluded_arrows = [Arrow(dots[i], dots[j], color=RED) for i, j in zip(excluded, excluded[1:] + [excluded[0]])]
        self.play(FadeOut(question_mark))
        self.play(AnimationGroup(*([dots[i].animate.set_color(RED) for i in excluded] + [dots[i].animate.set_color(WHITE) for i in optional if i not in excluded])))
        self.play(AnimationGroup(*[GrowArrow(arrow) for arrow in visited_arrows], lag_ratio=.2))
        self.play(AnimationGroup(*[GrowArrow(arrow) for arrow in excluded_arrows], lag_ratio=.2))
        self.play(FadeIn(annex_2))
        self.pause()
        self.wait()


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

