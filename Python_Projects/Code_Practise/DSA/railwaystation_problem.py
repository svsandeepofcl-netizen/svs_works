class Solution:    
    def minPlatform(self, arr, dep):
        # code here
        arr.sort()
        dep.sort()
        
        max_platforms=1
        platforms=1
        i,j = 1,0
        
        while i<len(arr):
                
            if arr[i]<=dep[j]:
                platforms+=1
                i+=1
            else:
                platforms-=1
                j+=1
            
            max_platforms=max(max_platforms, platforms)
            
            # i+=1
            # j+=1
            
        return max_platforms
