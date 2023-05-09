import pathlib

from image import *

base_dir = "D:\\extracted_emotes\\"
path_big = f"{base_dir}need_correction\\"
path_failed = f"{base_dir}failed\\"

pathlib.Path(path_big).mkdir(exist_ok=True)
pathlib.Path(path_failed).mkdir(exist_ok=True)

if __name__ == "__main__":
    with open("D:\\extracted_emotes\\links.txt", "r") as links:
        for link in links.readlines():
            current_image = Image(link.strip())
            initial_true_emote_size = current_image.true_size_frombytes()
            print(f"processing emote {current_image.name}, size {initial_true_emote_size}")
            current_image.put_to(base_dir)
            target = 256000
            if initial_true_emote_size > target:
                print("emote is too big! trying to optimize :3")
                res = current_image.optimize(target)
                if res:
                    print(f"emote {current_image.name} added successfully UwU")
                else:
                    print(f"emote {current_image.name} is too big! you have to correct it T_T")
                    current_image.move_to(path_failed)
                    current_image.put_to(path_big)