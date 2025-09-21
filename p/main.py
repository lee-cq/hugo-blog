#!/bin/python3
"""

"""

class Solution(object):
    def countBalls_self(self, lowLimit, highLimit):
        """
        时间复杂度：O(N log n)
        空间复杂度：O(N)
        """
        rest = dict()

        def get_sum(n, s=0):
            if n == 0:
                return s
            n, _s = divmod(n, 10)
            return get_sum(n, s + _s)
        
        for i in range(lowLimit, highLimit+1):
            ss = get_sum(i)
            if ss in rest:
                rest[ss] += 1
            else:
                rest[ss] = 1
        
        return max(rest.values())
