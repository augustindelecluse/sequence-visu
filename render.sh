# render the visualisation from sequence-slide.py and run it
rm -rf media
manim -qh sequence-slide.py VRPIntro
manim-presentation --fullscreen VRPIntro
