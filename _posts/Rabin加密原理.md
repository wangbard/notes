# Rabin加密原理

昨天做一道ctf遇到了Rabin加密，其实之前我也想过这个问题，RSA加密最小的 $e=3$ 
因为 $\varphi=(p-1)(q-1)$，$p,q$ 都是质数，所以 $\varphi$ 是偶数 $gcd(2,phi)=2$ ，无法取模逆。
之前遇到过一道题目 $e=2p$ ($p$为质数)，当时是先用 $p$ 当做 $e$ 解RSA, 然后爆破解决最后的平方模, 当时就在想有没有什么数学方法，爆破实在是大海捞针。
这次学习了Rabin加密，对于二次剩余有了更深入的理解，加之查找资料的时候发现很多博文都非常简略（我太菜了），所以这里详细的记录一下，方便自己回看之余，也希望也能帮到一些人。

## 1. 二次剩余

**定义：**对于 $x^{2} \equiv a \ mod \ p$ , $a$ 为模 $p$ 的二次剩余，反之则称为非二次剩余
**定理1：**二次剩余满足关于$p$对称，即 $x^{2} \equiv (p-x)^{2}  \ mod \ p $
**推论1：**模 $p$ 的全部二次剩余为：$1^{2} ,2^{2} ,\cdots ,(\frac{p-1}{2}) ^{2} \ mod \ p$
已知寻找模 $p$ 的全部二次剩余系的最直接的方法是计算： 
$1^{2} ,2^{2} ,\cdots ,(\frac{p-1}{2}) ^{2},(\frac{p+1}{2}) ^{2},\cdots ,(p-1)^{2} \ \ mod \ p $
根据定理1，易知推论1
**定理2：**对于奇素数 $p$ ，二次剩余 $a$ 的个数为 $\frac{p-1}{2} $ ,二次非剩余的也为 $\frac{p-1}{2}  $
**证明：**假设存在整数 $a,b (a\ne b) $，$1 \le a,  b\le \frac{p-1}{2}  $，如果我们能证明对于任意 $a,b$ 的二次剩余不相同，就相当于证明了二次剩余个数为$ \frac{p-1}{2} $ 。
**反证法：**假设 $a^{2} \equiv b^{2} \ mod \ p$ (二次剩余相同），可得 $a^{2}- b^{2} \equiv 0\ \ mod \ p$ ，$ p\mid (a+b)(a-b) $
$\because  p$ 为奇素数，又有 $a+b\le p-1 $，$ p$ 的因子只有 $ 1,p $，$a+b,a-b$ 都不是 $p$ 的因子
$\therefore$  只能存在 $p\mid a-b$ ( $p\mid 0 $恒成立） 
**$a\ne b $ 证伪**
**定理3**： 对于奇素数 $p$
$a$ 是模 $p$ 的二次剩余的充要条件为：$a^{\frac{p-1}{2} } \equiv 1\ \ mod \ p $
$a$ 是模 $p$ 的二次非剩余的充要条件为：$ a^{\frac{p-1}{2} } \equiv -1\ \ mod \ p $
**证明：**根据欧拉定理: 对于素数 $p$ ，$a^{p-1} \equiv 1\ \ mod \ p \ \Longleftrightarrow \ a^{\frac{p-1}{2} } \equiv \pm 1\ \ mod \ \  p  $
上述式子说明 对于任意给定 $x$ ，$x^{\frac{p-1}{2} }  \ mod \ \  p $$  有且只有 $ $\pm1$ 两个解
假设 $a$ 是模 $p$ 的二次剩余（$ x^{2} \equiv a \ mod \ p $），那么等式 $a^{\frac{p-1}{2} } \equiv  1\ \ mod \ \  p $
等价于 $(x^{2} )^{\frac{p-1}{2} } \equiv  1\equiv x^{p-1}  \ \ mod \ \  p$ ，根据欧拉定理可知，等式恒成立
$\because   x^{\frac{p-1}{2} }  \ mod \ \  p$ 的根的数量最多为指数的数量 $\frac{p-1}{2}$  
$\because$  根据定理2，二次剩余的数量为 $\frac{p-1}{2}$  
$\therefore$  充要得证
补充1：$x^{ 2}\equiv  1 \ \ mod \ \ p \Longleftrightarrow x\equiv \pm 1 \ \ mod \ \ p$ 刚刚的证明用到了这个条件
证明(正向)：$\Rightarrow(x+1)(x-1)\equiv 0 \ \ mod \ \ p \Rightarrow$ 两根为 $\pm 1$ 
那么现在用到的轮子都已经造好了，开始解密Rabin

## 2. Rabin解密原理

Rabin其实就是 $e =2$ 情况下的RSA。对于明文 $m$ ，密文 $c$ ，有：$m^{2} \equiv c \ \ mod \ \ n $
$n=pq$ ，$p,q$ 为两个大质数，跟RSA一样，破解Rabin的难度等同于质因数分解 $n$ 

## 2.1 解密过程：

已知 $c,n,p,q$ 求明文 $m$ 
$\because m^{2} \equiv c \ \ mod \ \ n\ $
$\therefore m^{2} \equiv c \ \ mod \ \ p$ 
$m^{2} \equiv c \ \ mod \ \ q $
$c$ 是 $p,q$ 的二次剩余
根据等式构造出 $r,s$，满足：
$r^{2} \equiv c \ \ mod \ \ p\Longrightarrow r\equiv \sqrt{c} \ \ mod \ \ p $
$s^{2} \equiv c \ \ mod \ \ q\Longrightarrow s\equiv \sqrt{c} \ \ mod \ \ q $ 
 因为 $p,q$ 是质数，所以一定能找到一个大数 $M$，满足：
$M\equiv r \ \ mod \ \ p $
$M\equiv s \ \ mod \ \ q $
这里问题就变得开朗了，用**中国余数定理**就可以解得唯一解 $m\equiv M \ \ mod \ \ n$ ：
对于只有两个模数的中国余数定理，先用bezout算出 $px+qy=1$ 的 $x,y$ 值
$m= (q\cdot( r y \ \ mod\ p)+p\cdot (sx\ \ mod \ q))\ \ mod\ \ n $
现在就差上面式子中 $r,s$ 的值带入即可
根据定理3：$c^{\frac{p-1}{2} } \equiv 1\ \ mod \ p$ 
可得：$r^{2}  \equiv  c^{\frac{p-1}{2} }\cdot c\equiv c^{\frac{p+1}{2} } \equiv (c^{\frac{p+1}{4} })^{2}   \ \ mod \ \ p $
由于常规Rabin加密规定 $p,q\equiv 3 \ \ mod \ \ 4$，所以 $\frac{p+1}{4}$ 是整数，可得：
$r\equiv \pm \ c^{\frac{p+1}{4} }  \ \ mod \ \ p $
$s\equiv \pm \ c^{\frac{p+1}{4} }  \ \ mod \ \ q $
$m$ 的四个解依次带入即可得

## 2.2  p,q 模4不等于3

##### 等看懂了再写 猪鼻巴巴