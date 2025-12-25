import random
import heapq
import time
import sys
from collections import deque

# --- I. 系統資料初始化 ---

# [陣列 List] 背包/掉落物 (初始時會隨機生成)
INVENTORY = []
IS_SORTED = False

# [雜湊表 Dict] 魔法資料庫
SPELL_DATABASE = {
    "fire": {"name": "豪火球之術", "dmg": 500, "type": "火系"},
    "ice": {"name": "絕對零度", "dmg": 450, "type": "冰系"},
    "heal": {"name": "大回復術", "dmg": -200, "type": "治癒"},
    "thunder": {"name": "麒麟", "dmg": 600, "type": "雷系"}
}

# [圖 Graph/Dict] 地圖連接表 (節點: {鄰居: 距離})
MAP_GRAPH = {
    'A': {'B': 5, 'C': 10},         # A: 新手村
    'B': {'A': 5, 'D': 15, 'E': 20}, # B: 迷霧森林
    'C': {'A': 10, 'F': 25},        # C: 礦坑
    'D': {'B': 15, 'G': 30},        # D: 古代遺跡
    'E': {'B': 20, 'G': 10},        # E: 精靈湖
    'F': {'C': 25, 'G': 5},         # F: 巨龍山脈
    'G': {}                         # G: 魔王城 (終點)
}

# [字典 Dict] 地點名稱
LOCATIONS = {
    'A': '新手村', 'B': '迷霧森林', 'C': '礦坑',
    'D': '古代遺跡', 'E': '精靈湖', 'F': '巨龍山脈', 'G': '魔王城'
}

def generate_initial_data():
    """生成模擬數據並初始化背包。"""
    global INVENTORY, IS_SORTED
    names = ["生鏽劍", "勇者劍", "木  棒", "石中劍", "雷神槌", "平底鍋"]
    INVENTORY = []
    # 重新生成 10 件裝備
    for i in range(10):
        item_name = random.choice(names)
        power = random.randint(10, 999)
        INVENTORY.append({'id': i, 'name': item_name, 'power': power})
    IS_SORTED = False
    print(">>> 系統初始化完成：已隨機生成 10 件掉落裝備。")

# --- II. 核心功能函式 (基於資料結構與演算法) ---

# --- 功能 1: 排序 (Sorting) ---
def show_inventory():
    """顯示背包並提供排序功能。"""
    global INVENTORY, IS_SORTED
    print(f"\n[背包系統] 目前狀態: {'已排序 (可二分搜尋)' if IS_SORTED else '亂七八糟'}")
    print("-" * 40)
    print(f"{'ID':<5} {'裝備名稱':<10} {'攻擊力':<10}")
    print("-" * 40)
    for item in INVENTORY:
        print(f"{item['id']:<5} {item['name']:<10} {item['power']:<10}")
    
    if not IS_SORTED:
        cmd = input("\  背包太亂了！是否執行「攻擊力排序演算法」? (y/n): ")
        if cmd.lower() == 'y':
            # 使用 Python 的 Timsort (高效的合併排序+插入排序)
            INVENTORY.sort(key=lambda x: x['power'])
            IS_SORTED = True
            print(">>>   排序執行中... (Sorting)... 完成！")
            show_inventory() # 重新顯示

# --- 功能 2: 搜尋 (Binary Search) ---
def search_item():
    """執行二分搜尋法查找裝備。"""
    global INVENTORY, IS_SORTED
    print("\n [裝備檢索系統]")
    if not IS_SORTED:
        print(" 錯誤：二分搜尋法 (Binary Search) 要求資料必須先排序！請先去背包整理裝備 (選項 1)。")
        return

    try:
        target = int(input(">>> 請輸入你想尋找的「攻擊力數值」: "))
    except ValueError:
        print("請輸入數字！")
        return

    # 二分搜尋實作
    low = 0
    high = len(INVENTORY) - 1
    found = False
    steps = 0
    
    # 讓使用者對二分搜尋的邏輯更有感覺
    print(f"   正在範圍 [0 ~ {high}] 中搜索...")
    
    while low <= high:
        steps += 1
        mid = (low + high) // 2
        mid_val = INVENTORY[mid]['power']
        
        # 視覺化搜尋過程
        print(f"   步驟 {steps}: 檢查索引 {mid} (數值 {mid_val})...")
        
        if mid_val == target:
            print(f"\n  找到了！在第 {mid+1} 格發現 [{INVENTORY[mid]['name']}]，攻擊力 {target}")
            found = True
            break
        elif mid_val < target:
            # 目標值在右半邊
            print(f"   目標 {target} > {mid_val}，縮小搜尋範圍至 [ {mid+1} ~ {high} ]")
            low = mid + 1
        else: # mid_val > target
            # 目標值在左半邊
            print(f"   目標 {target} < {mid_val}，縮小搜尋範圍至 [ {low} ~ {mid-1} ]")
            high = mid - 1
    
    if not found:
        print(f"\n  搜尋結束：沒有找到攻擊力剛好是 {target} 的裝備。")


# --- 功能 3: 雜湊 (Hashing) ---
def cast_magic():
    """使用雜湊表進行 O(1) 快速施法。"""
    print("\n [快速施法系統]")
    print("可用咒語簡碼 (Key): fire, ice, heal, thunder")
    code = input(">>> 請輸入咒語簡碼 (Key) 以觸發魔法: ").lower()
    
    # 雜湊查找 O(1)
    spell = SPELL_DATABASE.get(code)
    
    if spell:
        print(f"\n  詠唱成功！{spell['name']} 啟動！")
        print(f"   屬性: {spell['type']}")
        print(f"   數值: {spell['dmg']} (正數為傷害，負數為回復)")
    else:
        # 雜湊碰撞/找不到 Key
        print("\n 噗... 什麼事都沒發生 (Key Error: 咒語不存在)。請檢查你的咒語簡碼！")
    

# --- 功能 4: 地圖導航與圖論 (Dijkstra, BFS) ---

def navigation():
    """提供基於圖論演算法的地圖導航功能。"""
    print("\n [地圖導航系統]")
    print("地點代號與名稱:")
    for k, v in LOCATIONS.items():
        print(f"  {k}: {v}")
    
    start = input(">>> 請輸入起點代號 (例如 A): ").upper()
    if start not in LOCATIONS:
        print("無效的起點！")
        return

    print("\n--- 請選擇你想執行的圖論演算法 ---")
    print("1. Dijkstra (尋找最短路徑/最少耗時)")
    print("2. BFS (廣度優先搜尋 - 尋找最少轉乘次數的路)")
    algo_choice = input(">>> 請輸入選項 (1或2): ")

    if algo_choice == '1':
        dijkstra_search(start)
    elif algo_choice == '2':
        bfs_search(start)
    else:
        print("無效的演算法選項。")

def dijkstra_search(start_node):
    """實作 Dijkstra 演算法尋找單源最短路徑。"""
    distances = {node: float('infinity') for node in LOCATIONS}
    distances[start_node] = 0
    pq = [(0, start_node)] # (距離, 節點) - 使用 heapq 實現優先佇列
    previous_nodes = {node: None for node in LOCATIONS}

    print(">>> 正在計算最短路徑 (Dijkstra Algorithm)...")
    
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        
        if current_dist > distances[current_node]: continue

        # 遍歷鄰居
        for neighbor, weight in MAP_GRAPH.get(current_node, {}).items():
            distance = current_dist + weight
            
            # 如果發現更短的路徑 (鬆弛操作)
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))
    

    # 顯示結果
    print(f"\n從 [{LOCATIONS[start_node]}] 出發的最短耗時：")
    for node, dist in distances.items():
        if dist != float('infinity'):
            print(f"  -> 前往 [{LOCATIONS[node]} ({node})]: {dist} 分鐘")
    
    # 特別顯示去魔王城('G')的路徑
    if distances['G'] != float('infinity'):
        path = []
        curr = 'G'
        while curr:
            path.append(curr)
            curr = previous_nodes[curr]
        
        full_path = ' -> '.join([LOCATIONS[n] for n in reversed(path)])
        print(f"\n  魔王城最短建議路線 (總耗時 {distances['G']} 分鐘): {full_path}")

def bfs_search(start_node):
    """實作廣度優先搜尋 (BFS) 尋找最少轉乘次數通往魔王城('G')的路徑。"""
    print(">>> 正在執行廣度優先搜尋 (BFS) 找轉乘次數最少的路徑...")
    
    # 使用 deque 模擬 Queue (FIFO)
    queue = deque([start_node])
    visited = {start_node}
    path_trace = {start_node: [start_node]} # 追蹤從起點到當前節點的路徑
    
    while queue:
        current_node = queue.popleft() # 隊首出隊 O(1)
        current_path = path_trace[current_node]

        print(f"   BFS 探索: 正在 {LOCATIONS[current_node]}...")
        
        if current_node == 'G':
            full_path = ' -> '.join([LOCATIONS[n] for n in current_path])
            print(f"\n  BFS 發現路徑 (最少轉乘): {full_path} (共 {len(current_path) - 1} 站)")
            return

        # 依序拜訪所有未拜訪過的鄰居 (廣度優先)
        for neighbor in MAP_GRAPH.get(current_node, {}):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                path_trace[neighbor] = current_path + [neighbor]

    print("\n  BFS 結束：沒有找到通往魔王城的可行路徑。")
    

# --- III. 主程式迴圈 ---
def main_game():
    """遊戲主迴圈與選單。"""
    generate_initial_data() # 確保一開始就有資料
    
    while True:
        print("\n" + "="*50)
        print("  - 勇者OS v2.1 主選單- ")
        print("1.  整理背包 (排序 Sorting) ")
        print("2.  尋找裝備 (搜尋 Binary Search) ")
        print("3.  詠唱魔法 (雜湊 Hashing) ")
        print("4.  地圖導航 (圖論 Dijkstra/BFS) ")
        print("5.  重新開始 (重置資料)")
        print("6.  關機 (Exit)")
        print("="*50)
        
        choice = input(">>> 請輸入選項 (1-6): ")
        
        if choice == '1':
            show_inventory()
        elif choice == '2':
            search_item()
        elif choice == '3':
            cast_magic()
        elif choice == '4':
            navigation()
        elif choice == '5':
            generate_initial_data()
        elif choice == '6':
            print("系統關機中... 謝謝你的冒險！")
            break
        else:
            print("無效指令，請重新輸入。")
        
        time.sleep(1)

if __name__ == "__main__":

    main_game()
