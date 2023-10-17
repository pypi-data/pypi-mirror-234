import numpy as np
from pyroll.core import Unit, PassSequence
from pyroll.report import hookimpl, utils


@hookimpl(specname="unit_plot")
def temperatures_plot(unit: Unit):
    if isinstance(unit, PassSequence):
        """Plot the temperatures of all profiles"""
        fig, ax = utils.create_sequence_plot(unit)
        ax.set_ylabel(r"temperature $T$")
        ax.set_title("Mean Profile Temperatures")

        units = list(unit)
        if len(units) > 0:
            def gen_seq():
                yield -0.5, units[0].in_profile.temperature
                for i, u in enumerate(units):
                    yield i + 0.5, u.out_profile.temperature

            x, y = np.transpose(
                list(gen_seq())
            )

            ax.plot(x, y, marker="x")

            return fig
