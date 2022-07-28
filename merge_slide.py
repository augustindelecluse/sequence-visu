# merge all Slide subclass from a file together to form one presentation
"""
all slides are merged in the order in which they are written
all construct() MUST end with a self.pause()\nself.wait() instruction
"""
import re

to_merge = "sequence-slide.py"
merged = "presentation.py"
INDENT = " " * 4  # base indent from within the file

if __name__ == "__main__":
    header = []
    construct = []
    pattern_construct = "\W+def\W+construct\W*\(\W*self\W*\)\W*:"
    pattern_slide = "class\W+(.+)\(\W*Slide\W*\)\W*:"
    in_construct = False
    in_header = True
    new_slide_demark = f"{INDENT * 2}# {'=' * 30}\n"

    with open(to_merge) as file:
        for line in file:
            if (search_obj := re.search(pattern_construct, line)) is not None:
                # within a new construct
                in_construct = True
                if construct:
                    # content already written to construct
                    # get back to the previous "self.pause(), self.wait()" instructions written
                    # and remove the self.wait() by a self.clear()
                    for i, content in enumerate(construct[::-1]):
                        if "self.wait()" in content:
                            replaced = content.replace("self.wait()", "self.clear()")
                            construct[-(i + 1)] = replaced
                            break
            elif (search_obj := re.search(pattern_slide, line)) is not None:
                class_name = search_obj.group(1)
                construct.append(f"\n{new_slide_demark}{INDENT * 2}# SLIDE {class_name}\n{new_slide_demark}\n")
                in_header = False
                in_construct = False
                # within a new Slide
            else:
                if in_header:
                    # always append the header
                    header.append(line)
                elif in_construct:
                    construct.append(line)

    with open(merged, "w") as file:
        file.writelines(header)
        file.writelines(["class Presentation(Slide):\n", "\n", f"{INDENT}def construct(self):\n"])
        file.writelines(construct)
