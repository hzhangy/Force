import numpy as np
import matplotlib.pyplot as plt

def run_final_horizon_audit():
    print("--- N.E.A. 黑洞视界终极结算 (v2.0: 修正总债务) ---")

    # 1. 核心常数
    B = 1.0                     # 单节点带宽基准 (ZY)
    A_core = 12                 # K12 团簇的节点数
    H_unit = 3.1754             # 每个节点的超载租金
    H_space = 1.3333            # 正常空间的租金
    
    # 核心总赤字 (Total Debt)
    # 这是 12 个逻辑单形挤在一起产生的总“空头头寸”
    total_deficit = A_core * (H_unit - H_space) # 约 22.1 ZY
    
    # 2. 空间传导
    r = np.linspace(0.1, 15, 1000) # 从极近处开始扫描
    
    # 3D 离散格林函数传导：U(r) 是单位节点分摊到的债务压力
    # 这里的 1/4pi 是 3D 空间的标准扩散系数
    U_r = total_deficit / (4 * np.pi * r)
    
    # 3. 计算可用带宽 f_ext
    # 根据 BAL: f_int^2 + f_ext^2 = 1.0
    # 这里的内部压力 f_int 包括了基础租金的内部项(约0.4)和传导来的债务 U_r
    # 我们简化逻辑：当 U_r 达到 1.0 时，外部带宽彻底归零
    f_int_total = U_r 
    
    # 这里的 np.maximum 保证不出现负值
    available_f_ext = np.sqrt(np.maximum(0, B**2 - f_int_total**2))

    # 4. 寻找视界 (第一个 f_ext 归零的点)
    zero_points = np.where(available_f_ext <= 1e-3)[0]
    
    if len(zero_points) > 0:
        r_horizon = r[zero_points[-1]] # 找到最外层熔断点
        print(f"\n[清算报告]")
        print(f"  > 团簇总债务余额: {total_deficit:.4f} ZY")
        print(f"  > 逻辑熔断半径 (视界): {r_horizon:.4f} 逻辑单位")
        print(f"  > 视界内状态: 1D 骨架回归 (3D 空间由于欠费被强制注销)")
        
        # 换算物理比例：
        # 如果 1 个单位是原子尺度 1e-10m，
        # 这对应了一个微型黑洞的视界。
    else:
        print("\n[审计失败] 空间仍然没有熔断，请检查物理常数。")
        return

    # 5. 绘图
    plt.figure(figsize=(10, 6))
    plt.plot(r, available_f_ext, 'b-', label='External Bandwidth $f_{ext}$')
    plt.fill_between(r, 0, available_f_ext, color='blue', alpha=0.1)
    plt.axvline(x=r_horizon, color='red', linestyle='--', label=f'Event Horizon (r={r_horizon:.2f})')
    plt.title("N.E.A. Black Hole v2.0: Bandwidth Meltdown Profile")
    plt.xlabel("Radial Distance $r$ (C8 cells)")
    plt.ylabel("Available Bandwidth $f_{ext}$ (ZY)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

if __name__ == "__main__":
    run_final_horizon_audit()