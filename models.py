from sqlalchemy import Boolean,Column,ForeignKey,Integer,String

from database import Base,engine,sessionmaker

Session = sessionmaker(bind=engine)
session = Session()




class Parking_Space_List(Base):
    __tablename__='parking_spacelist1'

    space_id=Column(String,primary_key=True,index=True)
    Level=Column(Integer,index=True)
    Slot=Column(Integer,index=True)
    Availbility_status=Column(String, index=True)


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)









if session.query(Parking_Space_List).count() == 0:
    parking_slots = []
    for level in range(1, 4):  # Level 1 to 3
        prefix = chr(64 + level)  # A for 1, B for 2, C for 3
        for slot in range(1, 11):
            space_id = f"{prefix}{slot}"
            parking_slots.append(
                Parking_Space_List(space_id=space_id, Level=level, Slot=slot, Availbility_status="Vacant")
            )
    session.add_all(parking_slots)
    session.commit()
    print("Inserted 30 new parking slots (A1–C10).")
else:
    print("Table already populated.")




