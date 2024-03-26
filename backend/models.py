from config import db

mob_zone_association = db.Table('mob_zone_association',
    db.Column('mob_id', db.Integer, db.ForeignKey('mob.id')),
    db.Column('zone_id', db.Integer, db.ForeignKey('zone.id'))
)

item_mob_association = db.Table('item_mob_association',
    db.Column('item_id', db.Integer, db.ForeignKey('item.id')),
    db.Column('mob_id', db.Integer, db.ForeignKey('mob.id'))
)

item_slot_association = db.Table('item_slot_association',
    db.Column('item_id', db.Integer, db.ForeignKey('item.id')),
    db.Column('item_slot_id', db.Integer, db.ForeignKey('item_slot.id'))
)

item_class_association = db.Table('item_class_association',
    db.Column('item_id', db.Integer, db.ForeignKey('item.id')),
    db.Column('class_id', db.Integer, db.ForeignKey('class.id'))
)

item_race_association = db.Table('item_race_association',
    db.Column('item_id', db.Integer, db.ForeignKey('item.id')),
    db.Column('race_id', db.Integer, db.ForeignKey('race.id'))
)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(), nullable=False)
    dropped_by = db.relationship('Mob', secondary=item_mob_association, backref=db.backref('drops', lazy='dynamic'))
    location = db.relationship('Zone', backref=db.backref('items', lazy='dynamic'))
    date_added = db.Column(db.DateTime)
    item_slots = db.relationship('ItemSlot', secondary=item_slot_association, backref=db.backref('items', lazy='dynamic'))
    classes = db.relationship('Class', secondary=item_class_association, backref=db.backref('items', lazy='dynamic'))
    races = db.relationship('Race', secondary=item_race_association, backref=db.backref('items', lazy='dynamic'))
    item_lore = db.Column(db.String())

    def to_json(self):
        mobs = [{'id': mob.id, 'mob_name': mob.mob_name} for mob in self.dropped_by]
        zones = [{'id': zone.id, 'zone_name': zone.zone_name} for zone in self.location.zones]
        item_slots = [{'id': slot.id, 'slot_name': slot.slot_name} for slot in self.item_slots]
        classes = [{'id': class_.id, 'class_name': class_.class_name} for class_ in self.classes]
        races = [{'id': race.id, 'race_name': race.race_name} for race in self.races]

        return {
            "id": self.id,
            "item_name": self.item_name,
            "date_added": self.date_added,
            "dropped_by": mobs,
            "zones": zones,
            "item_slots": item_slots,
            "classes": classes,
            "races": races,
            "item_lore": self.item_lore
        }

class Mob(db.model):
    id = db.Column(db.Integer, primary_key=True)
    mob_name = db.Column(db.String(), nullable=False)
    zones = db.relationship('Zone', secondary=mob_zone_association, backref=db.backref('mobs', lazy='dynamic'))

class Zone(db.model):
    id = db.Column(db.Integer, primary_key=True)
    zone_name = db.Column(db.String(), nullable=False)

class Class(db.model):
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(), nullable=False)
    class_short_name = db.Column(db.String(), nullable=False)

class Race(db.model):
    id = db.Column(db.Integer, primary_key=True)
    race_name = db.Column(db.String(), nullable=False)
    race_short_name = db.Column(db.String(), nullable=False)

class ItemSlot(db.model):
    id = db.Column(db.Integer, primary_key=True)
    slot_name = db.Column(db.String(), nullable=False)
