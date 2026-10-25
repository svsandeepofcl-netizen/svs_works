class Solution:

    def encode(self, strs: List[str]) -> str:
        e_str=''
        for i in strs:
            e_str=e_str+str(len(i))+"#"+i

        return e_str


    def decode(self, s: str) -> List[str]:
        decoded_str=[]
        i=0
        
        while i < len(s):
            j=i
            while j<len(s):                     
                if s[j]=='#':
                    length = int(s[i:j])
                    break
                j+=1
    
            decoded_str.append(s[j+1:j+1+length])
            i=j+1+length
        
        return decoded_str