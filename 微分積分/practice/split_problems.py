#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
problems.txtを問題ごとに分割し、問題と解答を分けて整理するスクリプト
"""

import re
from pathlib import Path

def clean_cite(text):
    """引用マーカーを削除"""
    # [cite_start] と [cite: N] を削除
    text = re.sub(r'\[cite_start\]', '', text)
    text = re.sub(r'\[cite:\s*\d+(?:,\s*\d+)*\]', '', text)
    return text.strip()

def extract_problem_number(title):
    """問題番号を抽出してファイル名に適した形式に変換"""
    # ex. 4.1.2, prop. 4.1.9, Th 4.2.2 などを抽出
    match = re.search(r'(?:ex\.?|prop\.?|Th|e\.x\.?|ex)\s*([\d.]+)', title, re.IGNORECASE)
    if match:
        num = match.group(1).replace('.', '_')
        # タイプを判定
        if 'prop' in title.lower():
            return f"prop_{num}"
        elif 'th' in title.lower():
            return f"th_{num}"
        else:
            return f"ex_{num}"
    
    # 演習問題などの場合
    if '演習問題' in title:
        return 'exercise'
    if '極限' in title or '4.2.3' in title:
        return 'limit_4_2_3'
    if '偏微分' in title or '4.3.3' in title:
        return 'partial_derivative_4_3_3'
    if 'マクローリン' in title:
        return 'maclaurin'
    if '連続' in title or '4.2.6' in title:
        return 'continuity_4_2_6'
    if '極値' in title or '4.6.4' in title:
        return 'extremum_4_6_4'
    if '接平面' in title:
        return 'tangent_plane'
    if '制約条件' in title or '4.6.8' in title:
        return 'constraint_4_6_8'
    if '4.4.5' in title:
        return 'differentiability_4_4_5'
    if '4.6.6' in title:
        return 'implicit_4_6_6'
    
    # デフォルト
    return 'problem'

def is_solution_start(line):
    """解答の開始を判定"""
    line_clean = clean_cite(line).lower()
    
    # 解答の開始を示すキーワード
    solution_keywords = [
        '証明', '解く', 'とする', '計算', '定義より', '背理法',
        'よって', 'したがって', 'まず', '次に', '### (', '#### (',
        'lim', 'f_{x}', 'f_{y}', '偏微分', '全微分'
    ]
    
    # 問題文のキーワード（これらが含まれている場合は問題文の可能性が高い）
    problem_keywords = ['示せ', '求めよ', '調べよ', '証明せよ', '展開せよ', '偏微分せよ']
    
    # 問題文のキーワードが含まれている場合は問題文
    if any(keyword in line_clean for keyword in problem_keywords):
        return False
    
    # 解答のキーワードが含まれている場合は解答
    if any(keyword in line_clean for keyword in solution_keywords):
        return True
    
    # 数式のみの行（$$で囲まれている）は解答の可能性が高い
    if '$$' in line or (line_clean.startswith('$') and '=' in line_clean):
        return True
    
    return False

def split_problems(input_file, output_dir):
    """問題を分割して保存"""
    input_path = Path(input_file)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    with input_path.open('r', encoding='utf-8') as f:
        content = f.read()
    
    # セクションで分割（## で始まる行）
    sections = re.split(r'\n(?=##\s)', content)
    
    problem_count = 0
    
    for section in sections:
        if not section.strip() or section.startswith('お預かり') or section.strip() == '---':
            continue
        
        lines = section.split('\n')
        if not lines:
            continue
        
        # セクションタイトルを取得
        title_line = lines[0]
        if not title_line.startswith('##'):
            continue
        
        title = clean_cite(title_line.replace('##', '').strip())
        if not title:
            continue
        
        problem_num = extract_problem_number(title)
        
        # 問題と解答を分離
        problem_lines = []
        solution_lines = []
        in_solution = False
        found_problem_content = False
        
        for i, line in enumerate(lines[1:], 1):
            line_stripped = line.strip()
            if not line_stripped:
                # 空行は問題文と解答の両方に含める可能性がある
                if in_solution:
                    solution_lines.append(line)
                elif found_problem_content:
                    problem_lines.append(line)
                continue
            
            # セパレーター（---）の場合はスキップ
            if line_stripped == '---':
                continue
            
            # 解答の開始を判定
            if not in_solution and is_solution_start(line):
                in_solution = True
            
            # 問題文の内容があるかチェック
            if not found_problem_content and not in_solution:
                line_clean = clean_cite(line)
                # 問題文の内容（数式定義、問題文など）
                if any(keyword in line_clean for keyword in ['示せ', '求めよ', '調べよ', '証明せよ', '展開せよ', '偏微分せよ']) or \
                   ('$' in line_clean and '=' in line_clean) or \
                   'begin{cases}' in line_clean:
                    found_problem_content = True
            
            # 問題文または解答に追加
            if in_solution:
                solution_lines.append(line)
            else:
                problem_lines.append(line)
        
        # 問題と解答が分離できた場合のみ保存
        if problem_lines or solution_lines:
            problem_count += 1
            problem_dir = output_path / f"problem_{problem_count:02d}_{problem_num}"
            problem_dir.mkdir(exist_ok=True)
            
            # 問題文を保存
            problem_text = f"# {title}\n\n"
            if problem_lines:
                problem_text += '\n'.join(problem_lines).strip()
            
            if problem_text.strip() and len(problem_text.strip()) > len(f"# {title}\n\n"):
                (problem_dir / "problem.md").write_text(problem_text, encoding='utf-8')
            
            # 解答を保存
            solution_text = f"# {title} - 解答\n\n"
            if solution_lines:
                solution_text += '\n'.join(solution_lines).strip()
            
            if solution_text.strip() and len(solution_text.strip()) > len(f"# {title} - 解答\n\n"):
                (problem_dir / "solution.md").write_text(solution_text, encoding='utf-8')
            
            print(f"✅ 問題 {problem_count}: {title[:60]}...")
    
    print(f"\n✅ 合計 {problem_count} 個の問題を分割しました。")
    print(f"📁 出力先: {output_path}")

if __name__ == "__main__":
    input_file = Path(__file__).parent / "problems.txt"
    output_dir = Path(__file__).parent / "problems"
    
    split_problems(input_file, output_dir)
