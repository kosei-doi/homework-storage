# 4.2.3 極限 - 解答

(1) [cite_start]$\lim_{(x,y)	o(0,0)} rac{xy}{\sqrt{x^{2}+y^{2}}}$ [cite: 78]
[cite_start]$x=r\cos	heta, y=r\sin	heta$ とする [cite: 80]
$$\lim_{r	o 0} rac{r\cos	heta \cdot r\sin	heta}{\sqrt{r^{2}\cos^{2}	heta+r^{2}\sin^{2}	heta}} = \lim_{r	o 0} rac{r^{2}\cos	heta \sin	heta}{r} = \lim_{r	o 0} r\cos	heta \sin	heta$$
$g(r)=r$ とすると $|r\cos	heta \sin	heta| [cite_start]\le g(r)$ [cite: 82]
[cite_start]$\lim_{r	o 0} g(r)=0$ [cite: 82]
[cite_start]よって $\lim_{(x,y)	o(0,0)} rac{xy}{\sqrt{x^{2}+y^{2}}} = \lim_{r	o 0} r\cos	heta \sin	heta = 0$ [cite: 84]

(2) [cite_start]$\lim_{(x,y)	o(0,0)} rac{xy}{x^{2}+y^{2}}$ [cite: 84]
$$\lim_{r	o 0} rac{r^{2}\cos	heta \sin	heta}{r^{2}} = \lim_{r	o 0} \cos	heta \sin	heta$$
$r	o 0$ の方向から近づけると $\cos	heta \sin	heta$
一律、$	heta=rac{\pi}{4}$ の方向から近づけると $\cosrac{\pi}{4}\sinrac{\pi}{4} = rac{1}{2}$
[cite_start]よって、近づける方向によって値が変わるので収束しない [cite: 85]

(3) [cite_start]$\lim_{(x,y)	o(0,0)} rac{x^{3}+y^{3}}{x^{2}+y^{2}}$ [cite: 86]
[cite_start]$$\lim_{r	o 0} rac{r^{3}(\cos^{3}	heta+\sin^{3}	heta)}{r^{2}} = \lim_{r	o 0} r(\cos^{3}	heta+\sin^{3}	heta)$$ [cite: 86, 87]
$g(r)=r$ とすると $|r(\cos^{3}	heta+\sin^{3}	heta)| [cite_start]\le 2r = g(r)$ [cite: 88]
[cite_start]$\lim_{r	o 0} g(r)=0$ [cite: 89]
[cite_start]よって $\lim_{(x,y)	o(0,0)} rac{x^{3}+y^{3}}{x^{2}+y^{2}} = \lim_{r	o 0} r(\cos^{3}	heta+\sin^{3}	heta) = 0$ [cite: 89]

(4) [cite_start]$\lim_{(x,y)	o(0,0)} rac{xy^{2}}{x^{2}+y^{4}}$ [cite: 79]
[cite_start]$y^2=kx$ とする。 [cite: 90]
$$\lim_{x	o 0} rac{x(kx)^{2}}{x^{2}+(kx)^{4}} = \lim_{x	o 0} rac{k^{2}x^{2}}{x^{2}(1+k^{4}x)} = \lim_{x	o 0} rac{k^{2}}{1+k^{4}x} = k^{2}$$
間違い
$y^2=kx^{2}$ とする。 $\lim_{x	o 0} rac{x(kx^{2})^{2}}{x^{2}+(kx^{2})^{4}} = \lim_{x	o 0} rac{k^{2}x^{5}}{x^{2}(1+k^{4}x^{5})}$
(90) [cite_start]$y^2=kx$ とする。 $\lim_{x	o 0} rac{k^{2}x^{2}}{x^{2}+k^{4}x^{4}} = \lim_{x	o 0} rac{k^{2}}{1+k^{4}x}$ [cite: 90]
[cite_start]$k=0$ の方向から近づけると $0$ [cite: 92]
[cite_start]$k=1$ の方向から近づけると $rac{1}{1+k^{4}x} 	o 1$ [cite: 92]
間違い
[cite_start]$y^2=kx$ とする。 $\lim_{x	o 0} rac{k x^{2}}{x^{2}+k^{2}x^{2}} = \lim_{x	o 0} rac{k}{1+k^{2}} = rac{k}{1+k^{2}}$ [cite: 90, 91]
[cite_start]$k=0$ の方向から近づけると $rac{0}{1}=0$ [cite: 92]
[cite_start]$k=1$ の方向から近づけると $rac{1}{1+1}=rac{1}{2}$ [cite: 92]
[cite_start]近づける方向によって値が変わるので、収束しない。 [cite: 92]