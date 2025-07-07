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
    1: 1_000_000,
    2: 5_000_000,
    3: 15_000_000,
    4: 600_000,
    5: 1_600_000,
    6: 5_600_000,
    7: 15_600_000,
    8: 10_000,
    9: 50_000,
    10: 200_000,
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
    for level, count in data["byLevel"].items():
        level_name = LEVEL_MAP[int(level)]
        result[level_name] = count
        vet_staked[level_name] = VET_COLLATERAL_MAP[int(level)] * count
    
    return result, total, vet_staked


if __name__ == "__main__":
    result, total = fetch_nft_mint_counts()
    print(f"Total holders: {total}")
    for level, count in result.items():
        print(f"{level}: {count}")