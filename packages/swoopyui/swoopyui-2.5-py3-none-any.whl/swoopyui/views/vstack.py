from .subviewparent import SubViewParent



class VStack (SubViewParent):
    """Align the subviews in a parent stack verticaly."""
    def __init__(self, padding:int=0) -> None:
        super().__init__()

        self.padding : int = padding

        self.vdata.update({
            "name" : "VStack",
            "props" : {
                "padding" : self.padding
            }
        })
    
    def update (self):
        self.vdata.update({
            "props" : {
                "padding" : int(self.padding)
            }
        })
        super().update()