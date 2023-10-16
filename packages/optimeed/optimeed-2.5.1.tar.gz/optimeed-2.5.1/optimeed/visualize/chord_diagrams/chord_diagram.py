"""
Tools to draw a chord diagram in python
"""

from collections.abc import Sequence

import matplotlib as mpl
import matplotlib.patches as patches

from matplotlib.colors import ColorConverter, Colormap
from matplotlib.path import Path
from optimeed.core import adjust_lightness_1, is_light_color

import numpy as np

from .gradient import gradient
from .utilities import compute_positions_v2, dist, polar2xy, total_arc_length


LW = 0.3


def condition_matrices_picking(mat, sum_rows):
    """Condition matrices by filling until its full (sum(S2[i, :] or S2[:, i] < ST[i]), beginning by the largest elems.
    Guarantees the scale of the interactions are not modified, but does not represent all of them."""
    new_sum_rows = np.maximum(sum_rows, np.zeros(len(sum_rows)))
    new_mat = np.zeros(mat.shape)

    all_i, all_j = np.unravel_index(np.argsort(mat, axis=None), mat.shape)
    for i, j in zip(reversed(all_i), reversed(all_j)):
        if i != j:
            elem = mat[i, j]
            if ((np.nansum(new_mat[i, :])+elem) < new_sum_rows[i]) and ((np.nansum(new_mat[j, :])+elem) < new_sum_rows[j]) :
                if elem >= 0:
                    new_mat[i, j] = elem
                    new_mat[j, i] = elem
    np.fill_diagonal(new_mat, np.minimum(sum_rows, np.diagonal(mat)))
    new_mat = np.clip(new_mat, 0, 100)
    sum_rows = np.clip(sum_rows, 0, 100)
    return new_mat, sum_rows


def condition_matrices_rescaling(mat, sum_rows, rel_threshold=0.01):
    """Condition matrices by rescaling globally S2 (for sum(S2) <= sum(ST)), then by rescaling line by line (sum(S2[i, :]) <= ST[i]).
    Guarantees all interactions are represented, but changes the scale of them
    Removes element greater than max(S2)*threshold"""

    new_ST = np.clip(sum_rows, 0, 100)
    new_mat = np.copy(mat)
    new_mat = np.clip(new_mat, 0, 100)

    # get diagonal
    diag = np.diagonal(mat)
    new_diag = np.minimum(diag, new_ST)

    # Fills diagonal with zero to compute the sum
    np.fill_diagonal(new_mat, 0.0)
    sum_S2 = np.sum(new_mat)
    sum_ST = np.sum(new_ST)

    # Globally rescale all the elements
    if sum_S2 >= sum_ST:
        f = sum_ST/sum_S2
        new_mat *= f

    # Locally rescale the lines
    for i in range(len(mat)):
        sum_S2_line = np.nansum(new_mat[i, :])
        if sum_S2_line >= new_ST[i] and sum_S2_line >= 1e-5:
            f = new_ST[i]/sum_S2_line
            new_mat[i, :] = f*new_mat[i, :]
            new_mat[:, i] = f*new_mat[:, i]

    # Remove irrelevant lines
    threshold = np.max(new_mat)*rel_threshold
    for i in range(len(mat)):
        for j in range(len(mat)):
            if new_mat[i, j] <= threshold:
                new_mat[i, j] = 0
                new_mat[j, i] = 0
                print("Removed elements {} {} from S2, inferior to threshold")
    np.fill_diagonal(new_mat, new_diag)
    return new_mat, new_ST

def chord_diagram(mat, sum_rows=None, names=None, order=None, sort="size",
                  colors=None, cmap=None, use_gradient=False, chord_colors=None, highlights=None, falpha_not_highlighted=0.5, alpha=0.7,
                  start_at=0, extent=360, width=0.1, pad=2., gap=0.03, chordwidth=0.7, min_chord_width=0,
                  fontsize=10, gap_out_S1=0.01, gap_in_S1 = 0.01, outer_radius=1,
                  with_ticks=True, ticks_to_label='two', tick_percent=2, tick_direction='in', tick_position='out', tick_clockwise=False,  # two or all
                  fontcolor="k", rotate_names=False, ax=None, show=False, ):
    """
    Plot a chord diagram. Draws a representation of many-to-many interactions between elements, given by an interaction matrix.

    Typical application: sensitivity analyses, the diagonal is the self interacting elements (=S1). The total index can be given using sum_rows.
    In which case the sensitivity matrix is reconditioned to take the higher interacting values first (prevent overflow of the diagram).

    The elements are represented by arcs proportional to their degree and the
    interactions (or fluxes) are drawn as chords joining two arcs:

    * for undirected chords, the size of the arc is proportional to its
      out-degree (or simply its degree if the matrix is fully symmetrical), i.e.
      the sum of the element's row.

    Parameters
    ----------
    mat : square matrix. Note: if sum_rows is given, it will be automatically reconditioned.
        Flux data, ``mat[i, j]`` is the flux from i to j.
    sum_rows : vector. Fraction of the circle for each row (replaces sum(row)).
    names : list of str, optional (default: no names)
        Names of the nodes that will be displayed (must be ordered as the
        matrix entries).
    order : list, optional (default: order of the matrix entries)
        Order in which the arcs should be placed around the trigonometric
        circle.
    sort : str, optional (default: "size")
        Order in which the chords should be sorted: either None (unsorted),
        "size" (default, drawing largest chords first), or "distance"
        (drawing the chords of the two closest arcs at each end of the current
        arc, then progressing towards the connexions with the farthest arcs in
        both drections as we move towards the center of the current arc).
    colors : list, optional (default: from `cmap`)
        List of user defined colors or floats.
    cmap : str or colormap object (default: viridis)
        Colormap that will be used to color the arcs and chords by default.
        See `chord_colors` to use different colors for chords.
    use_gradient : bool, optional (default: False)
        Whether a gradient should be use so that chord extremities have the
        same color as the arc they belong to.
    chord_colors : str, or list of colors, optional (default: None)
        Specify color(s) to fill the chords differently from the arcs.
        When the keyword is not used, chord colors default to the colomap given
        by `colors`.
        Possible values for `chord_colors` are:

        * a single color (do not use an RGB tuple, use hex format instead),
          e.g. "red" or "#ff0000"; all chords will have this color
        * a list of colors, e.g. ``["red", "green", "blue"]``, one per node
          (in this case, RGB tuples are accepted as entries to the list).
          Each chord will get its color from its associated source node, or
          from both nodes if `use_gradient` is True.
    alpha : float in [0, 1], optional (default: 0.7)
        Opacity of the chord diagram.
    start_at : float, optional (default : 0)
        Location, in degrees, where the diagram should start on the unit circle.
        Default is to start at 0 degrees, i.e. (x, y) = (1, 0) or 3 o'clock),
        and move counter-clockwise
    extent : float, optional (default : 360)
        The angular aperture, in degrees, of the diagram.
        Default is to use the whole circle, i.e. 360 degrees, but in some cases
        it can be useful to use only a part of it.
    width : float, optional (default: 0.1)
        Width/thickness of the ideogram arc.
    pad : float, optional (default: 2)
        Distance between two neighboring ideogram arcs. Unit: degree.
    gap : float, optional (default: 0)
        Distance between the arc and the beginning of the cord.
    chordwidth : float, optional (default: 0.7)
        Position of the control points for the chords, controlling their shape.
    min_chord_width : float, optional (default: 0)
        Minimal chord width to replace small entries and zero reciprocals in
        the matrix.
    fontsize : float, optional (default: 12.8)
        Size of the fonts for the names.
    fontcolor : str or list, optional (default: black)
        Color of the fonts for the names.
    rotate_names : (list of) bool(s), optional (default: False)
        Whether to rotate all names (if single boolean) or some of them (if
        list) by 90°.
    ax : matplotlib axis, optional (default: new axis)
        Matplotlib axis where the plot should be drawn.
    show : bool, optional (default: False)
        Whether the plot should be displayed immediately via an automatic call
        to `plt.show()`.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots()

    mat = np.array(mat, copy=True)

    num_nodes = mat.shape[0]

    # set min entry size for small entries and zero reciprocals
    # mat[i, j]:  i -> j
    if min_chord_width:
        nnz = mat > 0

        mat[nnz] = np.maximum(mat[nnz], min_chord_width)

        # check zero reciprocals
        for i, j in zip(*np.where(~nnz)):
            if mat[j, i]:
                mat[i, j] = min_chord_width

    # check name rotations
    if isinstance(rotate_names, Sequence):
        assert len(rotate_names) == num_nodes, \
            "Wrong number of entries in 'rotate_names'."
    else:
        rotate_names = [rotate_names]*num_nodes

    # check order
    if order is not None:
        mat = mat[order][:, order]

        rotate_names = [rotate_names[i] for i in order]

        if names is not None:
            names = [names[i] for i in order]

        if colors is not None:
            colors = [colors[i] for i in order]

    # configure colors
    if highlights is None:
        highlights = [True]*num_nodes

    if colors is None:
        colors = np.linspace(0, 1, num_nodes)

    if isinstance(fontcolor, str):
        fontcolor = [fontcolor]*num_nodes
    else:
        assert len(fontcolor) == num_nodes, \
            "One fontcolor per node is required."

    if cmap is None:
        cmap = mpl.colormaps["viridis"]
    elif not isinstance(cmap, Colormap):
        cmap = mpl.colormaps[cmap]

    if isinstance(colors, (list, tuple, np.ndarray)):
        assert len(colors) == num_nodes, "One color per node is required."

        # check color type
        first_color = colors[0]

        if isinstance(first_color, (int, float, np.integer)):
            colors = cmap(colors)[:, :3]
        else:
            colors = [ColorConverter.to_rgb(c) for c in colors]
    else:
        raise ValueError("`colors` should be a list.")

    if chord_colors is None:
       chord_colors = colors
    else:
        try:
            chord_colors = [ColorConverter.to_rgb(chord_colors)] * num_nodes
        except ValueError:
            assert len(chord_colors) == num_nodes, \
                "If `chord_colors` is a list of colors, it should include " \
                "one color per node (here {} colors).".format(num_nodes)

    # sum over rows
    if sum_rows is None:
        degree = mat.sum(axis=1)  # = sum S1 + S2
    else:
        mat, degree = condition_matrices_rescaling(mat, np.array(sum_rows))
        # degree = sum_rows

    # compute all values and optionally apply sort
    arc, rotation, nodePos, pos = compute_positions_v2(mat, degree, start_at, sort, extent, pad, outer_radius)

    # plot
    for i in range(num_nodes):
        color = colors[i]

        alphai = alpha if highlights[i] else alpha*falpha_not_highlighted

        # plot the arcs
        start_at, end = arc[i]

        ideogram_arc(start=start_at, end=end, radius=outer_radius, color=color,
                     width=width, alpha=alphai, ax=ax)

        if tick_position == 'out':
            tick_radius = outer_radius
        else:
            tick_radius = outer_radius-width
        angular_graduations(tick_radius, start_at, end, total_arc_length(extent, pad, num_nodes), ax=ax, with_ticks=with_ticks,
                            ticks_to_label=ticks_to_label, tick_percent=tick_percent, tick_direction=tick_direction, tick_clockwise=tick_clockwise,
                            alpha=min(1.0, alphai*1.2), color=color)
        chord_color = chord_colors[i]

        # plot self-chords if directed is False
        if mat[i, i]:
            start1, end1, _, _ = pos[(i, i)]
            if is_light_color(chord_color, base=1):
                color_chord = adjust_lightness_1(chord_color, amount=0.9)
            else:
                color_chord = adjust_lightness_1(chord_color, amount=1.2)
            self_chord_arc(start1, end1, radius_out=outer_radius-width-gap_out_S1, radius_in=outer_radius - width - gap + gap_in_S1,
                           color=color_chord,
                           alpha=alphai, ax=ax)

        # plot all other chords
        targets = range(i)

        for j in targets:
            cend = chord_colors[j]

            alphaij = alpha if (highlights[i] and highlights[j]) else alpha*falpha_not_highlighted

            start1, end1, start2, end2 = pos[(i, j)]

            if mat[i, j] > 0 or mat[j, i] > 0:
                chord_arc(
                    start1, end1, start2, end2, radius=outer_radius - width - gap,
                    chordwidth=chordwidth, color=chord_color, cend=cend,
                    alpha=alphaij, ax=ax, use_gradient=use_gradient,
                    extent=extent)

    # add names if necessary
    if names is not None:

        assert len(names) == num_nodes, "One name per node is required."

        prop = {
            "fontsize": fontsize,
            "ha": "center",
            "va": "center",
            "rotation_mode": "anchor"
        }

        for i, (pos, name, r) in enumerate(zip(nodePos, names, rotation)):
            alphai = alpha if highlights[i] else alpha*falpha_not_highlighted

            f = 1.1
            ax.text(pos[0]*f, pos[1]*f, name, va="center", ha="center", color=adjust_lightness_1(colors[i], amount=0.5), alpha=min(1.0, 1.2*alphai))

    # configure axis
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)

    ax.set_aspect(1)
    ax.axis('off')

    plt.tight_layout()

    if show:
        plt.show()

    return nodePos


# ------------ #
# Subfunctions #
# ------------ #

def initial_path(start, end, radius, width, factor=4/3):
    ''' First 16 vertices and 15 instructions are the same for everyone '''
    if start > end:
        start, end = end, start

    start *= np.pi/180.
    end   *= np.pi/180.

    # optimal distance to the control points
    # https://stackoverflow.com/questions/1734745/
    # how-to-create-circle-with-b%C3%A9zier-curves
    # use 16-vertex curves (4 quadratic Beziers which accounts for worst case
    # scenario of 360 degrees)
    inner = radius*(1-width)
    opt   = factor * np.tan((end-start)/ 16.) * radius
    inter1 = start*(3./4.)+end*(1./4.)
    inter2 = start*(2./4.)+end*(2./4.)
    inter3 = start*(1./4.)+end*(3./4.)

    verts = [
        polar2xy(radius, start),
        polar2xy(radius, start) + polar2xy(opt, start+0.5*np.pi),
        polar2xy(radius, inter1) + polar2xy(opt, inter1-0.5*np.pi),
        polar2xy(radius, inter1),
        polar2xy(radius, inter1),
        polar2xy(radius, inter1) + polar2xy(opt, inter1+0.5*np.pi),
        polar2xy(radius, inter2) + polar2xy(opt, inter2-0.5*np.pi),
        polar2xy(radius, inter2),
        polar2xy(radius, inter2),
        polar2xy(radius, inter2) + polar2xy(opt, inter2+0.5*np.pi),
        polar2xy(radius, inter3) + polar2xy(opt, inter3-0.5*np.pi),
        polar2xy(radius, inter3),
        polar2xy(radius, inter3),
        polar2xy(radius, inter3) + polar2xy(opt, inter3+0.5*np.pi),
        polar2xy(radius, end) + polar2xy(opt, end-0.5*np.pi),
        polar2xy(radius, end)
    ]

    codes = [
        Path.MOVETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
    ]

    return start, end, verts, codes


def ideogram_arc(start, end, radius=1., width=0.2, color="r", alpha=0.7,
                 ax=None):
    '''
    Draw an arc symbolizing a region of the chord diagram.

    Parameters
    ----------
    start : float (degree in 0, 360)
        Starting degree.
    end : float (degree in 0, 360)
        Final degree.
    radius : float, optional (default: 1)
        External radius of the arc.
    width : float, optional (default: 0.2)
        Width of the arc.
    ax : matplotlib axis, optional (default: not plotted)
        Axis on which the arc should be plotted.
    color : valid matplotlib color, optional (default: "r")
        Color of the arc.
    '''
    start, end, _, _ = initial_path(start, end, radius, width)

    patch = patches.Wedge((0,0), radius, start*180/np.pi, end*180/np.pi, width=width, facecolor=color, alpha=alpha, lw=0)
    ax.add_patch(patch)


def chord_arc(start1, end1, start2, end2, radius=1.0, pad=2,
              chordwidth=0.7, ax=None, color="r", cend="r", alpha=0.7,
              use_gradient=False, extent=360):
    '''
    Draw a chord between two regions (arcs) of the chord diagram.

    Parameters
    ----------
    start1 : float (degree in 0, 360)
        Starting degree.
    end1 : float (degree in 0, 360)
        Final degree.
    start2 : float (degree in 0, 360)
        Starting degree.
    end2 : float (degree in 0, 360)
        Final degree.
    radius : float, optional (default: 1)
        External radius of the arc.
    gap : float, optional (default: 0)
        Distance between the arc and the beginning of the cord.
    chordwidth : float, optional (default: 0.2)
        Width of the chord.
    ax : matplotlib axis, optional (default: not plotted)
        Axis on which the chord should be plotted.
    color : valid matplotlib color, optional (default: "r")
        Color of the chord or of its beginning if `use_gradient` is True.
    cend : valid matplotlib color, optional (default: "r")
        Color of the end of the chord if `use_gradient` is True.
    alpha : float, optional (default: 0.7)
        Opacity of the chord.
    use_gradient : bool, optional (default: False)
        Whether a gradient should be use so that chord extremities have the
        same color as the arc they belong to.
    extent : float, optional (default : 360)
        The angular aperture, in degrees, of the diagram.
        Default is to use the whole circle, i.e. 360 degrees, but in some cases
        it can be useful to use only a part of it.
    directed : bool, optional (default: False)
        Whether the chords should be directed, ending in an arrow.

    Returns
    -------
    verts, codes : lists
        Vertices and path instructions to draw the shape.
    '''
    chordwidth2 = chordwidth

    dtheta1 = min((start1 - end2) % extent, (end2 - start1) % extent)
    dtheta2 = min((end1 - start2) % extent, (start2 - end1) % extent)

    start1, end1, verts, codes = initial_path(start1, end1, radius, chordwidth)
    start2, end2, verts2, _ = initial_path(start2, end2, radius, chordwidth)

    chordwidth2 *= np.clip(0.4 + (dtheta1 - 2*pad) / (15*pad), 0.2, 1)

    chordwidth *= np.clip(0.4 + (dtheta2 - 2*pad) / (15*pad), 0.2, 1)

    rchord  = radius * (1-chordwidth)
    rchord2 = radius * (1-chordwidth2)

    verts += [polar2xy(rchord, end1), polar2xy(rchord, start2)] + verts2

    verts += [
        polar2xy(rchord2, end2),
        polar2xy(rchord2, start1),
        polar2xy(radius, start1),
    ]

    # update codes

    codes += [
        Path.CURVE4,
        Path.CURVE4,
    ]

    codes += [
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
    ]

    codes += [
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
    ]

    if ax is not None:
        path = Path(verts, codes)

        if use_gradient:
            # find the start and end points of the gradient
            points, min_angle = None, None

            if dtheta1 < dtheta2:
                points = [
                    polar2xy(radius, start1),
                    polar2xy(radius, end2),
                ]

                min_angle = dtheta1
            else:
                points = [
                    polar2xy(radius, end1),
                    polar2xy(radius, start2),
                ]

                min_angle = dtheta1

            # make the patch
            patch = patches.PathPatch(path, facecolor="none",
                                      edgecolor="none", lw=LW)
            ax.add_patch(patch)  # this is required to clip the gradient

            # make the grid
            x = y = np.linspace(-1, 1, 50)
            meshgrid = np.meshgrid(x, y)

            gradient(points[0], points[1], min_angle, color, cend, meshgrid,
                     patch, ax, alpha)
        else:
            patch = patches.PathPatch(path, facecolor=color, alpha=alpha,
                                      edgecolor=color, lw=LW)

            idx = 16

            ax.add_patch(patch)

    return verts, codes


def self_chord_arc(start, end, radius_out=1.0, radius_in=0.9, ax=None,
                   color=(1,0,0), alpha=0.7):
    start, end, _, _ = initial_path(start, end, radius_out, 0)

    patch = patches.Wedge((0,0), radius_out, start*180/np.pi, end*180/np.pi,
                          width=radius_out-radius_in, facecolor=color, alpha=alpha, edgecolor=color, lw=LW)

    if ax is not None:
        ax.add_patch(patch)


def angular_graduations(radius, start, stop, total_arc_length, ax=None,
                        with_ticks=True, ticks_to_label='all', tick_percent=2, tick_direction='in', alpha=0.5,
                        color=None,
                        tick_clockwise=False):
    interval = tick_percent/100
    space_ticks = total_arc_length*interval  # In degree

    if color is None:
        color = 'k'

    if is_light_color(color, base=1):
        color_graduations = adjust_lightness_1(color, 0.5)
    else:
        color_graduations = 'w' #adjust_lightness_1(color, 10)
    num_even = int(np.floor((stop-start)/space_ticks)) # In degree
    if tick_clockwise:
        theta1 = stop
        theta2 = stop - num_even*space_ticks
    else:
        theta1 = start
        theta2 = start + num_even * space_ticks
    radius = radius
    # patch = patches.Arc((0,0), radius*2, radius*2, theta1=theta1, theta2=theta2, color=color_graduations, linewidth=1.2)

    if ax is not None:
        # ax.add_patch(patch)

        if with_ticks:
            for i in range(num_even+1):
                if tick_clockwise:
                    angle = (stop-i*space_ticks)*np.pi/180
                else:
                    angle = (start + i*space_ticks)*np.pi/180

                if tick_direction == 'out':
                    xb, yb = polar2xy(radius*1.02, angle)
                    xe, ye = polar2xy(radius, angle)
                    xt, yt = polar2xy(radius*1.05, angle)
                else:
                    xb, yb = polar2xy(radius*0.995, angle)
                    xe, ye = polar2xy(radius * 0.99, angle)
                    xt, yt = polar2xy(radius*0.94, angle)

                ax.plot([xb, xe], [yb, ye], lw=1, color=color_graduations)

                if ticks_to_label=='all':
                    do_ticks = True
                elif ticks_to_label=='two':
                    do_ticks = i==num_even-1
                else:
                    do_ticks = False

                if do_ticks and i!=0:
                    rot_text = angle*180/np.pi-90
                    if 180<=start<=360 and 180<=stop<=360:
                        rot_text -= 180
                    va='center'
                    ha = 'center'
                    ax.text(xt, yt, "{}".format(int(i*interval*100)), horizontalalignment=ha, verticalalignment=va, fontsize='xx-small', rotation=rot_text, alpha=alpha, color=color_graduations)
