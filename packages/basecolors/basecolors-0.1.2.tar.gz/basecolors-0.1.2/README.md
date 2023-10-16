python 控制台文本的基本色
====

## 介绍：  

<ul>  
    <li>    <h6>为你的 python 脚本在控制台的输出上个色！</h6></li>    
    <li>    <h6>0.1.0版本支持win 和linux</h6></li>    
    <li>    <h6>跟 0.0.2 版本不同，由于考虑兼容性，0.1.0 版本之后会直接打印文本，不会返回包装后的文本！务必注意</h6></li>    
    <li>    <h6>win平台只打印文本颜色，背景色和显示效果（闪烁等）暂时无效果</h6></li>    
</ul>  

---

### 简要使用说明：

#### &nbsp;&nbsp; 安装：  

```
$ pip install basecolors  
```

#### &nbsp;&nbsp; 终端命令：    

```  
$ colorit [-t --text [-fc --front_color] [-bc --back_color] [-md --show_mode]] [-a --show_all [-ne --show_all_but_no_effect]]  
  
# 显示帮助：  
$ colorit -h  
```    

<ul style="font-size:30">  
    <li>     <h5>参数解释：</h5>   
        <ul style="none">  
            <li><b>-t --text</b> 需要上色的文本</li>  
            <li><b>-fc --front_color</b> 字体颜色</li>  
            <li><b>-bc --back_color</b> 背景色</li>  
            <li><b>-md --show_mode</b> 显示模式，加深、闪烁、下划线等</li>  
            <li><b>-a --show_all</b> 显示所有颜色名称和代号</li>  
            <li><b>-ne --show_all_but_no_effect</b> 配合 -a 参数，显示颜色名称和代号但不展示效果</li>  
        </ul></li>  
</ul>  
  
#### &nbsp;&nbsp; 终端示例：    
  
```  
# 显示红色字样  
$ colorit -fc red  
  
# 显示红色加粗字样  
$ colorit -t 测试文本 -fc red -md highlight  
  
# 显示黄色下划线字样  
$ colorit -fc yellow -md underline  
   
# 显示蓝色闪烁字样  
$ colorit -fc blue -md blinking  
  
# 如果不确定颜色或显示模式的名称，可以输入 colorit -a -ne 或者 colorit -a 查看  
```  


#### &nbsp;&nbsp; 代码中调用：    
  
```  
from BaseColor.base_colors import *  
  
# 0.0.1 版本（只支持 linux）：  
print(red("测试文本"))  # 普通红色  
print(hred("测试文本"))  # 加粗红色  
  
# 0.1.0 版本（新版，支持 win 和 linux）：    
red("测试文本")  
  
# ============ linux 效果 ===============  
# 其他颜色也有普通和加粗显示的区别，就是在前面多个 h，例如上面的 red 和 hred    
# 其他配合颜色的 show_mode 暂时没有编写  
  
# 自定义颜色效果组合：  
color("测试文本", show_mode="underline", back_color="cyan", front_color="red")  
  
# 效果可以叠加使用，例如同时加粗和闪烁：  
hred(color("测试文本", 'blinking'))  
```
