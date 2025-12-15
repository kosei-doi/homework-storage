# ex. 4.6.8 制約条件 $\phi(x,y)=0$ の下での $f(x,y)$ の最大最小を求めよ。 - 解答

### (1)
[cite_start]$F(x,y,\lambda) = f(x,y)-\lambda \phi(x,y) = x^{2}+y^{2}-\lambda(xy-1)$ とおいて、$F_{x}=F_{y}=F_{\lambda}=0$ を解く。 [cite: 198]
[cite_start]$F_{x}=2x-\lambda y, F_{y}=2y-\lambda x, F_{\lambda}=-xy+1$ [cite: 199]
[cite_start]$$egin{cases} 2x-\lambda y=0 \ 2y-\lambda x=0 \ -xy+1=0 \end{cases}$$ [cite: 200]
$x 
e 0, y 
e 0$
$2x=\lambda y, 2y=\lambda x \implies \lambda = rac{2x}{y} = rac{2y}{x} \implies 2x^{2}=2y^{2} \implies x^{2}=y^{2} \implies y=\pm x$
$xy=1$ より $x^{2}=1 \implies x=\pm 1$
[cite_start]$(x,y)=(1,1), (-1,-1)$ [cite: 202]
[cite_start]$f(1,1)=1^{2}+1^{2}=2$ [cite: 203]
$f(-1,-1)=(-1)^{2}+(-1)^{2}=2$
制約条件 $y=1/x$ を代入して挙動をみる: $f(x, 1/x)=x^{2}+1/x^{2}$
[cite_start]$\lim_{x	o\pm\infty} f(x, 1/x) = \infty$, $\lim_{x	o 0} f(x, 1/x) = \infty$ [cite: 203]
[cite_start]よって $(x,y)=(1,1), (-1,-1)$ のとき最小値2、最大値はなし [cite: 203]