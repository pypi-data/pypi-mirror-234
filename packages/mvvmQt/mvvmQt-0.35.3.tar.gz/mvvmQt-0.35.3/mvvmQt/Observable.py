import asyncio, threading

class ObservableBase:
    def __init__(self):
        self.changeActionsList = []
        self.changeActionsList_once = []

    def useFunc(self, f, params):
        if asyncio.iscoroutinefunction(f):
            loop = asyncio.get_event_loop()
            loop.create_task(f(*params))
        else:
            f(*params)

    def trigger(self):
        [self.useFunc(v['func'], [self._value]) for v in self.changeActionsList]
        [self.useFunc(f, [self._value]) for f in self.changeActionsList_once]
        self.changeActionsList_once = []

    def once(self, f):
        self.changeActionsList_once.append(f)

    def subscribe(self, f, name=None, init=False): #name可以为订阅设置名称，通过name可以删除订阅，init代表是否绑定订阅的同时先调用一次
        self.changeActionsList.append({'func': f, 'name': name})
        if init:
            self.useFunc(f, [self._value])

    def removeSubscribe(self, name):
        remove_e = []
        for i, v in enumerate(self.changeActionsList):
            if v['name'] == name:
                remove_e.append(v)
        for i in remove_e:
            self.changeActionsList.remove(i)

class Observable(ObservableBase):
    def __init__(self, v, format=None):
        super().__init__()
        self.format = format
        self._value = v

    def __str__(self):
        if self.format:
            return self.format % self._value
        return self._value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        if v == self._value:
            return
        self._value = v
        # [v['func'](self._value) for v in self.changeActionsList]
        self.trigger()

    def setValue(self, v):
        self.value = v

class Computed(ObservableBase):
    def __init__(self, obs, func):
        super().__init__()
        self.obs = obs
        self.func = func
        self._value = func(self.allValue)
        for i, ob in enumerate(obs):
            ob.subscribe(lambda v: self.callFunc())

    def callFunc(self):
        self.value = self.func(self.allValue)

    @property
    def allValue(self):
        return [ob.value for ob in self.obs]

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        if v == self._value:
            return
        self._value = v
        # [v['func'](self._value) for v in self.changeActionsList]
        self.trigger()

    # def subscribe(self, f, name=None, init=False): #name可以为订阅设置名称，通过name可以删除订阅，init代表是否绑定订阅的同时先调用一次
    #     self.changeActionsList.append({'func': f, 'name': name})
    #     if init:
    #         f(self._value)

    # def removeSubscribe(self, name):
    #     remove_e = []
    #     for i, v in enumerate(self.changeActionsList):
    #         if v['name'] == name:
    #             remove_e.append(v)
    #     for i in remove_e:
    #         self.changeActionsList.remove(i)

class BoolFormat:
    def __init__(self, arr, format):
        self.format = format
        self.arr = arr

    def __mod__(self, v):
        return self.format % (self.arr[0] if v else self.arr[1])

class DebounceAsync:
    def __init__(self, interval):
        self.interval = interval
        self.debounced = None

    async def timer(self, func, *args, **kwargs):
        await asyncio.sleep(self.interval)
        self.debounced = None
        func(*args, **kwargs)

    def __call__(self, func):
        def decorator(*args, **kwargs):
            if self.debounced is not None:
                self.debounced.cancel()
            self.debounced = asyncio.get_event_loop().create_task(self.timer(func, *args, **kwargs))

        return decorator

class DebounceThread:
    def __init__(self, interval):
        self.interval = interval
        self.debounced = None

    def __call__(self, func):
        def decorator(*args, **kwargs):
            if self.debounced is not None:
                self.debounced.cancel()
            self.debounced = threading.Timer(self.interval, func, args, kwargs)
            self.debounced.start()

        return decorator


if __name__ == "__main__":
    import time, threading
    def testDebounce(v):
        print(v)

    @DebounceAsync(3)
    def changeB(v):
        b.value = v

    a = Observable(0)
    b = Observable(a.value)
    a.subscribe(changeB)
    b.subscribe(testDebounce)

    async def test():
        a.value = 1
        await asyncio.sleep(2)

        a.value = 3
        await asyncio.sleep(5)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())