from django.db import models
from sales.models import Sale

class Recap(models.Model):
    dias_trabajados = models.PositiveIntegerField(default=0)
    month = models.PositiveIntegerField(default=1)                                                        
    date = models.DateTimeField(auto_now_add=True)
    
    def get_total_sales(self):
        month_sales = Sale.objects.filter(fecha__year=self.date.year,fecha__month=self.month)

        return month_sales.count()
 

    def get_total_income(self):
        month_sales = Sale.objects.filter(fecha__year=self.date.year,fecha__month=self.month)
        total_income = 0
        for sale in month_sales:
            total_income += sale.calculate_total()
        
        return total_income

    def get_whites(self):
        month_sales = Sale.objects.filter(fecha__year=self.date.year,fecha__month=self.month)

        white_sales = month_sales.filter(tipo='en blanco')

        white_sales_total = sum(list(map(int,white_sales.values_list('cantidad', flat=True))))

        return white_sales_total

    def get_painted(self):
        month_sales = Sale.objects.filter(fecha__year=self.date.year,fecha__month=self.month)

        painted = month_sales.filter(tipo='pintado')

        painted_total = sum(list(map(int,painted.values_list('cantidad', flat=True))))


        return painted_total

    def get_avg_per_day(self):
        total_income = self.get_total_income()

        return total_income / self.dias_trabajados 

    def get_piece_per_day(self):
        month_sales = Sale.objects.filter(fecha__year=self.date.year,fecha__month=self.month)

        pieces = sum(list(map(int,month_sales.values_list('cantidad',flat=True))))    

        return pieces / self.dias_trabajados
        
    def get_avg_per_sale(self):
        total_income = self.get_total_income()
        total_sales = self.get_total_sales()

        if total_income and total_sales:

            return total_income / total_sales
        
        else:
            return [0,0]


    def __str__(self):
        return str(self.month) + ' / ' + str(self.date.year)