# Rabin加密原理

[toc]

昨天做一道ctf遇到了Rabin加密，其实之前我也想过这个问题，RSA加密最小的 $e=3 $

因为 $ \varphi=(p-1)(q-1) $ ，$p,q $ 都是质数，所以 $ \varphi $ 是偶数 $gcd(2,phi)=2 $ ，无法取模逆。

之前遇到过一道题目 $e=2p $ ( $p $ 为质数)，当时是先用 $p $ 当做 $e $ 解RSA, 然后爆破解决最后的平方模, 当时就在想有没有什么数学方法，爆破实在是大海捞针。

这次学习了Rabin加密，对于二次剩余有了更深入的理解，加之查找资料的时候发现很多博文都非常简略（我太菜了），所以这里详细的记录一下，方便自己回看之余，也希望也能帮到一些人。

## 1. 二次剩余

**定义：**对于 $x^{2} \equiv a \ mod \ p $ , $a $ 为模 $p $ 的二次剩余，反之则称为非二次剩余

**定理1：**二次剩余满足关于p对称，即 $x^{2} \equiv (p-x)^{2}  \ mod \ p $

**推论1：**模p的全部二次剩余为： $1^{2} ,2^{2} ,\cdots ,(\frac{p-1}{2}) ^{2} \ mod \ p $

已知寻找模p的全部二次剩余系的最直接的方法是计算：

$1^{2} ,2^{2} ,\cdots ,(\frac{p-1}{2}) ^{2},(\frac{p+1}{2}) ^{2},\cdots ,(p-1)^{2} \ \ mod \ p $

根据定理1，易知推论1

**定理2：**对于奇素数 $p $ ，二次剩余 $a $ 的个数为 $\frac{p-1}{2}  $ ,二次非剩余的也为 $\frac{p-1}{2}  $

**证明：**假设存在整数 $a,b $ $(a\ne b) $ ，$1 \le a,  b\le \frac{p-1}{2}  $ ，如果我们能证明对于任意 $a,b $ 的二次剩余不相同，就相当于证明了二次剩余个数为 $\frac{p-1}{2}  $ 。

反证法：假设 $a^{2} \equiv b^{2} \ mod \ p $ (二次剩余相同），可得 $a^{2}- b^{2} \equiv 0\ \ mod \ p $ ， $p\mid (a+b)(a-b) $

$\because  $ $p $ 为奇素数，又有 $a+b\le p-1 $ ， $p $ 的因子只有 $1,p $ ， $a+b,a-b $ 都不是 $p $ 的因子

$\therefore  $ 只能存在 $p\mid a-b $ ( $p\mid 0 $ 恒成立）

$a\ne b $ **证伪**

**定理3**（欧拉准则）**：** 对于奇素数 $p $

$a $ 是模 $p $ 的二次剩余的充要条件为： $a^{\frac{p-1}{2} } \equiv 1\ \ mod \ p $

$a $ 是模 $p $ 的二次非剩余的充要条件为： $a^{\frac{p-1}{2} } \equiv -1\ \ mod \ p $

**证明：**根据欧拉定理: 对于素数 $p $ ，$a^{p-1} \equiv 1\ \ mod \ p \ \Longleftrightarrow \ a^{\frac{p-1}{2} } \equiv \pm 1\ \ mod \ \  p  $

上述式子说明 对于任意给定 $x $ ， $ x^{\frac{p-1}{2} }  \ mod \ \  p  $ 有且只有 $ \pm1 $ 两个解

假设 $a $ 是模 $p $ 的二次剩余（ $x^{2} \equiv a \ mod \ p $ ），那么等式 $ a^{\frac{p-1}{2} } \equiv  1\ \ mod \ \  p  $

等价于 $(x^{2} )^{\frac{p-1}{2} } \equiv  1\equiv x^{p-1}  \ \ mod \ \  p  $ ，根据欧拉定理可知 等式恒成立

$\because  $ $ x^{\frac{p-1}{2} }  \ mod \ \  p  $ 的根的数量最多为指数的数量 $\frac{p-1}{2}  $

$\because  $ 根据定理2，二次剩余的数量为 $\frac{p-1}{2}  $

$\therefore  $ 充要得证

**补充1：** $x^{ 2}\equiv  1 \ \ mod \ \ p \Longleftrightarrow x\equiv \pm 1 \ \ mod \ \ p $ 刚刚的证明用到了这个条件

**证明**（正向）**：** $\Rightarrow(x+1)(x-1)\equiv 0 \ \ mod \ \ p $ $\Rightarrow $ 两根为 $ \pm 1 $

那么现在用到的轮子都已经造好了，开始解密Rabin

## 2. Rabin解密原理

Rabin其实就是 $e =2 $ 情况下的RSA。对于明文 $m $ ，密文 $c $ ，有： $m^{2} \equiv c \ \ mod \ \ n $

$n=pq $ ， $p,q $ 为两个大质数，跟RSA一样，破解Rabin的难度等同于质因数分解 $n $

### 2.1 Rabin解密原理

已知 $c,n,p,q $ 求明文 $m $

$\because m^{2} \equiv c \ \ mod \ \ n\ $

$\therefore m^{2} \equiv c \ \ mod \ \ p $

$\ \ \ \  m^{2} \equiv c \ \ mod \ \ q $

$c $ 是 $p,q  $ 的二次剩余

根据等式构造出 $r,s $ ，满足：

$r^{2} \equiv m^{2} \equiv c \ \ mod \ \ p\Longrightarrow r\equiv m \equiv \sqrt{c} \ \ mod \ \ p $

$s^{2} \equiv m^{2} \equiv c \ \ mod \ \ q\Longrightarrow s\equiv m \equiv \sqrt{c} \ \ mod \ \ q  $

这里问题就变得很明朗了，联立上述两个等式：

$m \equiv r \ \ mod \ \ p $

$m \equiv s \ \ mod \ \ q $

用中国余数定理就可以解得唯一解 $m \ \ mod \ \ (p\cdot q ) $

现在就需要获得上面式子中的 $r,s $ 值，带入即可。

根据定理3： $c^{\frac{p-1}{2} } \equiv 1\ \ mod \ p $

可得： $r^{2}  \equiv  c^{\frac{p-1}{2} }\cdot c\equiv c^{\frac{p+1}{2} } \equiv (c^{\frac{p+1}{4} })^{2}   \ \ mod \ \ p $

由于常规Rabin加密规定 $p,q\equiv 3 \ \ mod \ \ 4 $ ，所以 $\frac{p+1}{4}  $ 是整数，可得：

$r\equiv \pm \ c^{\frac{p+1}{4} }  \ \ mod \ \ p $

$s\equiv \pm \ c^{\frac{p+1}{4} }  \ \ mod \ \ q $

依次带入 $r,s $ 的四个解，即可得到 $m $ 。

## 3. 通解

**注意：**上述做法中解 $r,s $ 的过程中用到了一个先决条件 $p,q\equiv 3 \ \ mod \ \ 4 $ ，可以说这是Rabin解密的一个非常特殊的情况。那么有没有什么方法，能够在不需要先决条件的情况下，解出 $r,s $ 呢？

让我们再来回顾一下如何解 $r,s $ ：

$r^{2} \equiv m^{2} \equiv c \ \ mod \ \ p\Longrightarrow r\equiv m \equiv \sqrt{c} \ \ mod \ \ p $

$s^{2} \equiv m^{2} \equiv c \ \ mod \ \ q\Longrightarrow s\equiv m \equiv \sqrt{c} \ \ mod \ \ q  $

解 $r,s $ 的过程相当于求解二次剩余方程 $x^{2} \equiv c \ \ mod \ \ (p \ or \ q) $

### 3.1 Cipolla's algorithm

Cipolla's algorithm是解二次剩余方程 $x^{2}\equiv  n \ \ mod \ \ p $ ， $p $ 为奇素数时的通解。过程如下：

- 构造 $\omega  ^{2} $ 使得 $\omega ^{2}= a^{2}-n  \ \ mod \ \ p $ ， $a $ 为任意值 ，满足 $\omega^{2} $ 为 $p $ 的二次非剩余，即

  $(\omega^{2}) ^{\frac{p-1}{2} } \equiv -1\ \ mod \ p $ （定理3）。根据定理2，二次非剩余的概率为 $\frac{1}{2}  $ ，所以找到这样的 $a $ 并不困难。

- $x  \equiv (a+\omega) ^{\frac{p+1}{2} }   \ \ mod \ \ p  $ 即为方程的解

证明过程需要以下定理：

**定理4：** $(a+b)^{p}\equiv  a^{p}+b^{p} \ \ mod \ \ p   $

定理4其实很好理解，只需要二项式展开以下就会发现，对于二项式系数 $\binom{p}{k}  $ , $  k\in \left [ 0 ,p\right  ] $

除了 $  k= 0 , p $ 两种情况之外，全部都包含系数 $p $ ，模 $p $ 自然为 $0 $ 。

**补充2：**这里详细说明一下 $a $ 的取值，$a\in F_{p} \ , \ F_{p} \Leftrightarrow \left \{0,1,\dots ,p-1  \right \}  $

**Cipolla's algorithm 证明：**

$x^{2}  \equiv (a+\omega) ^{p+1} \equiv (a+\omega) ^{p}\cdot (a+\omega)\equiv (a^{p}+\omega^{p})  \cdot (a+\omega)  \ \ mod \ \ p $

$\because a^{p} \equiv a\ \ mod \ \ p  \ \Longleftarrow  $ 费马小定理

$\because \omega^{p}\equiv  \omega^{p-1}\cdot \omega \equiv (\omega^{2})^{\frac{p-1}{2}} \cdot\omega \equiv -\omega \ \ mod \ \ p \ \Longleftarrow  $ $\omega^{2} $ 是 $p $ 的二次非剩余(定理3)

$\therefore (a^{p}+\omega^{p})  \cdot (a+\omega)\equiv (a-\omega)\cdot (a+\omega)\equiv a^{2}-\omega^{2} \equiv n\ \ mod \ \ p    $

**证毕**

可能看到这里还是一头雾水，并且想大声骂题主，“你在扯淡， $\omega^{2} $ 你都说了是二次非剩余，既然都开不了根号，你怎么算出来 $\omega $ 的”。别着急，慢慢来，可以说这个算法乍一看似乎不难理解，推导过程很流畅，但这一步如果算得 $\omega $ 确实让人百思不得其解，这正是这个算法的高明之处，不得不佩服Cipolla的脑洞啊。

### 3.2 如何理解 $\omega $

已知 $\omega^{2}  $ 是 $p $ 的二次非剩余， $(\omega^{2}) ^{\frac{p-1}{2} } \equiv -1\ \ mod \ p $ ，可以把 $\omega $ 类比作虚数 $i $ 来理解， $\sqrt{-1} $ 没有实际的现实意义，但是引用了虚数给我们工程运算带来了极大方便，这里我们把 $\omega $ 当做虚数 $i $ 来理解，我们把原本的运

算域 $F_{p}  $ 扩充到 $F_{p^{2}} =F_{p} (\omega)=\left \{ x+y\cdot \omega:x,y\in F_{p}  \right \}  $ ，看这里像不像虚数运算！这里我们需要证明 $F_{p^{2}} $ 满足域的所有性质，感兴趣可以自己实践一下。

有了这个理论我们再看上面的证明推导过程，应该就会有所领悟，虽然我们在运算过程中带入了 $\omega $ ，但是结果是不会出现 $\omega $ 的，结果的运算域是 $F_{p} $ 不是 $F_{p^{2}} $ ，这是因为根据拉格朗日定理（别问，问我也不懂），幂函数的根的数量 $\le  $ 指数，所以二次剩余方程的根的数量最大为2，我们现在已经解出了 $F_{p^{2}} $ 下的两个根：

$(a+\omega) ^{\frac{p+1}{2} }  ，p-(a+\omega) ^{\frac{p+1}{2} }   $

所以这两个根也必须同时为 $F_{p} $ 下的根。实践的时候我们也会发现，虚数 $\omega $ 的部分确实也会神奇般的消掉。

### 3.3 代码实现

```python3
# 欧拉判别准则 判断n是否为p的二次剩余
# x^2 = n mod p
def testResidual(n,p):
    if pow(n,(p-1)//2)%p == p-1:
        return False
    else:
        return True

# Cipolla算法
# 解方程 x^2 = n mod p 中的x
# 因为是二次方程 所有有两个解
def Cipolla(n,p):
    # 如果n不是p的二次剩余 报错
    if testResidual(n,p) == False:
        raise Exception('No solution')

    # 随机取w^2
    import random
    while True:
        a = random.choice(range(1,(p-1)//2+1)) # [1,(p-1)//2]区间内任取a 这里取半个Fp区间是因为a^2是关于(p-1)//2对称的
        w_2 = (pow(a,2)-n)%p
        if testResidual(w_2,p) == False: # 找到一个w^2 是一个二次非剩余
            break
            
    # 定义Fp2这个域 在class里实现他的运算法则
    class omega_field:

        def __init__(self,a,b):
            self.a = a%p
            self.b = b%p

        # 乘法运算
        def mul(self,another):
            x = self.a*another.a + self.b*another.b*w_2
            y = self.b*another.a + self.a*another.b
            return omega_field(x,y)

        # 乘方运算
        # 快速幂运算
        # 常规循环累乘方的复杂度是O(n) 快速幂运算则是O(logn)
        # 把指数进行了二进制分解 循环次数等于二进制的位数
        def pow(self,n):
            ans = omega_field(1,0)
            t = self
            while(n):
                if n&1:
                    ans = omega_field.mul(ans,t)
                t = omega_field.mul(t,t)
                n >>= 1
            return ans
        
        # get method
        def get(self):
            return self.a,self.b
        
    x = omega_field.pow(omega_field(a,1),(p+1)//2).get()

    # x.b理论上讲一定为0 这里保险起见加一个报错
    if x[1] != 0:
        raise Exception('Please contact the coder, something goes wrong')
    else:
        x = x[0]
    return x,p-x

# 中国余数定理
# pairs是(n,c) n是模数 c是余数
def CRT(pairs):

    def inv(a,b,c):
        import gmpy2
        return (gmpy2.invert(a,c)*b)%c

    x = 0
    m = 1

    for i in pairs:
        m *= i[0]
        
    for i in pairs:
        x += m//i[0] * inv(m//i[0],i[1],i[0])

    return x%m

# Rabin解密 
# Rabin是公钥为(e=2,n)情况下的RSA
# 返回全部4个可能结果 输出结果为二进制
# c-密文 p,q-为n的质因数分解
def Rabin(c,p,q):

    r = Cipolla(c,p) # r^2 = c mod p
    s = Cipolla(c,q) # s^2 = c mod q

    # 联立上面两个等式
    # 解中国余数定理
    x = []
    n = p*q
    x.append(CRT([(p,r[0]),(q,s[0])]))
    x.append(n-x[0])
    x.append(CRT([(p,r[1]),(q,s[0])]))
    x.append(n-x[2])

    for i in x:
        #二进制输出
        print(bin(i)[2:])

        
if __name__ == '__main__':

    p = 10663
    q = 49123
    c = 162853095
    Rabin(c,p,q)
```

[[1\]](https://zhuanlan.zhihu.com/p/533927542#ref_1)[[2\]](https://zhuanlan.zhihu.com/p/533927542#ref_2)[[3\]](https://zhuanlan.zhihu.com/p/533927542#ref_3)[[4\]](https://zhuanlan.zhihu.com/p/533927542#ref_4)[[5\]](https://zhuanlan.zhihu.com/p/533927542#ref_5)

## 参考

1. [^](https://zhuanlan.zhihu.com/p/533927542#ref_1_0)Rabin加密算法和n次同余方程 https://xz.aliyun.com/t/5113

2. [^](https://zhuanlan.zhihu.com/p/533927542#ref_2_0)Cipolla算法学习小记 https://blog.csdn.net/doyouseeman/article/details/52033204

3. [^](https://zhuanlan.zhihu.com/p/533927542#ref_3_0)区块链中的数学-用Cipolla算法求解二次剩余方程 https://learnblockchain.cn/article/1520

4. [^](https://zhuanlan.zhihu.com/p/533927542#ref_4_0)区块链中的数学-Cipolla算法补充说明 https://learnblockchain.cn/article/1518

5. [^](https://zhuanlan.zhihu.com/p/533927542#ref_5_0)Cipolla's algorithm [https://en.wikipedia.org/wiki/Cipolla%27s_algorithm](https://en.wikipedia.org/wiki/Cipolla's_algorithm)