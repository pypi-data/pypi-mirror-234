import os
import logging

# This file will be at root of directory structure with all brickbundles (with only their .brick files and directory structure)

def package_dir():
    return os.path.dirname(os.path.abspath(__file__))

def check_bundle_path(bundle_path: str):
    return os.path.exists(f"{bundle_path}/Math/config.brick")

def bundle_path():
    # Use BRICK_BUNDLE_PATH if set
    if ("BRICK_BUNDLE_PATH" in os.environ):
        path = os.environ["BRICK_BUNDLE_PATH"]
        assert check_bundle_path(path)
        return path
    logging.info("BRICK_BUNDLE_PATH environment not set, searching for alternatives")
    # Check possible paths, in development we should set BRICK_BUNDLE_PATH to make sure we use the one we intend
    for path in [
                 f"C:\\algoryx\\rebrick\\brickbundles",   # Windows installation
                 f"/opt/Algoryx/rebrick/brickbundles",    # Linux/OSX installation
                 f"{package_dir()}",                      # package installed via pip, including editable install
    ]: 
        if check_bundle_path(path):
            path = os.path.abspath(path)
            logging.info(f"BRICK_BUNDLE_PATH={path}, set environment BRICK_BUNDLE_PATH if you expected a different path")
            return path
    raise Exception("Could not locate directory with brick bundles, i.e. bundle path")
