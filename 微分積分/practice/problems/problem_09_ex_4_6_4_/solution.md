# e.x. 4.6.4. 極値を調べよ - 解答

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