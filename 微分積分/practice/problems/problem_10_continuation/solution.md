# 続き - 解答

### (2)
[cite_start]$f_{x}(x,y)=3x^{2}-3y$, $f_{y}(x,y)=3y^{2}-3x$ [cite: 160]
[cite_start]$f_{x}=f_{y}=0$ を解く [cite: 160]
$$egin{cases} 3x^{2}=3y \ 3y^{2}=3x \end{cases} \implies egin{cases} y=x^{2} \ x=y^{2} \end{cases}$$
[cite_start]$x=(x^{2})^{2} \implies x=x^{4} \implies x(x^{3}-1)=0$ [cite: 161]
$x=0$ のとき $y=0$, $x=1$ のとき $y=1$
[cite_start]$(0,0), (1,1)$ が極値候補 [cite: 162]

2階偏導関数
[cite_start]$f_{xx}(x,y)=6x, f_{yy}(x,y)=6y, f_{xy}(x,y)=-3$ [cite: 163]
[cite_start]$D = (-3)^{2}-(6x)(6y) = 9-36xy$ [cite: 164]

* [cite_start]$(0,0)$: $D(0,0)=9>0$ [cite: 165]
    [cite_start]$	o$ 極値でない [cite: 165]
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
$f_{x}=0, f_{y}=0 \implies y=rac{3}{2}x^{2}$
$8x^{3}-6x(rac{3}{2}x^{2}) = 8x^{3}-9x^{3} = -x^{3} = 0 \implies x=0, y=0$
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
[cite_start]$m=rac{3}{2}$ のとき $f(x,rac{3}{2}x^{2}) = x^{4}(rac{3}{2}-1)(rac{3}{2}-2) = -rac{1}{4}x^{4} < 0 = f(0,0)$ [cite: 182]
[cite_start]$(0,0)$ は極値ではない。 [cite: 183]