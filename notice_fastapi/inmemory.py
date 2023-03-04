class PostDB():
    post_list : Dict[int,str]
    
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PostDB, cls, *args, **kwargs).__new__(cls, *args, **kwargs)
            cls.instance.post_list = {}

        return cls.instance

        
    # def __init__(self)