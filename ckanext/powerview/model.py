import datetime

from sqlalchemy import types, Table, Column, ForeignKey

from ckan.model import meta, domain_object
from ckan.model import types as ckan_types

import logging
log = logging.getLogger(__name__)


def init_tables():
    if not powerview_table.exists():
        powerview_table.create(checkfirst=True)
        powerview_resource_association_table.create(checkfirst=True)
        log.debug('PowerView tables created')
    else:
        log.debug('PowerView tables already exist')


class PowerviewBaseModel(domain_object.DomainObject):
    @classmethod
    def filter(cls, **kwargs):
        return meta.Session.query(cls).filter_by(**kwargs)

    @classmethod
    def get(cls, **kwargs):
        instance = cls.filter(**kwargs).first()
        return instance

    @classmethod
    def count(cls):
        return meta.Session.query(cls).count()

    @classmethod
    def exists(cls, **kwargs):
        if cls.filter(**kwargs).first():
            return True
        else:
            return False

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        meta.Session.add(instance)
        meta.Session.commit()
        return instance.as_dict()


class PowerviewResourceAssociation(PowerviewBaseModel):

    @classmethod
    def get_resource_ids_for_powerview(cls, powerview_id):
        '''
        Return a list of resource ids associated with the passed powerview_id.
        '''
        associated_resource_id_list = \
            meta.Session.query(cls.resource_id).filter_by(
                powerview_id=powerview_id).all()
        associated_resource_id_list = [res[0] for res in
                                       associated_resource_id_list]
        return associated_resource_id_list

powerview_resource_association_table = Table(
    'powerview_resource_association', meta.metadata,
    Column('resource_id', types.UnicodeText,
           ForeignKey('resource.id',
                      ondelete='CASCADE',
                      onupdate='CASCADE'),
           primary_key=True, nullable=False),
    Column('powerview_id', types.UnicodeText,
           ForeignKey('powerview.id',
                      ondelete='CASCADE',
                      onupdate='CASCADE'),
           primary_key=True, nullable=False)
)

meta.mapper(PowerviewResourceAssociation, powerview_resource_association_table)


class PowerView(PowerviewBaseModel):
    def as_dict(self):
        _dict = domain_object.DomainObject.as_dict(self)
        _dict['resources'] = \
            PowerviewResourceAssociation.get_resource_ids_for_powerview(
                self.id)
        return _dict

powerview_table = Table(
    'powerview', meta.metadata,
    Column('id', types.UnicodeText, primary_key=True,
           default=ckan_types.make_uuid),
    Column('title', types.UnicodeText, nullable=True),
    Column('description', types.UnicodeText, nullable=True),
    Column('view_type', types.UnicodeText, nullable=False),
    Column('config', ckan_types.JsonDictType),
    Column('created', types.DateTime, default=datetime.datetime.utcnow),
    Column('last_modified', types.DateTime),
    Column('owner_org', types.UnicodeText),
    Column('created_by', types.UnicodeText),
    Column('private', types.Boolean, default=False),
)

meta.mapper(PowerView, powerview_table)
