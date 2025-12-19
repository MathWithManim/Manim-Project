from manim import *
import random

class life(Scene):
  def construct(self):
    # --- setup ---
    latextemplate = TexTemplate(tex_compiler="pdflatex", output_format=".dvi")
    brightcyan = ManimColor("#00FFFF") 
    deepblue = ManimColor("#00008B")
    self.add(FullScreenRectangle(fill_color=BLACK, fill_opacity=1))

    # --- intro ---
    brandlogo = SVGMobject("ph.svg").scale(3.5).set_color(WHITE)
    brandtext = Tex(r"M\\A\\N\\I\\M").scale(1.5).set_color(WHITE)
    introbox = VGroup(brandlogo, brandtext).arrange(RIGHT, buff=1.0).move_to(ORIGIN)
    
    self.play(Write(introbox), run_time=1.5)
    self.wait(5) 
    self.play(introbox.animate.scale(0.18).to_corner(UL, buff=0.2), run_time=0.8)

    # --- top headers ---
    maintitle = Tex(r"Conway's Game of Life", tex_template=latextemplate, font_size=42)
    maintitle.to_edge(UP, buff=0.2)
    
    genlabel = Text("generation:", font_size=18, color=WHITE)
    gencounter = Integer(0).set_color(YELLOW).scale(0.7)
    headergroup = VGroup(genlabel, gencounter).arrange(RIGHT, buff=0.2).next_to(maintitle, DOWN, buff=0.1)
    
    self.play(Write(maintitle), FadeIn(headergroup))

    # --- rules and snippets (2x2 grid) ---
    def makesmallgrid(activelist):
      gridbox = VGroup()
      for i in range(9):
        tile = Square(side_length=0.15).set_stroke(WHITE, width=1, opacity=0.3)
        if i in activelist: tile.set_fill(brightcyan, opacity=1)
        gridbox.add(tile)
      return gridbox.arrange_in_grid(rows=3, cols=3, buff=0.04)

    ruledetails = [
      ("1. alone: < 2", [4], "if n < 2:\n die"),
      ("2. ok: 2-3", [4, 5, 7, 8], "if 2<=n<=3:\n live"),
      ("3. crowd: > 3", [1, 3, 4, 5, 7], "if n > 3:\n die"),
      ("4. birth: 3", [1, 3, 5], "if n == 3:\n new")
    ]

    allrulesblocks = VGroup()
    for textstring, tileindices, codestring in ruledetails:
      label = Text(textstring, font_size=14, color=YELLOW)
      minimap = makesmallgrid(tileindices)
      snippet = Code(
        code_string=codestring,
        language="python",
        background="window",
        paragraph_config={"font_size": 10}
      )
      rowtop = VGroup(label, minimap).arrange(RIGHT, buff=0.2)
      ruleblock = VGroup(rowtop, snippet).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
      allrulesblocks.add(ruleblock)

    # arranging blocks in a 2x2 grid
    rulesgrid = allrulesblocks.arrange_in_grid(rows=2, cols=2, buff=0.5)
    rulesgrid.to_edge(RIGHT, buff=0.5).shift(LEFT * 0.2).shift(DOWN * 0.5)

    for i, block in enumerate(allrulesblocks):
      self.play(FadeIn(block))
      if i in [0, 2]: 
        self.wait(0.5)
        self.play(block[0][1][4].animate.set_fill(BLACK, opacity=0))
      elif i == 3:
        self.wait(0.5)
        self.play(block[0][1][4].animate.set_fill(brightcyan, opacity=1))
      self.wait(1)

    # --- main simulation grid ---
    gridrows, gridcols = 18, 18
    cellsize = 0.28      
    currentpop = {(r, c): 1 if random.random() > 0.75 else 0 for r in range(gridrows) for c in range(gridcols)}
    longevitymap = {(r, c): 0 for r in range(gridrows) for c in range(gridcols)}
    
    cellmobjects = {}
    maingridgroup = VGroup()
    for (r, c), isactive in currentpop.items():
      cellunit = Square(side_length=cellsize).move_to([(c - gridcols/2) * cellsize - 3.4, (r - gridrows/2) * cellsize - 0.5, 0])
      cellunit.set_fill(brightcyan if isactive else BLACK, opacity=1 if isactive else 0)
      cellunit.set_stroke(WHITE, width=0.1, opacity=0.1)
      cellmobjects[(r, c)] = cellunit
      maingridgroup.add(cellunit)

    gridframe = SurroundingRectangle(maingridgroup, color=GRAY, buff=0.1, stroke_width=2)
    self.play(FadeIn(maingridgroup), Create(gridframe))

    # --- run simulation ---
    stagnantcount = 0
    for tick in range(1, 181):
      nextgenpop = {}
      frameanimations = []
      statehaschanged = False
      
      for r in range(gridrows):
        for c in range(gridcols):
          neighborcount = sum(currentpop.get((r+dr, c+dc), 0) for dr in [-1,0,1] for dc in [-1,0,1] if not (dr==0 and dc==0))
          currentlyalive = currentpop[(r, c)]
          survives = (currentlyalive and neighborcount in [2, 3]) or (not currentlyalive and neighborcount == 3)
          nextgenpop[(r, c)] = 1 if survives else 0
          
          if nextgenpop[(r, c)] != currentpop[(r, c)]:
            statehaschanged = True
            agecolor = interpolate_color(brightcyan, deepblue, min(longevitymap[(r, c)] / 15, 1)) if survives else BLACK
            activeopacity = 1.0 if survives else 0.0
            frameanimations.append(cellmobjects[(r, c)].animate(run_time=0.05).set_fill(agecolor, opacity=activeopacity))
          
          if survives: longevitymap[(r, c)] += 1
          else: longevitymap[(r, c)] = 0

      if not statehaschanged: stagnantcount += 1
      else: stagnantcount = 0

      if stagnantcount >= 10:
        stoptext = Text("stasis", color=RED, font_size=25).move_to(maingridgroup)
        self.play(FadeIn(stoptext))
        break

      currentpop = nextgenpop
      if frameanimations:
        self.play(*frameanimations, gencounter.animate.set_value(tick), run_time=0.1)
      else:
        self.play(gencounter.animate.set_value(tick), run_time=0.1)
    
    self.wait(2)