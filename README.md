# Chinese Flashcard Generator

Generate aesthetic flashcards with stroke order animation! Simple website UI runs python script locally to generate anki flashcard package. 

<!-- ![](Screenshots/ankiScreenshotDesktop.png)
![](Screenshots/ankiScreenshotMobile.jpg)
![](Screenshots/ankiScreenshotMobileBig.jpg) -->

<!-- <div style="display: flex; justify-content: space-evenly" >
    <div style="width: 60%">
        <img src="Screenshots/ankiScreenshotDesktop.png">
    </div>
    <div style="width: 16%">
        <img src="Screenshots/ankiScreenshotMobile.jpg">
    </div>
    <div style="width: 16%">
        <img src="Screenshots/ankiScreenshotMobileBig.jpg">
    </div>
</div> -->

<div style="display: flex; justify-content: space-evenly; width: 100%">
    <!-- <div style="width: 60%"> -->
        <img src="Screenshots/ankiScreenshotDesktop.png" width="60%">
    <!-- </div> -->
    <!-- <div style="width: 16%"> -->
        <img src="Screenshots/ankiScreenshotMobile.jpg" width="16%">
    <!-- </div> -->
    <!-- <div style="width: 16%"> -->
        <img src="Screenshots/ankiScreenshotMobileBig.jpg" width="16%">
    <!-- </div> -->
</div>

## Features:

- Custom HTML/CSS/Javascript template uses the HanziWriter javascript library to render Chinese flashcards with stroke order animation.
- Additional features:
  - Resize button
  - Tap the character to restart the animation
- Parses the vocab list text file, downloads HanziWriter stroke order data, and generates the front and back of flashcards (including examples) in a format compatible with my flashcard template.
- Uses genanki library to package decks of cards into an anki package.

## How to use:
- Check out the website at https://kabirbatradev.github.io/anki-chinese-flashcard-generator/
- Website runs python script locally; no need to download anything!

<img src="Screenshots/Chinese Flashcard Generator Website.png" width="80%">

If you enjoyed using this or have feature requests, feel free to [email me](mailto:kabirbatraa@gmail.com).

## Library references:
- HanziWriter: https://hanziwriter.org/
- genanki: https://github.com/kerrickstaley/genanki

