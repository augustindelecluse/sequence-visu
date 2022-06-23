# animation for CP Sequence variables
from manim import *
import numpy as np

# coloring
MEMBER = GREEN
POSSIBLE = BLUE
EXCLUDED = RED


class DashedArrow(Arrow):

    def __init__(
        self,
        *args,
        dash_length=DEFAULT_DASH_LENGTH,
        dashed_ratio=0.5,
        **kwargs
    ):
        self.dash_length = dash_length
        self.dashed_ratio = dashed_ratio
        super().__init__(*args, **kwargs)
        dashes = DashedVMobject(
            self,
            num_dashes=self._calculate_num_dashes(),
            dashed_ratio=dashed_ratio,
        )
        self.clear_points()
        self.add(*dashes)

    def _calculate_num_dashes(self) -> int:
        """Returns the number of dashes in the dashed line.

        Examples
        --------
        ::

            >>> DashedArrow()._calculate_num_dashes()
            20
        """

        # Minimum number of dashes has to be 2
        return max(
            2,
            int(np.ceil((self.get_length() / self.dash_length) * self.dashed_ratio)),
        )


class SequenceCreation(Scene):
    def construct(self) -> None:
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
        for dot in dots:
            self.add(dot)
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
        self.wait()

        # ordering for the members
        successors = [Arrow(i.get_center(), j.get_center(), color=MEMBER) for i, j in zip(members_group, members_group[1:])]
        # successors_group = VGroup(*successors)
        animations = [FadeIn(succ) for succ in successors]
        self.play(AnimationGroup(*animations, lag_ratio=0.25))
        #self.wait()

        # excluded nodes
        self.play(excluded_group.animate.set_color(EXCLUDED))
        #self.wait()

        # possible nodes
        self.play(possible_group.animate.set_color(POSSIBLE))
        #self.wait()
        # predecessors for the nodes
        #insertions_groups = {node: VGroup(*[Arrow(start=dots[pred].get_center(), end=dots[node].get_center(), positive_space_ratio=0.25) for pred in preds]) for node, preds in insertions.items()}
        insertions_groups = {node: VGroup(
            *[DashedArrow(start=dots[pred].get_center(), end=dots[node].get_center(), dashed_ratio=0.4, dash_length=0.15) for pred in
              preds]) for node, preds in insertions.items()}
        self.add(*[j for j in insertions_groups.values()])
        self.wait()
