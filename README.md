# SWRuneSorter
A tool that automatically scores, upgrades and sells runes for a certain Summoning game.


## Idea
No one wants to manually sort their runes. 
Most of the time, all we want to do is grind dungeons for a while and have the runes automatically upgraded and sold based on our preferences. 
This is what this project aims to do. 
You can define preferences in the form of weights that are used to determine the score of a rune. 
The score should range from 0 to 100 to have a reference point. 
Since there are so many ways to use runes, multiple such weights are needed. 
This allows you to have a weight profile for DPS, support, or even niche use case runes.
With a rune's score, you can set a threshold, and runes below that threshold can be sold.

## Approach
The general approach is to use OCR to recognize the rune, basic maths to score the rune, and mouse automation to navigate the menus. 
Exactly how (and how well) this works is still a work in progress that I will have to figure out as I go.
