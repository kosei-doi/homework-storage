# 演習問題 - 解答

#### (1)
[cite_start]$x=r\cos	heta, y=r\sin	heta$ とする [cite: 229]
[cite_start]$$\lim_{(x,y)	o(0,0)} f(x,y) = \lim_{r	o 0} rac{r^{2}\cos^{2}	heta \cdot r\sin	heta}{r^{2}} = \lim_{r	o 0} r\cos^{2}	heta \sin	heta$$ [cite: 226, 229]
$g(r)=r$ とおくと $|r\cos^{2}	heta \sin	heta| [cite_start]\le r = g(r)$ [cite: 227, 230]
[cite_start]$\lim_{r	o 0} g(r)=0$ [cite: 230]
[cite_start]よって $\lim_{(x,y)	o(0,0)} f(x,y) = 0 = f(0,0)$ より連続 [cite: 230, 231]

#### (2)
$x=y$ として近づけると $f(x,y)=0$ (定義より)
$y=kx, k
e 1$ として近づけると
$$\lim_{x	o 0} rac{x+kx}{x-kx} = \lim_{x	o 0} rac{1+k}{1-k}$$
$k=0$ の方向から近づけると $1$
[cite_start]$x=y$ 以外の方向から近づけると値が変わるので、極限は存在しない。 [cite: 232, 233]
[cite_start]よって不連続 [cite: 233]

### [cite_start]原点において、偏微分可能か？, 全微分可能か？ [cite: 234]
(1) [cite_start]$f(x,y)=|xy|$ [cite: 235]
(2) [cite_start]$f(x,y)=egin{cases}rac{|xy|}{\sqrt{x^{2}+y^{2}}} & (x,y)
e(0,0)\ 0 & (x,y)=(0,0)\end{cases}$ [cite: 235]

#### (1) $f(x,y)=|xy|$
[cite_start]$$f_{x}(0,0) = \lim_{h	o 0} rac{f(0+h,0)-f(0,0)}{h} = \lim_{h	o 0} rac{|h\cdot 0|-0}{h} = \lim_{h	o 0} rac{0}{h}=0$$ [cite: 237]
[cite_start]$\mathbf{x}$ に関して偏微分可、$\mathbf{y}$ についても同様 $f_{y}(0,0)=0$ [cite: 237]
[cite_start]$$\lim_{(x,y)	o(0,0)} rac{f(x,y)-f(0,0)-f_{x}(0,0)x-f_{y}(0,0)y}{\sqrt{x^{2}+y^{2}}} = \lim_{(x,y)	o(0,0)} rac{|xy|}{\sqrt{x^{2}+y^{2}}}$$ [cite: 239, 240, 241, 242]
$x=r\cos	heta, y=r\sin	heta$ とする
[cite_start]$$\lim_{r	o 0} rac{|r^{2}\cos	heta \sin	heta|}{r} = \lim_{r	o 0} r|\cos	heta \sin	heta|$$ [cite: 243, 244]
$g(r)=r$ とおくと $r|\cos	heta \sin	heta| [cite_start]\le r = g(r)$ [cite: 244, 247]
[cite_start]$\lim_{r	o 0} g(r)=0$ [cite: 248]
[cite_start]よって $=0$ 全微分可 [cite: 248]

#### (2) $f(x,y)=rac{|xy|}{\sqrt{x^{2}+y^{2}}}$
[cite_start]$$f_{x}(0,0) = \lim_{h	o 0} rac{f(0+h,0)-f(0,0)}{h} = \lim_{h	o 0} rac{0-0}{h}=0$$ [cite: 249]
[cite_start]$\mathbf{x}$ に関して偏微分可、$\mathbf{y}$ についても同様 $f_{y}(0,0)=0$ [cite: 249]
[cite_start]$$\lim_{(x,y)	o(0,0)} rac{f(x,y)-f(0,0)-f_{x}(0,0)x-f_{y}(0,0)y}{\sqrt{x^{2}+y^{2}}} = \lim_{(x,y)	o(0,0)} rac{rac{|xy|}{\sqrt{x^{2}+y^{2}}}}{\sqrt{x^{2}+y^{2}}} = \lim_{(x,y)	o(0,0)} rac{|xy|}{x^{2}+y^{2}}$$ [cite: 250]
$x=r\cos	heta, y=r\sin	heta$ とする
[cite_start]$$\lim_{r	o 0} rac{|r^{2}\cos	heta \sin	heta|}{r^{2}} = |\cos	heta \sin	heta|$$ [cite: 250]
例えば、$	heta=rac{\pi}{4}$ とすると $|\cosrac{\pi}{4}\sinrac{\pi}{4}| [cite_start]= rac{1}{2} (
e 0)$ [cite: 250]
[cite_start]よって全微分不可。 [cite: 250]