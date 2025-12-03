#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
光と波動 実験2 グラフ作成スクリプト
シータ（角度）をずらしたグラフを作成
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

# 日本語フォント設定
import platform
if platform.system() == 'Darwin':  # macOS
    rcParams['font.family'] = 'Hiragino Sans'
else:
    rcParams['font.family'] = 'DejaVu Sans'
rcParams['font.sans-serif'] = ['Hiragino Sans', 'Hiragino Kaku Gothic Pro', 'Yu Gothic', 'Meiryo', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']

def load_experiment_data(file_path):
    """Excelファイルから実験データを読み込む"""
    xl = pd.ExcelFile(file_path)
    
    experiments = {}
    sheet_names = ['実験2-1_グラフ', '実験2-2_グラフ', '実験2-3_グラフ']
    
    for sheet_name in sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=4)
        
        # 列名を確認（データが含まれる列を特定）
        # 角度、測定値、補正後の相対強度、理論値などを抽出
        data = []
        
        for i in range(len(df)):
            row = df.iloc[i]
            # 角度の列を探す
            angle_col = None
            for col_idx in range(len(row)):
                if pd.notna(row.iloc[col_idx]) and isinstance(row.iloc[col_idx], (int, float)):
                    if angle_col is None:
                        angle_col = col_idx
                        angle = row.iloc[col_idx]
                        if angle >= 0 and angle <= 180:
                            # 測定値、補正後の相対強度、理論値を取得
                            measured = row.iloc[angle_col + 1] if angle_col + 1 < len(row) else None
                            relative_intensity = row.iloc[angle_col + 3] if angle_col + 3 < len(row) else None
                            theoretical = row.iloc[angle_col + 4] if angle_col + 4 < len(row) else None
                            
                            if pd.notna(angle):
                                data.append({
                                    'angle': angle,
                                    'measured': measured if pd.notna(measured) else None,
                                    'relative_intensity': relative_intensity if pd.notna(relative_intensity) else None,
                                    'theoretical': theoretical if pd.notna(theoretical) else None
                                })
                            break
        
        experiments[sheet_name] = pd.DataFrame(data)
    
    return experiments

def load_experiment_data_improved(file_path):
    """Excelファイルから実験データを読み込む（改良版）"""
    experiments = {}
    sheet_names = ['実験2-1_グラフ', '実験2-2_グラフ', '実験2-3_グラフ']
    
    for sheet_name in sheet_names:
        # ヘッダー行をスキップしてデータを読み込む
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=4)
        
        # データフレームの列を確認
        # 通常、角度は1列目、測定値は2列目、相対強度は4列目、理論値は5列目あたり
        data = []
        
        # データ行を探す（NaNでない行）
        for idx, row in df.iterrows():
            # 角度の列（通常1列目）を確認
            if len(row) > 1:
                angle = row.iloc[1] if pd.notna(row.iloc[1]) else None
                
                # 角度が数値で0-180の範囲内なら有効なデータ行
                if angle is not None:
                    try:
                        angle = float(angle)
                        if 0 <= angle <= 180:
                            measured = row.iloc[2] if len(row) > 2 else None
                            relative_intensity = row.iloc[4] if len(row) > 4 else None
                            theoretical = row.iloc[5] if len(row) > 5 else None
                            
                            # NaNチェック
                            measured = measured if pd.notna(measured) else None
                            relative_intensity = relative_intensity if pd.notna(relative_intensity) else None
                            theoretical = theoretical if pd.notna(theoretical) else None
                            
                            data.append({
                                'angle': angle,
                                'measured': measured,
                                'relative_intensity': relative_intensity,
                                'theoretical': theoretical
                            })
                    except (ValueError, TypeError):
                        continue
        
        experiments[sheet_name] = pd.DataFrame(data).dropna(subset=['angle'])
    
    return experiments

def create_graph(experiments, output_path='graph.png'):
    """シータをずらしたグラフを作成"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 実験データの設定
    experiment_configs = {
        '実験2-1_グラフ': {'label': '実験2-1: 偏光板2枚', 'color': 'blue', 'marker': 'o'},
        '実験2-2_グラフ': {'label': '実験2-2: 偏光板3枚 (α=0°)', 'color': 'red', 'marker': 's'},
        '実験2-3_グラフ': {'label': '実験2-3: 偏光板3枚 (α=10°)', 'color': 'green', 'marker': '^'}
    }
    
    # 各実験のデータをプロット
    for sheet_name, config in experiment_configs.items():
        if sheet_name in experiments:
            df = experiments[sheet_name]
            
            # 角度と相対強度のデータを抽出
            angles = df['angle'].values
            intensities = df['relative_intensity'].values
            
            # NaNを除外
            valid_mask = ~np.isnan(intensities)
            angles_clean = angles[valid_mask]
            intensities_clean = intensities[valid_mask]
            
            if len(angles_clean) > 0:
                # 測定値をプロット
                ax.plot(angles_clean, intensities_clean, 
                       label=config['label'] + ' (測定値)', 
                       color=config['color'],
                       marker=config['marker'],
                       linestyle='-',
                       linewidth=2,
                       markersize=6)
            
            # 理論値もプロット（別のマスクで処理）
            theoretical = df['theoretical'].values
            angles_theory = df['angle'].values
            valid_theory_mask = ~np.isnan(theoretical) & (theoretical > 0)  # 0より大きい値のみ
            angles_theory_clean = angles_theory[valid_theory_mask]
            theoretical_clean = theoretical[valid_theory_mask]
            
            if len(angles_theory_clean) > 0:
                ax.plot(angles_theory_clean, theoretical_clean, 
                       label=f"{config['label']} (理論値)",
                       color=config['color'],
                       linestyle='--',
                       linewidth=1.5,
                       alpha=0.7)
    
    # グラフの設定
    ax.set_xlabel('角度 θ [degree]', fontsize=14)
    ax.set_ylabel('相対強度', fontsize=14)
    ax.set_title('光と波動 実験2 白色光の偏光特性', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='best', fontsize=9, framealpha=0.9)
    ax.set_xlim(0, 180)
    ax.set_ylim(0, None)  # y軸の下限を0に
    
    # 保存
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"グラフを {output_path} に保存しました。")
    
    return fig, ax

if __name__ == '__main__':
    file_path = '光と波動_実験2_グラフ.xlsx'
    
    print("データを読み込んでいます...")
    experiments = load_experiment_data_improved(file_path)
    
    # 各実験のデータを確認
    for sheet_name, df in experiments.items():
        print(f"\n{sheet_name}:")
        print(f"  データ点数: {len(df)}")
        print(f"  角度範囲: {df['angle'].min():.1f}° ～ {df['angle'].max():.1f}°")
        print(df.head(10))
    
    print("\nグラフを作成しています...")
    create_graph(experiments, output_path='偏光特性グラフ.png')
    
    # 表示（GUI環境でない場合はスキップ）
    try:
        plt.show()
    except:
        print("GUI環境がないため、グラフの表示をスキップしました。")
        print(f"グラフファイルは {output_path} に保存されています。")

