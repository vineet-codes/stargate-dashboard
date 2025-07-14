import requests
from collections import defaultdict

# Level mapping
LEVEL_MAP = {
    1: "Strength",
    2: "Thunder",
    3: "Mjolnir",
    4: "VeThorX",
    5: "StrengthX",
    6: "ThunderX",
    7: "MjolnirX",
    8: "Dawn",
    9: "Lightning",
    10: "Flash",
}

# VET collateral mapping
VET_COLLATERAL_MAP = {
    "Strength": 1_000_000,
    "Thunder": 5_000_000,
    "Mjolnir": 15_000_000,
    "VeThorX": 600_000,
    "StrengthX": 1_600_000,
    "ThunderX": 5_600_000,
    "MjolnirX": 15_600_000,
    "Dawn": 10_000,
    "Lightning": 50_000,
    "Flash": 200_000,
}

# Add limited supply mapping from the table
LIMITED_SUPPLY_MAP = {
    "Strength": 2500,    # Strength
    "Thunder": 300,     # Thunder
    "Mjolnir": 100,     # Mjolnir
    "VeThorX": 735,     # VeThor X
    "StrengthX": 843,     # Strength X
    "ThunderX": 180,     # Thunder X
    "MjolnirX": 158,     # Mjolnir X
    "Dawn": 500_000, # Dawn
    "Lightning": 100_000, # Lightning
    "Flash": 25_000, # Flash
}

def fetch_nft_mint_counts():
    url = "https://indexer.mainnet.vechain.org/api/v1/stargate/nft-holders"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")
    
    data = dict(response.json())
    total = data['total']
    
    result = {}
    vet_staked = {}
    nfts_remaining = {}
    for level, count in data["byLevel"].items():
        # print(level, count)
        # level_int = int(level)
        level_name = level
        result[level_name] = count
        vet_staked[level_name] = VET_COLLATERAL_MAP[level] * count
        # Calculate NFTs remaining for this level
        limited_supply = LIMITED_SUPPLY_MAP.get(level)
        nfts_remaining[level_name] = limited_supply - count if limited_supply is not None else None

    # print(result, total, vet_staked, nfts_remaining)
    
    return result, total, vet_staked, nfts_remaining


if __name__ == "__main__":
    result, total, vet_staked, nfts_remaining = fetch_nft_mint_counts()
    print(f"Total holders: {total}")
    print(f"{'Level':<12} {'Minted':<8} {'Remaining':<10} {'VET Staked':<12}")
    for level in result:
        print(f"{level:<12} {result[level]:<8} {nfts_remaining[level]:<10} {vet_staked[level]:<12}")