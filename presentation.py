import numpy as np
from manim import *
from manim_presentation import Slide
import re
import random

MEMBER = GREEN
POSSIBLE = BLUE
EXCLUDED = RED
REQUIRED = GOLD
BG = BLACK
FG = WHITE
TITLE_BUF = 0.5  # length between title and first text under it
TABLE_HIGHLIGHT = GREEN

config.background_color = BG

class DashedArrow(Arrow, DashedLine):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Presentation(Slide):

    def construct(self):

        # ==============================
        # SLIDE MainTitle
        # ==============================

        # title of paper + blablabla
        scale_title = 1.2
        scale_name = 0.7
        scale_description = 0.5
        text_paper_1 = Text("Sequence Variables", color=BLUE).scale(scale_title)
        text_paper_2 = Text("for Routing Problems", color=BLUE).scale(scale_title)
        text_paper = VGroup(text_paper_1, text_paper_2).arrange(DOWN).to_corner(UP)
        text_author_1 = Text("Augustin Delecluse").scale(scale_name)
        text_description_1 = Text("TRAIL, ICTEAM, UCLouvain, Louvain-la-Neuve, Belgium", slant=ITALIC).scale(scale_description)
        text_author_2 = Text("Pierre Schaus").scale(scale_name)
        text_description_2 = Text("ICTEAM, UCLouvain, Louvain-la-Neuve, Belgium", slant=ITALIC).scale(scale_description)
        text_author_3 = Text("Pascal Van Hentenryck").scale(scale_name)
        text_description_3 = Text("Georgia Institute of Technology, Atlanta, GA, USA", slant=ITALIC).scale(scale_description)

        logo_trail = ImageMobject("res/trail.png").scale_to_fit_height(1)
        logo_uclouvain = ImageMobject("res/640px-UCLouvain_logo.svg.png").scale_to_fit_height(1)
        logo_georgia_tech = ImageMobject("res/georgia_tech.png").scale_to_fit_height(1)
        logos_group = Group(logo_uclouvain, logo_trail, logo_georgia_tech).arrange(RIGHT)
        layout = VGroup(text_author_1, text_description_1,
                        text_author_2, text_description_2,
                        text_author_3, text_description_3,
                        ).arrange(DOWN).next_to(text_paper, DOWN, buff=TITLE_BUF)
        logos_group.to_corner(DOWN, buff=0.1)
        #background_logos = Rectangle(width=14.2, height=1.6, fill_color=BLUE,
        #                             fill_opacity=1, stroke_opacity=0).to_corner(DOWN, buff=0).set_sheen(-1, UP)
        background_logos = Rectangle(width=14.2, height=1.15, fill_color=WHITE,
                                     fill_opacity=1, stroke_opacity=0).to_corner(DOWN, buff=0)

        self.add(logos_group)
        self.add(text_paper)
        self.add(layout)
        self.bring_to_back(background_logos)
        self.wait()
        self.pause()
        self.clear()



        # ==============================
        # SLIDE VRPIntro
        # ==============================

        # introduction
        text_tsp_to_vrp = MarkupText(
            f"From <span fgcolor='{BLUE}'>TSP</span>\nto Vehicle Routing Problems (<span fgcolor='{BLUE}'>VRP</span>)")
        text_successor = MarkupText("Successor model", color=BLUE)
        text_group = VGroup(text_tsp_to_vrp, text_successor).arrange(DOWN, center=False, aligned_edge=LEFT).to_corner(
            UP + LEFT)
        coords = [
            np.array([-4.25, 0.75, 0]),
            np.array([-1.75, 2.75, 0]),
            np.array([-1.25, 1.25, 0]),
            np.array([-1, -0.5, 0]),
            np.array([2, 2.5, 0]),
            np.array([1.75, 1, 0]),
            np.array([3.25, -0.75, 0]),
            np.array([2.5, -1.75, 0]),
            np.array([1.5, 0, 0]),
        ]
        dots = [Dot(i) for i in coords]
        dot_group = VGroup(*dots)
        VGroup(text_group, dot_group).arrange(DOWN, buff=.5)
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
        # transform node 0 to become a depot
        depot = Square(side_length=dots[0].radius * 1.5).rotate(PI / 4).set_fill(FG, opacity=1.0).move_to(
            dots[0].get_center())
        self.play(Transform(dots[0], depot))
        text_depot = Text("Depot").scale(.7).next_to(depot, LEFT)
        self.play(FadeIn(text_depot))
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
            l = [(j - i) / 100 for i, j in zip(lengths, lengths[1:])]
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
        self.play(AnimationGroup(*(
                    [FadeOut(img) for img in pickup_img + drop_img] + [FadeIn(dot) for dot in dots[1:]] + [
                FadeOut(text_depot)])))
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
        self.play(AnimationGroup(*[FadeOut(box) for box in bounding_boxes], lag_ratio=0.2))
        self.pause()
        self.play(AnimationGroup(
            *[successor_candidates[1].animate.set_color(RED), successor_candidates[2].animate.set_color(RED)]))
        self.pause()
        self.play(AnimationGroup(*([FadeOut(successor_candidates[1]), FadeOut(successor_candidates[2])])))
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
        group_succ_1 = VGroup(VGroup(blist1, annex_1).arrange(RIGHT),
                                 VGroup(blist2, annex_2).arrange(RIGHT)
                                 ).arrange(DOWN, center=False, aligned_edge=LEFT)
        successor_group = VGroup(text_successor, group_succ_1).arrange(DOWN, center=False, aligned_edge=LEFT, buff=TITLE_BUF)
        self.pause()

        # drawback 1: insertion heuristics
        self.play(FadeIn(blist1))
        partial_ordering = [0, 1, 4, 5, 2]
        partial_route = [Arrow(dots[i], dots[j], color=BLUE) for i, j in
                         zip(partial_ordering, partial_ordering[1:] + [0])]
        self.play(AnimationGroup(*[GrowArrow(arrow) for arrow in partial_route], lag_ratio=.2))
        box = SurroundingRectangle(dots[8])
        self.play(Create(box))
        self.pause()
        self.play(FadeOut(partial_route[3]))
        partial_route.remove(partial_route[3])
        detour = [Arrow(dots[5], dots[8], color=BLUE), Arrow(dots[8], dots[2], color=BLUE)]
        self.play(AnimationGroup(*[GrowArrow(detour[0]), GrowArrow(detour[1])], lag_ratio=.2))
        self.play(FadeIn(annex_1))
        self.play(Uncreate(box))
        self.pause()

        # drawback 2: optional nodes
        self.play(AnimationGroup(*[FadeOut(arrow) for arrow in partial_route + detour]))
        optional = [8, 6, 7, 3]
        optional_circles = [Circle(radius=dots[0].radius, color=ORANGE).move_to(dots[i].get_center()) for i in optional]
        # transform optional nodes into circles
        # self.play(AnimationGroup(*[dots[i].animate.set_color(ORANGE) for i in optional]))
        self.play(AnimationGroup(*[Transform(dots[i], optional_circles[j]) for j, i in enumerate(optional)]))
        self.play(FadeIn(blist2))
        center = (
        sum(dots[i].get_x() for i in optional) / len(optional), sum(dots[i].get_y() for i in optional) / len(optional),
        0)
        question_mark = Text("?", color=ORANGE).move_to(center)
        self.play(Write(question_mark))
        self.pause()
        visited = [0, 1, 4, 5, 8, 2]
        excluded = [6, 7, 3]
        visited_arrows = [Arrow(dots[i], dots[j], color=BLUE) for i, j in zip(visited, visited[1:] + [0])]
        excluded_arrows = [Arrow(dots[i], dots[j], color=RED) for i, j in zip(excluded, excluded[1:] + [excluded[0]])]
        self.play(FadeOut(question_mark))
        # self.play(FadeOut(optional_circles[0]))
        self.play(Transform(dots[8], Dot(dots[8].get_center())))
        # self.play(AnimationGroup(*([dots[i].animate.set_color(RED) for i in excluded] + [dots[i].animate.set_color(FOREGROUND) for i in optional if i not in excluded])))
        self.play(AnimationGroup(*[GrowArrow(arrow) for arrow in visited_arrows], lag_ratio=.2))
        self.play(AnimationGroup(*[GrowArrow(arrow) for arrow in excluded_arrows], lag_ratio=.2))
        self.play(FadeIn(annex_2))
        self.pause()
        self.clear()



        # ==============================
        # SLIDE SequenceOtherWork
        # ==============================

        text_interval = Text("Interval Sequence Variables", color=BLUE)
        text_scale = .7
        text_cplex = Tex(r"$\vartriangleright$ Available in CP Optimizer ", "(CPLEX) ", "and ",
                         "Google OR-Tools").scale(text_scale).set_color_by_tex('CPLEX', BLUE).set_color_by_tex('Google',
                                                                                                               BLUE)
        # text_nodes_representation = Tex(r"$\vartriangleright$ Nodes = ", "Interval Variables", "space", "ordered through a ", "Sequence Variable").scale(text_scale).set_color_by_tex('Interval', BLUE).set_color_by_tex("space", BACKGROUND)
        # text_sequence = Tex().scale(text_scale).set_color_by_tex('Sequence', BLUE)
        # group_nodes_description = VGroup(text_nodes_representation, text_sequence).arrange(DOWN, center=False, aligned_edge=RIGHT)
        text_nodes_representation = Tex(r"$\vartriangleright$ Nodes = ", "Interval Variables ", "ordered through a ",
                                        "Sequence Variable").scale(text_scale).set_color_by_tex('Interval', BLUE)
        group_nodes_description = VGroup(text_nodes_representation).arrange(DOWN, center=False, aligned_edge=RIGHT)
        text_head_tail = Tex(r"$\vartriangleright$ Head-tail structure").scale(text_scale)
        text_group_1 = VGroup(text_cplex, group_nodes_description, text_head_tail).arrange(DOWN, center=False, aligned_edge=LEFT)
        text_group = VGroup(text_interval, text_group_1).arrange(DOWN, center=False, aligned_edge=LEFT, buff=TITLE_BUF).to_corner(
            UP + LEFT)
        coords = [
            np.array([0, 0, 0]),  # head
            np.array([0.5, 0, 0]),
            np.array([1, 0, 0]),  # last head

            np.array([2, 1, 0]),
            np.array([2.5, -0.25, 0]),
            np.array([3, .75, 0]),
            np.array([3.25, 0.25, 0]),
            np.array([3.75, 0.8, 0]),
            np.array([4.1, -0.1, 0]),
            np.array([4.5, 0.6, 0]),
            np.array([5, -0.2, 0]),
            np.array([5.25, 0.6, 0]),
            np.array([5.5, -.5, 0]),

            np.array([6.5, 0, 0]),  # last tail
            np.array([7, 0, 0]),
            np.array([7.5, 0, 0]),
            np.array([8, 0, 0]),  # tail
        ]
        circle_list = [0, 1, 4, 6, 7, 10, 11, 12, 14]
        dot_list = [i for i in range(len(coords)) if i not in circle_list]
        dots = [Dot(coords[i]) for i in circle_list]
        circles = [Circle(radius=dots[0].radius, color=FG).move_to(coords[i]) for i in dot_list]
        points_list = dots + circles
        y_coord = -1
        limit_length = 2.25
        head_color = BLUE
        head_cand_color = BLUE
        tail_color = GREEN
        tail_cand_color = GREEN
        head_start = [0, y_coord, 0]
        head_end = [1.25, y_coord, 0]
        arrow_head = Arrow(start=head_start, end=head_end, max_tip_length_to_length_ratio=.1, buff=0, color=head_color)
        head_limit = DashedLine(start=head_end, end=head_end + np.array([0, limit_length, 0]), color=head_color)
        tail_start = [8, y_coord, 0]
        tail_end = [6.25, y_coord, 0]
        arrow_tail = Arrow(start=tail_start, end=tail_end, max_tip_length_to_length_ratio=.1, buff=0, color=tail_color)
        tail_limit = DashedLine(start=tail_end, end=tail_end + np.array([0, limit_length, 0]), color=tail_color)
        text_head = MarkupText("Head", color=head_color).scale(.5).next_to(arrow_head, DOWN)
        text_tail = MarkupText("Tail", color=tail_color).scale(.5).next_to(arrow_tail, DOWN)
        text_not_sequenced = MarkupText("Not Sequenced").scale(.5).set_y(text_tail.get_y()).set_x(3.75)
        candidates_head = Ellipse(height=3, width=2, color=head_cand_color).rotate(-PI / 4).move_to(
            np.array([3.5, 0.25, 0]))  # head candidates
        candidates_tail = Ellipse(height=2.5, width=2, color=tail_cand_color).rotate(3 * PI / 8).move_to(
            np.array([4, 0.25, 0]))  # tail candidates
        text_candidates_head = MarkupText("Candidates Head", color=head_cand_color).scale(.5).move_to(
            np.array([2.2, 1.75, 0]))
        text_candidates_tail = MarkupText("Candidates Tail", color=tail_cand_color).scale(.5).move_to(
            np.array([5.3, 1.75, 0]))

        figure_list = points_list + \
                      [arrow_head, text_head, head_limit] + \
                      [arrow_tail, text_tail, tail_limit] + \
                      [candidates_head, text_candidates_head] + \
                      [candidates_tail, text_candidates_tail] + \
                      [text_not_sequenced]
        figures = VGroup(*figure_list).next_to(text_group, DOWN, buff=0.5).set_x(ORIGIN[0])
        text_pros_cons = MarkupText(
            f"<span fgcolor='{GREEN}'>OK</span> optional visits\n<span fgcolor='{RED}'>KO</span> cannot insert anywhere in the sequence").scale(
            .45)
        text_pros_cons.next_to(figures, DOWN).to_corner(LEFT)

        self.play(FadeIn(text_group))
        self.pause()

        self.play(AnimationGroup(*([FadeIn(c) for c in circles + dots])))
        self.pause()
        self.play(
            AnimationGroup(*[GrowArrow(arrow_head), FadeIn(text_head), GrowFromPoint(head_limit, arrow_head.get_end())],
                           lag_ratio=.3))
        self.play(
            AnimationGroup(*[GrowArrow(arrow_tail), FadeIn(text_tail), GrowFromPoint(tail_limit, arrow_tail.get_end())],
                           lag_ratio=.3))
        self.play(FadeIn(text_not_sequenced))
        self.pause()
        self.play(Create(candidates_head))
        self.play(FadeIn(text_candidates_head))
        self.play(Create(candidates_tail))
        self.play(FadeIn(text_candidates_tail))
        self.pause()
        self.play(FadeIn(text_pros_cons))
        self.pause()
        self.clear()



        # ==============================
        # SLIDE Sequences
        # ==============================

        text_contribution = Text("Our contribution", color=BLUE)

        text_sequence = Text("Sequence Variable", color=BLUE).to_corner(UP + LEFT)
        text_data_structure = Text("data structures", color=BLUE).next_to(text_sequence, RIGHT).to_corner(UP)
        insert_table = MathTable(
            [["Partial Sequence", "Operation"],
             [r"\alpha \rightarrow \omega", "Initialization"],
             [r"\alpha \rightarrow 1 \rightarrow \omega", r"Insert(\alpha, 1)"],
             [r"\alpha \rightarrow 1 \rightarrow 4 \rightarrow \omega", r"Insert(1, 4)"],
             [r"\alpha \rightarrow 5 \rightarrow 1 \rightarrow 4 \rightarrow \omega", r"Insert(\alpha, 5)"]
             ],
            include_outer_lines=False).next_to(text_sequence, DOWN, buff=TITLE_BUF).set_x(ORIGIN[0])
        for i, o in enumerate(insert_table.get_horizontal_lines()):
            if i == 0:
                o.set_color(BLUE)
            else:
                insert_table.remove(o)

        for i, o in enumerate(insert_table.get_vertical_lines()):
            o.set_color(BLUE)

        # coordinates for the dots
        coords = [
            np.array([-4.25, 0.75, 0]),  # alpha
            np.array([-1.75, 2.75, 0]),
            np.array([-1.25, 1.25, 0]),
            np.array([-1, -0.5, 0]),
            np.array([-4, -1.5, 0]),  # last member (omega)
            np.array([2, 2.5, 0]),
            np.array([1.75, 1, 0]),
            np.array([3.25, -0.75, 0]),  # last possible
            np.array([2.5, -2, 0]),
            np.array([3.5, 1.5, 0]),
        ]
        # draw the dots
        dots = [Dot(i, radius=0.16) for i in coords]
        # partition of the nodes
        members = [0, 1, 2, 3, 4]
        possible = [5, 6, 7]
        insertions = {
            5: [0, 1, 2, 3],
            6: [1, 2, 3, 5],
            7: [2, 3, 5, 6],
        }
        excluded = [8, 9]

        members_group = VGroup(*[dots[i] for i in members])
        excluded_group = VGroup(*[dots[i] for i in excluded])
        possible_group = VGroup(*[dots[i] for i in possible])
        text_first = Tex(r"$\alpha$", color=MEMBER).next_to(dots[0], LEFT, buff=0.1)
        text_last = Tex(r"$\omega$", color=MEMBER).next_to(dots[4], LEFT, buff=0.1)
        text_member = Text("members (S)", color=MEMBER).scale(0.5)
        text_possible = Text("possible (P)", color=POSSIBLE).scale(0.5)
        text_excluded = Text("excluded (E)", color=EXCLUDED).scale(0.5)
        all_dots = VGroup(*dots).next_to(text_sequence, DOWN, buff=.5).set_x(ORIGIN[0])
        description_group = VGroup(text_member, text_possible, text_excluded).arrange(RIGHT, buff=1).next_to(all_dots,
                                                                                                             DOWN)

        # ordering for the members
        successors = [Arrow(i.get_center(), j.get_center(), color=MEMBER) for i, j in
                      zip(members_group, members_group[1:])]
        # successors_group = VGroup(*successors)
        animations = [GrowArrow(succ) for succ in successors]

        # predecessors for the nodes
        insertions_arrows = {
            node:
                [DashedArrow(start=dots[pred].get_center(), end=dots[node].get_center(), dashed_ratio=0.4,
                             dash_length=0.15, color=FG) for pred in v]
            for node, v in insertions.items()
        }
        # make the arrows grow
        arrows_list = [arrow for k, v in insertions_arrows.items() for arrow in v]
        random.shuffle(arrows_list)
        grow_insertions = [GrowArrow(arrow) for arrow in arrows_list]

        # initial title, table of operations
        self.play(FadeIn(text_contribution))
        self.pause()
        self.play(FadeOut(text_contribution))
        self.play(FadeIn(text_sequence))
        self.play(FadeIn(insert_table))
        self.wait()
        self.pause()
        self.play(FadeOut(insert_table))
        # and the dots appear
        self.play(*[FadeIn(dot) for dot in dots])
        self.pause()
        # simply shows the text first and last node, arrows between them and explains nothing else
        temporary_arrow = Arrow(dots[0], dots[4], color=MEMBER)
        self.play(AnimationGroup(*[dots[i].animate.set_color(MEMBER) for i in [0, 4]]))
        self.play(AnimationGroup(*[FadeIn(text_first), FadeIn(text_last), GrowArrow(temporary_arrow)], lag_ratio=0.2))
        self.pause()
        self.play(FadeOut(temporary_arrow))
        # nodes that will be set as members
        self.play(members_group.animate.set_color(MEMBER))
        #self.play(AnimationGroup(*[FadeIn(text_first), FadeIn(text_last), FadeIn(text_member)]))
        self.play(FadeIn(text_member))
        self.pause()
        self.play(AnimationGroup(*animations, lag_ratio=0.25))
        self.pause()
        # excluded nodes
        self.play(excluded_group.animate.set_color(EXCLUDED))
        self.play(FadeIn(text_excluded))
        self.pause()
        # possible nodes
        self.play(possible_group.animate.set_color(POSSIBLE))
        self.play(FadeIn(text_possible))
        self.pause()
        # show the insertions
        self.play(AnimationGroup(*grow_insertions, lag_ratio=0.2))
        self.pause()
        # show an exclusion of a possible node (node 5)
        n = 5
        self.play(Indicate(dots[n], color=EXCLUDED))
        self.wait()
        arrows_changed = [insertions_arrows[node][i] for node, v in insertions.items() for i, pred in enumerate(v) if
                          pred == n or node == n]
        self.play(dots[n].animate.set_color(EXCLUDED))
        self.play(AnimationGroup(*([FadeOut(arrow) for arrow in arrows_changed])))
        self.pause()
        # revert to previous state
        self.play(AnimationGroup(*([FadeIn(arrow) for arrow in arrows_changed])))
        self.play(dots[n].animate.set_color(POSSIBLE))
        self.pause()
        # show the insertion of a possible node (node 5 after node 1)
        p = 1
        arrows_changed = [insertions_arrows[n][i] for i, pred in enumerate(insertions[n]) if pred != p]
        arrow_selected = [arrow for arrow in insertions_arrows[n] if arrow not in arrows_changed][0]
        arrow_detour_added = Arrow(start=dots[n], end=dots[2], color=MEMBER)
        arrow_detour_removed = successors[1]
        self.play(Indicate(dots[n], color=MEMBER))
        self.wait()
        self.play(dots[n].animate.set_color(MEMBER))
        self.play(AnimationGroup(*[FadeOut(arrow) for arrow in arrows_changed]))
        # change the arrow for the insertion
        arrow_selected.save_state()
        arrow_detour_removed.save_state()
        self.play(AnimationGroup(*[
            Transform(arrow_selected, Arrow(start=dots[p], end=dots[n], color=MEMBER)),
            FadeOut(arrow_detour_removed),
            GrowArrow(arrow_detour_added)
        ]))
        self.pause()
        # undo the insertion
        self.play(AnimationGroup(*[Restore(arrow_selected), Restore(arrow_detour_removed), FadeOut(arrow_detour_added),
                                   dots[n].animate.set_color(POSSIBLE)]))
        self.pause()
        self.wait()

        # present the data structures
        # unzoom the sequence to make place for the data structures
        nodes_labels = [
            text_first,
            Tex(r"$a$", color=MEMBER).next_to(dots[1], LEFT),
            Tex(r"$b$", color=MEMBER).next_to(dots[2], LEFT),
            Tex(r"$c$", color=MEMBER).next_to(dots[3], LEFT),
            text_last,
            Tex(r"$d$", color=POSSIBLE).next_to(dots[5], RIGHT),
            Tex(r"$e$", color=POSSIBLE).next_to(dots[6], RIGHT),
            Tex(r"$f$", color=POSSIBLE).next_to(dots[7], RIGHT),
            Tex(r"$g$", color=EXCLUDED).next_to(dots[8], RIGHT),
            Tex(r"$h$", color=EXCLUDED).next_to(dots[9], RIGHT),
        ]
        labels_group = VGroup(*nodes_labels)
        full_schema = VGroup(all_dots, *[arrow for n, v in insertions_arrows.items() for arrow in v],
                             description_group, *successors, labels_group)
        self.play(ScaleInPlace(full_schema, 0.8))
        self.play(AnimationGroup(*[full_schema.animate.to_corner(LEFT), FadeIn(text_data_structure)]))
        self.pause()
        # self.play(AnimationGroup(*[FadeIn(label) for label in nodes_labels if label not in [text_first, text_last]]))
        # table of insertions
        text_node = Tex("node $x$")
        text_insert = Tex("$I^x$")
        text_nsx = Tex("$n_s^x$")
        text_npx = Tex("$n_p^x$")
        header_buff = 0.4
        table_header_tiny = VGroup(text_node, text_insert).arrange(RIGHT, buff=header_buff)
        table_header_full = VGroup(table_header_tiny, text_nsx, text_npx).arrange(RIGHT, buff=header_buff)
        table_label = [
            Tex("$a$", color=MEMBER),
            Tex("$b$", color=MEMBER),
            Tex("$c$", color=MEMBER),
            Tex("$d$", color=POSSIBLE),
            Tex("$e$", color=POSSIBLE),
            Tex("$f$", color=POSSIBLE),
            Tex("$g$", color=EXCLUDED),
            Tex("$h$", color=EXCLUDED),
        ]
        table_insertions = [
            Tex("$\emptyset$"),
            Tex("$\emptyset$"),
            Tex("$\emptyset$"),
            MathTex(r"\{ {{ \alpha }}, {{ a }} , {{ b }} , {{ c }} \}"),
            MathTex("\{ {{ a }} , {{ b }} , {{ c }} , {{ d }} \}"),
            MathTex("\{ {{ b }} , {{ c }} , {{ d }} , {{ e }} \}"),
            Tex("$\emptyset$"),
            Tex("$\emptyset$"),
        ]
        table_nsx = [
            Tex("0", color=MEMBER),
            Tex("0", color=MEMBER),
            Tex("0", color=MEMBER),
            Tex("4", color=MEMBER),
            Tex("3", color=MEMBER),
            Tex("2", color=MEMBER),
            Tex("0", color=MEMBER),
            Tex("0", color=MEMBER),
        ]
        table_npx = [
            Tex("0", color=POSSIBLE),
            Tex("0", color=POSSIBLE),
            Tex("0", color=POSSIBLE),
            Tex("0", color=POSSIBLE),
            Tex("1", color=POSSIBLE),
            Tex("2", color=POSSIBLE),
            Tex("0", color=POSSIBLE),
            Tex("0", color=POSSIBLE),
        ]
        for c in [r'\alpha', 'a', 'b', 'c']:
            table_insertions[3].set_color_by_tex(c, MEMBER)
        for c in ['a', 'b', 'c']:
            table_insertions[4].set_color_by_tex(c, MEMBER)
        for c in ['d']:
            table_insertions[4].set_color_by_tex(c, POSSIBLE)
        for c in ['b', 'c']:
            table_insertions[5].set_color_by_tex(c, MEMBER)
        for c in ['d', 'e']:
            table_insertions[5].set_color_by_tex(c, POSSIBLE)

        table_shift = np.array([8, -1, 0])
        t0 = MobjectTable([
            [text_node.copy(), text_insert.copy()],
            *[[table_label[i].copy(), table_insertions[i].copy()] for i in range(3)]
        ], v_buff=0.1, h_buff=0.2).to_corner(UP + LEFT).shift(table_shift)
        t0.remove(*[o for i, o in enumerate(t0.get_vertical_lines()) if i != 0])
        t0.remove(*[o for i, o in enumerate(t0.get_horizontal_lines()) if i != 0])
        t1, t2 = [MobjectTable([
            [text_node.copy(), text_insert.copy(), text_nsx.copy(), text_npx.copy()],
            *[[table_label[i].copy(), table_insertions[i].copy(), table_nsx[i].copy(), table_npx[i].copy()] for i in
              range(j)]
        ], v_buff=0.1, h_buff=0.2).to_corner(UP + LEFT).shift(table_shift) for j in [6, len(table_npx)]]
        for t in t1, t2:
            t.remove(*[o for i, o in enumerate(t.get_vertical_lines()) if i != 0])
            t.remove(*[o for i, o in enumerate(t.get_horizontal_lines()) if i != 0]) \
                # self.play(AnimationGroup(*[FadeIn(text_node), FadeIn(text_insert), GrowFromPoint(header_line_tiny, header_line_tiny.get_start())]))
        self.play(Create(t0))
        self.wait()
        self.pause()
        self.play(Transform(t0, t1))
        self.wait()
        self.pause()
        # show insertions for node 6
        surrounding_rectangle_node_6 = SurroundingRectangle(dots[6])
        self.play(Create(surrounding_rectangle_node_6))
        # show member insertions
        self.play(AnimationGroup(
            *[Indicate(insertions_arrows[6][j], color=MEMBER, run_time=2) for j, pred in enumerate(insertions[6]) if
              pred in members]))
        surrounding_rectangle_1 = SurroundingRectangle(t2.get_cell((6, 3)), buff=0)
        self.play(Create(surrounding_rectangle_1))
        self.wait()
        self.pause()
        self.play(FadeOut(surrounding_rectangle_1))

        # show possible insertions
        self.play(AnimationGroup(
            *[Indicate(insertions_arrows[6][j], color=POSSIBLE) for j, pred in enumerate(insertions[6]) if
              pred in possible]))
        surrounding_rectangle_2 = SurroundingRectangle(t2.get_cell((6, 4)), buff=0)
        self.play(Create(surrounding_rectangle_2))
        self.wait()
        self.pause()
        self.play(AnimationGroup(*[Uncreate(surrounding_rectangle_node_6), FadeOut(surrounding_rectangle_2)]))
        self.play(FadeIn(t2))
        self.play(FadeOut(t1))
        self.pause()

        for i, (item, description) in enumerate([(t2.get_columns()[1], "sparse sets"),
                                                 (t2.get_columns()[2:4], "reversible\nintegers")]):
            highlight = SurroundingRectangle(item)
            text_description = Text(description, color=highlight.color).scale(0.5).next_to(highlight, DOWN)
            self.play(Create(highlight, lag_ratio=2))
            self.play(FadeIn(text_description))
            self.wait()
            self.pause()
            self.play(AnimationGroup(*[Uncreate(highlight), FadeOut(text_description)]))
            self.wait()
            self.pause()

        self.wait()
        # show successor array
        succ_array = MobjectTable([[MathTex("node"), MathTex("a"), MathTex("b"), MathTex("c"), MathTex("d"),
                                    MathTex("e"), MathTex("f"), MathTex("g"), MathTex("h"), MathTex(r"\alpha"), MathTex(r"\omega")],
                                   [MathTex("succ"), MathTex("b"), MathTex("c"), MathTex(r"\omega"), MathTex("d"),
                                    MathTex("e"), MathTex("f"), MathTex("g"), MathTex("h"), MathTex("a"), MathTex(r"\alpha")]
                                   ], h_buff=0.2, include_outer_lines=False).next_to(t2, DOWN)
        #succ_array = Table([['node', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'alpha', 'omega'],
        #                           ], h_buff=0.2, include_outer_lines=False).next_to(t2, DOWN)
        succ_array = MathTable([["node"] + [c for c in "abcdefgh"] + [r"\alpha", r"\omega"],
                                ["succ", "b", "c", r"\omega", "d", "e", "f", "g", "h", "a", r"\alpha"]],
                               h_buff=0.2, v_buff=0.1, include_outer_lines=False).next_to(t2, DOWN)
        for node in [0, 1, 2, 8, 9]:
            succ_array.add_highlighted_cell((1, node + 2), color=MEMBER)
            succ_array.add_highlighted_cell((2, node + 2), color=MEMBER)
        self.play(FadeIn(succ_array))
        self.wait()
        self.pause()
        # highlight differences with Charles Thomas's paper: required nodes
        text_required = Text("Required (R)", color=REQUIRED).scale(0.5).next_to(text_member, DOWN)
        # remove alpha and omega labels, add required label, change node 6 to required and remove npx and nsx
        cross_npx = Cross(t2.get_columns()[2:4])
        cross_first = Cross(text_first)
        cross_last = Cross(text_last)
        self.play(AnimationGroup(*[Create(cross_first), Create(cross_last), dots[6].animate.set_color(REQUIRED),
                                   nodes_labels[6].animate.set_color(REQUIRED), FadeIn(text_required), Create(cross_npx)]))

        self.pause()
        self.clear()



        # ==============================
        # SLIDE DomainConsistency
        # ==============================

        # domain consistency
        title = Text("Consistency of the domain", color=BLUE).to_corner(UP + LEFT)

        desc_scale = 0.8
        math_scale = 0.9
        math_tri_partition = MathTex(
            r"S \cup P \cup E = S \cap E =  P \cap E = \emptyset").scale(math_scale)
        text_tri_partition = Tex(r"$\bullet$ \hspace{2pt} Members (S), Possible (P), Excluded (E) nodes form a tri-partition").scale(desc_scale)
        tri_partition = VGroup(text_tri_partition, math_tri_partition).arrange(DOWN, center=False, aligned_edge=LEFT)

        math_excluded_not_pred = MathTex(
            r" p \in E \implies I^p = \emptyset \wedge \forall x: p \notin I^x").scale(math_scale)
        text_excluded_not_pred = Tex(r"$\bullet$ \hspace{2pt} An excluded element cannot be inserted nor be a predecessor").scale(desc_scale)
        excluded_not_pred = VGroup(text_excluded_not_pred, math_excluded_not_pred).arrange(DOWN, center=False,
                                                                                           aligned_edge=LEFT)

        math_member_not_insert = MathTex(r"p \in S \implies I^p = \emptyset").scale(math_scale)
        text_member_not_insert = Tex(r"$\bullet$ \hspace{2pt} A node in the sequence cannot be inserted (again)").scale(desc_scale)
        member_not_insert = VGroup(text_member_not_insert, math_member_not_insert).arrange(DOWN, center=False,
                                                                                           aligned_edge=LEFT)

        math_no_pred = MathTex(r" I^p = \emptyset \implies p \in S \vee p \in E").scale(math_scale)
        text_no_pred = Tex(r"$\bullet$ \hspace{2pt} An element without possible predecessor is excluded or in the sequence").scale(desc_scale)
        no_pred = VGroup(text_no_pred, math_no_pred).arrange(DOWN, center=False, aligned_edge=LEFT)

        layout = VGroup(tri_partition, excluded_not_pred, member_not_insert, no_pred) \
            .arrange(DOWN, center=False, aligned_edge=LEFT, buff=.5).next_to(title, DOWN, buff=TITLE_BUF).to_corner(LEFT)

        math_tri_partition.align_to(LEFT).shift(np.array([1, 0, 0]))
        math_excluded_not_pred.align_to(LEFT).shift(np.array([1, 0, 0]))
        math_member_not_insert.align_to(LEFT).shift(np.array([1, 0, 0]))
        math_no_pred.align_to(LEFT).shift(np.array([1, 0, 0]))
        self.play(FadeIn(title))
        self.pause()
        self.play(FadeIn(text_tri_partition))
        self.play(FadeIn(math_tri_partition))
        self.pause()
        self.play(FadeIn(text_excluded_not_pred))
        self.play(FadeIn(math_excluded_not_pred))
        self.pause()
        self.play(FadeIn(text_member_not_insert))
        self.play(FadeIn(math_member_not_insert))
        self.pause()
        self.play(FadeIn(text_no_pred))
        self.play(FadeIn(math_no_pred))
        self.pause()
        self.clear()
        # show the complexity
        complexity = Text("API and complexities", color=BLUE).to_corner(UP + LEFT)
        theta_p = MathTex(r"\Theta(|P|)")
        theta_1 = MathTex(r"\Theta(1)")
        table = MobjectTable([
            [Tex("Operation", color=BLUE), Tex("Description", color=BLUE), Tex("Complexity", color=BLUE)],
            [Tex("isBound(Sq)"), Tex("true iif $\mid P \mid = 0$"), theta_1.copy()],
            [Tex("is\{Member/Possible/Excluded\}(Sq, $x$)"), Tex("true iff $x \in \{S / P / E\}$"), theta_1.copy()],
            [Tex("get\{Member/Possible/Excluded\}(Sq, $x$)"), Tex("enumerates over $\{S / P / E\}$"),
             MathTex("\Theta(|\{S / P / E\}|)")],
            [Tex("succ(Sq, $x$)"), Tex("gives the successor of $x$"), theta_1.copy()],
            [Tex("pred(Sq, $x$)"), Tex("gives the predecessor of $x$"), theta_1.copy()],
            [Tex("insert(Sq, $p$, $x$)"), Tex("inserts $x$ after node $p$ in Sq"), theta_p.copy()],
            [Tex("exclude(Sq, $x$)"), Tex("excludes $x$ from Sq"), theta_p.copy()],
            [Tex("nMemberInserts(Sq, $x$)"), Tex("returns $n_s^x = \mid I^x \cap S \mid $"), theta_1.copy()],
            [Tex("nPossibleInserts(Sq, $x$)"), Tex("returns $n_p^x = \mid I^x \cap P \mid $"), theta_1.copy()],
            [Tex("getMemberInserts(Sq, $x$)"), Tex("enumerates over $I^x \cap S$"), MathTex("\Theta(\min(|I^x|, |S|))")],
            [Tex("getPossibleInserts(Sq, $x$)"), Tex("enumerates over $I^x \cap P$"), MathTex("\Theta(\min(|I^x|, |P|))")],
            [Tex("canInsert(Sq, $p$, $x$)"), Tex("true iff $p \in I^x$"), theta_1.copy()],
            [Tex("removeInsert(Sq, $p$, $x$)"), Tex("removes $p$ from $I^x$"), MathTex("\mathcal{O}(|P|)")],
        ], v_buff=0.1, h_buff=0.2).scale(0.65).next_to(complexity, DOWN).set_x(ORIGIN[0])

        #table.remove(*[o for i, o in enumerate(table.get_horizontal_lines()) if i != 0])
        notification = Text("Constraints notified by insertions, exclusion, removal of insertions", color=BLUE) \
            .scale(0.6).next_to(table, DOWN)
        # TODO color lines in the table
        for i, o in enumerate(table.get_horizontal_lines()):
            if i == 0:
                o.set_color(BLUE)
            else:
                table.remove(o)

        for i, o in enumerate(table.get_vertical_lines()):
            o.set_color(BLUE)
        self.play(FadeIn(complexity))
        self.play(FadeIn(table))
        self.pause()
        rows = table.get_rows()
        surrounding_insert = SurroundingRectangle(rows[6:8])
        surrounding_remove = SurroundingRectangle(rows[-1])
        self.play(Create(surrounding_insert))
        self.play(Create(surrounding_remove))
        self.wait()
        self.pause()
        self.play(FadeIn(notification))
        self.pause()
        self.clear()



        # ==============================
        # SLIDE TransitionTime
        # ==============================

        title = Text("Transition Time Constraint", color=BLUE)
        blist = BulletedList("Links with transition matrix, time windows, total transition time",
                             "Transitions must respect the time windows").scale(0.9)
        layout = VGroup(title, blist).arrange(DOWN, center=False, aligned_edge=LEFT, buff=2*TITLE_BUF).to_corner(UP + LEFT)
        formula_1 = MathTex(r"\text{\texttt{TransitionTimes}}(Sq, [start], [duration], [[trans]], transitionTime)").scale(0.9)
        formula_2 = MathTex(r"""\left\{ 
\overrightarrow{S} \in D(Sq) \left\vert 
\begin{matrix}
	\forall i, j \in \overrightarrow{S}, \text{if} \,\, i\,\,\text{precedes}\,\, j \implies 
	start_i + duration_i + trans_{i, j} \leq start_j \\ 
	\phantom{blabla} \\
	transitionTime = \sum_{i, j \in \overrightarrow{S} \; | \; i \xrightarrow{} j} trans_{i,j}
\end{matrix} 
\right.
\right\}""").scale(0.65)
        layout_formula = VGroup(formula_1, formula_2).arrange(DOWN, buff=2*TITLE_BUF).next_to(layout, DOWN, buff=2*TITLE_BUF).set_x(ORIGIN[0])
        filtering_step_1 = MarkupText(f"<span fgcolor='{BLUE}'>1) </span>Update the time windows").scale(0.6)
        filtering_step_2 = MarkupText(f"<span fgcolor='{BLUE}'>2) </span>Remove invalid insertions").scale(0.6)
        self.play(FadeIn(title))
        self.play(FadeIn(blist))
        self.pause()
        self.play(FadeIn(formula_1))
        self.play(FadeIn(formula_2))
        self.pause()

        # only keep the formula and present the algorithm
        self.play(AnimationGroup(*[FadeOut(formula_1), FadeOut(blist), FadeOut(title)]))
        self.play(formula_2.animate.to_corner(UP))
        test_cases_group = VGroup(filtering_step_1, filtering_step_2)\
            .arrange(RIGHT, center=False, buff=1)
        self.pause()
        test_cases_group.next_to(formula_2, DOWN).to_corner(LEFT)

        # setup for the drawing of the sequence
        # coordinates for the dots
        coords = [
            np.array([-4.25, 0.75, 0]),  # alpha
            np.array([-1.75, 2.75, 0]),
            np.array([-1.25, 1.25, 0]),
            np.array([-1, -0.5, 0]),
            np.array([-4, -1.5, 0]),  # last member
            np.array([2, 2.5, 0]),
            np.array([1.75, 1, 0]),
            np.array([3.25, -0.75, 0]),
            np.array([3.5, 1.5, 0]),  # last possible
            np.array([4, -0.2, 0]),
        ]
        # draw the dots
        dots = [Dot(i, radius=0.16) for i in coords]
        # partition of the nodes
        members = [0, 1, 2, 3, 4]
        possible = [5, 6, 7, 8]
        insertions = {
            5: [0, 1, 2, 3],
            6: [1, 2, 3, 5],
            7: [2, 3, 5, 6],
            8: [1],
        }
        excluded = [9]
        members_group = VGroup(*[dots[i] for i in members]).set_color(MEMBER)
        excluded_group = VGroup(*[dots[i] for i in excluded]).set_color(EXCLUDED)
        possible_group = VGroup(*[dots[i] for i in possible]).set_color(POSSIBLE)

        # ordering for the members
        successors = [Arrow(i.get_center(), j.get_center(), color=MEMBER) for i, j in
                      zip(members_group, members_group[1:])]

        # predecessors for the nodes
        insertions_arrows = {
            node:
                [DashedArrow(start=dots[pred].get_center(), end=dots[node].get_center(), dashed_ratio=0.4,
                             dash_length=0.15, color=FG) for pred in v]
            for node, v in insertions.items()
        }
        schema = VGroup(members_group, excluded_group, possible_group, *successors,
                        *[arrow for n, v in insertions_arrows.items() for arrow in v])\
            .next_to(test_cases_group, DOWN, buff=0.75)\
            .set_x(ORIGIN[0])
        # add time window on top of nodes: values between [0..99]
        tws = [
            [1, 99],
            [5, 99],
            [5, 99],
            [50, 99],
            [12, 98],  # last member
            [5, 45],  # case 1: too early starting from node 3
            [60, 87],  # case 2: cannot close starting from node 1
            [40, 95],
            [60, 99],  # case 3: too long
            [50, 67],
        ]
        # a time window is simply a red rectangle for the invalid time, a green for the valid time and a red again
        tw_animation_list = []
        tw_group_list = []
        height = 0.1
        tw_rectangles = []
        for i, dot in enumerate(dots):
            tw = tws[i]
            lengths = ([0] + tw + [99])
            l = [(j - i) / 100 for i, j in zip(lengths, lengths[1:])]
            before = Rectangle(color=RED, fill_opacity=1, width=l[0], height=height, stroke_width=0)
            during = Rectangle(color=GREEN, fill_opacity=1, width=l[1], height=height, stroke_width=0)
            after = Rectangle(color=RED, fill_opacity=1, width=l[2], height=height, stroke_width=0)
            tw_rectangles.append([before, during, after])
            group = VGroup(before, during, after).arrange(RIGHT, buff=0).next_to(dot, UP)
            tw_group_list.append(group)
            animation = GrowFromPoint(group, dot)
            tw_animation_list.append(animation)

        self.play(FadeIn(schema))
        self.play(AnimationGroup(*tw_animation_list))

        # time window update
        self.play(FadeIn(filtering_step_1))
        self.pause()
        # grow the "before" part from the sequence
        transitions = [10, 12, 13, 10]  # durations for the transitions, in integers
        start = tws[0][0]
        animations_tw_update = []
        for i, node in enumerate(members[1:]):
            start += transitions[i]
            if start > tws[node][0]:  # need to update the tw
                lengths = ([0] + tws[node] + [99])
                l = [(j - i) / 100 for i, j in zip(lengths, lengths[1:])]
                old_length = l[0]
                tws[node][0] = start
                lengths = ([0] + tws[node] + [99])
                l = [(j - i) / 100 for i, j in zip(lengths, lengths[1:])]
                diff = (l[0] - old_length) / 2
                old_before, old_during = tw_rectangles[node][0], tw_rectangles[node][1]
                new_before = Rectangle(color=RED, fill_opacity=1, width=l[0], height=height, stroke_width=0)\
                    .set_x(old_before.get_x() + diff).set_y(old_before.get_y())
                new_during = Rectangle(color=GREEN, fill_opacity=1, width=l[1], height=height, stroke_width=0)\
                    .set_x(old_during.get_x() + diff).set_y(old_during.get_y())
                animations_tw_update.append(AnimationGroup(*[Transform(old_before, new_before), Transform(old_during, new_during)]))

            else:
                start = tws[node][0]
        self.play(AnimationGroup(*animations_tw_update, lag_ratio=2))
        self.pause()

        # grow the "after" part from the sequence
        end = tws[4][1]
        animations_tw_update = []
        for i, node in enumerate(members[-2::-1]):  # iterate over from members[0]..members[-2] in reverse order
            end -= transitions[-i]
            if end < tws[node][1]:  # need to update the tw
                lengths = ([0] + tws[node] + [99])
                l = [(j - i) / 100 for i, j in zip(lengths, lengths[1:])]
                old_length = l[2]
                tws[node][1] = end
                lengths = ([0] + tws[node] + [99])
                l = [(j - i) / 100 for i, j in zip(lengths, lengths[1:])]
                diff = (l[2] - old_length) / 2
                old_after, old_during = tw_rectangles[node][2], tw_rectangles[node][1]
                new_after = Rectangle(color=RED, fill_opacity=1, width=l[2], height=height, stroke_width=0)\
                    .set_x(old_after.get_x() - diff).set_y(old_after.get_y())
                new_during = Rectangle(color=GREEN, fill_opacity=1, width=l[1], height=height, stroke_width=0)\
                    .set_x(old_during.get_x() - diff).set_y(old_during.get_y())
                animations_tw_update.append(AnimationGroup(*[Transform(old_after, new_after), Transform(old_during, new_during)]))
            else:
                end = tws[node][1]
        self.play(AnimationGroup(*animations_tw_update, lag_ratio=2))
        self.pause()

        # insertion removal
        self.play(FadeIn(filtering_step_2))

        self.pause()
        # cannot reach the node from the pred
        node, pred = (5, 2)
        highlight_1 = SurroundingRectangle(dots[node])
        highlight_2 = SurroundingRectangle(dots[insertions[node][pred]])
        self.play(AnimationGroup(*[
            Create(highlight_1),
            Create(highlight_2),
            insertions_arrows[node][pred].animate.set_color(RED)]))
        self.pause()
        self.play(AnimationGroup(*[
            FadeOut(highlight_1),
            FadeOut(highlight_2),
            FadeOut(insertions_arrows[node][pred])]))

        self.pause()
        # cannot close the sequence
        node, pred = (6, 0)
        highlight_1 = SurroundingRectangle(dots[node])
        highlight_2 = SurroundingRectangle(dots[insertions[node][pred]])
        highlight_3 = SurroundingRectangle(dots[2])
        self.play(AnimationGroup(*[
            Create(highlight_1),
            Create(highlight_2),
            Create(highlight_3),
            insertions_arrows[node][pred].animate.set_color(RED)]))
        self.pause()
        self.play(AnimationGroup(*[
            FadeOut(highlight_1),
            FadeOut(highlight_2),
            FadeOut(highlight_3),
            FadeOut(insertions_arrows[node][pred])]))

        self.pause()
        # exceeding max distance
        node, pred = (8, 0)
        highlight_1 = SurroundingRectangle(dots[node])
        highlight_2 = SurroundingRectangle(dots[insertions[node][pred]])
        self.play(AnimationGroup(*[
            Create(highlight_1),
            Create(highlight_2),
            insertions_arrows[node][pred].animate.set_color(RED)]))
        self.pause()
        self.play(AnimationGroup(*[
            FadeOut(highlight_1),
            FadeOut(highlight_2),
            FadeOut(insertions_arrows[node][pred])]))
        self.play(dots[node].animate.set_color(EXCLUDED))

        self.pause()
        self.clear()



        # ==============================
        # SLIDE OtherConstraints
        # ==============================

        text_title = Text("Current existing constraints", color=BLUE)
        text_dependence = MathTex(r"\bullet\hspace{5pt} \text{Dependency}")
        desc_dependence = MarkupText("Nodes are included / excluded together").scale(.5)
        dependence = VGroup(text_dependence, desc_dependence).arrange(DOWN, center=False, aligned_edge=LEFT)

        text_precedence = MathTex(r"\bullet \hspace{5pt} \text{Precedence}")
        desc_precedence = MarkupText("Nodes must respect a given order").scale(.5)
        precedence = VGroup(text_precedence, desc_precedence).arrange(DOWN, center=False, aligned_edge=LEFT)

        text_cumulative = MathTex(r"\bullet \hspace{5pt} \text{Cumulative}")
        desc_cumulative = MarkupText("Respect a max capacity (pickup and delivery problems)").scale(.5)
        cumulative = VGroup(text_cumulative, desc_cumulative).arrange(DOWN, center=False, aligned_edge=LEFT)

        text_disjoint = MathTex(r"\bullet \hspace{5pt} \text{Disjoint}")
        desc_disjoint = MarkupText("A node is visited by one of several Sequence ").scale(.5)
        disjoint = VGroup(text_disjoint, desc_disjoint).arrange(DOWN, center=False, aligned_edge=LEFT)

        layout_1 = VGroup(text_title, dependence, precedence, cumulative, disjoint) \
            .arrange(DOWN, center=False, aligned_edge=LEFT, buff=.5).to_corner(UP + LEFT)
        layout = VGroup(text_title, layout_1) \
            .arrange(DOWN, center=False, aligned_edge=LEFT, buff=TITLE_BUF).to_corner(UP + LEFT)
        for i in [desc_dependence, desc_precedence, desc_cumulative, desc_disjoint]:
            i.shift(np.array([0.5, 0, 0]))
        self.play(FadeIn(text_title))
        self.play(AnimationGroup(*[FadeIn(dependence), FadeIn(precedence), FadeIn(cumulative), FadeIn(disjoint)]))
        self.pause()
        self.clear()



        # ==============================
        # SLIDE Search
        # ==============================

        # search procedure template
        search_title = Text("Search procedure", color=BLUE).to_corner(UP + LEFT)
        myTemplate = TexTemplate(documentclass=r"\documentclass[boxed,border=2pt]{standalone}")
        myTemplate.add_to_preamble("\\usepackage[linesnumbered, titlenumbered,noend]{algorithm2e}\n\\DontPrintSemicolon")
        search = Tex(r"""
        	\hsize=10.9cm
	\setlength{\algomargin}{11pt}
	\begin{algorithm}[H]
		\If{isFixed(Sq)}{
			\Return solution \;
		}
		$node \gets {\arg\!\min}{\; \{ nMemberInserts(Sq, node) \; | \; \forall {node \in {possible\;node}}\} }$  \;
		$branching \gets \{  \}$ \;
		\For{$pred \in getMemberInserts(Sq, n)$}{
			$branching \gets branching + insert(Sq, pred, node)$ \;
		}
		
		sort $branching$ by increasing order of heuristic \;
		\Return $branching$ \;
	\end{algorithm}""", tex_template=myTemplate, tex_environment=None)\
            .scale(0.8)\
            .next_to(search_title, DOWN, buff=TITLE_BUF)\
            .set_x(ORIGIN[0])
        # LNS template

        lns = Tex(r"""
        		\hsize=10.9cm
	\setlength{\algomargin}{11pt}
\begin{algorithm}[H]
	$bestSol \gets initSol $ \;
	\For{$i \in \{ minSize \ldots  (maxSize-range) \}$}{
		\If{i = maxSize-range}{
			$i \gets minSize$ \;  
		}
		\For{$j \in \{0 \ldots range - 1\}$}{ 
			\For{$k \in \{ 1 \ldots numIter \}$}{ 
				relax(i + j) nodes from $bestSol$ \label{alg:lns_relax}\;
				$sol \gets optimize(dist)$ \label{alg:lns_optimize}\;
				\If{the solution has been improved}{
					$bestSol \gets sol$
				}
				\If{timeLimit is reached} {
					\Return $bestSol$
				}
			}
		}
	}
\end{algorithm}""", tex_template=myTemplate, tex_environment=None)\
            .scale(0.8)\
            .next_to(search_title, DOWN, buff=TITLE_BUF)\
            .set_x(ORIGIN[0])

        self.play(AnimationGroup(*[FadeIn(search_title), FadeIn(search)]))
        self.pause()
        self.play(FadeOut(search))
        self.play(FadeIn(lns))
        self.pause()
        self.clear()



        # ==============================
        # SLIDE Problems
        # ==============================

        # TSPTW
        title_tsptw = Text("TSP with Time windows", color=BLUE)
        desc_1 = [
            MathTex(r"\bullet\hspace{5pt} \text{Time window}"),
            MathTex(r"\bullet\hspace{5pt} \text{Objective = minimize traveled distance}"),
        ]
        tsptw_desc_group = VGroup(*desc_1).arrange(DOWN, center=False, aligned_edge=LEFT, buff=0.5)
        # DARP
        title_darp = Text("Dial-A-Ride Problem (DARP)", color=BLUE)
        desc_2 = [
            MathTex(r"\bullet\hspace{5pt} \text{Time window}"),
            MathTex(r"\bullet\hspace{5pt} \text{Multiple vehicles}"),
            MathTex(r"\vartriangleright \hspace{5pt} \text{Bounded travel time}").scale(.8),
            MathTex(r"\bullet\hspace{5pt} \text{Pickup and delivery}"),
            MathTex(r"\vartriangleright \hspace{5pt} \text{Bounded delivery time}").scale(.8),
            MathTex(r"\bullet\hspace{5pt} \text{Objective = minimize traveled distance}"),
        ]
        darp_desc_group = VGroup(*desc_2).arrange(DOWN, center=False, aligned_edge=LEFT, buff=0.5)
        #problems = VGroup(title_tsptw, desc_1[0], title_darp, text).arrange(DOWN, center=False, aligned_edge=LEFT, buff=0.5).to_corner(UP + LEFT)
        for i in [2, 4]:
            desc_2[i].shift(np.array([0.5, 0, 0]))

        # PTP
        title_ptp = Text("Patient Transportation Problem", color=BLUE).to_corner(UP + LEFT)
        desc_3 = [
            MathTex(r"\bullet\hspace{5pt} \text{DARP with extensions}"),
            MathTex(r"\bullet\hspace{5pt} \text{Transport patients to hospitals}"),
            MathTex(r"\vartriangleright \hspace{5pt} \text{And possibly back home}").scale(.8),
            MathTex(r"\vartriangleright \hspace{5pt} \text{Travel back by the same vehicle (or not)}").scale(.8),
            MathTex(r"\bullet\hspace{5pt} \text{Vehicle categories}"),
            MathTex(r"\vartriangleright \hspace{5pt} \text{Wheelchairs cannot go in all vehicles}").scale(.8),
            MathTex(r"\bullet\hspace{5pt} \text{Objective = maximize number of patients transported}"),
        ]
        ptp_desc_group = VGroup(*desc_3).arrange(DOWN, center=False, aligned_edge=LEFT, buff=0.5)
        for i in [2, 3, 5]:
            desc_3[i].shift(np.array([0.5, 0, 0]))

        for title in [title_tsptw, title_darp, title_ptp]:
            title.to_corner(UP)

        tsptw_desc_group.next_to(title_tsptw, DOWN, buff=TITLE_BUF).to_corner(LEFT)
        darp_desc_group.next_to(title_darp, DOWN, buff=TITLE_BUF).to_corner(LEFT)
        ptp_desc_group.next_to(title_ptp, DOWN, buff=TITLE_BUF).to_corner(LEFT)

        # tsptw
        text_results_tsptw = Text("Improved 32 instances in total").scale(0.7)
        table_tsptw = MobjectTable([
            [Tex("Instance", color=BLUE),
             Tex("Previous best", color=BLUE),
             Tex("New best", color=BLUE),
             Tex("Time [s]", color=BLUE)
             ],
            [Tex("rbg092a"), Tex("7160"), Tex("7158"), Tex("2.70")],
            [Tex("rbg132"), Tex("8470"), Tex("8468"), Tex("0.76")],
            [Tex("rbg132.2"), Tex("8200"), Tex("8194"), Tex("37.76")],
            [Tex("rbg152.3"), Tex("9797"), Tex("9796"), Tex("0.41")],
            [Tex("rbg172a"), Tex("10,961"), Tex("10,956"), Tex("113.83")],
            [Tex("rbg193"), Tex("12,547"), Tex("12,538"), Tex("55.57")],
            [Tex("rbg193.2"), Tex("12,167"), Tex("12,159"), Tex("242.54")],
            [Tex("rbg201"), Tex("12,967"), Tex("12,948"), Tex("152.53")],
            [Tex("rbg233"), Tex("15,031"), Tex("14,994"), Tex("264.70")],
            [Tex("rbg233.2"), Tex("14,549"), Tex("14,523"), Tex("24.20")],
        ], v_buff=0.15, h_buff=1, arrange_in_grid_config={"cell_alignment": RIGHT})\
            .scale(0.8)\
            .next_to(title_tsptw, DOWN, buff=TITLE_BUF).set_x(ORIGIN[0])
        text_results_tsptw.to_corner(DOWN + LEFT)
        for i, o in enumerate(table_tsptw.get_horizontal_lines()):
            if i == 0:
                o.set_color(BLUE)
            else:
                table_tsptw.remove(o)
        for i, o in enumerate(table_tsptw.get_vertical_lines()):
            o.set_color(BLUE)
        # table.remove(*[o for i, o in enumerate(table.get_horizontal_lines()) if i != 0])

        self.play(FadeIn(title_tsptw))
        self.play(FadeIn(tsptw_desc_group))
        self.pause()
        self.play(FadeOut(tsptw_desc_group))
        self.play(FadeIn(table_tsptw))
        self.play(FadeIn(text_results_tsptw))
        self.pause()
        self.play(FadeOut(table_tsptw, text_results_tsptw))

        ax = Axes(
            x_range=[0, 60, 5],
            y_range=[14900, 15800, 100],
            x_length=9,
            y_length=6,
            x_axis_config={"numbers_to_include": np.arange(0, 60, 5)},
            y_axis_config={"numbers_to_include": np.arange(14950, 15800, 100)},
            tips=False,
        ).scale(0.8).to_corner(DOWN)
        labels = ax.get_axis_labels(
            x_label=Tex("time [s]", color=BLUE), y_label=Tex("Objective", color=BLUE)
        )

        x_vals = []
        y_vals = []

        # string: "t = 6.329 cost = 15062"
        pattern = "t = (\d+.\d+) cost = (\d+)"

        with open("results_tsptw.txt") as file:
            for line in file:
                if (search_obj := re.search(pattern, line)) is not None:
                    time = float(search_obj.group(1))
                    cost = int(search_obj.group(2))
                    x_vals.append(time)
                    y_vals.append(cost)

        graph = ax.plot_line_graph(x_values=x_vals, y_values=y_vals, add_vertex_dots=False)
        graph_2 = ax.plot_line_graph(x_values=[-1, 61], y_values=[15031, 15031], line_color=RED, add_vertex_dots=False)

        self.play(FadeIn(ax, labels))
        self.play(Create(graph, run_time=3))
        self.pause()
        self.play(Create(graph_2))
        self.pause()
        self.play(FadeOut(graph, graph_2, ax, labels, title_tsptw))


        # darp
        #myTemplate = TexTemplate()
        #myTemplate.add_to_preamble(r"\usepackage{xcolor}")
        text_resuts_darp = Text("Mean of 10 runs of 15 minutes, initial solution provided").scale(0.6)
        table_darp = MobjectTable([
            [Tex("m", color=BLUE),
             Tex("n", color=BLUE),
             Tex("LNS-FFPA", color=BLUE),
             Tex("Sequence", color=BLUE),
             Tex("CPO", color=BLUE)
             ],
            [Tex("3"), Tex("24"), Tex("191.76"), Tex("190.89", color=TABLE_HIGHLIGHT), Tex("196.11")],
            [Tex("4"), Tex("36"), Tex("291.71", color=TABLE_HIGHLIGHT), Tex("294.72"), Tex("318.97")],
            [Tex("5"), Tex("48"), Tex("308.95"), Tex("309.09", color=TABLE_HIGHLIGHT), Tex("327.37")],
            [Tex("6"), Tex("72"), Tex("532.55"), Tex("531.84", color=TABLE_HIGHLIGHT), Tex("579.79")],
            [Tex("7"), Tex("72"), Tex("554.57", color=TABLE_HIGHLIGHT), Tex("554.65"), Tex("614.02")],
            [Tex("8"), Tex("108"), Tex("752.29", color=TABLE_HIGHLIGHT), Tex("794.86"), Tex("924.04")],
            [Tex("9"), Tex("96"), Tex("622.19", color=TABLE_HIGHLIGHT), Tex("625.68"), Tex("740.26")],
            [Tex("10"), Tex("144"), Tex("950.16", color=TABLE_HIGHLIGHT), Tex("1011.42"), Tex("t/o")],
            [Tex("11"), Tex("120"), Tex("699.32", color=TABLE_HIGHLIGHT), Tex("718.58"), Tex("861.74")],
            [Tex("13"), Tex("144"), Tex("878.33", color=TABLE_HIGHLIGHT), Tex("901.71"), Tex("1042.82")],
        ], v_buff=0.15, h_buff=1, arrange_in_grid_config={"cell_alignment": RIGHT})\
            .scale(0.9).next_to(title_tsptw, DOWN, buff=TITLE_BUF).set_x(ORIGIN[0])
        text_resuts_darp.to_corner(DOWN + LEFT)
        for i, o in enumerate(table_darp.get_horizontal_lines()):
            if i == 0:
                o.set_color(BLUE)
            else:
                table_darp.remove(o)
        for i, o in enumerate(table_darp.get_vertical_lines()):
            o.set_color(BLUE)

        '''
        table_darp = Tex(r"""
        \begin{tabular}[t]{|c|c|r|r|r|} 
        \hline
        \multicolumn5{|c|}{\textbf{15 minutes run - initial solution provided}} \\ 
        \hline 
        \multicolumn{2}{|c|}{\textbf{class} $a$} & \textbf{LNS-FFPA} & \textbf{Sequence} & \textbf{CPO}\\ 
        \hline 
        m & n & Mean & Mean & Mean \\ 
        \hline 
        3 & 24  & 191.76 & \textbf{190.89} & 196.11 \\ 
        4 & 36  & \textbf{291.71} & 294.72 & 318.97 \\ 
        5 & 48  & 308.95 & \textbf{307.09}  & 327.37 \\ 
        6 & 72  & 532.55  & \textbf{531.84} & 579.79 \\ 
        7 & 72  & \textbf{554.57} & 554.65  & 614.02 \\ 
        8 & 108  & \textbf{752.29} & 794.86 & 924.04 \\ 
        9 & 96  & \textbf{622.19}  & 625.68 & 740.26 \\ 
        10 & 144  & \textbf{950.16} & 1011.42  & t/o \\ 
        11 & 120  & \textbf{699.32} & 718.58  & 861.74 \\ 
        13 & 144  & \textbf{878.33} & 901.71  & 1042.82 \\ 
        \hline 
        \end{tabular}""").scale(0.75).next_to(title_darp, DOWN, buff=TITLE_BUF)
        '''

        self.play(FadeIn(title_darp))
        self.play(FadeIn(darp_desc_group))
        self.pause()
        self.play(FadeOut(darp_desc_group))
        self.play(FadeIn(table_darp))
        self.play(FadeIn(text_resuts_darp))
        self.pause()
        self.play(AnimationGroup(*[FadeOut(title_darp, table_darp, text_resuts_darp)]))

        # ptp
        table_ptp = MobjectTable([
            [Tex("Difficulty"),
             Tex("Name"),
             Tex("$|H|$"),
             Tex("$|V|$"),
             Tex("$|R|$"),
             Tex(r"SCHED\\+MSS"),
             Tex("Sequence"),
             ],
            [Tex("Easy"), Tex("RAND-E-8"), Tex("32"), Tex("12"), Tex("128"), Tex("128", color=TABLE_HIGHLIGHT), Tex("128", color=TABLE_HIGHLIGHT)],
            [Tex("Easy"), Tex("RAND-E-9"), Tex("36"), Tex("14"), Tex("144"), Tex("144", color=TABLE_HIGHLIGHT), Tex("143")],
            [Tex("Easy"), Tex("RAND-E-10"), Tex("40"), Tex("12"), Tex("160"), Tex("158", color=TABLE_HIGHLIGHT), Tex("156")],
            [Tex("Medium"), Tex("RAND-M-8"), Tex("64"), Tex("8"), Tex("128"), Tex("89"), Tex("91", color=TABLE_HIGHLIGHT)],
            [Tex("Medium"), Tex("RAND-M-9"), Tex("72"), Tex("8"), Tex("144"), Tex("89"), Tex("93", color=TABLE_HIGHLIGHT)],
            [Tex("Medium"), Tex("RAND-M-10"), Tex("80"), Tex("9"), Tex("160"), Tex("109"), Tex("113", color=TABLE_HIGHLIGHT)],
            [Tex("Hard"), Tex("RAND-H-8"), Tex("128"), Tex("8"), Tex("128"), Tex("77"), Tex("87", color=TABLE_HIGHLIGHT)],
            [Tex("Hard"), Tex("RAND-H-9"), Tex("144"), Tex("8"), Tex("144"), Tex("78"), Tex("84", color=TABLE_HIGHLIGHT)],
            [Tex("Hard"), Tex("RAND-H-10"), Tex("160"), Tex("8"), Tex("160"), Tex("76"), Tex("84", color=TABLE_HIGHLIGHT)],
        ], v_buff=0.15, h_buff=0.4, arrange_in_grid_config={"cell_alignment": RIGHT})\
            .next_to(title_tsptw, DOWN, buff=TITLE_BUF).set_x(ORIGIN[0])
        for i, o in enumerate(table_ptp.get_horizontal_lines()):
            if i % 3 == 0:
                o.set_color(BLUE)
            else:
                table_ptp.remove(o)
        for i, o in enumerate(table_ptp.get_vertical_lines()):
            if i in [4, 5]:
                o.set_color(BLUE)
            else:
                table_ptp.remove(o)

        self.play(FadeIn(title_ptp))
        self.play(FadeIn(ptp_desc_group))
        self.pause()
        self.play(FadeOut(ptp_desc_group))
        self.play(FadeIn(table_ptp))

        self.pause()
        self.clear()



        # ==============================
        # SLIDE Perspectives
        # ==============================

        title = Text("Perspectives", color=BLUE).scale(1.2).to_corner(UP)
        texts = [
            MathTex(r"\bullet\hspace{5pt} \text{Optimize and implement new constraints}"),
            MathTex(r"\bullet\hspace{5pt} \text{Tackle more VRP}"),
            MathTex(r"\vartriangleright \hspace{5pt} \text{Min-Cost TSP with Drone}").scale(.8),
            MathTex(r"\vartriangleright \hspace{5pt} \text{Capacitated VRP}").scale(.8),
            MathTex(r"\vartriangleright \hspace{5pt} \text{\dots}").scale(.8),
            MathTex(r"\bullet\hspace{5pt} \text{Use Sequence Variables on scheduling problems}"),
            MathTex(r"\bullet\hspace{5pt} \text{Analyze variations of the sequences}"),
            MathTex(r"\vartriangleright \hspace{5pt} \text{Different consistency}").scale(.8),
            MathTex(r"\vartriangleright \hspace{5pt} \text{Insertions = pairs of pred. and succ.}").scale(.8),
        ]
        text = VGroup(*texts).arrange(DOWN, center=False, aligned_edge=LEFT, buff=0.3)\
            .to_corner(DOWN + LEFT)
        for i in [2, 3, 4, 7, 8]:
            texts[i].shift(np.array([0.5, 0, 0]))
        self.play(FadeIn(title))
        self.wait()
        self.play(FadeIn(text))
        self.pause()
        self.clear()



        # ==============================
        # SLIDE Conclusion
        # ==============================

        #self.camera_class.set_background(np.array([255, 255, 255]))
        title = Text("Conclusion", color=BLUE).scale(1.2).to_corner(UP)
        text_1 = MathTex(r"\bullet\hspace{5pt} \text{Sequence Variables = CP alternative to successor model}", color=FG)
        text_2 = MathTex(r"\vartriangleright \hspace{5pt} \text{Can model optional visits}", color=FG).scale(.8)
        text_3 = MathTex(r"\vartriangleright \hspace{5pt} \text{Compatible with insertions heuristics}", color=FG).scale(.8)
        text_4 = MathTex(r"\bullet\hspace{5pt} \text{Efficient for several VRP}", color=FG)
        text_5 = MathTex(r"\bullet\hspace{5pt} \text{Many possibilities for further improvements}", color=FG)
        text = VGroup(text_1, text_2, text_3, text_4, text_5).arrange(DOWN, center=False, aligned_edge=LEFT, buff=0.5)\
            .scale(0.9)\
            .to_corner(LEFT)\
            .set_y(ORIGIN[1])
        text_2.shift(np.array([0.5, 0, 0]))
        text_3.shift(np.array([0.5, 0, 0]))
        text_bye = Text("Thanks for your attention!", color=BLUE).scale(0.9).next_to(text, DOWN, buff=TITLE_BUF).set_x(ORIGIN[0])
        text_mail = Text("augustin.delecluse@uclouvain.be", color=FG).scale(0.7).to_corner(DOWN)
        self.play(FadeIn(title))
        self.play(FadeIn(text))
        self.pause()
        self.play(FadeIn(text_bye))
        self.play(FadeIn(text_mail))
        self.pause()
        self.wait()
