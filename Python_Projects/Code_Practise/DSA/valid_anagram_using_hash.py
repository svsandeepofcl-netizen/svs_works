#leetcode 242
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        s_hash={}

        if len(s)!=len(t):
            return False
        
        for i in s:
            if i not in s_hash:
                s_hash[i]=1
            else:
                s_hash[i]+=1
 
        for i in t:
            if i in s_hash:
                s_hash[i]-=1

        for k,v in s_hash.items():
            if s_hash.get(k)!=0:
                return False
        
        return True