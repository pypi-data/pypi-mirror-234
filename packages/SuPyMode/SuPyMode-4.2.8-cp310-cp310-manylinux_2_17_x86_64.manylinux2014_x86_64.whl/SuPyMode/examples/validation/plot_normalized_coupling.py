"""
Validation: 3 for circular symmetric structure
==============================================
"""

# %%
# Imports
# ~~~~~~~
import numpy
from SuPyMode.tools.fibermodes_validation import FiberModeSolver
from SuPyMode.workflow import Workflow, fiber_catalogue, Boundaries2D, Fused1
from MPSPlots.Render2D import SceneList

wavelength = 1550e-9
mode_couples = [
    ('LP01', 'LP02'),
    ('LP01', 'LP03'),
    ('LP01', 'LP41_a'),
]

workflow = Workflow(
    fiber_list=[fiber_catalogue.SMF28(wavelength=wavelength)],
    clad_structure=Fused1,
    fusion_degree=None,
    wavelength=wavelength,
    resolution=60,  # For more accurate result resolution should be over 150. Mode labeling is wrong under 150.
    x_bounds="centering-left",
    y_bounds="centering-bottom",
    boundaries=[
        Boundaries2D(right='symmetric', top='symmetric'),
        Boundaries2D(right='symmetric', top='anti-symmetric')
    ],
    n_sorted_mode=6,
    n_added_mode=4,
    plot_geometry=False,
    debug_mode=False,
    auto_label=True,
)

superset = workflow.get_superset()

fibermode_solver = FiberModeSolver(wavelength=1550e-9)

fibermodes_data_sets = fibermode_solver.get_normalized_coupling(
    mode_couples=[(m0[:4], m1[:4]) for (m0, m1) in mode_couples],
    resolution=500,
    itr_list=numpy.linspace(1.0, 0.05, 100)
)

figure = SceneList(unit_size=(12, 4))

ax = figure.append_ax(
    x_label='Inverse taper ratio',
    y_label='Effective index',
    show_legend=True,
    font_size=18,
    tick_size=15,
    legend_font_size=18
)

for idx, (mode_couple, data_set) in enumerate(zip(mode_couples, fibermodes_data_sets)):
    color = f'C{idx}'
    not_nan_idx = numpy.where(~numpy.isnan(data_set.y))
    y_data = data_set.y[not_nan_idx]
    x_data = data_set.x[not_nan_idx]

    ax.add_line(
        x=x_data,
        y=y_data,
        label=mode_couple,
        line_style='-',
        line_width=2,
        color=color,
        layer_position=1
    )

    sub_samnpling = 15
    supermode_0 = getattr(superset, mode_couple[0])
    supermode_1 = getattr(superset, mode_couple[1])

    ax.add_scatter(
        x=superset.itr_list[::sub_samnpling],
        y=abs(supermode_0.normalized_coupling.get_values(supermode_1)[::sub_samnpling]),
        label=f"{mode_couple}",
        color='black',
        line_width=2,
        edge_color=color,
        marker_size=80,
        line_style='-',
        layer_position=2
    )

_ = figure.show()

# -
