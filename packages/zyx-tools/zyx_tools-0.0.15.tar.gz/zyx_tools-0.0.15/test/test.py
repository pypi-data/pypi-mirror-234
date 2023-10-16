import sys

sys.path.append("../../tools")
from zyx_tools import SvnTool, OtherTool

"""
svn://192.168.0.12/flower/trunk/client/share_lib/ProjectSettings
svn://192.168.0.12/flower/trunk/res_url/share_assets/win/shaders
svn://192.168.0.12/flower/trunk/client/share_lib/Resources
svn://192.168.0.13/share_lib/trunk/client/doc/%E4%BB%A3%E7%A0%81%E9%A3%8E%E6%A0%BC/c%23
svn://192.168.0.12/flower/trunk/client/share_lib/flower_effect/Editor/ShaderVariantPreprocess.cs
svn://192.168.0.13/share_lib/trunk/client/xLua/Assets/xLua_Mini@3810
svn://192.168.0.12/flower/trunk/client/share_lib/cinemachine
svn://192.168.0.12/flower/trunk/client/share_lib/flower_anim/script
svn://192.168.0.12/flower/trunk/client/share_lib/flower_effect/script
svn://192.168.0.12/flower/trunk/client/share_lib/flower_scene/script
svn://192.168.0.12/flower/trunk/client/share_lib/NavMeshComponents193
svn://192.168.0.12/flower/trunk/client/share_lib/PostProcessing320
svn://192.168.0.12/flower/trunk/client/share_lib/Presets
svn://192.168.0.12/flower/trunk/client/share_lib/RootMotion
svn://192.168.0.12/flower/trunk/client/share_lib/Spine38/Runtime
svn://192.168.0.12/flower/trunk/client/share_lib/wwise/Deployment
svn://192.168.0.12/flower/trunk/client/share_lib/timeline
svn://192.168.0.13/share_lib/trunk/client/fast_ui/script
svn://192.168.0.13/share_lib/trunk/client/nogi_lib/download4
svn://192.168.0.13/share_lib/trunk/client/nogi_lib/network
svn://192.168.0.13/share_lib/trunk/client/nogi_lib/standard
svn://192.168.0.12/flower/trunk/client/share_lib/input_system
svn://192.168.0.12/flower/trunk/client/share_lib/level_design/Runtime
svn://192.168.0.13/share_lib/trunk/client/thridpart/ILReader/Core
"""


def Test_svn_exteral():
    # res = SvnTool.get_svn_externals(
    #     "svn://192.168.0.12/flower/trunk/client/WholeClient",
    #     "res_builder",
    #     "res_builder",
    # )
    # print("\r\n".join(res))
    res = SvnTool.get_svn_externals(
        "svn://192.168.0.12/flower/trunk/server/script/",
        "res_builder",
        "res_builder",
    )
    print("\r\n".join(res))


def test_svn_getlog():
    res = SvnTool.get_svn_log(
        "svn://192.168.0.12/flower/trunk/client/WholeClient",
        "2023-09-26",
        "2023-09-28",
        search="合并",
    )
    for item in res:
        print(item.json(exclude_none=True, ensure_ascii=False))


def test_svn_ls():
    # res = SvnTool.get_svn_ls("svn://192.168.0.12/flower/trunk/doc/scheme/data/tags/")
    # for item in res:
    #     print(item)
    try:
        res = SvnTool.get_svn_ls("svn://192.168.0.12/flower/trunk/client/WholeClient1")
        for item in res:
            print(item)
    except Exception as e:
        print(f"err:{e}")


if __name__ == "__main__":
    OtherTool.init_log()
    # Test_svn_exteral()
    # test_svn_getlog()
    test_svn_ls()
