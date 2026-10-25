#leetcode 49
from collections import defaultdict
strs = ["eat","tea","tan","ate","nat","bat"]

class Solution:
    def groupAnagrams(self, strs):
        result=defaultdict(list)  
        for str in strs: 
            count=[0]*26
              
            for i in str:
                count[ord(i)-ord("a")]+=1
            
            result[tuple(count)].append(str)
        
        return result.values()
    

obj=Solution()
print(obj.groupAnagrams(strs))