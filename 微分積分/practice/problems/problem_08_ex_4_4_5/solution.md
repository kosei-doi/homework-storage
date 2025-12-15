# e.x. 4.4.5 原点において、偏微分可能か、全微分可能か - 解答

### (1)
#### 偏微分
[cite_start]$$f_{x}(0,0) = \lim_{h	o 0} rac{f(0+h,0)-f(0,0)}{h} = \lim_{h	o 0} rac{rac{h^{3}-0^{3}}{h^{2}+0^{2}}-0}{h} = \lim_{h	o 0} rac{h}{h}=1$$ [cite: 125]
[cite_start]$\mathbf{x}$ に関して偏微分可能で、$f_{x}(0,0)=1$ [cite: 126]
[cite_start]$$f_{y}(0,0) = \lim_{h	o 0} rac{f(0,0+h)-f(0,0)}{h} = \lim_{h	o 0} rac{rac{0^{3}-h^{3}}{0^{2}+h^{2}}-0}{h} = \lim_{h	o 0} rac{-h}{h}=-1$$ [cite: 127]
[cite_start]$\mathbf{y}$ に関して偏微分可能で、$f_{y}(0,0)=-1$ [cite: 128]

#### 全微分
[cite_start]全微分可能の定義式に代入 [cite: 129]
$$\lim_{(h,k)	o(0,0)} rac{f(h,k)-f(0,0)-f_{x}(0,0)h-f_{y}(0,0)k}{\sqrt{h^{2}+k^{2}}}$$
[cite_start]$$= \lim_{(h,k)	o(0,0)} rac{rac{h^{3}-k^{3}}{h^{2}+k^{2}}-0-1\cdot h-(-1)\cdot k}{\sqrt{h^{2}+k^{2}}} = \lim_{(h,k)	o(0,0)} rac{rac{h^{3}-k^{3}-(h-k)(h^{2}+k^{2})}{h^{2}+k^{2}}}{\sqrt{h^{2}+k^{2}}}$$ [cite: 129]
$$= \lim_{(h,k)	o(0,0)} rac{h^{3}-k^{3}-(h^{3}+hk^{2}-k h^{2}-k^{3})}{(h^{2}+k^{2})^{rac{3}{2}}} = \lim_{(h,k)	o(0,0)} rac{-hk^{2}+k h^{2}}{(h^{2}+k^{2})^{rac{3}{2}}}$$
[cite_start]$$= \lim_{(h,k)	o(0,0)} rac{hk(h-k)}{(h^{2}+k^{2})^{rac{3}{2}}}$$ [cite: 132]
[cite_start]$h=-k$ として近づけると $rac{(-k)k(k-(-k))}{(k^{2}+(-k)^{2})^{rac{3}{2}}} = rac{-2k^{3}}{(2k^{2})^{rac{3}{2}}} = rac{-2k^{3}}{2^{rac{3}{2}}k^{3}} = -rac{1}{\sqrt{2}} (
e 0)$ [cite: 132, 134, 135]
[cite_start]全微分不可。 [cite: 133]

### (2) [cite_start]$f(x,y)=\sqrt{|xy|}$ [cite: 136]
#### 偏微分
[cite_start]$$f_{x}(0,0) = \lim_{h	o 0} rac{f(0+h,0)-f(0,0)}{h} = \lim_{h	o 0} rac{\sqrt{|h\cdot 0|}-\sqrt{|0\cdot 0|}}{h} = \lim_{h	o 0} rac{0}{h}=0$$ [cite: 137]
[cite_start]$\mathbf{x}$ に関して偏微分可能で、$f_{x}(0,0)=0$ [cite: 138]
[cite_start]$$f_{y}(0,0) = \lim_{h	o 0} rac{f(0,0+h)-f(0,0)}{h} = \lim_{h	o 0} rac{0}{h}=0$$ [cite: 139]
[cite_start]$\mathbf{y}$ に関して偏微分可能で、$f_{y}(0,0)=0$ [cite: 140]

#### 全微分
全微分可能の定義式に代入
[cite_start]$$\lim_{(h,k)	o(0,0)} rac{f(0+h,0+k)-f(0,0)-f_{x}(0,0)h-f_{y}(0,0)k}{\sqrt{h^{2}+k^{2}}} = \lim_{(h,k)	o(0,0)} rac{\sqrt{|hk|}}{\sqrt{h^{2}+k^{2}}}$$ [cite: 141]
[cite_start]例えば、$h=k$ として近づけると [cite: 142]
[cite_start]$$rac{\sqrt{|k^{2}|}}{\sqrt{k^{2}+k^{2}}} = rac{|k|}{\sqrt{2}|k|} = rac{1}{\sqrt{2}} (
e 0)$$ [cite: 143]
[cite_start]全微分不可。 [cite: 144]