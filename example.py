"""
    @Description: Define a one-to-many dependency between objects so that when one object
                  changes state, all its dependents are notified and updatedautomatically.
    @Created: 2017/09/02
    @Author: Yui Qi Tang
    @Version: 0.1
"""

import abc
import threading, time

class Resturant(object):

    def __init__(self):
        self._customers = set() # store customer
        self._meal = None

    def attach(self, customer):
        customer._resturant = self # customer subscribe this resturant object
        self._customers.add(customer) 

    def deattach(self, customer):
        customer._resturant = None # customer discard this object
        self._customers.discard(customer)

    def _notify(self):
        for c in self._customers:
            c.update(self._meal) # new meal!!
 
    @property
    def meal_new_arrival(self):
        return self._meal

    @meal_new_arrival.setter
    def meal_new_arrival(self, meal_name):
        self._meal = meal_name
        self._notify()

class Customer(metaclass=abc.ABCMeta):

     def __init__(self):
         self._resturant = None
         self._meal = None
     
     @abc.abstractmethod
     def update(self, arg):
         pass
    
class CustomerObserver(Customer):
    
    def update(self, arg):
        self._meal = arg

    @property
    def today_lunch(self):
        return self._meal

# update meal every 1 sec
def auto_update_new_meal(resturant, meal_name_list):
    delay = 1
    for meal_name in meal_name_list:
        resturant.meal_new_arrival = meal_name
        time.sleep(delay)


def main():

    # create resturants
    rA = Resturant()
    rB = Resturant()

    # create customers
    cA = CustomerObserver()
    cC = CustomerObserver()
    cB = CustomerObserver()

    # subscribe
    rA.attach(cA)
    rA.attach(cC)
    rB.attach(cB)

    # auto update meal name by thread
    t1 = threading.Thread(target=auto_update_new_meal, args=(rA, ["rA_meal_1", "rA_meal_2", "banana", "apple", "cookie", "noddles", "fish"]))
    t2 = threading.Thread(target=auto_update_new_meal, args=(rB, ["rB_meal_1", "rB_meal_2", "rB_meal_3", "KFC", "McD"]))
    t1.start()
    t2.start()

    # customer take lunch 10 times every 1 sec.
    # demo here
    for i in range(10):
        print("==="*6) 
        print("round {} start".format(str(i)))
        print("===>Resturant A<===")
        print("custome A got new meal {0}".format(cA.today_lunch))
        print("custome C got new meal {0}".format(cC.today_lunch))
        print("===>Resturant B<===")
        print("custome B got new meal {0}".format(cB.today_lunch))
        print("round {} finish".format(str(i)))
        print("==="*6)
        time.sleep(1)

if __name__ == "__main__":
    main()
