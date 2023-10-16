'''
Created on 25 Sep 2023

@author: jacklok
'''
import logging
from trexmodel.models.datastore.ndb_models import BaseNModel, DictModel
from google.cloud import ndb
from datetime import datetime
import trexmodel.conf as model_conf
from trexmodel import program_conf

logger = logging.getLogger('model')

class RedemptionCatalogue(BaseNModel, DictModel):
    label                   = ndb.StringProperty(required=True)
    desc                    = ndb.StringProperty(required=False)
    completed_status        = ndb.StringProperty(required=True, choices=set(program_conf.REDEMPTION_CATALOGUE_STATUS))
    start_date              = ndb.DateProperty(required=True)
    end_date                = ndb.DateProperty(required=True)
    
    
