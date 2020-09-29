

class Video_Segment:

    def __init__(self, segment_id, qi):
        self.segment_id = segment_id
        self.qi         = qi


    def get_qi(self):
        return self.qi

    def get_segment_id(self):
        return self.segment_id