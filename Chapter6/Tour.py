#Tour.py
#상품정보를 담는 Class
class TourInfo :
    title = None
    price = None
    comment = None
    point = None
    period1 = None
    period2 = None

    def __init__(self, title, price, comment, point, period1, period2):
        self.title = title;      self.price = price
        self.comment =comment;   self.point = point
        self.period1 = period1;     self.period2 = period2

    def __str__(self):
        return "%s, %d, %s, %f, %s, %s" \
            % (self.title, self.price, self.comment, self.point, self.period1, self.period2)