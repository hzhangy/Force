import numpy as np

def run_carrier_audit():
    print("====================================================")
    print("   N.E.A. 载体资产持有成本与生存审计 (v13.2)   ")
    print("====================================================\n")

    # 1. 基础常数 (GTUO 继承)
    U_weak = 10 * np.sqrt(3) # 17.3205 ZY (空间开户总费)
    U_em = 0.4 * np.pi       # 1.2566 ZY (编织操作费)
    bankruptcy_line = 2.0    # 2.0 ZY (拓扑清算红线)
    cancellation_line = 3.0  # 3.0 ZY (物理注销红线)

    # 2. 定义载体属性
    carriers = {
        "C8 (Cube - 空间)": {
            "n": 8, "k": 3, "tiling": True, "task": "EM+GR"
        },
        "K4 (Simplex - 物质)": {
            "n": 4, "k": 3, "tiling": False, "task": "Strong"
        },
        "Octahedron (弱力)": {
            "n": 6, "k": 4, "tiling": False, "task": "Addressing"
        }
    }

    for name, attr in carriers.items():
        n = attr['n']
        k = attr['k']
        
        # 计算空载租金 (Baseline Enthalpy)
        H_base = 1.0 + (1.0 / k)
        
        # 计算瞬时压强 (Task Pressure)
        if attr['task'] == "Addressing":
            # 弱力寻址总租金分摊到 6 个节点
            pressure = U_weak / n 
        elif attr['task'] == "EM+GR":
            # EM 租金分摊到 8 个节点
            pressure = U_em / n
        else:
            # 强力锁定租金 (假设为 Layer II-III 稳定态)
            pressure = 0.1667 # 1.5 - 1.33
            
        H_total = H_base + pressure
        
        # 计算稀释后的持有成本 (Holding Cost)
        if attr['tiling']:
            # 成功密铺，租金被无限稀释 (分母为 N_max)
            holding_cost = 1.0000 
            status = "AAA (永生 / 背景化)"
        else:
            # 密铺失败，租金被禁闭
            holding_cost = H_total
            if H_total >= cancellation_line:
                status = "CANCELED (物理注销)"
            elif H_total >= bankruptcy_line:
                status = "BANKRUPT (拓扑塌缩)"
            else:
                status = "BBB (稳定持有的物质)"

        print(f"[{name}]")
        print(f"  > 顶点度数 k: {k} -> 空载租金: {H_base:.4f} ZY")
        print(f"  > 任务压强: {pressure:.4f} ZY")
        print(f"  > 瞬时总焓 H: {H_total:.4f} ZY")
        print(f"  > 稀释后持有成本: {holding_cost:.4f} ZY")
        print(f"  > 审计判定: {status}")
        print("-" * 30)

if __name__ == "__main__":
    run_carrier_audit()