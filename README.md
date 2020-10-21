# CLI Blackjack Game

I was bored so I made a quick CLI Blackjack game. 
Now you can look and feel like you're being productive but really just be playing blackjack!


### Requirements
- Python 3.7
- Anaconda/Miniconda (optional since there aren't too many uncommon libraries at use)
    - `conda env create -f environment.yml`
    - `conda activate blackjack`


### Todo
- Fix bug/add feature that will automatically rearrange chips to cover bet (currently only starting at top denominations not aggregating smaller chips to cover non-existent large denominations)
- Code in basic strategy for the dealer (currently the dealer does not do anything except match bets)


### More improvements coming
- Multiplayer via socket connection?
- Turn into a simulator and run analysis on gameplay?



### To Run:
```
$ python game.py
```
