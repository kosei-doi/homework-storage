# 授業内演習 - 解答

[cite_start]$X=\mathbb{R}^{2}$ [cite: 3]
$$d(x,y)=egin{cases}1 & x
e y \ 0 & x=y\end{cases}$$
[cite_start]この $d$ は $X(=\mathbb{R}^{2})$ 上の距離であることを示せ。 [cite: 4]

### (i) [cite_start]$d(x,y) \ge 0$ かつ $d(x,y)=0 \iff x=y$ を示す [cite: 5]
[cite_start]定義より、$d(x,y)$ の値は0または1なので、常に $1 \ge d(x,y) \ge 0$ [cite: 6]
[cite_start]また、$x=y$ のとき $d(x,y)=0$ であり、$d(x,y)=0$ のときも $x=y$ [cite: 6]
[cite_start]$d(x,y)=0 \iff x=y$ が成り立つ。 [cite: 6]

### (ii) [cite_start]$d(x,y)=d(y,x)$ [cite: 7]
* [cite_start]$x
e y$ のとき、$y
e x$ より $d(x,y)=1=d(y,x)$ [cite: 8]
* [cite_start]$x=y$ のとき $y=x$ なので、$d(x,y)=0=d(y,x)$ [cite: 9]

### (iii) [cite_start]$d(x,z) \le d(x,y)+d(y,z)$ [cite: 10]
(A) [cite_start]$x=y=z$ のとき、$d(x,z)=d(x,y)=d(y,z)=0$ [cite: 11]
[cite_start]よって $0 = 0+0$ [cite: 12]
(B) [cite_start]$x=y$ かつ $y
e z$ のとき、$d(x,y)=0$, $d(x,z)=d(y,z)=1$ [cite: 13]
[cite_start]よって $1 \le 0+1$ [cite: 13]
(C) [cite_start]$x
e y$ かつ $x
e z$ かつ $y
e z$ のとき、$d(x,y)=d(x,z)=d(y,z)=1$ [cite: 14]
[cite_start]よって $1 \le 1+1$ [cite: 14, 17]
(D) [cite_start]$x=z$ かつ $x
e y$ のとき $d(x,y)=d(z,y)=1$, $d(x,z)=0$ [cite: 15]
[cite_start]よって $0 \le 1+1$ [cite: 18]
[cite_start]いずれの場合も $d(x,z) \le d(x,y)+d(y,z)$ が成り立つ。 [cite: 16, 18]

### 結論
(i)[cite_start], (ii), (iii)より [cite: 19]
[cite_start]証明できた。 [cite: 20]