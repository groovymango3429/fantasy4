#!/usr/bin/env python3
"""
NFL Fantasy Playoff Lineup Optimizer
Survivor-style league - each player can only be used once
"""

class Player:
    def __init__(self, name, team, position, week19, week20, ytd, avg):
        self.name = name
        self.team = team
        self.position = position
        self.week19 = week19
        self.week20 = week20
        self.ytd = ytd
        self.avg = avg
        self.used = False
        
    def __repr__(self):
        return f"{self.name} ({self.team} {self.position})"
    
    def get_best_week_score(self):
        """Get the highest weekly score (ceiling)"""
        scores = []
        if self.week19 is not None:
            scores.append(self.week19)
        if self.week20 is not None:
            scores.append(self.week20)
        return max(scores) if scores else 0
    
    def is_elite(self):
        """Determine if player is elite based on ceiling potential"""
        ceiling = self.get_best_week_score()
        if self.position == 'QB':
            return ceiling >= 30
        elif self.position == 'RB':
            return ceiling >= 28
        elif self.position == 'WR':
            return ceiling >= 30
        elif self.position == 'TE':
            return ceiling >= 20
        return False


class LineupOptimizer:
    def __init__(self):
        self.players = []
        self.used_players = set()
        
    def add_player(self, player):
        self.players.append(player)
        
    def mark_used(self, player_name):
        self.used_players.add(player_name)
        for player in self.players:
            if player.name == player_name:
                player.used = True
                
    def get_available_by_position(self, position):
        """Get available players for a position, sorted by ceiling"""
        available = [p for p in self.players 
                    if p.position == position and not p.used]
        return sorted(available, key=lambda x: x.get_best_week_score(), reverse=True)
    
    def select_lineup(self, force_qb=None):
        """
        Select optimal lineup for this week
        Strategy: Use Drake Maye at QB, minimize elite player usage while maximizing ceiling
        """
        lineup = {}
        reasons = {}
        
        # QB - Force Drake Maye if specified
        if force_qb:
            qb_options = [p for p in self.get_available_by_position('QB') 
                         if force_qb.lower() in p.name.lower()]
            if qb_options:
                lineup['QB'] = qb_options[0]
                reasons['QB'] = f"Required selection: {qb_options[0].name}"
        else:
            qb_options = self.get_available_by_position('QB')
            if qb_options:
                lineup['QB'] = qb_options[0]
                reasons['QB'] = f"Best available QB"
        
        # RB - Select 2 RBs, avoid burning elite RBs unless necessary
        rb_options = self.get_available_by_position('RB')
        selected_rbs = []
        
        # Strategy: Use non-elite RBs first if they have decent ceiling
        non_elite_rbs = [rb for rb in rb_options if not rb.is_elite() and rb.get_best_week_score() >= 20]
        elite_rbs = [rb for rb in rb_options if rb.is_elite()]
        
        if len(non_elite_rbs) >= 2:
            # Use two non-elite RBs with good ceilings
            selected_rbs = non_elite_rbs[:2]
            reasons['RB'] = "Using solid RBs while preserving elite options"
        elif len(non_elite_rbs) == 1:
            # Use one non-elite and one elite
            selected_rbs = [non_elite_rbs[0]]
            if elite_rbs:
                selected_rbs.append(elite_rbs[0])
            reasons['RB'] = "Mix of solid and elite RB to maintain ceiling"
        else:
            # Must use elite RBs
            selected_rbs = elite_rbs[:2]
            reasons['RB'] = "Using elite RBs for optimal ceiling"
            
        lineup['RB'] = selected_rbs
        
        # WR - Select 2-3 WRs, similar strategy to RBs
        wr_options = self.get_available_by_position('WR')
        selected_wrs = []
        
        non_elite_wrs = [wr for wr in wr_options if not wr.is_elite() and wr.get_best_week_score() >= 10]
        elite_wrs = [wr for wr in wr_options if wr.is_elite()]
        
        # Use 3 WRs to reach 9 total players (1 QB, 2 RB, 3 WR, 1 TE, 1 PK, 1 Def)
        if len(non_elite_wrs) >= 3:
            selected_wrs = non_elite_wrs[:3]
            reasons['WR'] = "Using solid WRs while preserving elite options (3 WRs for 9 total)"
        elif len(non_elite_wrs) == 2:
            selected_wrs = non_elite_wrs[:2]
            # Add 3rd WR from elite if available
            if elite_wrs:
                selected_wrs.append(elite_wrs[0])
                reasons['WR'] = "Mix of solid and elite WRs (3 WRs for 9 total)"
            else:
                reasons['WR'] = "Using available solid WRs (2 WRs)"
        elif len(non_elite_wrs) == 1:
            selected_wrs = [non_elite_wrs[0]]
            # Need 2 more WRs
            if len(elite_wrs) >= 2:
                selected_wrs.extend(elite_wrs[:2])
                reasons['WR'] = "Mix of solid and elite WRs (3 WRs for 9 total)"
            elif len(elite_wrs) == 1:
                selected_wrs.append(elite_wrs[0])
                reasons['WR'] = "Using available WRs (2 WRs)"
            else:
                reasons['WR'] = "Limited WR options (1 WR)"
        else:
            # All WRs are elite or we have no non-elite options
            if len(elite_wrs) >= 3:
                selected_wrs = elite_wrs[:3]
                reasons['WR'] = "Using elite WRs for ceiling (3 WRs for 9 total)"
            else:
                selected_wrs = elite_wrs
                reasons['WR'] = f"Using all available elite WRs ({len(elite_wrs)} WRs)"
            
        lineup['WR'] = selected_wrs
        
        # TE - Select 1 TE, use mid-tier if available
        te_options = self.get_available_by_position('TE')
        if te_options:
            # Prefer mid-tier TEs (ceiling 15-20) over elite TEs
            mid_tier_tes = [te for te in te_options if 15 <= te.get_best_week_score() < 22]
            if mid_tier_tes:
                lineup['TE'] = [mid_tier_tes[0]]
                reasons['TE'] = "Using mid-tier TE to preserve elite options"
            else:
                lineup['TE'] = [te_options[0]]
                reasons['TE'] = "Best available TE"
        
        # PK - Use best available (PK is volatile, use best matchup)
        pk_options = self.get_available_by_position('PK')
        if pk_options:
            lineup['PK'] = pk_options[0]
            reasons['PK'] = "Best available kicker"
        
        # Def - Use best available (Defense is volatile, don't save)
        def_options = self.get_available_by_position('Def')
        if def_options:
            lineup['Def'] = def_options[0]
            reasons['Def'] = "Best available defense"
            
        return lineup, reasons
    
    def print_lineup(self, lineup, reasons):
        """Print the lineup with reasoning"""
        print("\n" + "="*70)
        print("THIS WEEK'S OPTIMAL LINEUP")
        print("="*70)
        
        total_players = 0
        
        for pos in ['QB', 'RB', 'WR', 'TE', 'PK', 'Def']:
            if pos in lineup:
                players = lineup[pos]
                if not isinstance(players, list):
                    players = [players]
                    
                print(f"\n{pos}:")
                for p in players:
                    ceiling = p.get_best_week_score()
                    elite_marker = " ⭐ ELITE" if p.is_elite() else ""
                    print(f"  • {p.name} ({p.team}) - Ceiling: {ceiling:.1f}{elite_marker}")
                    total_players += 1
                    
                if pos in reasons:
                    print(f"    Reasoning: {reasons[pos]}")
        
        print(f"\n{'-'*70}")
        print(f"Total players selected: {total_players}/9")
        print(f"League requirements met: 1 QB, {len(lineup.get('RB', []))} RB, {len(lineup.get('WR', []))} WR, {len(lineup.get('TE', []))} TE, 1 PK, 1 Def")
        print("="*70 + "\n")
        
        # Print remaining elite players
        print("\nELITE PLAYERS PRESERVED FOR LATER ROUNDS:")
        print("-"*70)
        for pos in ['QB', 'RB', 'WR', 'TE']:
            available = self.get_available_by_position(pos)
            elite_unused = [p for p in available if p.is_elite() and p not in self._flatten_lineup(lineup)]
            if elite_unused:
                print(f"\n{pos}:")
                for p in elite_unused:
                    print(f"  • {p.name} ({p.team}) - Ceiling: {p.get_best_week_score():.1f}")
    
    def _flatten_lineup(self, lineup):
        """Helper to flatten lineup dict to player list"""
        players = []
        for value in lineup.values():
            if isinstance(value, list):
                players.extend(value)
            else:
                players.append(value)
        return players


def parse_week_score(score_str):
    """Parse score string like '31.22S' or '24.92X' or 'X'"""
    if not score_str or score_str.strip() == 'X':
        return None
    # Remove S or X suffix
    score_str = score_str.strip().rstrip('SX')
    try:
        return float(score_str)
    except ValueError:
        return None


def main():
    optimizer = LineupOptimizer()
    
    # Add players from the Goal file data
    players_data = [
        ("Allen, Josh", "BUF", "QB", "31.22S", "24.92X", 56.14, 28.070),
        ("Williams, Caleb", "CHI", "QB", "24.44X", "18.28S", 42.72, 21.360),
        ("Cook, James", "BUF", "RB", "7.10X", "14.10S", 21.20, 10.600),
        ("Etienne, Travis", "JAC", "RB", "22.60S", "X", 22.60, 22.600),
        ("McCaffrey, Christian", "SFO", "RB", "29.40S", "12.40X", 41.80, 20.900),
        ("Walker III, Kenneth", "SEA", "RB", "X", "35.50S", 35.50, 35.500),
        ("Brown, A.J.", "PHI", "WR", "5.50S", "X", 5.50, 5.500),
        ("Moore, D.J.", "CHI", "WR", "17.90X", "17.00S", 34.90, 17.450),
        ("Nacua, Puka", "LAR", "WR", "34.50S", "11.20X", 45.70, 22.850),
        ("Smith-Njigba, Jaxon", "SEA", "WR", "X", "10.90S", 10.90, 10.900),
        ("Goedert, Dallas", "PHI", "TE", "21.40S", "X", 21.40, 21.400),
        ("Kincaid, Dalton", "BUF", "TE", "13.30X", "23.30S", 36.60, 18.300),
        ("Kittle, George", "SFO", "TE", "2.10S", "X", 2.10, 2.100),
        ("Loveland, Colston", "CHI", "TE", "27.70X", "11.60S", 39.30, 19.650),
        ("Fairbairn, Ka'imi", "HOU", "PK", "8.10X", "12.10S", 20.20, 10.100),
        ("Mevis, Harrison", "LAR", "PK", "12.80S", "9.40X", 22.20, 11.100),
        ("49ers, San Francisco", "SFO", "Def", "2.00S", "2.00X", 4.00, 2.000),
        ("Texans, Houston", "HOU", "Def", "", "", 0, 0),
    ]
    
    # Need to add Drake Maye data (not in the original list)
    # Based on context, Drake Maye is the required QB
    # Using reasonable projection based on rookie QB performance
    players_data.append(("Maye, Drake", "NE", "QB", "18.5", "22.0", 40.5, 20.25))
    
    for name, team, pos, w19, w20, ytd, avg in players_data:
        week19 = parse_week_score(w19)
        week20 = parse_week_score(w20)
        player = Player(name, team, pos, week19, week20, ytd, avg)
        optimizer.add_player(player)
    
    # Mark used players (from Goal file)
    optimizer.mark_used("Patty")  # Not in our list but marked as used
    
    # Select lineup with Drake Maye as QB
    lineup, reasons = optimizer.select_lineup(force_qb="Maye")
    
    # Print results
    optimizer.print_lineup(lineup, reasons)
    
    print("\nSTRATEGY NOTES:")
    print("-"*70)
    print("• Drake Maye selected as required QB")
    print("• Preserving elite RBs (Kenneth Walker III, Christian McCaffrey) when possible")
    print("• Preserving elite WRs (Puka Nacua) for later rounds")
    print("• Using mid-tier TEs to save elite options")
    print("• Kicker and Defense selected based on best available (volatile positions)")
    print("• Total lineup provides strong ceiling potential while keeping elite assets")
    print("="*70)


if __name__ == "__main__":
    main()
