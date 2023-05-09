import requests, json, os, pathlib, subprocess, time, sys

class Image:


    def __init__(self, source):
        #initialize all necessary stuff, download pic
        source_id = source[source.rfind('/'):]  #get source id of emote from link
        response = requests.get(f"https://7tv.io/v3/emotes/{source_id}")    #get request from api
        emote_info = json.loads(response.content.decode('utf-8'))   #load json from request
        banned_characters = """ " \ / : | < > * ? """ #banned characters that cant be used to name the emote
        self.extension = ".png" if emote_info["animated"] == False else ".gif"   #determine format
        # downloading emote itself
        img = f"https://cdn.7tv.app/emote/{source_id}/4x{self.extension}"
        self.image = requests.get(img).content
        self.name = ''.join([i if i not in banned_characters else 'x' for i in emote_info["name"]])  # get emote name


    def increment_name(self):
        from re import search
        check = search('(.+)\((\d+)\)$', self.name)
        if not check:
            self.name += '(1)'
        else:
            self.name = check.group(1) + f"({int(check.group(2)) + 1})"
        new_path = pathlib.Path(f"{self.path.parent}\\{self.name}{self.extension}")
        if new_path.exists():
            self.increment_name()
        else:
            self.path = self.path.rename(new_path)


    def put_to(self, path):
        #this has to put emote in specified directory
        self.path = pathlib.Path(f"{path}{self.name}{self.extension}")
        #renaming if exists
        if self.path.exists():
            self.increment_name()
        #writing
        with open(self.path, 'wb') as handler:
            handler.write(self.image)


    def true_size_frombytes(self):
        return sys.getsizeof(self.image) - sys.getsizeof(bytes())


    def emote_size(self, path):
        return os.path.getsize(path)


    def optimize(self, threshold):
        #trying different optimizaton methods, if size comes less than threshold, return True else False

        #workaround to wait till file appears
        time_to_wait = 10
        time_counter = 0
        while not self.path.exists():
            print(f"waiting till the file appears{'.' * time_counter}")
            time.sleep(1)
            time_counter += 1
            if time_counter > time_to_wait:
                print("waiting too long, stopping")
                return

        def optimization(path, steps, target, colors, lossiness, *args):
            print(f"--- steps:{steps}; additional flags:{' | '.join(args)} ---")
            arguments = lambda o: ["gifsicle", "-b", "+x", *o, path]
            ending = ["st", "nd", "rd"] + ["th"] * 8
            for i in range(steps):
                with open(path, 'wb') as handler:
                    handler.write(self.image)
                unopt = subprocess.run(arguments(["-U"]), shell=True)
                opt = subprocess.run(arguments(args + (f"--lossy={lossiness}", f"-k={colors}", "-O3")), shell=True)
                if self.emote_size(path) < threshold:
                    print(f"optimization successful on {i + 1}{ending[i]} step, emote size {self.emote_size(path) / 1000} kb")
                    return True
                else:
                    print(f"optimizing on {i + 1}{ending[i]} step, emote size {self.emote_size(path) / 1000} kb")
                colors -= 2
                lossiness += 20
            print("optimization failed :(")
            return False


        if optimization(self.path, 6, threshold, 32, 20, "--method=median-cut"):
            return True
        elif optimization(self.path, 5, threshold, 16, 100, "--use-colormap=web", "--method=median-cut"):
            return True
        elif optimization(self.path, 5, threshold, 16, 100, "--use-colormap=web", "--method=blend-diversity"):
            return True
        else:
            return False


    def move_to(self, new_path):
        #this has to move existing emote to new path, return False if exists
        end_path = pathlib.Path(f"{new_path}{self.path.name}")
        if end_path.exists():
            self.increment_name()
            self.move_to(new_path)
        else:
            pathlib.Path(self.path).rename(end_path)
            self.path = end_path

