import mvvmQt.attrTypes as t
import mvvmQt.attrFuncs as f

"""
结构格式为key: [qt function name or callable function, type]
如果为callable function, 最后一个参数必然为Element对象
"""

size = {
    'maxHeight': ['setMaximumHeight', int],
    'maxWidth': ['setMaximumWidth', int],
    'minHeight': ['setMinimumHeight', int],
    'minWidth': ['setMinimumWidth', int],
    'width': ['setFixedWidth', int],
    'height': ['setFixedHeight', int],
    'visible': ['setVisible', [int, bool]]
}

common = {
    'text': ['setText', str],
    'enable': ['setEnabled', [int, bool]]
}

align = {
    'align': ['setAlignment', t.alignment]
}

btn = {
    'checked': ['setChecked', [int, bool]],
    'checkable': ['setCheckable', [int, bool]]
}

style = {
    'qss': ['setStyleSheet', [str, t.readFile]],
    'style': [f.setStyleSheet, str]
}

ElementAttr = {
    'widget': {
        **size,
        **style,
        'title': ['setWindowTitle', str],
        'pos': ['move', t.toList(int)],
        'full': ['showType', [int, bool]]
    },
    'frame': {
        **size, **style,
        'shape': ['setFrameShape', t.frameShape],
        'shadow': ['setFrameShadow', t.frameShadow],
        'linew': ['setLineWidth', int],
        'lineMw': ['setMidLineWidth', int],
    },
    'grid': {
        'spacing': ['setSpacing', int],
        'vspacing': ['setVerticalSpacing', int],
        'hspacing': ['setHorizontalSpacing', int]
    },
    'button-group': {
        'exclusive': ['setExclusive', [int, bool]],
        'checked': [f.groupChecked, None]
    },
    'button': {
        **size, **common, **btn, **style,
        'shortcut': ['setShortcut', str],
        'tooltip': ['setToolTip', str],
        'icon': ['setIcon', str],
        'repeat': ['setAutoRepeat', [int, bool]],
        'repeatDelay': ['setAutoRepeatDelay', int],
        'repeatInterval': ['setAutoRepeatInterval', int]
    },
    'radio': {
        **common, **btn, **style
    },
    'label': {
        **size, **common, **align, **style,
        'cv': ['setTextOrPixmap', t.cvImg],
        'cvPath': ['setPixmap', [str, t.cvPathImg]],
        'scaledContents': ['setScaledContents', [int, bool]]
    },
    'tab': {
        **style,
        'pos': ['setTabPosition', t.tabPosition],
        'name': ['setTabText', t.toList([int, str])]
    },
    'status': {
        **style,
        'msg': ['showMessage', str]
    },
    'select': {
        **style,
        'index': [f.indexChanged, None]
    },
    'text-edit': {
        **style,
        'text': [f.textChanged, None],
        'html': [f.htmlChanged, None]
    },
    'menu': {
        **style,
        'title': ['setTitle', str]
    },
    'action': {
        **style,
        'text': ['setText', str],
        'tooltip': ['setToolTip', str],
        'shortcut': ['setShortcut', str],
        'enable': ['setEnabled', [int, bool]],
        'checked': ['setChecked', [int, bool]],
        'checkable': ['setCheckable', [int, bool]]
    }
}

ElementAttr['window'] = {
    **ElementAttr['widget']
}