from mvvmQt.Elements import Element
import uuid

def setStyleSheet(*params):
    v = params[0]
    o: Element = params[-2]
    token = uuid.uuid1()

    o.qt.setObjectName("%s" % token)
    style = "QFrame#%s{%s}" % (token, v)
    o.qt.setStyleSheet(style)

def __updateObIndexValue(ob, v, t):
    if t == bool:
        ob.value = bool(v - 1)
    else:
        ob.value = v - 1

def __updateObValue(ob, v):
    ob.value = v

def groupChecked(*params):
    v = params[0] #会自动根据初始值确定使用索引还是布尔值
    o: Element = params[-2]
    ob = params[-1]

    attr = list(filter(lambda _: _.key == 'checked', o.attrs))[0]

    if attr.twoWay and not getattr(o.qt, '_bindClicked', False):
        o.qt.buttonClicked[int].connect(lambda id: __updateObIndexValue(ob, id, type(v)))
        o.qt._bindClicked = True

    o.qt.buttons()[int(v)].setChecked(True)

def indexChanged(*params):
    v = params[0]
    o: Element = params[-2]
    ob = params[-1]

    attr = list(filter(lambda _: _.key == 'index', o.attrs))[0]

    if attr.twoWay and not getattr(o.qt, '_bindChanged', False):
        o.qt.currentIndexChanged[int].connect(lambda id: __updateObIndexValue(ob, id, type(v)))
        o.qt._bindChanged = True

    o.qt.setCurrentIndex(v)

def htmlChanged(*params):
    v = params[0]
    o: Element = params[-2]
    ob = params[-1]

    attr = list(filter(lambda _: _.key == 'html', o.attrs))[0]

    if attr.twoWay and not getattr(o.qt, '_bindHtml', False):
        o.qt.textChanged.connect(lambda: __updateObValue(ob, o.qt.toHtml()))
        o.qt._bindHtml = True
    
    if v != o.qt.toHtml():
        o.qt.setHtml(v)

def textChanged(*params):
    v = params[0]
    o: Element = params[-2]
    ob = params[-1]

    attr = list(filter(lambda _: _.key == 'text', o.attrs))[0]

    if attr.twoWay and not getattr(o.qt, '_bindText', False): #已绑定过不再进行绑定
        o.qt.textChanged.connect(lambda: __updateObValue(ob, o.qt.toPlainText()))
        o.qt._bindText = True
    
    if v != o.qt.toPlainText():
        o.qt.setPlainText(v)

def valueChanged(*params):
    v = params[0]
    o: Element = params[-2]
    ob = params[-1]

    attr = list(filter(lambda _: _.key == 'value', o.attrs))[0]

    if attr.twoWay and not getattr(o.qt, '_bindValue', False): #已绑定过不再进行绑定
        o.qt.valueChanged.connect(lambda: __updateObValue(ob, o.qt.value()))
        o.qt._bindValue = True
    
    if v != o.qt.value():
        o.qt.setValue(v)