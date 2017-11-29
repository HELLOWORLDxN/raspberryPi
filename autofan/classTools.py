import threading,six,warnings,functools

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
        userGetAttrExist='__getattr__' in attrs.keys() 
        if userGetAttrExist:
            userGetAttr=attrs['__getattr__']
        userGetAttributeExist='__getarrtibute__' in attrs.keys()
        if userGetAttributeExist:
            userGetAttribute=attrs['__getattribute__']
        userSetAttrExist='__setattr__' in attrs.keys()
        if userSetAttrExist:
            userSetAttr=attrs['__setattr__']

        def __getattr__(self,*args,**kwargs):
            with object.__getattribute__(self,'__threadSafeLock__'):
                if userGetAttrExist:
                    ret=userGetAttr(self,*args,**kwargs)
            return ret
        def __getattribute__(self,*args,**kwargs):
            with object.__getattribute__(self,'__threadSafeLock__'):
                if userGetAttributeExist:
                    ret=userGetAttribute(self,*args,**kwargs)
                else:
                    ret=object.__getattribute__(self,*args,**kwargs)
            return ret
        def __setattr__(self,*args,**kwargs):
            with object.__getattribute__(self,'__threadSafeLock__'):
                if userSetAttrExist:
                    ret=userSetAttr(self,*args,**kwargs)
                else:
                    ret=object.__setattr__(self,*args,**kwargs)
            return ret

        attrs.update({'__setattr__':__setattr__})
        if userGetAttrExist:
            attrs.update({'__getattr__':__getattr__})
        attrs.update({'__getattrbute__':__getattribute__})
        if '__threadSafeLock__' in attrs.keys():
            raise Exception('__threadSafeLock__ has been used by @threadSafe')
        rlock=threading.RLock()
        attrs.update({'__threadSafeLock__':rlock})
        return super().__new__(cls,name,bases,attrs)
threadSafe=six.add_metaclass(ThreadSafeAttr)
