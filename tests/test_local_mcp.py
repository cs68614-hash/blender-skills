import bpy
import fixtures as fx
from run_all import TMP, requires_gpu, skill_module


def bridge():
    return skill_module("blender-core", "mcp_bridge")


def state():
    sc = bpy.context.scene
    return (sc.frame_current, sc.frame_subframe, bpy.context.mode,
            bpy.context.view_layer.objects.active.name,
            tuple(sorted(o.name for o in bpy.context.selected_objects)),
            sc.render.engine, sc.camera.name if sc.camera else None,
            sc.render.image_settings.media_type, sc.render.image_settings.file_format,
            sc.render.image_settings.color_mode, sc.render.image_settings.color_depth,
            tuple((o.name, tuple(o.color), o.hide_render) for o in sc.objects))


def test_local_bridge_readonly_result():
    m = bridge()
    r = m.run("blender-core", "env_report")
    assert r["ok"] and r["background"]


def test_local_bridge_edit_mode_multiframe_restoration():
    requires_gpu()
    ob = fx.cube("ReviewCube")
    ob.color = (0.1, 0.2, 0.3, 0.4)
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    sc = bpy.context.scene
    sc.render.image_settings.file_format = "JPEG"
    sc.render.image_settings.color_mode = "BW"
    sc.frame_set(17, subframe=0.25)
    bpy.ops.object.mode_set(mode="EDIT")
    before = state()
    r = bridge().review(objects=[ob.name], mode="wire", frames=[1,10], views=["front","three_quarter"], res=96, out=str(TMP/"local_review.png"))
    assert state() == before, (before, state())
    assert len(r["reviews"]) == 2
    from pathlib import Path
    assert all(Path(x["sheet"]).stat().st_size > 100 for x in r["reviews"])
    assert sorted(o.name for o in sc.objects) == ["ReviewCube"]
    assert not bpy.data.cameras


def test_local_bridge_restoration_on_render_failure():
    ob = fx.cube("FailureCube")
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    sc = bpy.context.scene
    sc.render.image_settings.file_format = "JPEG"
    sc.render.image_settings.color_mode = "BW"
    bpy.ops.object.mode_set(mode="EDIT")
    m = bridge()
    shots = m._module("blender-asset-qa", "review_shots")
    original = shots.run
    def broken(**kw):
        bpy.ops.object.mode_set(mode="OBJECT")
        ob.color = (1,0,0,1)
        sc.render.image_settings.file_format = "PNG"
        sc.frame_set(33)
        raise RuntimeError("intentional render failure")
    before = state()
    shots.run = broken
    try:
        try:
            m.review(objects=[ob.name], frames=[10])
        except RuntimeError as e:
            assert str(e) == "intentional render failure"
        else:
            assert False, "expected failure"
        assert state() == before, (before, state())
    finally:
        shots.run = original
