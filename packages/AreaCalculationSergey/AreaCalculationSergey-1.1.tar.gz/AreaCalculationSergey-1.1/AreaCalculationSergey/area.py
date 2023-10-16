class AreaCalc:
    @staticmethod
    def area_of_circle(radius, round_result=2) -> float:
        pi = 3.1415926535
        if radius <= 0:
            raise ValueError("Radius has to be positive!")
        return round(pi * radius**2, round_result)

    @staticmethod
    def area_of_triangle(side1, side2, side3, round_result=2) -> float:
        if any(side <= 0 for side in [side1, side2, side3]):
            raise ValueError("Lengths of sides can`t be negative or equal 0!")
        elif side1 + side2 > side3 and side1 + side3 > side2 and side2 + side3 > side1: 
            half_of_perimeter = (side1 + side2 + side3) / 2
            area = (half_of_perimeter * (half_of_perimeter - side1) * (half_of_perimeter - side2) * (half_of_perimeter - side3)) ** 0.5
            return round(area, round_result)
        else:
            raise ValueError("Triangle doesn`t exist!")
        
    @staticmethod
    def right_triangle(side1, side2, side3):
        if any(side <= 0 for side in [side1, side2, side3]):
            raise ValueError("Lengths of sides can`t be negative or equal 0!")
        elif side1**2 + side2**2 == side3**2:
            return True
        elif side2**2 + side3**2 == side1**2:
            return True
        elif side3**2 + side1**2 == side2**2:
            return True
        else:
            return False
        
