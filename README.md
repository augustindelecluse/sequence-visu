# Visualisation of Sequence Variables

From Augustin Delecluse, Pierre Schaus, and Pascal Van Hentenryck. Sequence Variables for Routing Problems. 28th International Conference on Principles and Practice of Constraint Programming (CP 2022), 2022. 
[See the paper](https://drops.dagstuhl.de/opus/volltexte/2022/16648/)


## Render one section

Select the name of the class to render. For instance with the class `TransitionTime` from the file `sequence-slide.py` 

```
manim -ql sequence-slide.py TransitionTime
```

This renders in low quality. Use `-qh` for high quality

## View the rendering

Launch a box to switch slides (use left and right arrows to switch between them)

```
manim-presentation TransitionTime
```

## Full presentation

Watching the full presentation requires to merge all the slides from `sequence-slide.py` into a file `presentation.py`.
Then the rendering is done again and the presentation can be viewed

```
python3 merge_slide.py
manim -ql presentation.py
manim-presentation --fullscreen Presentation
```

This takes a LOT of time for the rendering, be wary!
