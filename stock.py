from .models import update_quantities_from_csv,MedicineDetails,render_template,Blueprint

stockblueprint=Blueprint('stockblueprint', __name__)

from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class DisplayUpdatedStockCommand(Command):
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        return self.receiver.display_updated_stock()

class StockReceiver:
    def __init__(self):
        pass
    def display_updated_stock(self):
        updated_stock=update_quantities_from_csv(r'D:\Design Patterns Project\order_history .csv')
        print("HELLO FRIENDS THIS IS THE UPDATED STOCK",updated_stock)
        return updated_stock
    
class StockManagerInvoker:
    def __init__(self):
        self.command = None

    def set_command(self, command):
        self.command = command

    def execute_command(self):
        if self.command:
            return self.command.execute()



@stockblueprint.route('/stocks')
def stocks():
    print("hello")
    stock_receiver=StockReceiver()
    display_updated_command = DisplayUpdatedStockCommand(stock_receiver)
    invoker = StockManagerInvoker()
    invoker.set_command(display_updated_command)
    report=invoker.execute_command()
    print(report)
    return render_template('stocks.html', report=report)

