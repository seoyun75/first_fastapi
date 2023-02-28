from notice import Notice

class NoticeDB():
    notice_list : dict
    
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(NoticeDB, cls, *args, **kwargs).__new__(cls, *args, **kwargs)
            cls.instance.notice_list = {}

        return cls.instance

        
    # def __init__(self)