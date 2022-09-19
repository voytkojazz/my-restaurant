# def count_profit_revenue(objects):
#     revenue = 0
#     profit = 0
#     for purchase in objects:
#         revenue += purchase.menu_item.price
        

#         purchase_cost = 0
#         purchase_rr = purchase.menu_item.reciperequirement_set.all()
#         for rr in purchase_rr:
#             quantity_to_cook = rr.quantity
#             quantity_of_ingridient = rr.ingridient.quantity
#             price_of_unit = rr.ingridient.unit_price
#             price_of_unit_to_cook = quantity_to_cook * (price_of_unit / quantity_of_ingridient)
#             purchase_cost += price_of_unit_to_cook
#             print(f'{rr.ingridient} -- {price_of_unit_to_cook}')
#         print(f'{purchase} --- {purchase_cost}')
#         profit += purchase.menu_item.price - purchase_cost


#     print(profit)
#     return revenue, profit
