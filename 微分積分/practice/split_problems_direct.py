#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
problems.txtの内容を直接読み取って問題ごとに分割し、問題と解答を分けて整理するスクリプト
"""

import re
from pathlib import Path

def clean_cite(text):
    """引用マーカーを削除"""
    text = re.sub(r'\[cite_start\]', '', text)
    text = re.sub(r'\[cite:\s*\d+(?:,\s*\d+)*\]', '', text)
    return text.strip()

def extract_problem_number(title):
    """問題番号を抽出してファイル名に適した形式に変換"""
    # ex. 4.1.2, prop. 4.1.9, Th 4.2.2 などを抽出
    match = re.search(r'(?:ex\.?|prop\.?|Th|e\.x\.?|ex)\s*([\d.]+)', title, re.IGNORECASE)
    if match:
        num = match.group(1).replace('.', '_')
        if 'prop' in title.lower():
            return f"prop_{num}"
        elif 'th' in title.lower():
            return f"th_{num}"
        else:
            return f"ex_{num}"
    
    # 特定の問題タイプを識別
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
    if '極値' in title and '4.6.4' not in title:
        return 'extremum'
    if '4.6.4' in title:
        return 'extremum_4_6_4'
    if '接平面' in title:
        return 'tangent_plane'
    if '制約条件' in title or '4.6.8' in title:
        return 'constraint_4_6_8'
    if '4.4.5' in title:
        return 'differentiability_4_4_5'
    if '4.6.6' in title:
        return 'implicit_4_6_6'
    if '続き' in title:
        return 'continuation'
    
    return 'problem'

def is_solution_start(line):
    """解答の開始を判定"""
    line_clean = clean_cite(line).lower()
    
    # 解答の開始を示すキーワード
    solution_keywords = [
        '証明', '解く', 'とする', '計算', '定義より', '背理法',
        'よって', 'したがって', 'まず', '次に', '### (', '#### (',
        'lim', 'f_{x}', 'f_{y}', '偏微分', '全微分', 'x=r', 'y=kx'
    ]
    
    # 問題文のキーワード
    problem_keywords = ['示せ', '求めよ', '調べよ', '証明せよ', '展開せよ', '偏微分せよ']
    
    if any(keyword in line_clean for keyword in problem_keywords):
        return False
    
    if any(keyword in line_clean for keyword in solution_keywords):
        return True
    
    if '$$' in line or (line_clean.startswith('$') and '=' in line_clean):
        return True
    
    return False

def split_problems_from_content(content, output_dir):
    """問題を分割して保存"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
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
                if in_solution:
                    solution_lines.append(line)
                elif found_problem_content:
                    problem_lines.append(line)
                continue
            
            if line_stripped == '---':
                continue
            
            # 解答の開始を判定
            if not in_solution and is_solution_start(line):
                in_solution = True
            
            # 問題文の内容があるかチェック
            if not found_problem_content and not in_solution:
                line_clean = clean_cite(line)
                if any(keyword in line_clean for keyword in ['示せ', '求めよ', '調べよ', '証明せよ', '展開せよ', '偏微分せよ']) or \
                   ('$' in line_clean and '=' in line_clean) or \
                   'begin{cases}' in line_clean:
                    found_problem_content = True
            
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

# ファイルの内容を直接読み込む
content = """お預かりしたPDFファイルの文字起こしをいたします。

---
## [cite_start]授業内演習 [cite: 1]
ex. [cite_start]4.1.2 [cite: 2]
[cite_start]$X=\mathbb{R}^{2}$ [cite: 3]
$$d(x,y)=\begin{cases}1 & x\ne y \\ 0 & x=y\end{cases}$$
[cite_start]この $d$ は $X(=\mathbb{R}^{2})$ 上の距離であることを示せ。 [cite: 4]

### (i) [cite_start]$d(x,y) \ge 0$ かつ $d(x,y)=0 \iff x=y$ を示す [cite: 5]
[cite_start]定義より、$d(x,y)$ の値は0または1なので、常に $1 \ge d(x,y) \ge 0$ [cite: 6]
[cite_start]また、$x=y$ のとき $d(x,y)=0$ であり、$d(x,y)=0$ のときも $x=y$ [cite: 6]
[cite_start]$d(x,y)=0 \iff x=y$ が成り立つ。 [cite: 6]

### (ii) [cite_start]$d(x,y)=d(y,x)$ [cite: 7]
* [cite_start]$x\ne y$ のとき、$y\ne x$ より $d(x,y)=1=d(y,x)$ [cite: 8]
* [cite_start]$x=y$ のとき $y=x$ なので、$d(x,y)=0=d(y,x)$ [cite: 9]

### (iii) [cite_start]$d(x,z) \le d(x,y)+d(y,z)$ [cite: 10]
(A) [cite_start]$x=y=z$ のとき、$d(x,z)=d(x,y)=d(y,z)=0$ [cite: 11]
[cite_start]よって $0 = 0+0$ [cite: 12]
(B) [cite_start]$x=y$ かつ $y\ne z$ のとき、$d(x,y)=0$, $d(x,z)=d(y,z)=1$ [cite: 13]
[cite_start]よって $1 \le 0+1$ [cite: 13]
(C) [cite_start]$x\ne y$ かつ $x\ne z$ かつ $y\ne z$ のとき、$d(x,y)=d(x,z)=d(y,z)=1$ [cite: 14]
[cite_start]よって $1 \le 1+1$ [cite: 14, 17]
(D) [cite_start]$x=z$ かつ $x\ne y$ のとき $d(x,y)=d(z,y)=1$, $d(x,z)=0$ [cite: 15]
[cite_start]よって $0 \le 1+1$ [cite: 18]
[cite_start]いずれの場合も $d(x,z) \le d(x,y)+d(y,z)$ が成り立つ。 [cite: 16, 18]

### 結論
(i)[cite_start], (ii), (iii)より [cite: 19]
[cite_start]証明できた。 [cite: 20]

---
## prop. [cite_start]4.1.9 [cite: 21]
(1) [cite_start]$A \subset \mathbb{R}^{2}$ : 閉集合とする [cite: 22]
[cite_start]$\{\mathbf{x}_{n}\} \subset A$, $\lim_{n\to\infty} \mathbf{x}_{n}=\mathbf{x}_{0}$ とする。このとき必ず $\mathbf{x}_{0} \in A$ [cite: 23]

### ex. [cite_start]4.1.11 [cite: 24]
(1)[cite_start]を証明せよ。 [cite: 27]
[cite_start]背理法を用いて証明する。 [cite: 30]
[cite_start]$\mathbf{x}_{0} \notin A$ と仮定する。すなわち、$\mathbf{x}_{0} \in A^{c}$ とする。 [cite: 32]
[cite_start]$A^{c}$ は開集合である。 [cite: 35]
[cite_start]よって、開集合の定義より、ある $\epsilon_{0}>0$ が存在し、$U(\mathbf{x}_{0}:\epsilon_{0}) \subset A^{c}$ [cite: 37]
$\lim_{n\to\infty} \mathbf{x}_{n}=\mathbf{x}_{0}$ より、上記の $\epsilon_{0}$ に対し、$N_{0} \in \mathbb{N}$ が存在し、$\forall n \ge N_{0}$ s.t. [cite_start]$d(\mathbf{x}_{n},\mathbf{x}_{0}) < \epsilon_{0}$ [cite: 43]
[cite_start]よって、$\forall n \ge N_{0}$ のとき、$\mathbf{x}_{n} \in U(\mathbf{x}_{0}:\epsilon_{0}) = \{\mathbf{y} \mid d(\mathbf{x}_{0},\mathbf{y}) < \epsilon_{0}\}$ [cite: 44, 45]
[cite_start]$U(\mathbf{x}_{0}:\epsilon_{0}) \subset A^{c}$ より、$\forall n \ge N_{0}$ に対し、$\mathbf{x}_{n} \in A^{c}$ [cite: 46]
[cite_start]これは $\{\mathbf{x}_{n}\} \subset A$ に矛盾 [cite: 48]
よって $\mathbf{x}_{0} \in A$ である。

---
## [cite_start]Th 4.2.2 [cite: 51]
[cite_start]$A \subset \mathbb{R}^{2}, f:A \to \mathbb{R}, \mathbf{x}_{0} \in A \cup \mathbb{R}$ とする。以下は同値 [cite: 52]

(i) [cite_start]$\lim_{\mathbf{x}\to\mathbf{x}_{0}} f(\mathbf{x})=\alpha$ [cite: 53]
(ii) [cite_start]$\lim_{n\to\infty} \mathbf{x}_{n}=\mathbf{x}_{0}$ となる任意の $\{\mathbf{x}_{n}\}_{n=1}^{\infty} \subset A$ に対し、$\lim_{n\to\infty} f(\mathbf{x}_{n})=\alpha$ [cite: 55]

### (proof) [cite_start][cite: 56]
#### (i) [cite_start]$\implies$ (ii) [cite: 57]
$\lim_{\mathbf{x}\to\mathbf{x}_{0}} f(\mathbf{x})=\alpha$ より、$\forall \epsilon>0$ に対し $\exists \delta>0$ が存在し、
$0 < d(\mathbf{x},\mathbf{x}_{0}) < \delta \implies |f(\mathbf{x})-\alpha| [cite_start]< \epsilon$ (*) が成立 [cite: 59, 60]
[cite_start]ここで、$\lim_{n\to\infty} \mathbf{x}_{n}=\mathbf{x}_{0}$ となる任意の点列 $\{\mathbf{x}_{n}\}$ をとる。 [cite: 61]
点列の収束の定義より、上記の $\delta$ に対して $N \in \mathbb{N}$ が存在し、$\forall n \ge N$ ならば
[cite_start]$0 < d(\mathbf{x}_{n},\mathbf{x}_{0}) < \delta$ [cite: 64]
すると、(*)より $n \ge N$ のとき $|f(\mathbf{x}_{n})-\alpha| [cite_start]< \epsilon$ が成り立つ [cite: 66]
[cite_start]これは $\lim_{n\to\infty} f(\mathbf{x}_{n})=\alpha$ の定義である。 [cite: 68]

#### (ii) [cite_start]$\implies$ (i) (背理法) [cite: 69]
(i)が成り立たない、すなわち
$\exists \epsilon_{0}>0, \forall n \in \mathbb{N}$ s.t. $0 < d(\mathbf{x}_{n},\mathbf{x}_{0}) < \frac{1}{n}$ かつ $|f(\mathbf{x}_{n})-\alpha| [cite_start]\ge \epsilon_{0}$ となる $\mathbf{x}_{n} \in A$ が存在する。 [cite: 70, 72]
[cite_start]このとき、$\mathbf{x}_{n} \to \mathbf{x}_{0}$ かつ $f(\mathbf{x}_{n}) \not\to \alpha$ [cite: 73]
[cite_start]これは(ii)に矛盾 [cite: 74]

---
## [cite_start]4.2.3 極限 [cite: 77]
(1) [cite_start]$\lim_{(x,y)\to(0,0)} \frac{xy}{\sqrt{x^{2}+y^{2}}}$ [cite: 78]
[cite_start]$x=r\cos\theta, y=r\sin\theta$ とする [cite: 80]
$$\lim_{r\to 0} \frac{r\cos\theta \cdot r\sin\theta}{\sqrt{r^{2}\cos^{2}\theta+r^{2}\sin^{2}\theta}} = \lim_{r\to 0} \frac{r^{2}\cos\theta \sin\theta}{r} = \lim_{r\to 0} r\cos\theta \sin\theta$$
$g(r)=r$ とすると $|r\cos\theta \sin\theta| [cite_start]\le g(r)$ [cite: 82]
[cite_start]$\lim_{r\to 0} g(r)=0$ [cite: 82]
[cite_start]よって $\lim_{(x,y)\to(0,0)} \frac{xy}{\sqrt{x^{2}+y^{2}}} = \lim_{r\to 0} r\cos\theta \sin\theta = 0$ [cite: 84]

(2) [cite_start]$\lim_{(x,y)\to(0,0)} \frac{xy}{x^{2}+y^{2}}$ [cite: 84]
$$\lim_{r\to 0} \frac{r^{2}\cos\theta \sin\theta}{r^{2}} = \lim_{r\to 0} \cos\theta \sin\theta$$
$r\to 0$ の方向から近づけると $\cos\theta \sin\theta$
一律、$\theta=\frac{\pi}{4}$ の方向から近づけると $\cos\frac{\pi}{4}\sin\frac{\pi}{4} = \frac{1}{2}$
[cite_start]よって、近づける方向によって値が変わるので収束しない [cite: 85]

(3) [cite_start]$\lim_{(x,y)\to(0,0)} \frac{x^{3}+y^{3}}{x^{2}+y^{2}}$ [cite: 86]
[cite_start]$$\lim_{r\to 0} \frac{r^{3}(\cos^{3}\theta+\sin^{3}\theta)}{r^{2}} = \lim_{r\to 0} r(\cos^{3}\theta+\sin^{3}\theta)$$ [cite: 86, 87]
$g(r)=r$ とすると $|r(\cos^{3}\theta+\sin^{3}\theta)| [cite_start]\le 2r = g(r)$ [cite: 88]
[cite_start]$\lim_{r\to 0} g(r)=0$ [cite: 89]
[cite_start]よって $\lim_{(x,y)\to(0,0)} \frac{x^{3}+y^{3}}{x^{2}+y^{2}} = \lim_{r\to 0} r(\cos^{3}\theta+\sin^{3}\theta) = 0$ [cite: 89]

(4) [cite_start]$\lim_{(x,y)\to(0,0)} \frac{xy^{2}}{x^{3}+y^{4}}$ [cite: 79]
[cite_start]$y=kx$ とする。 [cite: 90]
$$\lim_{x\to 0} \frac{x(kx)^{2}}{x^{3}+(kx)^{4}} = \lim_{x\to 0} \frac{k^{2}x^{3}}{x^{3}(1+k^{4}x)} = \lim_{x\to 0} \frac{k^{2}}{1+k^{4}x} = k^{2}$$
間違い
$y=kx^{2}$ とする。 $\lim_{x\to 0} \frac{x(kx^{2})^{2}}{x^{3}+(kx^{2})^{4}} = \lim_{x\to 0} \frac{k^{2}x^{5}}{x^{3}(1+k^{4}x^{5})}$
(90) [cite_start]$y=kx$ とする。 $\lim_{x\to 0} \frac{k^{2}x^{3}}{x^{3}+k^{4}x^{4}} = \lim_{x\to 0} \frac{k^{2}}{1+k^{4}x}$ [cite: 90]
[cite_start]$k=0$ の方向から近づけると $0$ [cite: 92]
[cite_start]$k=1$ の方向から近づけると $\frac{1}{1+k^{4}x} \to 1$ [cite: 92]
間違い
[cite_start]$y=kx$ とする。 $\lim_{x\to 0} \frac{k x^{2}}{x^{2}+k^{2}x^{2}} = \lim_{x\to 0} \frac{k}{1+k^{2}} = \frac{k}{1+k^{2}}$ [cite: 90, 91]
[cite_start]$k=0$ の方向から近づけると $\frac{0}{1}=0$ [cite: 92]
[cite_start]$k=1$ の方向から近づけると $\frac{1}{1+1}=\frac{1}{2}$ [cite: 92]
[cite_start]近づける方向によって値が変わるので、収束しない。 [cite: 92]

## [cite_start]ex 4.2.6 原点において、連続かどうか調べよ [cite: 95]
(1) [cite_start]$f(x,y)=\begin{cases}\frac{xy}{x^{2}+y^{2}} & (x,y)\ne(0,0)\\ 0 & (x,y)=(0,0)\end{cases}$ [cite: 96]
(2) [cite_start]$f(x,y)=\begin{cases}\frac{x^{3}+y^{3}}{x^{2}+y^{2}} & (x,y)\ne(0,0)\\ 0 & (x,y)=(0,0)\end{cases}$ [cite: 97]

(1) [cite_start]4.2.3 (2)より $\mathbf{x}\to\mathbf{0}$ のとき $f(x,y)$ は収束しない。 [cite: 98]
[cite_start]よって原点において連続でない。 [cite: 98]
(2) [cite_start]4.2.3 (3) より $\mathbf{x}\to\mathbf{0}$ のとき $f(x,y)$ は $0$ に収束する [cite: 99]
[cite_start]よって、$\lim_{\mathbf{x}\to\mathbf{0}} f(\mathbf{x})=f(\mathbf{0})$ より連続 [cite: 100]

---
## [cite_start]4.3.3 偏微分せよ。 [cite: 101]
(1) [cite_start]$f(x,y)=x+y^{2}$ [cite: 102]
[cite_start]$$f_{x}(x,y) = \lim_{h\to 0} \frac{f(x+h,y)-f(x,y)}{h} = \lim_{h\to 0} \frac{(x+h+y^{2})-(x+y^{2})}{h} = \lim_{h\to 0} \frac{h}{h}=1$$ [cite: 102]
[cite_start]$f_{x}(x,y)=1$ [cite: 102]
[cite_start]$f_{y}(x,y)=2y$ [cite: 103]

(2) [cite_start]$f(x,y)=\arctan\frac{y}{x}$ [cite: 104]
[cite_start]$\frac{d}{du}\arctan u = \frac{1}{1+u^{2}}$ [cite: 107]
[cite_start]$$f_{x} = \frac{1}{1+(\frac{y}{x})^{2}} \cdot y \cdot (-1)\frac{1}{x^{2}} = -\frac{y}{x^{2}+y^{2}}$$ [cite: 108]
[cite_start]$$f_{y} = \frac{1}{1+(\frac{y}{x})^{2}} \cdot \frac{1}{x} = \frac{x}{x^{2}+y^{2}}$$ [cite: 108]

## [cite_start]マクローリン展開せよ [cite: 109]
(1) [cite_start]$f(x,y)=e^{x}\log(1+y)$ (原点の近くで) (2次まで) [cite: 110]
(2) [cite_start]$f(x,y)=\sin(x+y^{2})$ (4次まで) [cite: 111, 113]

(1) $e^{x} = 1+x+\frac{1}{2!}x^{2} + \dots$
$\log(1+y) = y - \frac{1}{2}y^{2} + \frac{1}{3}y^{3} - \dots$
[cite_start]$$f(x,y) = (1+x+\frac{1}{2}x^{2})(y-\frac{1}{2}y^{2}) + \dots$$ [cite: 115, 116]
$$= y - \frac{1}{2}y^{2} + xy - \frac{1}{2}xy^{2} + \frac{1}{2}x^{2}y - \frac{1}{4}x^{2}y^{2} + \dots$$
2次の項は $y+xy-\frac{1}{2}y^{2}$
[cite_start]間違い $e^{x}\log(1+y) = (1+x+\frac{1}{2}x^{2})(y-\frac{1}{2}y^{2})$ [cite: 116]
[cite_start]$= y+xy-\frac{1}{2}y^{2}$ (2次の項まで) [cite: 116]

(2) [cite_start]$x+y^{2}=t$ とする。 $\sin t = t - \frac{1}{3!}t^{3} + \frac{1}{5!}t^{5} - \dots$ [cite: 117, 118]
[cite_start]$$\sin(x+y^{2}) = (x+y^{2}) - \frac{1}{6}(x+y^{2})^{3} + \dots$$ [cite: 118]
[cite_start]$$= x+y^{2} - \frac{1}{6}\{x^{3}+3x^{2}y^{2}+3xy^{4}+\dots\}$$ [cite: 119]
[cite_start]$$= x+y^{2} - \frac{1}{6}x^{3} - \frac{1}{2}x^{2}y^{2} + \dots$$ (4次の項まで) [cite: 119]

## e.x. [cite_start]4.4.5 原点において、偏微分可能か、全微分可能か [cite: 120, 122]
(1) [cite_start]$f(x,y)=\begin{cases}\frac{x^{3}-y^{3}}{x^{2}+y^{2}} & (x,y)\ne(0,0)\\ 0 & (x,y)=(0,0)\end{cases}$ [cite: 123]
(2) [cite_start]$f(x,y)=\sqrt{|xy|}$ [cite: 124]

### (1)
#### 偏微分
[cite_start]$$f_{x}(0,0) = \lim_{h\to 0} \frac{f(0+h,0)-f(0,0)}{h} = \lim_{h\to 0} \frac{\frac{h^{3}-0^{3}}{h^{2}+0^{2}}-0}{h} = \lim_{h\to 0} \frac{h}{h}=1$$ [cite: 125]
[cite_start]$\mathbf{x}$ に関して偏微分可能で、$f_{x}(0,0)=1$ [cite: 126]
[cite_start]$$f_{y}(0,0) = \lim_{h\to 0} \frac{f(0,0+h)-f(0,0)}{h} = \lim_{h\to 0} \frac{\frac{0^{3}-h^{3}}{0^{2}+h^{2}}-0}{h} = \lim_{h\to 0} \frac{-h}{h}=-1$$ [cite: 127]
[cite_start]$\mathbf{y}$ に関して偏微分可能で、$f_{y}(0,0)=-1$ [cite: 128]

#### 全微分
[cite_start]全微分可能の定義式に代入 [cite: 129]
$$\lim_{(h,k)\to(0,0)} \frac{f(h,k)-f(0,0)-f_{x}(0,0)h-f_{y}(0,0)k}{\sqrt{h^{2}+k^{2}}}$$
[cite_start]$$= \lim_{(h,k)\to(0,0)} \frac{\frac{h^{3}-k^{3}}{h^{2}+k^{2}}-0-1\cdot h-(-1)\cdot k}{\sqrt{h^{2}+k^{2}}} = \lim_{(h,k)\to(0,0)} \frac{\frac{h^{3}-k^{3}-(h-k)(h^{2}+k^{2})}{h^{2}+k^{2}}}{\sqrt{h^{2}+k^{2}}}$$ [cite: 129]
$$= \lim_{(h,k)\to(0,0)} \frac{h^{3}-k^{3}-(h^{3}+hk^{2}-k h^{2}-k^{3})}{(h^{2}+k^{2})^{\frac{3}{2}}} = \lim_{(h,k)\to(0,0)} \frac{-hk^{2}+k h^{2}}{(h^{2}+k^{2})^{\frac{3}{2}}}$$
[cite_start]$$= \lim_{(h,k)\to(0,0)} \frac{hk(h-k)}{(h^{2}+k^{2})^{\frac{3}{2}}}$$ [cite: 132]
[cite_start]$h=-k$ として近づけると $\frac{(-k)k(k-(-k))}{(k^{2}+(-k)^{2})^{\frac{3}{2}}} = \frac{-2k^{3}}{(2k^{2})^{\frac{3}{2}}} = \frac{-2k^{3}}{2^{\frac{3}{2}}k^{3}} = -\frac{1}{\sqrt{2}} (\ne 0)$ [cite: 132, 134, 135]
[cite_start]全微分不可。 [cite: 133]

### (2) [cite_start]$f(x,y)=\sqrt{|xy|}$ [cite: 136]
#### 偏微分
[cite_start]$$f_{x}(0,0) = \lim_{h\to 0} \frac{f(0+h,0)-f(0,0)}{h} = \lim_{h\to 0} \frac{\sqrt{|h\cdot 0|}-\sqrt{|0\cdot 0|}}{h} = \lim_{h\to 0} \frac{0}{h}=0$$ [cite: 137]
[cite_start]$\mathbf{x}$ に関して偏微分可能で、$f_{x}(0,0)=0$ [cite: 138]
[cite_start]$$f_{y}(0,0) = \lim_{h\to 0} \frac{f(0,0+h)-f(0,0)}{h} = \lim_{h\to 0} \frac{0}{h}=0$$ [cite: 139]
[cite_start]$\mathbf{y}$ に関して偏微分可能で、$f_{y}(0,0)=0$ [cite: 140]

#### 全微分
全微分可能の定義式に代入
[cite_start]$$\lim_{(h,k)\to(0,0)} \frac{f(0+h,0+k)-f(0,0)-f_{x}(0,0)h-f_{y}(0,0)k}{\sqrt{h^{2}+k^{2}}} = \lim_{(h,k)\to(0,0)} \frac{\sqrt{|hk|}}{\sqrt{h^{2}+k^{2}}}$$ [cite: 141]
[cite_start]例えば、$h=k$ として近づけると [cite: 142]
[cite_start]$$\frac{\sqrt{|k^{2}|}}{\sqrt{k^{2}+k^{2}}} = \frac{|k|}{\sqrt{2}|k|} = \frac{1}{\sqrt{2}} (\ne 0)$$ [cite: 143]
[cite_start]全微分不可。 [cite: 144]

## e.x. 4.6.4. [cite_start]極値を調べよ [cite: 145]
(1) [cite_start]$f(x,y)=4xy-2y^{2}-x^{4}$ [cite: 146]

### (1)
[cite_start]$f_{x}(x,y)=4y-4x^{3}$ [cite: 149]
[cite_start]$f_{y}(x,y)=4x-4y$ [cite: 149]
[cite_start]$f_{x}=0, f_{y}=0$ を解く [cite: 150, 151]
[cite_start]$4x-4y=0 \implies y=x$ [cite: 152]
[cite_start]$4x-4x^{3}=0 \implies 4x(1-x^{2})=0 \implies 4x(1-x)(1+x)=0$ [cite: 152]
[cite_start]極値候補は、$(-1,-1), (0,0), (1,1)$ [cite: 152]

2階偏導関数
[cite_start]$f_{xx}=-12x^{2}, f_{yy}=-4, f_{xy}=4$ [cite: 153]
[cite_start]$D = (f_{xy})^{2}-f_{xx}f_{yy} = 4^{2}-(-12x^{2})(-4) = 16-48x^{2}$ [cite: 154]

* [cite_start]$(0,0)$: $D(0,0)=16>0$ [cite: 155]
    [cite_start]よって $(0,0)$ は極値でない (鞍点) [cite: 155]
* [cite_start]$(1,1)$: $D(1,1)=16-48=-32<0$ [cite: 156]
    [cite_start]$f_{xx}(1,1)=-12<0$ [cite: 156]
    [cite_start]よって $(1,1)$ は極大で、$f(1,1)=4(1)(1)-2(1)^{2}-1^{4}=1$ [cite: 156]
* [cite_start]$(-1,-1)$: $D(-1,-1)=16-48(-1)^{2}=-32<0$ [cite: 157]
    [cite_start]$f_{xx}(-1,-1)=-12(-1)^{2}=-12<0$ [cite: 157]
    [cite_start]よって $(-1,-1)$ は極大で、$f(-1,-1)=4(-1)(-1)-2(-1)^{2}-(-1)^{4}=1$ [cite: 157]

---
## 続き
(2) [cite_start]$f(x,y)=x^{3}+y^{3}-3xy$ [cite: 159]

### (2)
[cite_start]$f_{x}(x,y)=3x^{2}-3y$, $f_{y}(x,y)=3y^{2}-3x$ [cite: 160]
[cite_start]$f_{x}=f_{y}=0$ を解く [cite: 160]
$$\begin{cases} 3x^{2}=3y \\ 3y^{2}=3x \end{cases} \implies \begin{cases} y=x^{2} \\ x=y^{2} \end{cases}$$
[cite_start]$x=(x^{2})^{2} \implies x=x^{4} \implies x(x^{3}-1)=0$ [cite: 161]
$x=0$ のとき $y=0$, $x=1$ のとき $y=1$
[cite_start]$(0,0), (1,1)$ が極値候補 [cite: 162]

2階偏導関数
[cite_start]$f_{xx}(x,y)=6x, f_{yy}(x,y)=6y, f_{xy}(x,y)=-3$ [cite: 163]
[cite_start]$D = (-3)^{2}-(6x)(6y) = 9-36xy$ [cite: 164]

* [cite_start]$(0,0)$: $D(0,0)=9>0$ [cite: 165]
    [cite_start]$\to$ 極値でない [cite: 165]
* [cite_start]$(1,1)$: $D(1,1)=9-36=-27<0$ [cite: 167]
    [cite_start]$f_{xx}(1,1)=6>0$ [cite: 167]
    [cite_start]よって、$(1,1)$ は極小で、$f(1,1)=1^{3}+1^{3}-3(1)(1)=-1$ [cite: 167]

(3) [cite_start]$f(x,y)=x^{4}+y^{4}$ [cite: 168]
[cite_start]$f_{x}=4x^{3}, f_{y}=4y^{3}$ [cite: 169]
[cite_start]$f_{x}=0, f_{y}=0 \implies x=0, y=0$ [cite: 169]
極値候補は $(0,0)$

2階偏導関数
[cite_start]$f_{xx}=12x^{2}, f_{yy}=12y^{2}, f_{xy}=0$ [cite: 170]
[cite_start]$D = 0^{2}-(12x^{2})(12y^{2}) = -144x^{2}y^{2}$ [cite: 171]
[cite_start]$D(0,0)=0$ なので、判定法は使えない。 [cite: 172]
[cite_start]$f(0,0)=0$ [cite: 173]
[cite_start]$(x,y) \in \mathbb{R}^{2}$ に対し、$f(0,0)=0 \le f(x,y)$ [cite: 173]
[cite_start]よって $(0,0)$ は極小。 [cite: 173]

(4) [cite_start]$f(x,y)=2x^{4}-3x^{2}y+y^{2}$ [cite: 174]
[cite_start]$f_{x}=8x^{3}-6xy$, $f_{y}=-3x^{2}+2y$ [cite: 175]
$f_{x}=0, f_{y}=0 \implies y=\frac{3}{2}x^{2}$
$8x^{3}-6x(\frac{3}{2}x^{2}) = 8x^{3}-9x^{3} = -x^{3} = 0 \implies x=0, y=0$
極値候補は $(0,0)$

2階偏導関数
[cite_start]$f_{xx}=24x^{2}-6y$, $f_{yy}=2$, $f_{xy}=-6x$ [cite: 176]
$D = (-6x)^{2}-(24x^{2}-6y)(2) = 36x^{2}-48x^{2}+12y = -12x^{2}+12y$
[cite_start]$D(0,0)=0$ : 判定不可。 [cite: 177]
[cite_start]$f(0,0)=0$ [cite: 178]
$y=mx^{2}$ として近づける。
[cite_start]$$f(x,mx^{2}) = 2x^{4}-3x^{2}(mx^{2})+(mx^{2})^{2} = x^{4}(2-3m+m^{2}) = x^{4}(m^{2}-3m+2)$$ [cite: 179]
[cite_start]$$= x^{4}(m-1)(m-2)$$ [cite: 180]
[cite_start]例えば $m=3$ のとき $f(x,3x^{2}) = x^{4}(3-1)(3-2) = 2x^{4} > 0 = f(0,0)$ [cite: 181]
$m=0$ のとき $f(x,0) = 2x^{4} > 0 = f(0,0)$
[cite_start]$m=\frac{3}{2}$ のとき $f(x,\frac{3}{2}x^{2}) = x^{4}(\frac{3}{2}-1)(\frac{3}{2}-2) = -\frac{1}{4}x^{4} < 0 = f(0,0)$ [cite: 182]
[cite_start]$(0,0)$ は極値ではない。 [cite: 183]

## e.x. [cite_start]4.6.6 [cite: 184]
[cite_start]$(\begin{smallmatrix} x_{0} \\ y_{0} \end{smallmatrix})$ で $\phi(x,y(x))=0$ かつ $y(x_{0})=y_{0}$ をみたす関数 $y(x)$ が存在することを確認し、 $y'(x)$ を求めよ。 [cite: 185, 186]

(1) $\phi(x,y)=x^{2}+y^{2}-1, (\begin{smallmatrix} x_{0} \\ y_{0} \end{smallmatrix})=(\begin{smallmatrix} 1/\sqrt{2} \\ -1/\sqrt{2} \end{smallmatrix})$
[cite_start]$\phi_{y}(x,y)=2y$ [cite: 188]
[cite_start]$\phi_{y}(1/\sqrt{2}, -1/\sqrt{2}) = -2/\sqrt{2} \ne 0$ [cite: 189]
[cite_start]よって条件を満たす $y(x)$ が存在する。 [cite: 189]
[cite_start]$y'(x) = -\frac{\phi_{x}}{\phi_{y}} = -\frac{2x}{2y} = -\frac{x}{y}$ [cite: 190]

(2) [cite_start]$\phi(x,y)=x^{3}+y^{3}-2xy, (\begin{smallmatrix} x_{0} \\ y_{0} \end{smallmatrix})=(\begin{smallmatrix} 1 \\ 1 \end{smallmatrix})$ [cite: 187]
[cite_start]$\phi_{x}=3x^{2}-2y, \phi_{y}=3y^{2}-2x$ [cite: 191]
[cite_start]$\phi_{y}(1,1)=3(1)^{2}-2(1)=1 \ne 0$ [cite: 192]
[cite_start]よって $(1,1)$ の近くで陰関数 $y(x)$ が存在する [cite: 193]
[cite_start]$y'(x) = -\frac{\phi_{x}}{\phi_{y}} = -\frac{3x^{2}-2y}{3y^{2}-2x}$ [cite: 194]

## ex. [cite_start]4.6.8 制約条件 $\phi(x,y)=0$ の下での $f(x,y)$ の最大最小を求めよ。 [cite: 195]
(1) [cite_start]$\phi(x,y)=xy-1, f(x,y)=x^{2}+y^{2}$ [cite: 196]

### (1)
[cite_start]$F(x,y,\lambda) = f(x,y)-\lambda \phi(x,y) = x^{2}+y^{2}-\lambda(xy-1)$ とおいて、$F_{x}=F_{y}=F_{\lambda}=0$ を解く。 [cite: 198]
[cite_start]$F_{x}=2x-\lambda y, F_{y}=2y-\lambda x, F_{\lambda}=-xy+1$ [cite: 199]
[cite_start]$$\begin{cases} 2x-\lambda y=0 \\ 2y-\lambda x=0 \\ -xy+1=0 \end{cases}$$ [cite: 200]
$x \ne 0, y \ne 0$
$2x=\lambda y, 2y=\lambda x \implies \lambda = \frac{2x}{y} = \frac{2y}{x} \implies 2x^{2}=2y^{2} \implies x^{2}=y^{2} \implies y=\pm x$
$xy=1$ より $x^{2}=1 \implies x=\pm 1$
[cite_start]$(x,y)=(1,1), (-1,-1)$ [cite: 202]
[cite_start]$f(1,1)=1^{2}+1^{2}=2$ [cite: 203]
$f(-1,-1)=(-1)^{2}+(-1)^{2}=2$
制約条件 $y=1/x$ を代入して挙動をみる: $f(x, 1/x)=x^{2}+1/x^{2}$
[cite_start]$\lim_{x\to\pm\infty} f(x, 1/x) = \infty$, $\lim_{x\to 0} f(x, 1/x) = \infty$ [cite: 203]
[cite_start]よって $(x,y)=(1,1), (-1,-1)$ のとき最小値2、最大値はなし [cite: 203]

---
## 続き
(2) [cite_start]$\phi(x,y)=x^{3}+y^{3}+x+y-4, f(x,y)=xy$ [cite: 204]

### (2)
[cite_start]$F(x,y,\lambda) = xy-\lambda(x^{3}+y^{3}+x+y-4)$ [cite: 205]
[cite_start]$F_{x}=F_{y}=F_{\lambda}=0$ を解く [cite: 206]
[cite_start]$F_{x}=y-3\lambda x^{2}-\lambda, F_{y}=x-3\lambda y^{2}-\lambda, F_{\lambda}=-x^{3}-y^{3}-x-y+4$ [cite: 207]
[cite_start]$$\begin{cases} y=\lambda(3x^{2}+1) \\ x=\lambda(3y^{2}+1) \\ x^{3}+y^{3}+x+y-4=0 \end{cases}$$ [cite: 208]
[cite_start]$\lambda = \frac{y}{3x^{2}+1} = \frac{x}{3y^{2}+1}$ [cite: 210]
[cite_start]$y(3y^{2}+1)=x(3x^{2}+1)$ [cite: 209]
[cite_start]$3y^{3}+y=3x^{3}+x \implies 3(x^{3}-y^{3})+(x-y)=0$ [cite: 210]
[cite_start]$3(x-y)(x^{2}+xy+y^{2})+(x-y)=0$ [cite: 210]
[cite_start]$(x-y)\{3(x^{2}+xy+y^{2})+1\}=0$ [cite: 210]
[cite_start]$3(x^{2}+xy+y^{2})+1 > 0$ なので $x-y=0 \implies x=y$ [cite: 211]
[cite_start]制約条件に代入: $x^{3}+x^{3}+x+x-4=0 \implies 2x^{3}+2x-4=0 \implies 2(x^{3}+x-2)=0$ [cite: 212]
[cite_start]$2(x-1)(x^{2}+x+2)=0$ [cite: 213]
$x^{2}+x+2 = (x+\frac{1}{2})^{2}+\frac{7}{4} > 0$
[cite_start]よって $x=1$ [cite: 215]
[cite_start]$x=y=1$ より $(x,y)=(1,1)$ [cite: 215]
[cite_start]$f(1,1)=1\cdot 1=1$ [cite: 214]
[cite_start]$x\to\infty$ のとき、制約条件 $x^{3}+y^{3}+x+y-4=0$ を満たすためには、$y\to -\infty$ でなくてはいけない。 [cite: 216]
[cite_start]そしてそのとき $f(x,y)=xy \to -\infty$ [cite: 217]
[cite_start]同様に $x\to -\infty$ のときは $y\to \infty$ で $f(x,y) \to -\infty$ [cite: 217, 218]
[cite_start]よって、$(x,y)=(1,1)$ のとき最大値1、最小値なし [cite: 219]

---
## [cite_start]演習問題 [cite: 220]
### [cite_start]原点において連続か調べよ [cite: 221]
(1) [cite_start]$f(x,y)=\begin{cases}\frac{x^{2}y}{x^{2}+y^{2}} & (x,y)\ne(0,0)\\ 0 & (x,y)=(0,0)\end{cases}$ [cite: 222]
(2) [cite_start]$f(x,y)=\begin{cases}\frac{x+y}{x-y} & x\ne y \\ 0 & x=y \end{cases}$ [cite: 225]

#### (1)
[cite_start]$x=r\cos\theta, y=r\sin\theta$ とする [cite: 229]
[cite_start]$$\lim_{(x,y)\to(0,0)} f(x,y) = \lim_{r\to 0} \frac{r^{2}\cos^{2}\theta \cdot r\sin\theta}{r^{2}} = \lim_{r\to 0} r\cos^{2}\theta \sin\theta$$ [cite: 226, 229]
$g(r)=r$ とおくと $|r\cos^{2}\theta \sin\theta| [cite_start]\le r = g(r)$ [cite: 227, 230]
[cite_start]$\lim_{r\to 0} g(r)=0$ [cite: 230]
[cite_start]よって $\lim_{(x,y)\to(0,0)} f(x,y) = 0 = f(0,0)$ より連続 [cite: 230, 231]

#### (2)
$x=y$ として近づけると $f(x,y)=0$ (定義より)
$y=kx, k\ne 1$ として近づけると
$$\lim_{x\to 0} \frac{x+kx}{x-kx} = \lim_{x\to 0} \frac{1+k}{1-k}$$
$k=0$ の方向から近づけると $1$
[cite_start]$x=y$ 以外の方向から近づけると値が変わるので、極限は存在しない。 [cite: 232, 233]
[cite_start]よって不連続 [cite: 233]

### [cite_start]原点において、偏微分可能か？, 全微分可能か？ [cite: 234]
(1) [cite_start]$f(x,y)=|xy|$ [cite: 235]
(2) [cite_start]$f(x,y)=\begin{cases}\frac{|xy|}{\sqrt{x^{2}+y^{2}}} & (x,y)\ne(0,0)\\ 0 & (x,y)=(0,0)\end{cases}$ [cite: 235]

#### (1) $f(x,y)=|xy|$
[cite_start]$$f_{x}(0,0) = \lim_{h\to 0} \frac{f(0+h,0)-f(0,0)}{h} = \lim_{h\to 0} \frac{|h\cdot 0|-0}{h} = \lim_{h\to 0} \frac{0}{h}=0$$ [cite: 237]
[cite_start]$\mathbf{x}$ に関して偏微分可、$\mathbf{y}$ についても同様 $f_{y}(0,0)=0$ [cite: 237]
[cite_start]$$\lim_{(x,y)\to(0,0)} \frac{f(x,y)-f(0,0)-f_{x}(0,0)x-f_{y}(0,0)y}{\sqrt{x^{2}+y^{2}}} = \lim_{(x,y)\to(0,0)} \frac{|xy|}{\sqrt{x^{2}+y^{2}}}$$ [cite: 239, 240, 241, 242]
$x=r\cos\theta, y=r\sin\theta$ とする
[cite_start]$$\lim_{r\to 0} \frac{|r^{2}\cos\theta \sin\theta|}{r} = \lim_{r\to 0} r|\cos\theta \sin\theta|$$ [cite: 243, 244]
$g(r)=r$ とおくと $r|\cos\theta \sin\theta| [cite_start]\le r = g(r)$ [cite: 244, 247]
[cite_start]$\lim_{r\to 0} g(r)=0$ [cite: 248]
[cite_start]よって $=0$ 全微分可 [cite: 248]

#### (2) $f(x,y)=\frac{|xy|}{\sqrt{x^{2}+y^{2}}}$
[cite_start]$$f_{x}(0,0) = \lim_{h\to 0} \frac{f(0+h,0)-f(0,0)}{h} = \lim_{h\to 0} \frac{0-0}{h}=0$$ [cite: 249]
[cite_start]$\mathbf{x}$ に関して偏微分可、$\mathbf{y}$ についても同様 $f_{y}(0,0)=0$ [cite: 249]
[cite_start]$$\lim_{(x,y)\to(0,0)} \frac{f(x,y)-f(0,0)-f_{x}(0,0)x-f_{y}(0,0)y}{\sqrt{x^{2}+y^{2}}} = \lim_{(x,y)\to(0,0)} \frac{\frac{|xy|}{\sqrt{x^{2}+y^{2}}}}{\sqrt{x^{2}+y^{2}}} = \lim_{(x,y)\to(0,0)} \frac{|xy|}{x^{2}+y^{2}}$$ [cite: 250]
$x=r\cos\theta, y=r\sin\theta$ とする
[cite_start]$$\lim_{r\to 0} \frac{|r^{2}\cos\theta \sin\theta|}{r^{2}} = |\cos\theta \sin\theta|$$ [cite: 250]
例えば、$\theta=\frac{\pi}{4}$ とすると $|\cos\frac{\pi}{4}\sin\frac{\pi}{4}| [cite_start]= \frac{1}{2} (\ne 0)$ [cite: 250]
[cite_start]よって全微分不可。 [cite: 250]

---
## [cite_start]極値を調べよ。 [cite: 251]
[cite_start]$f(x,y)=x^{4}+y^{4}-x^{2}-2xy-y^{2}+3$ [cite: 252]
[cite_start]$f_{x}=4x^{3}-2x-2y$, $f_{y}=4y^{3}-2x-2y$ [cite: 252]
[cite_start]$f_{xx}=12x^{2}-2$, $f_{yy}=12y^{2}-2$, $f_{xy}=-2$ [cite: 252, 254]

[cite_start]$f_{x}=f_{y}=0$ を解く [cite: 255]
[cite_start]$4x^{3}-2x-2y=4y^{3}-2x-2y \implies 4x^{3}-4y^{3}=0 \implies x^{3}-y^{3}=0 \implies x=y$ [cite: 257, 259]
[cite_start]$4x^{3}-2x-2x=0 \implies 4x^{3}-4x=0 \implies 4x(x^{2}-1)=0$ [cite: 258, 261]
$x=0, 1, -1$
[cite_start]極値候補は $(0,0), (1,1), (-1,-1)$ [cite: 259]

[cite_start]$D = (f_{xy})^{2}-f_{xx}f_{yy} = (-2)^{2}-(12x^{2}-2)(12y^{2}-2)$ [cite: 260]
[cite_start]$$D = 4-(144x^{2}y^{2}-24x^{2}-24y^{2}+4) = -144x^{2}y^{2}+24x^{2}+24y^{2} = 24(-6x^{2}y^{2}+x^{2}+y^{2})$$ [cite: 260, 262, 263, 271]

* [cite_start]$(0,0)$: $D(0,0)=0$ [cite: 264]
    [cite_start]$f(0,0)=3$ [cite: 264, 269]
    [cite_start]$f(x,y)=x^{4}+y^{4}-(x+y)^{2}+3$ [cite: 265, 266]
    [cite_start]$y=-x (x\ne 0)$ のとき $f(x,-x)=x^{4}+x^{4}-0+3 = 2x^{4}+3 > 3 = f(0,0)$ [cite: 267]
    [cite_start]$y=x$ のとき $f(x,x)=x^{4}+x^{4}-(2x)^{2}+3 = 2x^{4}-4x^{2}+3$ [cite: 268]
    $2x^{4}-4x^{2} = 2x^{2}(x^{2}-2)$
    $x \to 0$ の近くで $x^{2}-2 < 0$ なので $f(x,x)-3 < 0 \implies f(x,x) < 3 = f(0,0)$
    [cite_start]$(0,0)$ のどんな近くにも $f(x,y) > f(0,0)$ となる点と $f(x,y) < f(0,0)$ となる点があるから、$(0,0)$ は極値でない。 [cite: 270]

* [cite_start]$(-1,-1)$: $D(-1,-1)=24(-6+1+1)=-96<0$ [cite: 273]
    [cite_start]$f_{xx}(-1,-1)=12(-1)^{2}-2=10>0$ [cite: 276]
    [cite_start]$(-1,-1)$ は極小で、$f(-1,-1)=(-1)^{4}+(-1)^{4}-(-1)^{2}-2(-1)(-1)-(-1)^{2}+3=1+1-1-2-1+3=1$ [cite: 276]

* [cite_start]$(1,1)$: $D(1,1)=24(-6+1+1)=-96<0$ [cite: 277]
    [cite_start]$f_{xx}(1,1)=12(1)^{2}-2=10>0$ [cite: 278]
    [cite_start]$(1,1)$ で極小値 $f(1,1)=1$ [cite: 278]

---
## 続き
(2) [cite_start]$\phi(x,y)=x^{3}+y^{3}+2x+2y-6=0$ の下で $f(x,y)=2xy$ の最大・最小を調べよ。 [cite: 279]
[cite_start]$F(x,y,\lambda) = f(x,y)-\lambda \phi(x,y) = 2xy-\lambda(x^{3}+y^{3}+2x+2y-6)$ [cite: 281, 282]
[cite_start]$F_{x}=F_{y}=F_{\lambda}=0$ を解く [cite: 283]
[cite_start]$F_{x}=2y-3\lambda x^{2}-2\lambda, F_{y}=2x-3\lambda y^{2}-2\lambda$ [cite: 284]
[cite_start]$F_{x}-F_{y}=0 \implies 2y-2x-3\lambda x^{2}+3\lambda y^{2}=0$ [cite: 285]
$2(y-x)-3\lambda(x^{2}-y^{2})=0$
$2(y-x)+3\lambda(y-x)(x+y)=0$
[cite_start]$(y-x)\{2+3\lambda(x+y)\}=0$ [cite: 288]
$x=y$ または $2+3\lambda(x+y)=0$

1. [cite_start]$x=y$ のとき [cite: 294]
[cite_start]制約条件に代入: $x^{3}+x^{3}+2x+2x-6=0 \implies 2x^{3}+4x-6=0$ [cite: 289, 290]
[cite_start]$2(x^{3}+2x-3)=0 \implies 2(x-1)(x^{2}+x+3)=0$ [cite: 291]
[cite_start]$x^{2}+x+3>0$ より $x=1$ [cite: 292]
[cite_start]極値候補は $(1,1)$, $f(1,1)=2(1)(1)=2$ [cite: 293]

2. $2+3\lambda(x+y)=0$ のとき $\lambda = -\frac{2}{3(x+y)}$
$\lambda$ を $F_{x}=0$ に代入: $2y-3(-\frac{2}{3(x+y)})x^{2}-2(-\frac{2}{3(x+y)})=0$
$2y+\frac{2x^{2}}{x+y}+\frac{4}{3(x+y)}=0 \implies 6y(x+y)+6x^{2}+4=0 \implies 6xy+6y^{2}+6x^{2}+4=0$
$6(x^{2}+xy+y^{2})+4=0$
$x^{2}+xy+y^{2} \ge \frac{1}{4}(x+y)^{2} + \frac{3}{4}(x-y)^{2} \ge 0$ なので、これは解なし

[cite_start]$x\to\infty$ ならば $\phi=0$ を満たすには $y\to -\infty$ が必要 [cite: 295]
[cite_start]このとき $f(x,y)=2xy \to -\infty$ [cite: 296]
[cite_start]$f(1,1)=2$ は最大値、最小値なし [cite: 297]

---
## [cite_start]③ $x_{0},y_{0}$ における接平面の方程式を求めよ。(全微分可能は認める。) [cite: 298]
曲面 $z=f(x,y)$ の点 $(x_{0},y_{0},f(x_{0},y_{0}))$ で曲面に接する平面の方程式は
[cite_start]$$Z = f(x_{0},y_{0}) + f_{x}(x_{0},y_{0})(x-x_{0}) + f_{y}(x_{0},y_{0})(y-y_{0})$$ [cite: 300]
[cite_start]例: $f(x,y)=xe^{xy}$ [cite: 301]
[cite_start]$f_{x} = 1\cdot e^{xy} + x\cdot e^{xy}\cdot y = e^{xy}(1+xy)$ [cite: 302]
[cite_start]$f_{y} = x\cdot e^{xy}\cdot x = x^{2}e^{xy}$ [cite: 302]
接平面の方程式は
[cite_start]$$Z = x_{0}e^{x_{0}y_{0}} + e^{x_{0}y_{0}}(1+x_{0}y_{0})(x-x_{0}) + x_{0}^{2}e^{x_{0}y_{0}}(y-y_{0})$$ [cite: 303, 304]

---
## 続き
[cite_start]$f(x,y)=e^{-(x^{2}+y^{2})}$, $x=g(t), y=h(t)$ ($g,h$ は微分可能とする。) [cite: 305]
[cite_start]$\frac{df}{dt}=0$ となる条件を求めよ。 [cite: 305]
[cite_start]$$\frac{df}{dt} = \frac{\partial f}{\partial x}\frac{dx}{dt} + \frac{\partial f}{\partial y}\frac{dy}{dt}$$ [cite: 305]
[cite_start]$f_{x}=-2xe^{-(x^{2}+y^{2})}$, $f_{y}=-2ye^{-(x^{2}+y^{2})}$ [cite: 306]
[cite_start]$x=g(t), y=h(t)$ を代入して [cite: 307]
[cite_start]$$\frac{df}{dt} = -2xe^{-(x^{2}+y^{2})}g'(t) - 2ye^{-(x^{2}+y^{2})}h'(t)$$ [cite: 308]
[cite_start]$$= -2e^{-(x^{2}+y^{2})}\{x g'(t)+y h'(t)\}$$ [cite: 308]
[cite_start]$\frac{df}{dt}=0$ となるためには、$e^{-(x^{2}+y^{2})} \ne 0$ より $x g'(t)+y h'(t)=0$ が必要 [cite: 310]
[cite_start]$$g(t)g'(t)+h(t)h'(t)=0$$ [cite: 311]

---
## 続き
[cite_start]$(\chi,y) \mapsto (t,s)=(2x+y, x-y) \mapsto f(t(x,y), s(x,y))$ ($f$ : 微分可)とする。 [cite: 313]
(1) [cite_start]$f_{x}, f_{y}$ を $f_{t}, f_{s}$ で表せ [cite: 314]
(2) [cite_start]$f_{t}, f_{s}$ を $f_{x}, f_{y}$ で表せ [cite: 315]

[cite_start]$$\begin{cases} t=2x+y \\ s=x-y \end{cases}$$ [cite: 316]

### (1)
[cite_start]$$\frac{\partial f}{\partial x} = \frac{\partial f}{\partial t}\frac{\partial t}{\partial x} + \frac{\partial f}{\partial s}\frac{\partial s}{\partial x} = f_{t}\cdot 2 + f_{s}\cdot 1 = 2f_{t}+f_{s}$$ [cite: 318, 323]
[cite_start]$$\frac{\partial f}{\partial y} = \frac{\partial f}{\partial t}\frac{\partial t}{\partial y} + \frac{\partial f}{\partial s}\frac{\partial s}{\partial y} = f_{t}\cdot 1 + f_{s}\cdot (-1) = f_{t}-f_{s}$$ [cite: 319, 320]

### (2)
[cite_start]$t+s = (2x+y)+(x-y)=3x \implies x = \frac{1}{3}t+\frac{1}{3}s$ [cite: 324]
[cite_start]$t-2s = (2x+y)-2(x-y)=3y \implies y = \frac{1}{3}t-\frac{2}{3}s$ [cite: 322]
[cite_start]$$\frac{\partial f}{\partial t} = \frac{\partial f}{\partial x}\frac{\partial x}{\partial t} + \frac{\partial f}{\partial y}\frac{\partial y}{\partial t} = f_{x}\cdot \frac{1}{3} + f_{y}\cdot \frac{1}{3} = \frac{1}{3}f_{x}+\frac{1}{3}f_{y}$$ [cite: 326, 327]
[cite_start]$$\frac{\partial f}{\partial s} = \frac{\partial f}{\partial x}\frac{\partial x}{\partial s} + \frac{\partial f}{\partial y}\frac{\partial y}{\partial s} = f_{x}\cdot \frac{1}{3} + f_{y}\cdot (-\frac{2}{3}) = \frac{1}{3}f_{x}-\frac{2}{3}f_{y}$$ [cite: 326, 327]
"""

if __name__ == "__main__":
    output_dir = Path(__file__).parent / "problems"
    split_problems_from_content(content, output_dir)
