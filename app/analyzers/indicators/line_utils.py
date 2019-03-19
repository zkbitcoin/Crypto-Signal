class LineUtils():
    
    class Point():
        def __init__(self, x_init, y_init):
            self.x = x_init
            self.y = y_init
            
        
    def onSegment(self, p, q, r):
        if (q.x <= max(p.x, r.x) and q.x >= min(p.x, r.x) and q.y <= max(p.y, r.y) and q.y >= min(p.y, r.y)):
            return True

        return False
    
    """
     To find orientation of ordered triplet (p, q, r). 
    // The function returns following values 
    // 0 --> p, q and r are colinear 
    // 1 --> Clockwise 
    // 2 --> Counterclockwise 
    """
    def orientation(self, p, q, r):
        #See https://www.geeksforgeeks.org/orientation-3-ordered-points/ 
        #for details of below formula. 
        val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)

        if (val == 0):
            return 0  # colinear 

        return 1 if (val > 0) else 2 #clock or counterclock wise    
    
    # The main function that returns true if line segment 'p1q1' 
    # and 'p2q2' intersect.  doIntersect(Point p1, Point q1, Point p2, Point q2) 
    def doIntersect(self, point_p1, point_q1, point_p2, point_q2) :
        
        p1 = self.Point(point_p1[0], point_p1[1])
        q1 = self.Point(point_q1[0], point_q1[1])
        
        p2 = self.Point(point_p2[0], point_p2[1])
        q2 = self.Point(point_q2[0], point_q2[1])
        
       
        # Find the four orientations needed for general and 
        # special cases 
        o1 = self.orientation(p1, q1, p2); 
        o2 = self.orientation(p1, q1, q2); 
        o3 = self.orientation(p2, q2, p1); 
        o4 = self.orientation(p2, q2, q1); 

        #General case 
        if (o1 != o2 and o3 != o4) :
            return True

        #Special Cases 
        #p1, q1 and p2 are colinear and p2 lies on segment p1q1 
        if (o1 == 0 and self.onSegment(p1, p2, q1)):
            return True

        #p1, q1 and q2 are colinear and q2 lies on segment p1q1 
        if (o2 == 0 and self.onSegment(p1, q2, q1)) :
            return True

        #p2, q2 and p1 are colinear and p1 lies on segment p2q2 
        if (o3 == 0 and self.onSegment(p2, p1, q2)):
            return True

        #p2, q2 and q1 are colinear and q1 lies on segment p2q2 
        if (o4 == 0 and self.onSegment(p2, q1, q2)):
            return True

        return False #Doesn't fall in any of the above cases   