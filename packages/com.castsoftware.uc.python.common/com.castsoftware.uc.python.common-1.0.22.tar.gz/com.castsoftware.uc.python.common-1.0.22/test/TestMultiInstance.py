from cast_common.highlight import Highlight
from cast_common.logger import INFO,DEBUG


class A (Highlight):
        pass

class B (Highlight):
        pass


hl = A('n.kaplan+MerckMSD@castsoftware.com','vadKpBFAZ8KIKb2f2y',4711,'TPS',hl_base_url='https://cloud.casthighlight.com',log_level=DEBUG)
df = hl.get_green_detail('TPS')

hl2 = B('n.kaplan+MerckMSD@castsoftware.com','vadKpBFAZ8KIKb2f2y',4711,'TPS',hl_base_url='https://cloud.casthighlight.com',log_level=DEBUG)

pass
