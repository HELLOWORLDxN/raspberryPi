import threading,six,warnings

class Func(type):
    def __new__(cls,name,bases,attrs):
        def callFunc(cls,*args,**kwargs):
            return cls.__call__(cls,*args,**kwargs)
        if '__call__' not in attrs.keys():
            raise Exception('Class '+str(cls)+'need to define func <__call__(cls,*arg,**kwarg)> when use @toFunc')
        attrs.update({'__new__':callFunc})
        return super().__new__(cls,name,bases,attrs)
toFunc=six.add_metaclass(Func)
        
@toFunc
class Singleton():
    __modleSingletonClassMap={}
    __singletonSafeLock=threading.Lock()
    def __call__(cls,decoCls):
        @functools.wraps(cls)
        def wrap(*args,**kwargs):
            with cls.__singletonSafeLock :
                instance=cls.__modleSingletonClassMap.setdefault(decoCls,decoCls())
            return instance
        return wrap

class ThreadSafeAttr(type):
    def __new__(cls,name,bases,attrs):
        def __getattr__(self,*args,**kwargs):
            with self.__threadSafeLock__:
                if '__getattr__' in attrs :
                    ret=attrs['__getattr__'](self,*args,**kwargs)
                else:
                    ret=super().__getattr__(*args,**kwargs)
            return ret
        def __getattribute__(self,*args,**kwargs):
            with self.__threadSafeLock__:
                if '__getarrtibute__' in attrs:
                    ret=attrs['__getattribute__'](self,*args,**kwargs)
                else:
                    ret=super().__getattribute__(*args,**kwargs)
            return ret
        if '__getattr__' in attrs :
            warnings.warn('@threadSafeAttr will create __getattribute__ in your class,so maybe your __getattr__ will not work!',DeprecationWarning)
        attrs.update({'__getattr__':__getattr__})
        attrs.update({'__getattrbute__':__getattribute__})
        return super().__new__(cls,name,bases,attrs)
threadSafe=six.add_metaclass(ThreadSafeAttr)
