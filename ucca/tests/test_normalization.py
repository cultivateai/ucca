import pytest

from ucca import layer1
from ucca.normalization import normalize, COORDINATED_MAIN_REL
from .conftest import create_passage, attach_terminals

"""Tests normalization module correctness and API."""


def root_scene():
    p, l1, terms = create_passage()
    a1 = l1.add_fnode(None, layer1.EdgeTags.Participant)
    p1 = l1.add_fnode(None, layer1.EdgeTags.Process)
    a2 = l1.add_fnode(None, layer1.EdgeTags.Participant)
    attach_terminals(terms, a1, p1, a2)
    return p


def top_scene():
    p, l1, terms = create_passage()
    ps1 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    a1 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    p1 = l1.add_fnode(ps1, layer1.EdgeTags.Process)
    a2 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    attach_terminals(terms, a1, p1, a2)
    return p


def nested_center():
    p, l1, terms = create_passage(5)
    ps1 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    a1 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    f1 = l1.add_fnode(a1, layer1.EdgeTags.Function)
    c1 = l1.add_fnode(a1, layer1.EdgeTags.Center)
    f2 = l1.add_fnode(c1, layer1.EdgeTags.Function)
    c2 = l1.add_fnode(c1, layer1.EdgeTags.Center)
    p1 = l1.add_fnode(ps1, layer1.EdgeTags.Process)
    a2 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    attach_terminals(terms, f1, f2, c2, p1, a2)
    return p


def flat_center():
    p, l1, terms = create_passage(5)
    ps1 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    a1 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    f1 = l1.add_fnode(a1, layer1.EdgeTags.Function)
    f2 = l1.add_fnode(a1, layer1.EdgeTags.Function)
    c1 = l1.add_fnode(a1, layer1.EdgeTags.Center)
    p1 = l1.add_fnode(ps1, layer1.EdgeTags.Process)
    a2 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    attach_terminals(terms, f1, f2, c1, p1, a2)
    return p


def unary_center():
    p, l1, terms = create_passage(5)
    ps1 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    a1 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    c1 = l1.add_fnode(a1, layer1.EdgeTags.Center)
    f1 = l1.add_fnode(c1, layer1.EdgeTags.Function)
    f2 = l1.add_fnode(c1, layer1.EdgeTags.Function)
    c2 = l1.add_fnode(c1, layer1.EdgeTags.Center)
    p1 = l1.add_fnode(ps1, layer1.EdgeTags.Process)
    a2 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    attach_terminals(terms, f1, f2, c2, p1, a2)
    return p


def unary_function():
    p, l1, terms = create_passage(5)
    ps1 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    a1 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    f1 = l1.add_fnode(a1, layer1.EdgeTags.Function)
    f2 = l1.add_fnode(f1, layer1.EdgeTags.Function)
    c1 = l1.add_fnode(f1, layer1.EdgeTags.Center)
    c2 = l1.add_fnode(a1, layer1.EdgeTags.Center)
    p1 = l1.add_fnode(ps1, layer1.EdgeTags.Process)
    a2 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    attach_terminals(terms, f2, c1, c2, p1, a2)
    return p


def unary_participant():
    """
    Whenever there is an A as an only child, remove it.
    """
    p, l1, terms = create_passage()
    ps1 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    a = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    ps2 = l1.add_fnode(a, layer1.EdgeTags.ParallelScene)
    p1 = l1.add_fnode(ps2, layer1.EdgeTags.Process)
    linker = l1.add_fnode(a, layer1.EdgeTags.Linker)
    ps3 = l1.add_fnode(a, layer1.EdgeTags.ParallelScene)
    p2 = l1.add_fnode(ps3, layer1.EdgeTags.Process)
    attach_terminals(terms, p1, linker, p2)
    return p


def simple_linkage():
    """
    Whenever there is an A as an only child, remove it.
    """
    p, l1, terms = create_passage()
    ps1 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    p1 = l1.add_fnode(ps1, layer1.EdgeTags.Process)
    linker = l1.add_fnode(None, layer1.EdgeTags.Linker)
    ps2 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    p2 = l1.add_fnode(ps2, layer1.EdgeTags.Process)
    attach_terminals(terms, p1, linker, p2)
    return p


def simple_function():
    p, l1, terms = create_passage()
    ps1 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    a1 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    p1 = l1.add_fnode(ps1, layer1.EdgeTags.Process)
    f1 = l1.add_fnode(ps1, layer1.EdgeTags.Function)
    attach_terminals(terms, a1, p1, f1)
    return p


def complex_function():
    p, l1, terms = create_passage()
    ps1 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    a1 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    f1 = l1.add_fnode(ps1, layer1.EdgeTags.Function)
    p1 = l1.add_fnode(f1, layer1.EdgeTags.Process)
    c2 = l1.add_fnode(f1, layer1.EdgeTags.Center)
    attach_terminals(terms, a1, p1, c2)
    return p


def unary_punct():
    p, l1, terms = create_passage(3, 3)
    ps1 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    a1 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    p1 = l1.add_fnode(ps1, layer1.EdgeTags.Process)
    a2 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    attach_terminals(terms, a1, p1)
    l1.add_punct(a2, terms[2])
    return p


def unattached_punct():
    p, l1, terms = create_passage(3, 3)
    ps1 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    a1 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    p1 = l1.add_fnode(ps1, layer1.EdgeTags.Process)
    attach_terminals(terms, a1, p1)
    return p


def top_punct():
    p, l1, terms = create_passage(3, 3)
    ps1 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    a1 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    p1 = l1.add_fnode(ps1, layer1.EdgeTags.Process)
    attach_terminals(terms, a1, p1)
    l1.add_punct(None, terms[2])
    return p


def attached_punct():
    p, l1, terms = create_passage(3, 3)
    ps1 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    a1 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    p1 = l1.add_fnode(ps1, layer1.EdgeTags.Process)
    attach_terminals(terms, a1, p1)
    l1.add_punct(ps1, terms[2])
    return p


def top_punct_only():
    p, l1, terms = create_passage(1, 1)
    l1.add_punct(None, terms[0])
    return p


def moved_punct():
    p, l1, terms = create_passage(3, 3)
    ps1 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    a1 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    p1 = l1.add_fnode(ps1, layer1.EdgeTags.Process)
    attach_terminals(terms, a1, p1)
    l1.add_punct(a1, terms[2])
    return p


def multi_punct():
    p, l1, terms = create_passage(4, 3, 4)
    ps1 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    a1 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    p1 = l1.add_fnode(ps1, layer1.EdgeTags.Process)
    attach_terminals(terms, a1, p1)
    punct1 = l1.add_punct(ps1, terms[2])
    punct1.add(layer1.EdgeTags.Terminal, terms[3])
    return p


def split_punct():
    p, l1, terms = create_passage(4, 3, 4)
    ps1 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    a1 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    p1 = l1.add_fnode(ps1, layer1.EdgeTags.Process)
    attach_terminals(terms, a1, p1)
    l1.add_punct(ps1, terms[2])
    l1.add_punct(ps1, terms[3])
    return p


def cycle():
    p, l1, terms = create_passage()
    ps1 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    a1 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    p1 = l1.add_fnode(ps1, layer1.EdgeTags.Process)
    a2 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    l1.add_remote(a2, layer1.EdgeTags.Elaborator, ps1)
    attach_terminals(terms, a1, p1, a2)
    return p


def unanalyzable():
    p, l1, terms = create_passage(5)
    ps1 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    a1 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    p1 = l1.add_fnode(ps1, layer1.EdgeTags.Process)
    a2 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    attach_terminals(terms, a1, p1, a2, a2, a2)
    return p


def unanalyzable_punct():
    p, l1, terms = create_passage(5, 3, 4, 5)
    ps1 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    a1 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    p1 = l1.add_fnode(ps1, layer1.EdgeTags.Process)
    a2 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    attach_terminals(terms, a1, p1, a2, a2, a2)
    return p


def punct_inside_unanalyzable():
    p, l1, terms = create_passage(5, 4)
    ps1 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    a1 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    p1 = l1.add_fnode(ps1, layer1.EdgeTags.Process)
    a2 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    attach_terminals(terms, a1, p1, a2)
    a2.add(layer1.EdgeTags.Terminal, terms[4])
    l1.add_punct(a2, terms[3])
    return p


def unattached_punct_inside_unanalyzable():
    p, l1, terms = create_passage(5, 4)
    ps1 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    a1 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    p1 = l1.add_fnode(ps1, layer1.EdgeTags.Process)
    a2 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    attach_terminals(terms, a1, p1, a2)
    a2.add(layer1.EdgeTags.Terminal, terms[4])
    return p


def punct_outside_unanalyzable():
    p, l1, terms = create_passage(5, 5)
    ps1 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    a1 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    p1 = l1.add_fnode(ps1, layer1.EdgeTags.Process)
    a2 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    attach_terminals(terms, a1, p1, a2, a2)
    l1.add_punct(ps1, terms[4])
    return p


def unattached_punct_outside_unanalyzable():
    p, l1, terms = create_passage(5, 5)
    ps1 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    a1 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    p1 = l1.add_fnode(ps1, layer1.EdgeTags.Process)
    a2 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    attach_terminals(terms, a1, p1, a2, a2)
    return p


def unattached_terms():
    p, l1, terms = create_passage()
    ps1 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    a1 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    p1 = l1.add_fnode(ps1, layer1.EdgeTags.Process)
    attach_terminals(terms, a1, p1)
    return p


def attached_terms():
    p, l1, terms = create_passage()
    ps1 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    a1 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    p1 = l1.add_fnode(ps1, layer1.EdgeTags.Process)
    f1 = l1.add_fnode(ps1, layer1.EdgeTags.Function)
    attach_terminals(terms, a1, p1, f1)
    return p


def cmr_no_attrib():
    p, l1, terms = create_passage(4)
    ps1 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    a = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    p1 = l1.add_fnode(ps1, layer1.EdgeTags.Process)
    c1 = l1.add_fnode(p1, layer1.EdgeTags.Center)
    n = l1.add_fnode(p1, layer1.EdgeTags.Connector)
    c2 = l1.add_fnode(p1, layer1.EdgeTags.Center)
    attach_terminals(terms, a, c1, n, c2)
    return p


def insert_cmr(l1, scene):
    p = l1.add_fnode(scene, layer1.EdgeTags.Process)
    p.incoming[0].attrib[COORDINATED_MAIN_REL] = True
    c1 = l1.add_fnode(p, layer1.EdgeTags.Center)
    n = l1.add_fnode(p, layer1.EdgeTags.Connector)
    c2 = l1.add_fnode(p, layer1.EdgeTags.Center)
    return p, c1, n, c2


def cmr():
    p, l1, terms = create_passage(4)
    ps1 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    a = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    p1, c1, n, c2 = insert_cmr(l1, ps1)
    attach_terminals(terms, a, c1, n, c2)
    return p


def expanded_cmr():
    p, l1, terms = create_passage(4)
    ps1 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    linker = l1.add_fnode(None, layer1.EdgeTags.Linker)
    ps2 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    a = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    l1.add_remote(ps2, layer1.EdgeTags.Participant, a)
    p1 = l1.add_fnode(ps1, layer1.EdgeTags.Process)
    p2 = l1.add_fnode(ps2, layer1.EdgeTags.Process)
    attach_terminals(terms, a, p1, linker, p2)
    return p


def remote_cmr():
    p, l1, terms = create_passage(6)
    ps1 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    linker = l1.add_fnode(None, layer1.EdgeTags.Linker)
    ps2 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    a1 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    p1, c1, n, c2 = insert_cmr(l1, ps1)
    a2 = l1.add_fnode(ps2, layer1.EdgeTags.Participant)
    l1.add_remote(ps2, layer1.EdgeTags.Process, p1)
    attach_terminals(terms, a1, c1, n, c2, linker, a2)
    return p


def expanded_remote_cmr():
    p, l1, terms = create_passage(6)
    ps1 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    linker1 = l1.add_fnode(None, layer1.EdgeTags.Linker)
    ps2 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    linker2 = l1.add_fnode(None, layer1.EdgeTags.Linker)
    ps3 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    # ps4 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)  # ??? scene with only remotes
    a1 = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    l1.add_remote(ps2, layer1.EdgeTags.Participant, a1)
    p1 = l1.add_fnode(ps1, layer1.EdgeTags.Process)
    p2 = l1.add_fnode(ps2, layer1.EdgeTags.Process)
    a2 = l1.add_fnode(ps3, layer1.EdgeTags.Participant)
    l1.add_remote(ps3, layer1.EdgeTags.Process, p1)
    # l1.add_remote(ps4, layer1.EdgeTags.Process, p2)
    # l1.add_remote(ps4, layer1.EdgeTags.Participant, a2)  # ???
    attach_terminals(terms, a1, p1, linker1, p2, linker2, a2)
    return p


def cmr_with_relator_outside():
    """
    [suitable_S [for_R the_F [breeding_C and_N growing_C]_P|CMR [of_R giants_C]_A]_A]_H
    """
    p, l1, terms = create_passage(8)
    ps = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    s = l1.add_fnode(ps, layer1.EdgeTags.State)
    a_scene = l1.add_fnode(ps, layer1.EdgeTags.Participant)
    r1 = l1.add_fnode(a_scene, layer1.EdgeTags.Relator)
    f = l1.add_fnode(a_scene, layer1.EdgeTags.Function)
    p1, c1, n, c2 = insert_cmr(l1, a_scene)
    a2 = l1.add_fnode(a_scene, layer1.EdgeTags.Participant)
    r2 = l1.add_fnode(a2, layer1.EdgeTags.Relator)
    c3 = l1.add_fnode(a2, layer1.EdgeTags.Center)
    attach_terminals(terms, s, r1, f, c1, n, c2, r2, c3)
    return p


def expanded_cmr_with_relator_outside():
    """
    [suitable_S [for_R [[the_F breeding_C]_P [of_R giants_C]_A]_H and_L [[growing_P] [*of giants]_A]_H]_H
    """
    p, l1, terms = create_passage(8)
    ps1 = l1.add_fnode(None, layer1.EdgeTags.ParallelScene)
    s = l1.add_fnode(ps1, layer1.EdgeTags.State)
    a_superscene = l1.add_fnode(ps1, layer1.EdgeTags.Participant)
    r1 = l1.add_fnode(a_superscene, layer1.EdgeTags.Relator)
    ps2 = l1.add_fnode(a_superscene, layer1.EdgeTags.ParallelScene)
    linker = l1.add_fnode(a_superscene, layer1.EdgeTags.Linker)
    ps3 = l1.add_fnode(a_superscene, layer1.EdgeTags.ParallelScene)
    p1 = l1.add_fnode(ps2, layer1.EdgeTags.Process)
    f = l1.add_fnode(ps2, layer1.EdgeTags.Function)
    a = l1.add_fnode(ps2, layer1.EdgeTags.Participant)
    r2 = l1.add_fnode(a, layer1.EdgeTags.Relator)
    c2 = l1.add_fnode(a, layer1.EdgeTags.Center)
    p2 = l1.add_fnode(ps3, layer1.EdgeTags.Process)
    l1.add_remote(ps3, layer1.EdgeTags.Participant, a)
    attach_terminals(terms, s, r1, f, p1, linker, p2, r2, c2)
    return p


def normalize_and_compare(unnormalized, normalized, extra=False):
    p1 = unnormalized()
    p2 = normalized()
    if unnormalized != normalized:
        assert not p1.equals(p2), "Unnormalized and normalized passage: %s == %s" % (str(p1), str(p2))
    normalize(p1, extra=extra)
    assert p1.equals(p2), "Normalized passage: %s != %s" % (str(p1), str(p2))


@pytest.mark.parametrize("unnormalized, normalized", (
        (root_scene, top_scene),
        (nested_center, flat_center),
        (unary_center, flat_center),
        (unary_function, flat_center),
        (complex_function, simple_function),
        (unary_punct, attached_punct),
        (unattached_punct, attached_punct),
        (top_punct, attached_punct),
        (top_punct_only, top_punct_only),
        (moved_punct, attached_punct),
        (multi_punct, split_punct),
        (cycle, top_scene),
        (unanalyzable, unanalyzable),
        (unanalyzable_punct, unanalyzable_punct),
        (punct_inside_unanalyzable, punct_inside_unanalyzable),
        (unattached_punct_inside_unanalyzable, punct_inside_unanalyzable),
        (punct_outside_unanalyzable, punct_outside_unanalyzable),
        (unattached_punct_outside_unanalyzable, punct_outside_unanalyzable),
        (cmr_no_attrib, cmr_no_attrib),
        (cmr, expanded_cmr),
        (remote_cmr, expanded_remote_cmr),
        (cmr_with_relator_outside, expanded_cmr_with_relator_outside),
        (unary_participant, simple_linkage),
))
def test_normalize(unnormalized, normalized):
    normalize_and_compare(unnormalized, normalized)


@pytest.mark.parametrize("unnormalized, normalized", (
        (unattached_terms, attached_terms),
))
def test_normalize_extra(unnormalized, normalized):
    normalize_and_compare(unnormalized, normalized, extra=True)
