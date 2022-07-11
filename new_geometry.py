from utils import *


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
