import math


def _auto_bend_1(i, fd):
    p = fd.propagators[i]
    p.bend = True
    ref = []
    # collect all references to the same vertex
    for c in fd.propagators:
        if c.target == p.target:
            ref += [fd.get_point(c.source)]
        if c.source == p.target:
            ref += [fd.get_point(c.target)]
    sumrefx = 0
    sumrefy = 0
    me = fd.get_point(p.target)
    for r in ref:
        sumrefx += r.x - me.x
        sumrefy += r.y - me.y

    dire = "up"
    if sumrefy > 0:
        dire = "down"
    else:
        dire = "up"

    if dire == "up":
        b_in = 45
        b_out = 135
    if dire == "down":
        b_in = -45
        b_out = -135

    dire = math.atan2(sumrefy, sumrefx) * 180 / math.pi + 180
    b_in = dire + 45
    b_out = dire - 45
    p.style.setProperty("bend-in", b_in)
    p.style.setProperty("bend-out", b_out)
    p.style.setProperty("bend-min-distance", "2cm")
    p.style.setProperty("bend-loop", True)


def _auto_bend(pa, pb):
    if pa.target == pb.target and pa.source == pb.source:
        pa.style.setProperty("bend-direction", "right")
        pb.style.setProperty("bend-direction", "left")
    if pa.target == pb.source and pa.source == pb.target:
        pa.style.setProperty("bend-direction", "left")
        pb.style.setProperty("bend-direction", "left")


def _auto_bend_2(i, fd):
    objs = fd.propagators
    pa = objs[i]
    for j, pb in enumerate(objs):
        if i < j:
            _auto_bend(pa, pb)


def _auto_bend_3(i, fd):
    objs = fd.propagators
    pa = objs[i]
    for j, pb in enumerate(objs):
        for k, _ in enumerate(objs):
            # pc is the third propagator we keep it straight
            if i < j and j < k:
                _auto_bend(pa, pb)


# TODO bend legs?
def auto_bend(ifd):
    """Automatically bend lines to avoid overlaps."""
    fd = ifd
    objs = fd.propagators
    duplications = [0] * len(objs)

    # count duplications
    for i, pa in enumerate(objs):
        for _, pb in enumerate(objs):
            if pa.target == pb.target and pa.source == pb.source:
                duplications[i] += 1
            if pa.target == pb.source and pa.source == pb.target:
                duplications[i] += 1

    for i, pa in enumerate(objs):
        if duplications[i] == 1:
            pass
        elif duplications[i] == 2:
            _auto_bend_2(i, fd)
        elif duplications[i] == 3:
            _auto_bend_3(i, fd)
        else:
            raise ValueError(
                f"Too many propagators between the same vertices. {duplications[i]} propagators between {pa.target} and {pa.source}."
            )

            # print(pa.target, pb.target, pa.source, pb.source)

    # self linked tadpole
    for i, p in enumerate(objs):
        if p.target == p.source:
            _auto_bend_1(i, fd)
    return fd
