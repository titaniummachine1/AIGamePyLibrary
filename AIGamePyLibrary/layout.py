"""Chain layout: rows follow top-input chains, columns give every wire its
2-square entry gap.

Rules (left -> right, top -> bottom):
  1. the top input port of a node defines its row: a chain feeder sits flat
     on its consumer's row, so the main pipeline runs dead straight
  2. secondary feeders stack downward, one 64px row each
  3. a commutative node (add/multiply/and/...) with one pure source and one
     chain feeder wires the SOURCE into the top port, so the flat wire is
     the source's (Ball Speed -> Multiply stays horizontal)
  4. columns work right-to-left from the sink: every feeder's exit sits a
     64px gap left of its consumer's entry (2 grid squares, no more unless
     occlusion forces it)
  5. a wide Get node with a 256-wide sibling input aligns its center with
     the sibling's left edge (Court Width over Float 0,5, Ball Speed over
     Multiply, Is Serve Phase over NOT); with no sibling it keeps a full
     wide step from its consumer
  6. a node that would intersect an already-placed box slides left in grid
     steps until clear - occlusion is the only thing allowed to grow a gap

Hard constraints: no two node boxes ever intersect, everything snaps to the
editor grid (x = 2 mod 32, y = 26 mod 32).
"""
import math

from .data import NODE_SIZES, DEFAULT_NODE_SIZE, DROPDOWN_OPTIONS
from .lib import _set_layout_position, data

GRID = 32
PIVOT = (2, -6)   # node anchors: x = 2 mod 32, y = 26 mod 32
GAP = 64          # 2 squares: producer exit -> consumer entry
WIDE_STEP = 512   # wide Get without a sibling: consumer center - 512
ROW = 64          # row pitch for secondary feeders

# nodes whose port stack renders taller than the prefab height
_EXTRA_HEIGHT = {"Vector3Split": 96}

# dropdown Get nodes show a selector: their interactive box is narrower
# than the serialized width, so collision tests use the narrower box
_NARROW_PREFIXES = ("TennisGet", "ParkingGet", "SoccerGet", "RacingV2Get",
                    "DemoDerbyGet", "SurvivalGet")

_COMMUTATIVE = {"AddFloats", "MultiplyFloats", "AddVector3", "And", "Or", "Xor"}


def _dims(node_id):
    w, h = NODE_SIZES.get(node_id, DEFAULT_NODE_SIZE)
    return w, max(h, _EXTRA_HEIGHT.get(node_id, 0))


def _col_box_w(node_id):
    w, _ = _dims(node_id)
    if node_id.startswith(_NARROW_PREFIXES):
        w = 256
    return w


def _port_sort_key(node_id, port_id):
    if node_id == "TimePlot":
        order = ("String1", "Color1", "String2", "Float1", "Float2", "Float3")
        return order.index(port_id) if port_id in order else 99
    for suffix in ("3", "2", "1"):
        if port_id.endswith(suffix):
            return int(suffix) - 1
    return 99


def _in_ports_visual(node):
    """Input port sIDs, top-first (creation order is NOT visual order)."""
    ins = [p for p in node["serializablePorts"] if p.get("polarity") == 0]
    ins.sort(key=lambda p: _port_sort_key(node["id"], p["id"]))
    return [p["sID"] for p in ins]


def _is_commutative(node):
    if node["id"] in _COMMUTATIVE:
        return True
    opts = DROPDOWN_OPTIONS.get(node["id"])
    mod = str(node.get("modifier", ""))
    if opts and mod.isdigit():
        label = opts[int(mod) % len(opts)].casefold()
        if node["id"] == "CompareBool":
            return label in ("and", "or", "xor")
        if node["id"] == "CompareFloats":
            return label in ("==", "!=")
    return False


def _box(n, x, y):
    w = _col_box_w(n["id"])
    _, h = _dims(n["id"])
    return (x - w / 2.0, y - h / 2.0, x + w / 2.0, y + h / 2.0)


def _intersect(a, b):
    return (min(a[2], b[2]) - max(a[0], b[0]) > 0.5 and
            min(a[3], b[3]) - max(a[1], b[1]) > 0.5)


def _snap(v):
    return round((v - PIVOT[0]) / GRID) * GRID + PIVOT[0]


def direct_layout(tune=True):
    """Arrange the graph by the rules in the module docstring.
    Returns the wire fitness of the result."""
    nodes = data["serializableNodes"]
    if not nodes:
        return 0.0
    sid2n = {n["sID"]: n for n in nodes}

    port_node = {}
    for n in nodes:
        for p in n.get("serializablePorts", []):
            port_node[p["sID"]] = (n, p)

    in_wires = {n["sID"]: [] for n in nodes}
    out_wires = {n["sID"]: [] for n in nodes}
    for c in data["serializableConnections"]:
        a = port_node.get(c.get("port0SID"))
        b = port_node.get(c.get("port1SID"))
        if not a or not b or a[0]["sID"] == b[0]["sID"]:
            continue
        prod, cons = (a, b) if a[1].get("polarity") == 1 else (b, a)
        in_wires[cons[0]["sID"]].append(
            {"prod": prod[0]["sID"], "port": cons[1]["sID"], "conn": c})
        out_wires[prod[0]["sID"]].append(cons[0]["sID"])

    # rule 3: pure source onto the top port of a commutative node
    for sid, wires in in_wires.items():
        if len(wires) != 2 or len({w["prod"] for w in wires}) != 2:
            continue
        if not _is_commutative(sid2n[sid]):
            continue
        top, bot = wires
        top_chain = bool(in_wires.get(top["prod"]))
        bot_source = not in_wires.get(bot["prod"])
        if not (top_chain and bot_source):
            continue
        visual = _in_ports_visual(sid2n[sid])
        if len(visual) < 2:
            continue
        for w, port in ((top, visual[1]), (bot, visual[0])):
            key = "port0SID" if w["conn"].get("port0SID") == w["port"] else "port1SID"
            w["conn"][key] = port
            w["port"] = port

    for sid in in_wires:
        port_order = {p: i for i, p in enumerate(_in_ports_visual(sid2n[sid]))}
        in_wires[sid].sort(key=lambda w: port_order.get(w["port"], 99))

    sinks = [n["sID"] for n in nodes if not out_wires[n["sID"]]]
    if not sinks:
        sinks = [nodes[-1]["sID"]]

    # rows (rules 1-2): top feeder shares the row, the rest stack downward
    assigned_y = {}
    cur_row = 26.0

    def assign_rows(sid, y, seen):
        nonlocal cur_row
        if sid in assigned_y or sid in seen:
            return
        seen.add(sid)
        assigned_y[sid] = y
        for w in in_wires.get(sid, []):
            if w["prod"] in assigned_y:
                continue
            if w is in_wires[sid][0]:
                assign_rows(w["prod"], y, seen)
            else:
                cur_row -= ROW
                assign_rows(w["prod"], cur_row, seen)

    seen = set()
    for s in sinks:
        if s not in assigned_y:
            if seen:
                cur_row -= ROW
            assign_rows(s, cur_row, seen)

    # columns (rules 4-6): right-to-left from the sink
    levels = {}

    def level(sid, seen=()):
        if sid in levels:
            return levels[sid]
        if sid in seen:
            return 0
        ins = [w["prod"] for w in in_wires.get(sid, [])]
        lv = 1 + max((level(p, seen + (sid,)) for p in ins), default=0) if ins else 0
        levels[sid] = lv
        return lv

    for n in nodes:
        level(n["sID"])

    max_lvl = max(levels.values())
    sink_x = _snap(226 + max_lvl * 320)
    assigned_x = {s: sink_x for s in sinks}
    ideal_x = {s: sink_x for s in sinks}
    placed = [(sink_x, assigned_y[s], _box(sid2n[s], sink_x, assigned_y[s]))
              for s in sinks]

    by_level = {}
    for sid, lv in levels.items():
        by_level.setdefault(lv, []).append(sid)

    for lv in sorted(by_level, reverse=True):
        for u in by_level[lv]:
            ux = assigned_x[u]
            uy = assigned_y[u]
            uw = _dims(sid2n[u]["id"])[0]
            u_left = ux - uw / 2.0
            inputs = in_wires.get(u, [])
            chains = [w for w in inputs if in_wires.get(w["prod"])]
            sources = [w for w in inputs if not in_wires.get(w["prod"])]
            # narrow siblings first, so a wide Get can align to their edge
            sources.sort(key=lambda w: _dims(sid2n[w["prod"]]["id"])[0] > 256)
            first_chain_x = None
            for w in chains + sources:
                p = w["prod"]
                if p in assigned_x:
                    assigned_x[p] = min(assigned_x[p], u_left - GAP
                                        - _dims(sid2n[p]["id"])[0] / 2.0)
                    continue
                pw, _ = _dims(sid2n[p]["id"])
                x = u_left - GAP - pw / 2.0
                if w in chains and first_chain_x is not None:
                    # a fan-out chain branch runs as its own channel one
                    # full column left (Split Vector3 pair), a leaf tail
                    # stacks in the same column (Operation over Multiply)
                    if len(out_wires[p]) > 1:
                        x = first_chain_x - 320
                sibs = [q for q in (chains + sources) if q is not w
                        and _dims(sid2n[q["prod"]]["id"])[0] <= 256
                        and q["prod"] in assigned_x]
                if pw > 256:
                    if sibs:
                        x = assigned_x[sibs[0]["prod"]] - 128
                    else:
                        x = ux - WIDE_STEP
                x = _snap(x)
                x = _snap(x)
                ideal_x[p] = x  # pre-slide target, for _restore_x
                box = _box(sid2n[p], x, assigned_y[p])
                for _ in range(24):  # box overlap: slide left only
                    if not any(_intersect(box, pb) for _, _, pb in placed):
                        break
                    x -= GRID
                    box = _box(sid2n[p], x, assigned_y[p])
                assigned_x[p] = x
                if w in chains and first_chain_x is None:
                    first_chain_x = x
                placed.append((x, assigned_y[p], box))

    for sid, n in sid2n.items():
        _set_layout_position(n["serializableRectTransform"],
                             assigned_x.get(sid, 34.0),
                             assigned_y.get(sid, 26.0))
    _nudge_rows()
    _restore_x(sid2n, ideal_x)
    _slide_overlaps(sid2n)
    _push_apart()
    return wire_fitness()


def _restore_x(sid2n, ideal_x):
    """After row nudges remove the reason for a left-slide, walk a node
    back right to its ideal column - but only when the FULL walk is clear;
    a node still blocked (CompareBool beside Is Serve Phase) keeps its
    slid position."""
    nodes = data["serializableNodes"]
    sid2t = {n["sID"]: n["serializableRectTransform"] for n in nodes}
    for sid, n in sid2n.items():
        t = sid2t[sid]
        x0 = t["anchoredPosition"]["x"]
        ideal = ideal_x.get(sid, x0)
        steps = int(round((ideal - x0) / GRID))
        if steps <= 0:
            continue
        other = [_box(sid2n[m], sid2t[m]["anchoredPosition"]["x"],
                      sid2t[m]["anchoredPosition"]["y"])
                 for m in sid2n if m != sid]
        clear = True
        for k in range(1, steps + 1):
            box = _box(n, x0 + k * GRID, t["anchoredPosition"]["y"])
            if any(_intersect(box, b) for b in other):
                clear = False
                break
        if clear:
            _set_layout_position(t, ideal, t["anchoredPosition"]["y"])


def _slide_overlaps(sid2n):
    """Box-overlap repair: slide the offending chain node (with its entire
    upstream closure) left in grid steps until clear. Sources never move;
    downstream consumers keep their gaps."""
    nodes = data["serializableNodes"]
    sid2t = {n["sID"]: n["serializableRectTransform"] for n in nodes}
    port_node = {p["sID"]: n for n in nodes for p in n.get("serializablePorts", [])}
    ins = {n["sID"]: set() for n in nodes}
    for c in data["serializableConnections"]:
        a, b = port_node.get(c.get("port0SID")), port_node.get(c.get("port1SID"))
        if not a or not b or a["sID"] == b["sID"]:
            continue
        pa = next(p for p in a["serializablePorts"] if p["sID"] == c["port0SID"])
        prod, cons = (a, b) if pa.get("polarity") == 1 else (b, a)
        ins[cons["sID"]].add(prod["sID"])

    def closure(sid):
        seen, stack = {sid}, [sid]
        while stack:
            u = stack.pop()
            for v in ins[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        return seen

    def overlaps():
        boxes = [(n["sID"],
                  _box(n, n["serializableRectTransform"]["anchoredPosition"]["x"],
                       n["serializableRectTransform"]["anchoredPosition"]["y"]))
                 for n in nodes]
        pairs = []
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                if _intersect(boxes[i][1], boxes[j][1]):
                    pairs.append((boxes[i][0], boxes[j][0]))
        return pairs

    for _ in range(40):
        pairs = overlaps()
        if not pairs:
            return
        a_sid, b_sid = pairs[0]
        # slide the non-source with the smaller x (the chain node)
        cands = [s for s in (a_sid, b_sid) if ins[s]]
        if not cands:
            cands = [a_sid]
        mover = min(cands, key=lambda s: sid2t[s]["anchoredPosition"]["x"])
        group = closure(mover)
        for _ in range(24):
            for s in group:
                t = sid2t[s]
                _set_layout_position(t, t["anchoredPosition"]["x"] - GRID,
                                     t["anchoredPosition"]["y"])
            if not any(mover in p for p in overlaps()):
                break
        else:
            break


def _violations():
    """(overlap count, wire-through-node count) of the current layout."""
    nodes = data["serializableNodes"]
    boxes = [_box(n,
                  n["serializableRectTransform"]["anchoredPosition"]["x"],
                  n["serializableRectTransform"]["anchoredPosition"]["y"])
             for n in nodes]
    overlaps = 0
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            if _intersect(boxes[i], boxes[j]):
                overlaps += 1
    segs = _wire_segments()
    clips = 0
    for prod, cons, p0, p1 in segs:
        own = {id(prod), id(cons)}
        for j, box in enumerate(boxes):
            if id(nodes[j]) in own:
                continue
            if _seg_hits_box((p0, p1), box):
                clips += 1
    return overlaps, clips


def _nudge_rows():
    """Wire-clip repair: slide a row (with the flat chain hanging off it)
    up/down in grid steps, but ONLY while a wire still passes through a
    node box. Overlaps never trigger it (the X-slide owns those), clean
    graphs are never touched, and a zigzag appears exactly where a wire
    would otherwise cut through a node."""
    nodes = data["serializableNodes"]
    sid2t = {n["sID"]: n["serializableRectTransform"] for n in nodes}
    port_node = {p["sID"]: n for n in nodes for p in n.get("serializablePorts", [])}
    outs = {n["sID"]: set() for n in nodes}
    ins = {n["sID"]: set() for n in nodes}
    for c in data["serializableConnections"]:
        a, b = port_node.get(c.get("port0SID")), port_node.get(c.get("port1SID"))
        if not a or not b or a["sID"] == b["sID"]:
            continue
        pa = next(p for p in a["serializablePorts"] if p["sID"] == c["port0SID"])
        prod, cons = (a, b) if pa.get("polarity") == 1 else (b, a)
        outs[prod["sID"]].add(cons["sID"])
        ins[cons["sID"]].add(prod["sID"])

    def clips():
        return _violations()[1]

    def flat_tail(sid):
        """sid plus same-row SOURCE neighbors upstream: carrying them keeps
        their flat wires flat without moving the clip target downstream."""
        tail, seen = [sid], {sid}
        i = 0
        while i < len(tail):
            u = tail[i]
            i += 1
            uy = sid2t[u]["anchoredPosition"]["y"]
            for v in ins[u]:
                if v not in seen and sid2t[v]["anchoredPosition"]["y"] == uy:
                    seen.add(v)
                    tail.append(v)
        return tail

    for _ in range(6):
        improved = False
        for n in sorted(nodes, key=lambda m:
                        -m["serializableRectTransform"]["anchoredPosition"]["x"]):
            if not clips():
                break
            before = clips()
            tail = flat_tail(n["sID"])
            old = [(u, sid2t[u]["anchoredPosition"]["x"],
                    sid2t[u]["anchoredPosition"]["y"]) for u in tail]
            for d in (GRID, -GRID, 2 * GRID, -2 * GRID):
                for u, ux, uy in old:
                    _set_layout_position(sid2t[u], ux, uy + d)
                if clips() < before:
                    improved = True
                    break
                for u, ux, uy in old:
                    _set_layout_position(sid2t[u], ux, uy)
        if not improved:
            break


def _push_apart():
    """Hard guarantee: no two node boxes may ever intersect. Pushes the
    lower node of an intersecting pair down in grid steps until clear."""
    nodes = data["serializableNodes"]
    for _ in range(200):
        boxes = [_box(n,
                      n["serializableRectTransform"]["anchoredPosition"]["x"],
                      n["serializableRectTransform"]["anchoredPosition"]["y"])
                 for n in nodes]
        lower = None
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                if _intersect(boxes[i], boxes[j]):
                    a, b = nodes[i], nodes[j]
                    lower = a if a["serializableRectTransform"]["anchoredPosition"]["y"] \
                        < b["serializableRectTransform"]["anchoredPosition"]["y"] else b
                    break
            if lower:
                break
        if not lower:
            return
        t = lower["serializableRectTransform"]
        _set_layout_position(t, t["anchoredPosition"]["x"],
                             t["anchoredPosition"]["y"] - GRID)


def _wire_segments():
    """Per connection: (prod_node, cons_node, (x0, y0), (x1, y1)) with
    endpoints at PORT height: producer output at node center, first input
    at consumer center, second input 32px below it."""
    nodes = data["serializableNodes"]
    if not nodes:
        return []
    sid2n = {n["sID"]: n for n in nodes}
    port_node = {p["sID"]: n for n in nodes for p in n.get("serializablePorts", [])}
    port_def = {}
    for n in nodes:
        ins = [p for p in n["serializablePorts"] if p.get("polarity") == 0]
        ins.sort(key=lambda p: _port_sort_key(n["id"], p["id"]))
        for i, p in enumerate(ins):
            port_def[p["sID"]] = -32.0 * i  # row offset from node center
        outs_list = [p for p in n["serializablePorts"] if p.get("polarity") == 1]
        # multi-output nodes (Vector3Split x/y/z) spread their rows around
        # the center; single outputs sit dead center
        mid = (len(outs_list) - 1) / 2.0
        for i, p in enumerate(outs_list):
            port_def[p["sID"]] = (mid - i) * 32.0

    segs = []
    for c in data["serializableConnections"]:
        a, b = port_node.get(c.get("port0SID")), port_node.get(c.get("port1SID"))
        if not a or not b or a["sID"] == b["sID"]:
            continue
        pa = next(p for p in a["serializablePorts"] if p["sID"] == c["port0SID"])
        prod, cons = (a, b) if pa.get("polarity") == 1 else (b, a)
        out_p = c["port0SID"] if prod is a else c["port1SID"]
        in_p = c["port1SID"] if prod is a else c["port0SID"]
        pw = _col_box_w(prod["id"])
        cw = _col_box_w(cons["id"])
        px = prod["serializableRectTransform"]["anchoredPosition"]["x"]
        py = prod["serializableRectTransform"]["anchoredPosition"]["y"]
        cx = cons["serializableRectTransform"]["anchoredPosition"]["x"]
        cy = cons["serializableRectTransform"]["anchoredPosition"]["y"]
        segs.append((prod, cons,
                     (px + pw / 2.0, py + port_def.get(out_p, 0.0)),
                     (cx - cw / 2.0, cy + port_def.get(in_p, 0.0))))
    return segs


def _seg_hits_box(seg, box):
    """True when the straight wire segment passes through a node box."""
    (x0, y0), (x1, y1) = seg
    bx0, by0, bx1, by1 = box
    if max(x0, x1) <= bx0 + 0.5 or min(x0, x1) >= bx1 - 0.5:
        return False
    if x1 == x0:
        y_at = lambda x: y0  # noqa: E731
    else:
        y_at = lambda x: y0 + (y1 - y0) * (x - x0) / (x1 - x0)  # noqa: E731
    for x in (max(x0, bx0), min(x1, bx1)):
        if min(x0, x1) - 0.5 <= x <= max(x0, x1) + 0.5:
            y = y_at(x)
            if by0 + 0.5 < y < by1 - 0.5:
                return True
    return False


def wire_fitness():
    """Per wire: 10 for a flat wire at the perfect 2-square gap, decaying
    exponentially with height and linearly with extra distance. A gap under
    2 squares, any box overlap, or a wire passing through a node is never
    worth trading for."""
    nodes = data["serializableNodes"]
    if not nodes:
        return 0.0

    total = 0.0
    segs = _wire_segments()
    for prod, cons, (x0, y0), (x1, y1) in segs:
        gap = x1 - x0
        dy = abs(y1 - y0)
        if gap < GAP - 0.5:
            total -= 1000.0
            continue
        total += max(0.0, 10.0 - (math.exp(dy / 32.0) - 1.0)
                     - 0.5 * abs(gap - GAP) / 32.0)

    boxes = [_box(n,
                  n["serializableRectTransform"]["anchoredPosition"]["x"],
                  n["serializableRectTransform"]["anchoredPosition"]["y"])
             for n in nodes]
    for i, seg in enumerate(segs):
        own = {id(segs[i][0]), id(segs[i][1])}
        for j, box in enumerate(boxes):
            if id(nodes[j]) in own:
                continue
            if _seg_hits_box((seg[2], seg[3]), box):
                total -= 1e6
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            if _intersect(boxes[i], boxes[j]):
                total -= 1e9
    return total
