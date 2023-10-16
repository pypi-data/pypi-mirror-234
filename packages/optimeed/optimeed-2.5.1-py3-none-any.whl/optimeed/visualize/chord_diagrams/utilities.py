"""
Utilities for the chord diagram.
"""

from collections import defaultdict
import numpy as np


def dist(points):
    '''
    Compute the distance between two points.

    Parameters
    ----------
    points : array of length 4
        The coordinates of the two points, P1 = (x1, y1) and P2 = (x2, y2)
        in the order [x1, y1, x2, y2].
    '''
    x1, y1 = points[0]
    x2, y2 = points[1]

    return np.sqrt((x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1))


def polar2xy(r, theta):
    '''
    Convert the coordinates of a point P from polar (r, theta) to cartesian
    (x, y).
    '''
    return np.array([r*np.cos(theta), r*np.sin(theta)])


def total_arc_length(extent, pad, num_nodes):
    """Return total arc length in degrees"""
    return extent - pad * num_nodes

def compute_positions_v2(mat, deg, start_at, sort,
                      extent, pad, outer_radius):
    num_nodes = len(deg)

    # find position for each start and end
    y = deg / np.sum(deg).astype(float) * total_arc_length(extent, pad, num_nodes)  # proportion of each arc w.r.t full circle
    starts = [start_at] + (
        start_at + np.cumsum(y + pad*np.ones(num_nodes))).tolist()

    out_ends = [s + d for s, d in zip(starts, y)]


    # relative positions within an arc
    rel_thickness_chord = [
        _get_normed_line(mat, i, deg, starts[i],
                         out_ends[i])
        for i in range(num_nodes)
    ]
    zin_mat = rel_thickness_chord

    # sort
    mat_ids = _get_sorted_ids(sort, rel_thickness_chord, num_nodes)

    pos = {}
    arc = []
    nodePos = []
    rotation = []

    # compute positions
    for i in range(num_nodes):
        # # DO ARCS !!
        start_arc = starts[i]
        end_arc = start_arc + y[i]
        arc.append((start_arc, end_arc))
        angle = 0.5*(start_arc + end_arc)-80

        rotation.append(False)

        nodePos.append(
            tuple(polar2xy(outer_radius*1.02, 0.5*(start_arc + end_arc)*np.pi/180.)) + (angle,))

        # # DO CHORDS !!
        z = rel_thickness_chord[i]
        z0 = start_arc
        for j in mat_ids[i]:
            # compute the arrival points
            zj = zin_mat[j]
            startj = starts[j]  # start of arc

            jids = mat_ids[j]

            stop = np.where(np.equal(jids, i))[0][0]

            startji = startj
            for index_jids in jids[:stop]:
                if index_jids != i:
                    startji += zj[index_jids]

            if i==j:
                pos[(i, j)] = (out_ends[i]-z[j], out_ends[i], None, None)
            else:
                pos[(i, j)] = (z0, z0 + z[j], startji, startji + zj[jids[stop]])
                # start1, end1, start2, end2 = pos[(i, j)]
            z0 += z[j]

    return arc, rotation, nodePos, pos

# In-file functions

def _get_normed_line(mat, i, x, start_degree, end_degree):
    vect = (mat[i, :] / x[i]) * (end_degree - start_degree)
    return vect


def _get_sorted_ids(sort, zmat, num_nodes):
    mat_ids = defaultdict(lambda: list(range(num_nodes)))

    if sort == "size":
        mat_ids = [np.argsort(z) for z in zmat]
    elif sort == "distance":
        mat_ids = []
        for i in range(num_nodes):
            remainder = 0 if num_nodes % 2 else -1
            ids = list(range(i - int(0.5*num_nodes), i))[::-1]
            # ids += [i]
            ids += list(range(i + int(0.5*num_nodes) + remainder, i, -1))

            # put them back into [0, num_nodes[
            ids = np.array(ids)
            ids[ids < 0] += num_nodes
            ids[ids >= num_nodes] -= num_nodes
            ids = ids.tolist()
            ids.append(i)
            mat_ids.append(ids)

    elif sort is not None:
        raise ValueError("Invalid `sort`: '{}'".format(sort))

    return mat_ids
