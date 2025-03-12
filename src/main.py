import sys
import os
import shutil
from build_site import generate_pages_recursive

from copystatic import copy_files_recursive


basepath = sys.argv[0]
print(f"basepath: {basepath}")

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "template.html"
dest_dir_path = dir_path_public



def main():

    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath)


main()