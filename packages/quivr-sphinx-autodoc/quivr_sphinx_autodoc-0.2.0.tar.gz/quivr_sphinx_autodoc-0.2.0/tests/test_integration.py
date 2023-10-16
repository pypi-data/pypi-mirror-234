import os
import shutil
import subprocess


def test_integration(tmp_path):
    # Copy ./integration_test_src to tmp_dir
    src_dir = os.path.join(os.path.dirname(__file__), "integration_test_src")
    dst_dir = os.path.join(tmp_path, "test")
    shutil.copytree(src_dir, dst_dir)

    # Run sphinx-build in tmp_dir
    subprocess.check_call(["sphinx-build", "-b", "singlehtml", ".", "testoutput"], cwd=dst_dir)  # noqa: S603,S607
