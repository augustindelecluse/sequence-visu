# render the visualisation from sequence-slide.py and run it
rm -rf media
python3 merge_slide.py
manim -ql presentation.py
manim-presentation --fullscreen Presentation
