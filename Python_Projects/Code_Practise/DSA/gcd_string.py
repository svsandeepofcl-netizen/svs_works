from math import gcd

class Solution(object):
    def gcdOfStrings(self, str1, str2):
        """
        :type str1: str
        :type str2: str
        :rtype: str
        """   
        if str1+str2!=str2+str1:
            return ""
        leng=gcd(len(str1), len(str2))

        return str1[:leng]


obj=Solution()
print(obj.gcdOfStrings("ABABAB", "ABAB"))