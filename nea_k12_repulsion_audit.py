import numpy as np
import matplotlib.pyplot as plt

def run_repulsion_audit():
    print("====================================================")
    print("   N.E.A. K12 团簇拓扑硬度与内部排斥审计 (v1.9)   ")
    print("====================================================\n")

    # 1. 定义常数
    B_ceiling = 3.0  # 物理注销线 (ZY)
    
    # 2. 计算全连通图 Kn 的单位租金
    # 对于全连通图，非零特征值均为 n，数量为 n-1
    # Q = (n-1) * sqrt(n), H = Q/n
    def h_kn(n):
        return (n - 1) * np.sqrt(n) / n

    n_range = np.arange(2, 31) # 扫描从 2 到 30 个节点的团簇
    h_values = h_kn(n_range)
    
    # 3. 计算“边际租金成本”（即内部排斥力的强度）
    # 力的本质是焓的梯度: F_internal = dH/dn
    internal_pressure = np.diff(h_values)

    # 4. 寻找关键点
    k12_h = h_kn(12)
    k24_h = h_kn(24)

    print(f"[数据清算]")
    print(f"  > K12 (黑洞种子) 单位租金: {k12_h:.4f} ZY")
    print(f"  > K24 (合并后) 单位租金: {k24_h:.4f} ZY")
    print(f"  > 结论: 合并导致租金上涨 {(k24_h - k12_h):.2f} ZY")
    
    # 5. 审计判决
    print(f"\n[审计判决]")
    print(f"  > 边际租金变化 (dH/dn): 全线为正 (Positive)")
    print(f"  > 物理意义: 在黑洞核心，增加节点密度会剧烈增加系统负担。")
    print(f"  > 结论: K12 节点之间存在“拓扑硬度”，这种向外的抗力顶住了引力坍缩。")

    # 6. 可视化
    plt.figure(figsize=(10, 6))
    plt.plot(n_range, h_values, 'b-o', label='Per-node Enthalpy H(n)')
    plt.axhline(y=B_ceiling, color='r', linestyle='--', label='Physical Cancellation (3.0 ZY)')
    plt.axvline(x=12, color='g', linestyle=':', label='K12 Stability Limit')
    
    plt.fill_between(n_range, h_values, 5, where=(h_values >= 3.0), 
                     color='red', alpha=0.1, label='Forbidden Zone')
    
    plt.title("The Origin of Repulsion: Why K12 Clusters Refuse to Merge")
    plt.xlabel("Number of Nodes in Cluster (n)")
    plt.ylabel("Enthalpy per Node (ZY)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

if __name__ == "__main__":
    run_repulsion_audit()