# SWRuneSorter
A tool that automatically scores, upgrades and sells runes for a certain Summoning game.


## Idea
No one wants to manually sort their runes. 
Most of the time, all we want to do is grind dungeons for a while and have the runes automatically upgraded and sold based on our preferences. 
This is what this project aims to do. 
You can define preferences in the form of rune descriptions or filters.
The motivation comes from the game itself, with its sell exclusion.

## Approach
The general approach is to use OCR to recognize the rune, basic rune filtering, and mouse automation to navigate the menus. 
Exactly how (and how well) this works is still a work in progress that I will have to figure out as I go.

### DSL
The DSL should be used to describe a rune to be upgraded.
This DSL is an embedded DSL written in python.

The DSL should support easy access to rune attributes:
- `Level`: Current upgrade level (e.g., `Level == 0`)
- `Quality`: Rune quality (e.g. `Legend`)
- `Stars`: Rune stars (e.g. `Stars == 5`)
- `Slot`: Rune slot (e.g. `Slot == 1`)
- `Set`: Rune set (e.g., `Set == "Violent"` or `Set.In(["Swift", "Rage"])`)
- `Stat`: Rune stat (e.g. `SPD` or `SPD >= 6`)
- `Main.Stat`: Rune main stat (e.g., `Main.SPD`)
- `Innate.Stat`: Rune innate stat (e.g., `Innate.SPD` or `Innate.SPD >= 6`)

The DSL should support different operations for these rune attributes:
- Comparisons: `==`, `>=`, `<=`, `>`, `<`, `!=`
- Logical operator: `AND`, `OR`, `NOT`
- Thresholds: `AtLeast(N, [conditions])`

## Limitations
There are, of course, limitations to this project and its use.
Endgame players may not need this tool, as they have sufficient knowledge of runes. 
This project is made by a beginner who wants to automate the boring and repetitive task of upgrading and selling useless runes.

# Components
## ScreenMarker
### Overview
The ScreenMarker component is designed to assist in the marking of relevant locations on the screen for the main application. 
This can be a button to click on or a Region of Interest (ROI) to read information from. 

## RuneUpgrader
A cli tool that requires the `json-dump.json` from the `ScreenMarker` component to be in the current working directory.
The manage rune window should be open with no filter applied, sorted by `Power-up Lv.` descending and no slots selected:
![Manage Runes.png](resources/readme/manage-runes.png)
Launch while the game is running with:
```bash
python rune_upgrader.py
```

The script will automatically move your mouse to select runes, take screenshots and use ocr to recognize runes and 
use the determined score to upgrade or sell the selected rune.
The script should not sell any of your already upgraded runes on its own.
After going through all 6 slots of runes, the script will stop.

### Limitation
The tool uses hardcoded delays for navigating the menu and different animation when upgrading.
However, certain actions, such as selling or upgrading, require communication with the server with inconsistent delays, 
leading to unexpected behaviour, e.g. skipping runes after selling a rune.