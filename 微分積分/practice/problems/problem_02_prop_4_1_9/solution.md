# prop. 4.1.9 - 解答

(1) [cite_start]$A \subset \mathbb{R}^{2}$ : 閉集合とする [cite: 22]
[cite_start]$\{\mathbf{x}_{n}\} \subset A$, $\lim_{n	o\infty} \mathbf{x}_{n}=\mathbf{x}_{0}$ とする。このとき必ず $\mathbf{x}_{0} \in A$ [cite: 23]

### ex. [cite_start]4.1.11 [cite: 24]
(1)[cite_start]を証明せよ。 [cite: 27]
[cite_start]背理法を用いて証明する。 [cite: 30]
[cite_start]$\mathbf{x}_{0} 
otin A$ と仮定する。すなわち、$\mathbf{x}_{0} \in A^{c}$ とする。 [cite: 32]
[cite_start]$A^{c}$ は開集合である。 [cite: 35]
[cite_start]よって、開集合の定義より、ある $\epsilon_{0}>0$ が存在し、$U(\mathbf{x}_{0}:\epsilon_{0}) \subset A^{c}$ [cite: 37]
$\lim_{n	o\infty} \mathbf{x}_{n}=\mathbf{x}_{0}$ より、上記の $\epsilon_{0}$ に対し、$N_{0} \in \mathbb{N}$ が存在し、$orall n \ge N_{0}$ s.t. [cite_start]$d(\mathbf{x}_{n},\mathbf{x}_{0}) < \epsilon_{0}$ [cite: 43]
[cite_start]よって、$orall n \ge N_{0}$ のとき、$\mathbf{x}_{n} \in U(\mathbf{x}_{0}:\epsilon_{0}) = \{\mathbf{y} \mid d(\mathbf{x}_{0},\mathbf{y}) < \epsilon_{0}\}$ [cite: 44, 45]
[cite_start]$U(\mathbf{x}_{0}:\epsilon_{0}) \subset A^{c}$ より、$orall n \ge N_{0}$ に対し、$\mathbf{x}_{n} \in A^{c}$ [cite: 46]
[cite_start]これは $\{\mathbf{x}_{n}\} \subset A$ に矛盾 [cite: 48]
よって $\mathbf{x}_{0} \in A$ である。