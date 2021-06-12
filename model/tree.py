class Tree():
    fathers = [None, None]

    x1 = 0
    y1 = 0
    angle = 0
    depth = 0
    fork_angle = 0
    branch_angle = 0
    base_len = 0
    branch_base_len = 0
    branch_base = 0
    branches = 0

    def __str__(self):
        data = {
            "angle" : self.angle,
            "depth" : self.depth,
            "fork_angle" : self.fork_angle,
            "branch_angle" : self.branch_angle,
            "base_len" : self.base_len,
            "branch_base_len" : self.branch_base_len,
            "branch_base" : self.branch_base,
            "branches" : self.branches
        }

        return str(data)