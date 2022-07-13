import numpy as np
from manim import *
from manim_presentation import Slide
import random

MEMBER = GREEN
POSSIBLE = BLUE
EXCLUDED = RED
BACKGROUND = BLACK
FOREGROUND = WHITE


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
        depot = Square(side_length=dots[0].radius * 1.5).rotate(PI/4).set_fill(FOREGROUND, opacity=1.0).move_to(dots[0].get_center())
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
        self.play(AnimationGroup(*([FadeOut(img) for img in pickup_img + drop_img] + [FadeIn(dot) for dot in dots[1:]] + [FadeOut(text_depot)])))
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
        self.play(AnimationGroup(*[successor_candidates[1].animate.set_color(RED), successor_candidates[2].animate.set_color(RED)]))
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

        # drawback 2: optional nodes
        self.play(AnimationGroup(*[FadeOut(arrow) for arrow in partial_route + detour]))
        optional = [8, 6, 7, 3]
        optional_circles = [Circle(radius=dots[0].radius, color=ORANGE).move_to(dots[i].get_center()) for i in optional]
        # transform optional nodes into circles
        #self.play(AnimationGroup(*[dots[i].animate.set_color(ORANGE) for i in optional]))
        self.play(AnimationGroup(*[Transform(dots[i], optional_circles[j]) for j, i in enumerate(optional)]))
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
        #self.play(FadeOut(optional_circles[0]))
        self.play(Transform(dots[8], Dot(dots[8].get_center())))
        #self.play(AnimationGroup(*([dots[i].animate.set_color(RED) for i in excluded] + [dots[i].animate.set_color(FOREGROUND) for i in optional if i not in excluded])))
        self.play(AnimationGroup(*[GrowArrow(arrow) for arrow in visited_arrows], lag_ratio=.2))
        self.play(AnimationGroup(*[GrowArrow(arrow) for arrow in excluded_arrows], lag_ratio=.2))
        self.play(FadeIn(annex_2))
        self.pause()
        self.wait()


class SequenceOtherWork(Slide):

    def construct(self):
        text_interval = Text("Interval Sequence Variables", color=BLUE)
        text_scale = .7
        text_cplex = Tex(r"$\vartriangleright$ Available in CP Optimizer ", "(CPLEX) ", "and ", "Google OR-Tools").scale(text_scale).set_color_by_tex('CPLEX', BLUE).set_color_by_tex('Google', BLUE)
        #text_nodes_representation = Tex(r"$\vartriangleright$ Nodes = ", "Interval Variables", "space", "ordered through a ", "Sequence Variable").scale(text_scale).set_color_by_tex('Interval', BLUE).set_color_by_tex("space", BACKGROUND)
        #text_sequence = Tex().scale(text_scale).set_color_by_tex('Sequence', BLUE)
        #group_nodes_description = VGroup(text_nodes_representation, text_sequence).arrange(DOWN, center=False, aligned_edge=RIGHT)
        text_nodes_representation = Tex(r"$\vartriangleright$ Nodes = ", "Interval Variables ", "ordered through a ", "Sequence Variable").scale(text_scale).set_color_by_tex('Interval', BLUE)
        group_nodes_description = VGroup(text_nodes_representation).arrange(DOWN, center=False, aligned_edge=RIGHT)
        text_head_tail = Tex(r"$\vartriangleright$ Head-tail structure").scale(text_scale)
        text_group = VGroup(text_interval, text_cplex, group_nodes_description, text_head_tail).arrange(DOWN, center=False, aligned_edge=LEFT).to_corner(UP + LEFT)
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
        circles = [Circle(radius=dots[0].radius, color=FOREGROUND).move_to(coords[i]) for i in dot_list]
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
        candidates_head = Ellipse(height=3, width=2, color=head_cand_color).rotate(-PI/4).move_to(np.array([3.5, 0.25, 0]))  # head candidates
        candidates_tail = Ellipse(height=2.5, width=2, color=tail_cand_color).rotate(3*PI/8).move_to(np.array([4, 0.25, 0]))  # tail candidates
        text_candidates_head = MarkupText("Candidates Head", color=head_cand_color).scale(.5).move_to(np.array([2.2, 1.75, 0]))
        text_candidates_tail = MarkupText("Candidates Tail", color=tail_cand_color).scale(.5).move_to(np.array([5.3, 1.75, 0]))

        figure_list = points_list + \
                      [arrow_head, text_head, head_limit] + \
                      [arrow_tail, text_tail, tail_limit] + \
                      [candidates_head, text_candidates_head] + \
                      [candidates_tail, text_candidates_tail] + \
                      [text_not_sequenced]
        figures = VGroup(*figure_list).next_to(text_group, DOWN, buff=0.5).set_x(ORIGIN[0])
        text_pros_cons = MarkupText(f"<span fgcolor='{GREEN}'>OK</span> optional visits\n<span fgcolor='{RED}'>KO</span> cannot insert anywhere in the sequence").scale(.5)
        text_pros_cons.next_to(figures, DOWN).to_corner(LEFT)

        self.play(FadeIn(text_group))
        self.pause()

        self.play(AnimationGroup(*([FadeIn(c) for c in circles+dots])))
        self.pause()
        self.play(AnimationGroup(*[GrowArrow(arrow_head), FadeIn(text_head), GrowFromPoint(head_limit, arrow_head.get_end())], lag_ratio=.3))
        self.play(AnimationGroup(*[GrowArrow(arrow_tail), FadeIn(text_tail), GrowFromPoint(tail_limit, arrow_tail.get_end())], lag_ratio=.3))
        self.play(FadeIn(text_not_sequenced))
        self.pause()
        self.play(Create(candidates_head))
        self.play(FadeIn(text_candidates_head))
        self.play(Create(candidates_tail))
        self.play(FadeIn(text_candidates_tail))
        self.pause()
        self.play(FadeIn(text_pros_cons))
        self.pause()
        self.wait()


class Sequences(Slide):

    def construct(self):
        text_sequence = Text("Sequence Variable", color=BLUE).to_corner(UP + LEFT)
        insert_table = MathTable(
            [["Partial Sequence", "Operation"],
            [r"\alpha \rightarrow \omega", "Initialization"],
            [r"\alpha \rightarrow 1 \rightarrow \omega", r"Insert(\alpha, 1)"],
            [r"\alpha \rightarrow 1 \rightarrow 4 \rightarrow \omega", r"Insert(1, 4)"],
            [r"\alpha \rightarrow 5 \rightarrow 1 \rightarrow 4 \rightarrow \omega", r"Insert(\alpha, 5)"]
            ],
            include_outer_lines=True).next_to(text_sequence, DOWN).set_x(ORIGIN[0])

        # coordinates for the dots
        coords = [
            np.array([-4.25, 0.75, 0]),   # alpha
            np.array([-1.75, 2.75, 0]),
            np.array([-1.25, 1.25, 0]),
            np.array([-1, -0.5, 0]),
            np.array([-4, -1.5, 0]),  # last member
            np.array([2, 2.5, 0]),
            np.array([1.75, 1, 0]),
            np.array([3.25, -0.75, 0]),  # last possible
            np.array([2.5, -2, 0]),
            np.array([4.75, 1, 0]),
        ]
        # draw the dots
        dots = [Dot(i, radius=0.16) for i in coords]
        # partition of the nodes
        members = [0, 1, 2, 3, 4]
        possible = [5, 6, 7]
        insertions = {
            5: [1, 2, 3],
            6: [1, 2, 3, 5],
            7: [1, 2, 3, 5, 6],
        }
        excluded = [8, 9]

        members_group = VGroup(*[dots[i] for i in members])
        excluded_group = VGroup(*[dots[i] for i in excluded])
        possible_group = VGroup(*[dots[i] for i in possible])
        text_first = Tex(r"$\alpha$", color=MEMBER).next_to(dots[0], LEFT)
        text_last = Tex(r"$\omega$", color=MEMBER).next_to(dots[4], LEFT)
        text_member = Text("members", color=MEMBER).scale(0.5)
        text_possible = Text("possible", color=POSSIBLE).scale(0.5)
        text_excluded = Text("excluded", color=EXCLUDED).scale(0.5)
        all_dots = VGroup(*dots).next_to(text_sequence, DOWN, buff=.5).set_x(ORIGIN[0])
        description_group = VGroup(text_member, text_possible, text_excluded).arrange(RIGHT, buff=1).next_to(all_dots, DOWN)

        # ordering for the members
        successors = [Arrow(i.get_center(), j.get_center(), color=MEMBER) for i, j in zip(members_group, members_group[1:])]
        # successors_group = VGroup(*successors)
        animations = [GrowArrow(succ) for succ in successors]

        # predecessors for the nodes
        insertions_arrows = {
            node:
                [DashedArrow(start=dots[pred].get_center(), end=dots[node].get_center(), dashed_ratio=0.4, dash_length=0.15, color=FOREGROUND) for pred in v]
            for node, v in insertions.items()
        }
        # make the arrows grow
        arrows_list = [arrow for k, v in insertions_arrows.items() for arrow in v]
        random.shuffle(arrows_list)
        grow_insertions = [GrowArrow(arrow) for arrow in arrows_list]

        # initial title, table of operations
        self.play(FadeIn(text_sequence))
        self.play(Create(insert_table))
        self.wait()
        self.pause()
        self.play(FadeOut(insert_table))
        # and the dots appear
        self.play(*[FadeIn(dot) for dot in dots])
        self.pause()
        # nodes that will be set as members
        self.play(members_group.animate.set_color(MEMBER))
        self.play(AnimationGroup(*[FadeIn(text_first), FadeIn(text_last), FadeIn(text_member)]))
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
        arrows_changed = [insertions_arrows[node][i] for node, v in insertions.items() for i, pred in enumerate(v) if pred == n or node == n]
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
        #self.play(AnimationGroup(*[Restore(arrow_selected), Restore(arrow_detour_removed), FadeOut(arrow_detour_added), dots[n].animate.set_color(POSSIBLE)]))
        #self.pause()
        self.wait()


class DomainConsistency(Slide):

    def construct(self):
        # domain consistency
        title = Text("Consistency of the domain", color=BLUE).to_corner(UP + LEFT)

        math_tri_partition = MathTex(r"\bullet\hspace{5pt} S \cup P \cup E = X \wedge S \cap P = S \cap E =  P \cap E = \phi")
        text_tri_partition = MarkupText("Members (S), Possible (P), Excluded (E) nodes form a tri-partition").scale(.5)
        tri_partition = VGroup(math_tri_partition, text_tri_partition).arrange(DOWN, center=False, aligned_edge=LEFT)

        math_excluded_not_pred = MathTex(r"\bullet \hspace{5pt} p \in E \implies I^p = \phi \wedge \forall x: p \notin I^x")
        text_excluded_not_pred = MarkupText("An excluded element cannot be inserted nor be a predecessor").scale(.5)
        excluded_not_pred = VGroup(math_excluded_not_pred, text_excluded_not_pred).arrange(DOWN, center=False, aligned_edge=LEFT)

        math_member_not_insert = MathTex(r"\bullet \hspace{5pt} p \in S \implies I^p = \phi")
        text_member_not_insert = MarkupText("An element in the sequence cannot be inserted (again)").scale(.5)
        member_not_insert = VGroup(math_member_not_insert, text_member_not_insert).arrange(DOWN, center=False, aligned_edge=LEFT)

        math_no_pred = MathTex(r"\bullet \hspace{5pt} I^p = \phi \implies p \in S \vee p \in E")
        text_no_pred = MarkupText("An element without possible predecessor is either excluded or in the sequence").scale(.5)
        no_pred = VGroup(math_no_pred, text_no_pred).arrange(DOWN, center=False, aligned_edge=LEFT)

        layout = VGroup(title, tri_partition, excluded_not_pred, member_not_insert, no_pred)\
            .arrange(DOWN, center=False, aligned_edge=LEFT, buff=.5).to_corner(UP + LEFT)

        text_tri_partition.align_to(LEFT).shift(np.array([1, 0, 0]))
        text_excluded_not_pred.align_to(LEFT).shift(np.array([1, 0, 0]))
        text_member_not_insert.align_to(LEFT).shift(np.array([1, 0, 0]))
        text_no_pred.align_to(LEFT).shift(np.array([1, 0, 0]))
        self.play(FadeIn(title))
        self.pause()
        self.play(FadeIn(math_tri_partition))
        self.play(FadeIn(text_tri_partition))
        self.pause()
        self.play(FadeIn(math_excluded_not_pred))
        self.play(FadeIn(text_excluded_not_pred))
        self.pause()
        self.play(FadeIn(math_member_not_insert))
        self.play(FadeIn(text_member_not_insert))
        self.pause()
        self.play(FadeIn(math_no_pred))
        self.play(FadeIn(text_no_pred))
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

