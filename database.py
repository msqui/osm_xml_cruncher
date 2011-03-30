from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import insert

def save_to_db(places):
    """
        Saves given proposals to database
    """
    # engine = create_engine('mysql://python_jobs_user:python_jobs@localhost/python_jobs?charset=utf8', encoding='utf-8')
    engine = create_engine('postgresql://sergey:os@localhost/openstreet?charset=utf8', encoding='utf-8')
    meta = MetaData()
    meta.bind = engine
    conn = engine.connect()
    places_table = Table('places', meta, autoload=True)
    
    for place in places:
        ins = places_table.insert().values(id=place.id, type_class=place.tags.get())
    
    
    # for prop in proposals:
    #     ins = python_jobs.insert().values(title=prop.title, link=prop.link, description=prop.description, guid=prop.guid, pub_date=prop.pub_date)
    #     conn.execute(ins)
    #     # print ins.compile().params