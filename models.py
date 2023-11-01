class FirstMany(db.Model, SerializerMixin):
    __tablename__ = 'first_many_table'

    id = db.Column(db.Integer, primary_key=True)
    property = db.Column(db.String)

    # Add relationship
    joins = db.relationship('Join', back_populates=('first_many'), cascade='all, delete-orphan')
    second_many = association_proxy('joins', 'second_many')
    
    # Add serialization rules
    serialize_rules = ('-joins.first_many', )
    
    def __repr__(self):
        return f'<Many {self.id}: {self.property}>'
    
class Join(db.Model, SerializerMixin):
    __tablename__ = 'join_table'

    id = db.Column(db.Integer, primary_key=True)
    property = db.Column(db.Integer)

    first_many_id = db.Column(db.Integer, db.ForeignKey('first_many_table.id'))
    second_many_id = db.Column(db.Integer, db.ForeignKey('second_many_table.id'))

    # Add relationships
    first_many = db.relationship('FirstMany', back_populates=('joins'))
    second_many = db.relationship('SecondMany', back_populates=('joins'))
    
    # Add serialization rules
    serialize_rules = ('-first_many.joins', '-first_many.second_many', '-second_many.joins', '-second_many.first_many')
    
    # Add validation
    @validates('property')
    def validates_property(self, key, property):
        if 0 <= property <= 23:
            return property
        else:
            raise ValueError('Property must be an integer between 0 and 23, representing the hour of the day.')
    
    def __repr__(self):
        return f'<Join {self.id}: {self.property}>'