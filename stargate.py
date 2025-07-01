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

def fetch_nft_mint_counts():
    url = "https://indexer.mainnet.vechain.org/api/v1/stargate/nft-holders"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")
    
    data = dict(response.json())
    total = data['total']
    
    result = {}
    for level, count in data["byLevel"].items():
        level_name = LEVEL_MAP[int(level)]
        result[level_name] = count
    
    return result, total


if __name__ == "__main__":
    result, total = fetch_nft_mint_counts()
    print(f"Total holders: {total}")
    for level, count in result.items():
        print(f"{level}: {count}")