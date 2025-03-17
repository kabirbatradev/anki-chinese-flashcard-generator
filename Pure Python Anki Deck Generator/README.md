# anki-chinese-flashcard-generator

Takes in a chinese vocab list generates an anki deck package with stroke order animation.

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

- Custom HTML/CSS/Javascript template uses the HanziWriter javascript library to render Chinese flashcards with stroke order.
  - includes resize button
  - includes ability to tap the character to restart the animation
  - includes stroke speed slider (feature in progress)
- Parses the vocab list text file, downloads HanziWriter stroke order data, and generates the front and back of flashcards (including examples) in a format compatible with my flashcard template.
- Uses genanki library to package decks of cards into an anki package.

## How to use:
1. Download this repository.
2. Add vocab list as a text file into the folder.
   - You can use the `testList.txt` as an example of a vocab list text file.
3. Go into `createAnkiDeckPackage.py` and edit the variables up top.
   - `outerDeckName`: will be used to name the deck containing the subdecks
   - `vocabListFileName`: name of the vocab list text file
4. Run `python createAnkiDeckPackage.py` in the terminal. 
   - Make sure python is installed.
   - You will need to install libraries: requests, genanki, random.
   - use pip install \<library name\>.
5. That's it! Running this script will create the apkg file for you!

If you enjoyed using this or have feature requests, feel free to [email me](mailto:kabirbatraa@gmail.com).

## Library references:
- HanziWriter: https://hanziwriter.org/
- genanki: https://github.com/kerrickstaley/genanki

