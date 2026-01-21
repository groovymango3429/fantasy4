# Fantasy Football Survivor League Optimizer

This repository contains tools for optimizing weekly lineup choices in a survivor-style NFL fantasy playoff league.

## Overview

In a **survivor-style fantasy league**, each player can only be used once throughout the playoff weeks. The optimizer helps you:

- Maximize weekly ceiling potential
- Preserve elite players for later rounds  
- Avoid burning high-value assets in low-upside matchups
- Ensure no player is reused
- Meet league roster requirements

## Files

- **`Goal:`** - Original objective and strategy document (contains player data and used players tracking)
- **`lineup_optimizer.py`** - Python script that optimizes lineup selection based on ceiling potential and elite preservation
- **`WEEK_21_LINEUP.md`** - Current week's recommended lineup with detailed strategy and reasoning
- **`README.md`** - This file - documentation and usage instructions

## Usage

### Running the Optimizer

```bash
python3 lineup_optimizer.py
```

This will output:
- Optimal lineup for the current week
- Reasoning for each position
- Elite players preserved for future rounds
- Strategy notes

### Week 21 Lineup Summary

**Required:** Drake Maye at QB

**Selected Starters (9 total):**
- QB: Drake Maye (NE) - 22.0 ceiling
- RB: Travis Etienne (JAC) - 22.6 ceiling
- RB: Kenneth Walker III (SEA) - 35.5 ceiling ⭐ ELITE
- WR: D.J. Moore (CHI) - 17.9 ceiling
- WR: Jaxon Smith-Njigba (SEA) - 10.9 ceiling
- WR: Puka Nacua (LAR) - 34.5 ceiling ⭐ ELITE
- TE: Dallas Goedert (PHI) - 21.4 ceiling
- PK: Harrison Mevis (LAR) - 12.8 ceiling
- Def: San Francisco 49ers - 2.0 ceiling

**Total Projected Ceiling:** 146.1 points

**Elite Players Preserved:**
- Josh Allen (QB) - 31.2 ceiling
- Christian McCaffrey (RB) - 29.4 ceiling
- Colston Loveland (TE) - 27.7 ceiling
- Dalton Kincaid (TE) - 23.3 ceiling

## Strategy Philosophy

### Core Principles

1. **Ceiling Over Floor** - In survivor leagues, high-upside weeks matter more than consistency
2. **Position Scarcity** - RBs are most valuable; preserve top-tier RBs for later rounds
3. **Volatile Positions Early** - Use kickers and defenses based on best matchup (don't save them)
4. **Elite Preservation** - Save elite QBs and RBs unless matchup strongly favors a spike week

### Position Priorities

1. **RBs** - Most valuable survivor assets; prioritize saving elite RBs
2. **QBs** - Elite QBs should be held unless matchup is ideal
3. **WRs** - One elite WR per round is acceptable
4. **TEs** - Use mid-tier TEs early; save elite TE for scarcity situations
5. **Defense/Kicker** - Use best matchup this week; too volatile to plan long-term

### Win Condition

Enter the final playoff week with:
- At least one elite RB
- One top-tier QB or WR  
- Avoid being forced into low-upside or replacement-level starters

## Customization

To update the optimizer with new data:

1. Edit the `players_data` list in `lineup_optimizer.py`
2. Update `optimizer.mark_used()` calls to reflect players already used
3. Run the optimizer to get new recommendations

## League Requirements

- **Total Players:** 9
- **QB:** 1
- **RB:** 2-3
- **WR:** 2-3
- **TE:** 1-2
- **PK:** 1
- **Def:** 1

## Elite Player Thresholds

The optimizer considers a player "elite" based on ceiling potential:
- **QB:** ≥30 points
- **RB:** ≥28 points
- **WR:** ≥30 points
- **TE:** ≥20 points

These thresholds can be adjusted in the `is_elite()` method of the `Player` class.
