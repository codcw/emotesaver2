from image import *

#necessary directories
base_dir = pathlib.Path.cwd()
path_big = base_dir / "need_correction"
path_failed = base_dir / "failed"

#make necessary directories if not exist
pathlib.Path(path_big).mkdir(exist_ok=True)
pathlib.Path(path_failed).mkdir(exist_ok=True)

def execute():
    failed = completed = 0
    with open(base_dir / "links.txt", "r") as links:
        for link in links.readlines():
            current_image = Image(link.strip())
            print(f"processing emote {current_image.name}, size {current_image.size()}")
            current_image.put_to(base_dir)
            target = 256000
            if current_image.size() > target:
                res = current_image.optimize(target)
                if res:
                    print(f"emote {current_image.name} added successfully UwU")
                    completed += 1
                else:
                    print(f"emote {current_image.name} is too big! you have to correct it T_T")
                    current_image.move_to(path_failed)
                    current_image.put_to(path_big)
                    failed += 1
    print(f"failed: {failed}, completed: {completed}, total: {failed + completed}")

if __name__ == "__main__":
    execute()