import numpy as np
import networkx as nx
import scipy.linalg as la

def run_blackhole_audit():
    print("--- N.E.A. 黑洞逻辑单形与接触力 深度审计 ---")

    # 1. 构造三种“相态”的图
    # 空间态：C8 立方体
    c8 = nx.hypercube_graph(3)
    # 物质态：K4 四面体
    k4 = nx.complete_graph(4)
    # 黑洞态：逻辑单形团簇 (假设12个节点的全连通图 K12)
    # 模拟在黑洞内部，节点放弃所有几何规则，直接进入暴力邻接
    kn = nx.complete_graph(12) 

    def get_audit_data(G, name):
        L = nx.laplacian_matrix(G).toarray()
        eigenvals = la.eigvalsh(L)
        eigenvals = np.maximum(eigenvals, 1e-10)
        # 租金 (f_int)
        rent = np.sum(np.sqrt(eigenvals)) / len(G)
        # 定位度 (IPR)
        _, vecs = la.eigh(L)
        ipr = np.mean(np.sum(vecs**4, axis=0))
        # 计算“接触应力” (Laplacian 范数增益)
        stress = np.linalg.norm(L, 'fro') / len(G)
        return rent, ipr, stress

    r_c8, i_c8, s_c8 = get_audit_data(c8, "C8")
    r_k4, i_k4, s_k4 = get_audit_data(k4, "K4")
    r_kn, i_kn, s_kn = get_audit_data(kn, "K12")

    print(f"\n[资产负债对比]")
    print(f"相态      | 单位租金(ZY) | 定位度(IPR) | 接触应力(强度)")
    print(f"--------------------------------------------------")
    print(f"空间(C8)  | {r_c8:10.4f} | {i_c8:10.4f} | {s_c8:10.4f}")
    print(f"物质(K4)  | {r_k4:10.4f} | {i_k4:10.4f} | {s_k4:10.4f}")
    print(f"黑洞(K12) | {r_kn:10.4f} | {i_kn:10.4f} | {s_kn:10.4f}")

    # 4. 判定 3.0 ZY 注销线
    print(f"\n[审计判决]")
    if r_kn > 2.0:
        print(f"  > 警告：黑洞态单位租金 ({r_kn:.2f}) 击穿了 2.0 ZY 拓扑清算线！")
        print(f"  > 结论：3D 空间感在内部完全丧失，回归 1D 骨架直连。")
    print(f"  > 接触力强度比 (黑洞/空间): {s_kn/s_c8:.2f} 倍")

if __name__ == "__main__":
    run_blackhole_audit()