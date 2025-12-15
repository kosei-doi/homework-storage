# Th 4.2.2 - 解答

[cite_start]$A \subset \mathbb{R}^{2}, f:A 	o \mathbb{R}, \mathbf{x}_{0} \in A \cup \mathbb{R}$ とする。以下は同値 [cite: 52]

(i) [cite_start]$\lim_{\mathbf{x}	o\mathbf{x}_{0}} f(\mathbf{x})=lpha$ [cite: 53]
(ii) [cite_start]$\lim_{n	o\infty} \mathbf{x}_{n}=\mathbf{x}_{0}$ となる任意の $\{\mathbf{x}_{n}\}_{n=1}^{\infty} \subset A$ に対し、$\lim_{n	o\infty} f(\mathbf{x}_{n})=lpha$ [cite: 55]

### (proof) [cite_start][cite: 56]
#### (i) [cite_start]$\implies$ (ii) [cite: 57]
$\lim_{\mathbf{x}	o\mathbf{x}_{0}} f(\mathbf{x})=lpha$ より、$orall \epsilon>0$ に対し $\exists \delta>0$ が存在し、
$0 < d(\mathbf{x},\mathbf{x}_{0}) < \delta \implies |f(\mathbf{x})-lpha| [cite_start]< \epsilon$ (*) が成立 [cite: 59, 60]
[cite_start]ここで、$\lim_{n	o\infty} \mathbf{x}_{n}=\mathbf{x}_{0}$ となる任意の点列 $\{\mathbf{x}_{n}\}$ をとる。 [cite: 61]
点列の収束の定義より、上記の $\delta$ に対して $N \in \mathbb{N}$ が存在し、$orall n \ge N$ ならば
[cite_start]$0 < d(\mathbf{x}_{n},\mathbf{x}_{0}) < \delta$ [cite: 64]
すると、(*)より $n \ge N$ のとき $|f(\mathbf{x}_{n})-lpha| [cite_start]< \epsilon$ が成り立つ [cite: 66]
[cite_start]これは $\lim_{n	o\infty} f(\mathbf{x}_{n})=lpha$ の定義である。 [cite: 68]

#### (ii) [cite_start]$\implies$ (i) (背理法) [cite: 69]
(i)が成り立たない、すなわち
$\exists \epsilon_{0}>0, orall n \in \mathbb{N}$ s.t. $0 < d(\mathbf{x}_{n},\mathbf{x}_{0}) < rac{1}{n}$ かつ $|f(\mathbf{x}_{n})-lpha| [cite_start]\ge \epsilon_{0}$ となる $\mathbf{x}_{n} \in A$ が存在する。 [cite: 70, 72]
[cite_start]このとき、$\mathbf{x}_{n} 	o \mathbf{x}_{0}$ かつ $f(\mathbf{x}_{n}) 
ot	o lpha$ [cite: 73]
[cite_start]これは(ii)に矛盾 [cite: 74]