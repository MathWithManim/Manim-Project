from manim import *
import random

# user input for the seed
userSeed = input("enterSeed: ")
if userSeed:
  random.seed(userSeed)

class life(Scene):
  def construct(self):
    # setup
    latexTemplate = TexTemplate(tex_compiler="pdflatex", output_format=".dvi")
    brightCyan = ManimColor("#00FFFF") 
    deepBlue = ManimColor("#00008B")
    self.add(FullScreenRectangle(fill_color=BLACK, fill_opacity=1))

    # intro
    brandLogo = SVGMobject("ph.svg").scale(3.5).set_color(WHITE)
    brandText = Tex(r"M\\A\\N\\I\\M").scale(1.5).set_color(WHITE)
    introBox = VGroup(brandLogo, brandText).arrange(RIGHT, buff=1.0).move_to(ORIGIN)
    
    self.play(Write(introBox), run_time=1.5)
    self.wait(5) 
    self.play(introBox.animate.scale(0.18).to_corner(UL, buff=0.2), run_time=0.8)

    # headers
    mainTitle = Tex(r"Conway's Game of Life", tex_template=latexTemplate, font_size=42)
    mainTitle.to_edge(UP, buff=0.2)
    genLabel = Text("generation:", font_size=18, color=WHITE)
    genCounter = Integer(0).set_color(YELLOW).scale(0.7)
    headerGroup = VGroup(genLabel, genCounter).arrange(RIGHT, buff=0.2).next_to(mainTitle, DOWN, buff=0.1)
    self.play(Write(mainTitle), FadeIn(headerGroup))

    # rules
    def makeSmallGrid(activeList):
      gridBox = VGroup()
      for i in range(9):
        tile = Square(side_length=0.15).set_stroke(WHITE, width=1, opacity=0.3)
        if i in activeList:
          tile.set_fill(brightCyan, opacity=1)
        gridBox.add(tile)
      return gridBox.arrange_in_grid(rows=3, cols=3, buff=0.04)

    ruleDetails = [
      ("1. Alone: < 2", [4], "if n < 2:\n die"),
      ("2. Alive: 2-3", [4, 5, 7, 8], "if 2<=n<=3:\n live"),
      ("3. Crowd: > 3", [1, 3, 4, 5, 7], "if n > 3:\n die"),
      ("4. Birth: 3", [1, 3, 5], "if n == 3:\n new")
    ]

    allRulesBlocks = VGroup()
    for textString, tileIndices, codeString in ruleDetails:
      label = Text(textString, font_size=14, color=YELLOW)
      miniMap = makeSmallGrid(tileIndices)
      snippet = Code(code_string=codeString, language="python", background="window", paragraph_config={"font_size": 10})
      rowTop = VGroup(label, miniMap).arrange(RIGHT, buff=0.2)
      ruleBlock = VGroup(rowTop, snippet).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
      allRulesBlocks.add(ruleBlock)

    rulesGrid = allRulesBlocks.arrange_in_grid(rows=2, cols=2, buff=0.5)
    rulesGrid.to_edge(RIGHT, buff=0.5).shift(LEFT * 0.2).shift(DOWN * 0.5)

    for i, block in enumerate(allRulesBlocks):
      self.play(FadeIn(block))
      if i in [0, 2]: 
        self.wait(0.5)
        self.play(block[0][1][4].animate.set_fill(BLACK, opacity=0))
      elif i == 3:
        self.wait(0.5)
        self.play(block[0][1][4].animate.set_fill(brightCyan, opacity=1))
      self.wait(1)

    # main simulation
    gridRows = 18
    gridCols = 18
    cellSize = 0.28      
    currentPop = {(r, c): 1 if random.random() > 0.75 else 0 for r in range(gridRows) for c in range(gridCols)}
    longevityMap = {(r, c): 0 for r in range(gridRows) for c in range(gridCols)}
    stateHistory = []
    
    cellMobjects = {}
    mainGridGroup = VGroup()
    for (r, c), isActive in currentPop.items():
      cellUnit = Square(side_length=cellSize).move_to([(c - gridCols/2) * cellSize - 3.4, (r - gridRows/2) * cellSize - 0.5, 0])
      cellUnit.set_fill(brightCyan if isActive else BLACK, opacity=1 if isActive else 0)
      cellUnit.set_stroke(WHITE, width=0.1, opacity=0.1)
      cellMobjects[(r, c)] = cellUnit
      mainGridGroup.add(cellUnit)

    gridFrame = SurroundingRectangle(mainGridGroup, color=GRAY, buff=0.1, stroke_width=2)
    self.play(FadeIn(mainGridGroup), Create(gridFrame))

    # run
    for tick in range(1, 151):
      nextGenPop = {}
      frameAnimations = []
      currentState = tuple(currentPop.values())
      
      # Oscillator Stasis Detection (checks back 2 frames)
      if currentState in stateHistory[-2:]:
        stasisText = Text("stasis", color=RED, font_size=25).move_to(mainGridGroup)
        self.play(FadeIn(stasisText))
        break
      stateHistory.append(currentState)

      for r in range(gridRows):
        for c in range(gridCols):
          neighborCount = sum(currentPop.get((r+dr, c+dc), 0) for dr in [-1,0,1] for dc in [-1,0,1] if not (dr==0 and dc==0))
          currentlyAlive = currentPop[(r, c)]
          survives = (currentlyAlive and neighborCount in [2, 3]) or (not currentlyAlive and neighborCount == 3)
          nextGenPop[(r, c)] = 1 if survives else 0
          
          if nextGenPop[(r, c)] != currentPop[(r, c)]:
            ageColor = interpolate_color(brightCyan, deepBlue, min(longevityMap[(r, c)] / 15, 1)) if survives else BLACK
            activeOpacity = 1.0 if survives else 0.0
            frameAnimations.append(cellMobjects[(r, c)].animate(run_time=0.05).set_fill(ageColor, opacity=activeOpacity))
          
          if survives:
            longevityMap[(r, c)] += 1
          else:
            longevityMap[(r, c)] = 0

      currentPop = nextGenPop
      if frameAnimations:
        self.play(*frameAnimations, genCounter.animate.set_value(tick), run_time=0.1)
      else:
        self.play(genCounter.animate.set_value(tick), run_time=0.1)
    
    self.wait(2)