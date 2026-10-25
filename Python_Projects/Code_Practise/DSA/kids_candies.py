class Solution:
    def kidsWithCandies(self, candies: List[int], extraCandies: int) -> List[bool]:

        bool_list=[]
        max_value=max(candies)
        
        for i in candies:
            total=i+extraCandies
            
            if total >=max_value:
                bool_list.append(True)
            else:
                bool_list.append(False)

        return bool_list
        