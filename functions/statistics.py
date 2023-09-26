from fastapi import HTTPException
from sqlalchemy import and_, func
from sqlalchemy.orm import joinedload
from utils.db_operations import save_in_db, the_one, the_one_model_name
from utils.pagination import pagination
from models.orders import Orders
from models.order_done_products import Order_done_products


def order_statistics(order_id, from_time, to_time, page, limit, db):
    orders = db.query(Orders)
    if order_id:
        orders = orders.filter(Orders.id == order_id)
    if from_time and to_time:
        orders = orders.filter(func.date(Orders.date).between(from_time, to_time))
    for order in orders.all() :
        total_kpi = db.query(func.sum(Order_done_products.kpi_money)).filter(Order_done_products.order_id == order.id).scalar()
    # return pagination(orders, page, limit)