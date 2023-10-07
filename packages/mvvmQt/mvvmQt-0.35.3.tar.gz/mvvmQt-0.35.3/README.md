<!-- 
python setup.py sdist
twine upload dist/* 
-->

# 简介
使用mvvmQt可以方便的使用jinja2的模板创建Qt界面，并且提供了mvvm的方式来进行数据操作和展示，提高开发速度。

# 控件
## 1. 窗体
### Widget、Window
> 使用Widget可以创建一个普通窗体，Window则在Widget的基础上提供更好的可视化操作，使用&lt;widget&gt;&lt;/widget&gt;或&lt;window&gt;&lt;/window&gt;表示。

#### examples/window/templates/index.jinja2
```html
<!-- desktop为内置的获取桌面信息的对象，具体可参考PyQt5文档 -->
<app>
    <window>
        <attr-full v="0" />
        <attr-minWidth v="{{ (desktop.width() * 2 / 3) | round | int }}" />
        <attr-minHeight v="{{ (desktop.height() * 2 / 3) | round | int }}" />
        <attr-maxWidth v="{{ desktop.width() }}" />
        <attr-maxHeight v="{{ desktop.height() }}" />
        <attr-title v="Window测试窗体" />
        <attr-pos v="200, 200" />

        <frame>
            <attr-width v="500" />
            <attr-height v="500" />
            <hbox>
                <Label>这是一个窗体</Label>
            </hbox>
        </frame>
    </window>
</app>
```

#### examples/window/app.py
```python
from mvvmQt.Parser import Parser
import os

if __name__ == "__main__":
    p = Parser(os.path.abspath("%s/../" % __file__))
    p.build()
    p.run()
```

## 2. 布局
### 网格布局
> 使用网格布局的作用相同于QGridLayout, 使用&lt;grid&gt;&lt;/grid&gt;表示，行则用&lt;row&gt;&lt;/row&gt;表示，列则用&lt;col&gt;&lt;/col&gt;表示，通过在col添加span属性表示跨多少列，添加offset属性表示偏移多少列，rowSpan属性表示跨多少行，rowOffset属性表示偏移多少行。

#### examples/grid/templates/index.jinja2
```html
<app>
    <window>
        <attr-full v="0" />
        <attr-minWidth v="{{ (desktop.width() * 2 / 3) | round | int }}" />
        <attr-minHeight v="{{ (desktop.height() * 2 / 3) | round | int }}" />
        <attr-maxWidth v="{{ desktop.width() }}" />
        <attr-maxHeight v="{{ desktop.height() }}" />
        <attr-title v="Grid Layout" />
        <attr-pos v="200, 200" />

        <frame>
            <attr-width v="500" />
            <attr-height v="500" />
            <grid>
                <row>
                    <col>
                        <attr-rowOffset v="3" />
                        <label>左侧垂直居中</label>
                    </col>
                    <col>
                        <attr-rowSpan v="7" />
                        <text-edit></text-edit>
                    </col>
                    <col>
                        <attr-rowOffset v="6" />
                        <label>右侧在底部</label>
                    </col>
                </row>
            </grid>
        </frame>
    </window>
</app>
```

#### examples/grid/app.py
```python
from mvvmQt.Parser import Parser
import os

if __name__ == "__main__":
    p = Parser(os.path.abspath("%s/../" % __file__))
    p.build()
    p.run()
```

### 横/纵向布局
> 使用横/纵向布局可以方便的将布局下的控件自动按横/纵向布局排版，横向布局使用&lt;hbox&gt;&lt;/hbox&gt;，纵向布局使用&lt;vbox&gt;&lt;/vbox&gt;

#### example/box/templates/index.jinja2
```html
<app>
    <window>
        <attr-full v="0" />
        <attr-minWidth v="550" />
        <attr-minHeight v="550" />
        <attr-maxWidth v="550" />
        <attr-maxHeight v="550" />
        <attr-title v="Hbox And Vbox" />
        <attr-pos v="200, 200" />

        <frame>
            <attr-width v="500" />
            <attr-height v="500" />
            <vbox>
                <hbox>
                    <label>横向布局: </label>
                    {% for i in range(5) %}
                    <label>Label {{ i + 1 }}</label>
                    {% endfor %}
                </hbox>
                <vbox>
                    <label>纵向布局:</label>
                    {% for i in range(5) %}
                    <label>Label {{ i + 1 }}</label>
                    {% endfor %}
                </vbox>
            </vbox>
        </frame>
    </window>
</app>
```

#### examples/box/app.py
```python
from mvvmQt.Parser import Parser
import os

if __name__ == "__main__":
    p = Parser(os.path.abspath("%s/../" % __file__))
    p.build()
    p.run()
```

### 常用控件
> 以下例子展示常用控件

#### examples/controls/templates/index.jinja2
