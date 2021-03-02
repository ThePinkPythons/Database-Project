import db.sql.query.utilities
import db.crud.executor

db_handler = db.sql.query.utilities
executor = db.crud.executor


def view_past_orders():
    query = db_handler.create_select()
    return executor.get_record(query)


def recommend_to_user():
    query = db_handler.create_select()
    return executor.get_record(query)


def products_under():
    query = db_handler.create_select()
    return executor.get_record(query)
