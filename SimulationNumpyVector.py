import numpy as np

def simulate_slot_rtp(num_spins: int = 1_000_000, bet_per_spin: float = 1.0) -> dict:
    """
    Simulates a simplified 3-reel slot game using vectorized NumPy operations.
    """
    # 0 = Cherry, 1 = Lemon, 2 = Seven, 3 = BAR
    symbols = np.array([0, 1, 2, 3])
    weights = np.array([0.40, 0.35, 0.20, 0.05])  # Reel probability distribution
    
    
    reels = np.random.choice(symbols, size=(num_spins, 3), p=weights)
    
   
    payouts = np.zeros(num_spins)
    
    # Rule 1: Three BARs paying 50x
    three_bars = np.all(reels == 3, axis=1)
    payouts[three_bars] = 50.0
    
    # Rule 2: Three Sevens paying 25x
    three_sevens = np.all(reels == 2, axis=1)
    payouts[three_sevens] = 25.0
    
    # Rule 3: Any Three Matching paying 7x (excluding Sevens and BARs already counted)
    three_matching = (reels[:, 0] == reels[:, 1]) & (reels[:, 1] == reels[:, 2])
    payouts[three_matching & ~three_bars & ~three_sevens] = 7.0
    
    
    total_wagered = num_spins * bet_per_spin
    total_returned = np.sum(payouts)
    rtp = (total_returned / total_wagered) * 100
    hit_frequency = (np.count_nonzero(payouts) / num_spins) * 100
    volatility_sd = np.std(payouts)
    
    return {
        "RTP (%)": round(rtp, 2),
        "Hit Frequency (%)": round(hit_frequency, 2),
        "Standard Deviation": round(volatility_sd, 4)
    }


results = simulate_slot_rtp(1_000_000)
print(results)

# RTP (Return to Player): The theoretical percentage of all wagered money
#  a slot machine pays back to players over time. An RTP of 95% means the 
#  machine returns $95 for every $100 put in, keeping a $5 "house edge."""