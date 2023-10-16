'''
Created on 1 Jun 2021

@author: jacklok
'''

from google.cloud import ndb
from trexmodel.models.datastore.ndb_models import BaseNModel, DictModel
from trexmodel.models.datastore.user_models import User
from trexmodel.models.datastore.merchant_models import MerchantAcct, Outlet, MerchantUser
from trexlib.utils.string_util import is_empty, is_not_empty
import logging, json
from trexmodel import conf, program_conf
from datetime import datetime, timedelta
from trexmodel.utils.model.model_util import generate_transaction_id
from trexmodel.models.datastore.reward_models import CustomerPointReward,\
    CustomerStampReward, CustomerEntitledVoucher
from trexmodel.models.datastore.model_decorators import model_transactional
from trexmodel.models.datastore.customer_models import Customer
from trexmodel.models.datastore.transaction_models import CustomerTransaction
from trexmodel.models.datastore.prepaid_models import CustomerPrepaidReward


logger = logging.getLogger('debug')


class CustomerRedeemedItemUpstream(DictModel):
    
    dict_properties         = ['customer_key', 'merchant_key', 'redeemed_outlet_key', 'transaction_id', 'redeemed_amount',
                               'reward_format', 'voucher_key', 'redeemed_datetime', 'reverted',
                               'reverted_datetime', 'is_revert'
                               ]
    
    def __init__(self, customer_key=None, merchant_key=None, redeemed_outlet_key=None, transaction_id=None, redeemed_amount=0, reward_format=None, 
                 voucher_key=None, redeemed_datetime=None, reverted=False, reverted_datetime=None, is_revert=False):
        self.customer_key           = customer_key
        self.merchant_key           = merchant_key
        self.redeemed_outlet_key    = redeemed_outlet_key
        self.transaction_id         = transaction_id
        self.redeemed_amount        = redeemed_amount
        self.reward_format          = reward_format
        self.voucher_key            = voucher_key
        self.redeemed_datetime      = redeemed_datetime
        self.reverted               = reverted
        self.reverted_datetime      = reverted_datetime
        self.is_revert              = is_revert
        
        

class CustomerRedemption(BaseNModel, DictModel):
    '''
    Customer as ancestor
    '''
    
    merchant_acct               = ndb.KeyProperty(name="merchant_acct", kind=MerchantAcct)
    user_acct                   = ndb.KeyProperty(name="user_acct", kind=User)
    redeemed_outlet             = ndb.KeyProperty(name="redeemed_outlet", kind=Outlet)
    
    reward_format               = ndb.StringProperty(required=True)
    redeemed_amount             = ndb.FloatProperty(required=True, default=1)
    
    redeemed_summary            = ndb.JsonProperty(required=True)
    
    transaction_id              = ndb.StringProperty(required=True)
    invoice_id                  = ndb.StringProperty(required=False)
    remarks                     = ndb.StringProperty(required=False)
    
    status                      = ndb.StringProperty(required=True, default=program_conf.REDEEM_STATUS_VALID)
    
    redeemed_datetime           = ndb.DateTimeProperty(required=True, auto_now_add=True)
    redeemed_by                 = ndb.KeyProperty(name="redeemed_by", kind=MerchantUser)
    redeemed_by_username        = ndb.StringProperty(required=False)
    
    reverted_datetime           = ndb.DateTimeProperty(required=False)
    reverted_by                 = ndb.KeyProperty(name="reverted_by", kind=MerchantUser)
    reverted_by_username        = ndb.StringProperty(required=False)
    
    is_tier_program_redemption  = ndb.BooleanProperty(required=False, default=False) 
    tier_program_transaction_id = ndb.StringProperty(required=False)
    
    
    dict_properties         = ['transaction_id', 'invoice_id', 'remarks', 'redeemed_amount', 'reward_format',
                               'redeemed_summary', 'redeemed_customer_acct', 'redeemed_outlet_details', 'redeemed_merchant_acct',
                               'redeemed_datetime', 'is_revert', 'allow_to_revert', 
                               'is_system_redemption', 'is_tier_program_redemption', 'tier_program_transaction_id',
                               'redeemed_by_username', 'reverted_datetime', 'reverted_by_username',
                               ]
    
    @staticmethod
    def get_by_transaction_id(transaction_id):
        return CustomerRedemption.query(CustomerRedemption.transaction_id==transaction_id).get()
    
    @property
    def is_valid(self):
        return self.status == program_conf.REDEEM_STATUS_VALID
    
    @property
    def is_system_redemption(self):
        return self.is_tier_program_redemption
    
    @property
    def allow_to_revert(self):
        return self.is_revert == False and self.is_tier_program_redemption==False
    
    @property
    def is_revert(self):
        return self.status == program_conf.REDEEM_STATUS_REVERTED
    
    @property
    def is_voucher_redemption(self):
        return self.redeemed_summary.get('vouchers')is not None and len(self.redeemed_summary.get('vouchers'))>0
    
    @property
    def redeemed_voucher_keys_list(self):
        return self.redeemed_summary.get('vouchers') 
    
    @property
    def redeemed_voucher_keys_list_in_str(self):
        vourchers =  self.redeemed_summary.get('vouchers')
        if vourchers:
            return json.dumps(vourchers)
        else:
            return ''
    
    @property
    def redeemed_merchant_acct(self):
        return MerchantAcct.fetch(self.merchant_acct.urlsafe())
    
    @property
    def redeemed_merchant_acct_key(self):
        return self.merchant_acct.urlsafe().decode('utf-8')
    
    @property
    def redeemed_outlet_key(self):
        return self.redeemed_outlet.urlsafe().decode('utf-8')
    
    @property
    def redeemed_outlet_details(self):
        return Outlet.fetch(self.redeemed_outlet_key)
    
    @property
    def redeemed_customer_key(self):
        return self.parent_key
    
    @property
    def redeemed_customer_acct(self):
        return Customer.fetch(self.parent_key)
    
    @property
    def redeem_format_label(self):
        pass
    
    @property
    def voucher_count(self):
        count = 0
        if self.reward_format == program_conf.REWARD_FORMAT_VOUCHER:
            if self.redeemed_summary:
                
                for voucher_redeemed_details in  self.redeemed_summary.get(program_conf.REWARD_FORMAT_VOUCHER).get('vouchers').values():
                    count+=voucher_redeemed_details.get('amount')
            
        return count
    
    def to_upstream_info(self):
        return CustomerRedeemedItemUpstream(
                                        customer_key        = self.redeemed_customer_key,
                                        merchant_key        = self.redeemed_merchant_acct_key,
                                        redeemed_outlet_key = self.redeemed_outlet_key,
                                        transaction_id      = self.transaction_id,
                                        reward_format       = self.reward_format,
                                        redeemed_datetime   = self.redeemed_datetime,
                                        redeemed_amount     = self.redeemed_amount,
                                        
                                    )
        
    def to_voucher_upstream_info_list(self):
        upstream_info_list = []
        for merchant_voucher_key, voucher_redeemed_details in  self.redeemed_summary.get(program_conf.REWARD_FORMAT_VOUCHER).get('vouchers').items():
            upstream_info_list.append(CustomerRedeemedItemUpstream(
                                        customer_key        = self.redeemed_customer_key,
                                        merchant_key        = self.redeemed_merchant_acct_key,
                                        redeemed_outlet_key = self.redeemed_outlet_key,
                                        transaction_id      = self.transaction_id,
                                        reward_format       = self.reward_format,
                                        redeemed_datetime   = self.redeemed_datetime,
                                        redeemed_amount     = voucher_redeemed_details.get('amount'),
                                        voucher_key         = merchant_voucher_key,
                                    ))    
        return upstream_info_list
    
    def revert(self, reverted_by, reverted_datetime=None):
        self.status = program_conf.REWARD_STATUS_REVERTED
        if reverted_datetime is None:
            reverted_datetime = datetime.now()
        
        self.reverted_datetime      = reverted_datetime
        self.reverted_by            = reverted_by.create_ndb_key()
        self.reverted_by_username   = reverted_by.username
        self.put()
    
    @staticmethod
    def list_by_customer(customer, status=program_conf.REWARD_STATUS_VALID, limit = conf.MAX_FETCH_RECORD):
        return CustomerRedemption.query(ndb.AND(CustomerRedemption.status==status), ancestor=customer.create_ndb_key()).fetch(limit=limit)
    
    @staticmethod
    def list_customer_redemption(customer_acct, offset=0, limit=conf.PAGINATION_SIZE, start_cursor=None, return_with_cursor=False):
        query = CustomerRedemption.query(ancestor = customer_acct.create_ndb_key()).order(-CustomerRedemption.redeemed_datetime)
        
        return CustomerRedemption.list_all_with_condition_query(query, offset=offset, limit=limit, start_cursor=start_cursor, return_with_cursor=return_with_cursor)
    
    @staticmethod
    def list_by_outlet(redeemed_outlet, offset=0, limit=conf.PAGINATION_SIZE, start_cursor=None, return_with_cursor=False):
        query = CustomerRedemption.query(ndb.AND(CustomerRedemption.redeemed_outlet==redeemed_outlet.create_ndb_key())).order(-CustomerRedemption.redeemed_datetime)
        
        return CustomerRedemption.list_all_with_condition_query(query, offset=offset, limit=limit, start_cursor=start_cursor, return_with_cursor=return_with_cursor)
    
    @staticmethod
    def list_merchant_transaction(merchant_acct, offset=0, limit=conf.PAGINATION_SIZE, start_cursor=None, return_with_cursor=False, reverse_order=True):
        if reverse_order:
            query = CustomerRedemption.query(ndb.AND(CustomerRedemption.merchant_acct==merchant_acct.create_ndb_key()))
        else:
            query = CustomerRedemption.query(ndb.AND(CustomerRedemption.merchant_acct==merchant_acct.create_ndb_key()))
        
        return CustomerRedemption.list_all_with_condition_query(query, offset=offset, limit=limit, start_cursor=start_cursor, return_with_cursor=return_with_cursor)
    
    @staticmethod
    def count_customer_redemption(customer_acct, limit=conf.MAX_FETCH_RECORD):
        query = CustomerRedemption.query(ancestor = customer_acct.create_ndb_key())
        
        return CustomerRedemption.count_with_condition_query(query, limit=limit)
    
    @staticmethod
    def count_merchant_redemption(merchant_acct, limit=conf.MAX_FETCH_RECORD):
        query = CustomerRedemption.query(ndb.AND(CustomerRedemption.merchant_acct==merchant_acct.create_ndb_key()))
        
        return CustomerRedemption.count_with_condition_query(query, limit=limit)
    
    @staticmethod
    def create(customer, reward_format, redeemed_outlet, transaction_id=None, 
               redeemed_amount=1, is_tier_program_redemption=False, tier_program_transaction_id=None,
               redeemed_voucher_keys_list=None, invoice_id=None, remarks=None, redeemed_by=None, redeemed_datetime=None):
        
        
        reward_summary              = customer.reward_summary
        prepaid_summary             = customer.prepaid_summary
        entitled_voucher_summary    = customer.entitled_voucher_summary
        
        if is_not_empty(redeemed_by):
            if isinstance(redeemed_by, MerchantUser):
                redeemed_by_username = redeemed_by.username

        
        redeem_transaction_id = transaction_id or generate_transaction_id(prefix='r')
        
        if redeemed_datetime is None:
            redeemed_datetime = datetime.utcnow()
        
        redeemed_summary = {}
        
        #@model_transactional(desc='redeem reward')
        def __start_redeem(__customer, __total_redeemed_amount, cursor, reward_cls):
            (result, next_cursor) = reward_cls.list_by_valid_with_cursor(__customer, limit=50, start_cursor=cursor)
            
            if result:
                 
                redeemed_items_list = []
                transaction_id_list = []
                for r in result:
                    redeemed_amount                     = .0
                    reward_balance_before_redeem        = r.reward_balance
                    
                    logger.debug('__start_redeem: reward_balance_before_redeem before=%s',  reward_balance_before_redeem)
                    logger.debug('__start_redeem: __total_redeemed_amount before=%s',  __total_redeemed_amount)
                    
                    if reward_balance_before_redeem>0:
                        
                        if reward_balance_before_redeem<__total_redeemed_amount:
                            logger.debug('__start_redeem: redeem partial amount from redeem amount')
                            redeemed_amount = reward_balance_before_redeem
                            __total_redeemed_amount -=reward_balance_before_redeem
                            r.update_used_reward_amount(reward_balance_before_redeem)
                            reward_balance_before_redeem = 0
                            
                        else:
                            logger.debug('__start_redeem: redeem remaining balance from redeem amount')
                            redeemed_amount = __total_redeemed_amount
                            r.update_used_reward_amount(__total_redeemed_amount)
                            reward_balance_before_redeem -= __total_redeemed_amount
                            __total_redeemed_amount = 0
                         
                        
                        logger.debug('__start_redeem: __total_redeemed_amount=%s',  __total_redeemed_amount)
                        logger.debug('__start_redeem: reward_balance_before_redeem after =%s',  reward_balance_before_redeem)
                        
                        transaction_id_list.append(r.transaction_id)
                    
                        #record customer CustomerPointReward/CustomerStampReward key and used_reward_amount
                        redeemed_items_list.append({
                                                    'key'      : r.key_in_str, 
                                                    'amount'   : redeemed_amount,
                                                    
                                                    })
                        
                        if __total_redeemed_amount<=0:
                            break
                    else:
                        logger.debug('__start_redeem reward balance is ZERO')
                
                logger.debug('after finished reading reward') 
                
                transaction_id_list = set(transaction_id_list) 
                for transaction_id in transaction_id_list:
                    CustomerTransaction.update_transaction_reward_have_been_redeemed(transaction_id, redeem_transaction_id)
                
                return (__total_redeemed_amount, next_cursor,  redeemed_items_list)
            else:
                raise Exception('Reward not found')
        
        if reward_format == program_conf.REWARD_FORMAT_POINT:
            total_redeemed_amount               = redeemed_amount
            cursor                              = None
            redeemed_reward_details_list        = [] 
            no_sufficient_to_redeem             = False
            while total_redeemed_amount>0:
                (total_redeemed_amount, cursor, __redeemed_reward_details_list) = __start_redeem(customer, total_redeemed_amount, cursor, 
                                                                                        CustomerPointReward)
                logger.debug('after __start_redeem total_redeemed_amount= %s, cursor=%s', total_redeemed_amount, cursor)
                logger.debug('__redeemed_reward_details_list count=%d', len(__redeemed_reward_details_list))
                if __redeemed_reward_details_list:
                    redeemed_reward_details_list.extend(__redeemed_reward_details_list)
                    
                if total_redeemed_amount>0 and cursor is None:
                    no_sufficient_to_redeem = True
                    break    
            
            if no_sufficient_to_redeem:
                raise Exception('No sufficient balance to redeem')    
            
            redeemed_summary = {
                                    reward_format               : {
                                        
                                                                    'amount'                    : redeemed_amount,        
                                                                    'customer_point_rewards'    : redeemed_reward_details_list
                                                                    }
                                    }
                
            reward_balance = reward_summary[reward_format]['amount'] - redeemed_amount
            if reward_balance<0:
                reward_balance = 0
                
            reward_summary[reward_format]['amount'] = reward_balance
        
        elif reward_format == program_conf.REWARD_FORMAT_STAMP:
            total_redeemed_amount           = redeemed_amount
            cursor                          = None
            redeemed_reward_details_list    = [] 
            no_sufficient_to_redeem         = False
            
            while total_redeemed_amount>0:
                (total_redeemed_amount, cursor, __redeemed_reward_details_list) = __start_redeem(customer, total_redeemed_amount, cursor, 
                                                                                        CustomerStampReward)
                
                logger.debug('after __start_redeem total_redeemed_amount= %s, cursor=%s', total_redeemed_amount, cursor)
                logger.debug('__redeemed_reward_details_list count=%d', len(__redeemed_reward_details_list))
                
                if __redeemed_reward_details_list:
                    redeemed_reward_details_list.extend(__redeemed_reward_details_list)
                    
                if total_redeemed_amount>0 and is_empty(cursor):
                    no_sufficient_to_redeem = True
                    logger.debug('suppose stop here')
                    break  
                else:
                    logger.warn('still continue')
                
            if no_sufficient_to_redeem:
                raise Exception('No sufficient balance to redeem')      
            
            redeemed_summary = {
                                reward_format               : {
                                
                                                            'amount'                    : redeemed_amount,        
                                                            'customer_stamp_rewards'    : redeemed_reward_details_list
                                                            }
                            
                            }
                
            reward_balance = reward_summary[reward_format]['amount'] - redeemed_amount
            if reward_balance<0:
                reward_balance = 0
                
            reward_summary[reward_format]['amount'] = reward_balance    
            
        elif reward_format == program_conf.REWARD_FORMAT_PREPAID:
            total_redeemed_amount           = redeemed_amount
            cursor                          = None
            redeemed_reward_details_list    = [] 
            no_sufficient_to_redeem         = False
            
            while total_redeemed_amount>0:
                (total_redeemed_amount, cursor, __redeemed_reward_details_list) = __start_redeem(customer, total_redeemed_amount, cursor, 
                                                                                        CustomerPrepaidReward)
                
                logger.debug('after __start_redeem total_redeemed_amount= %s, cursor=%s', total_redeemed_amount, cursor)
                logger.debug('__redeemed_reward_details_list count=%d', len(__redeemed_reward_details_list))
                
                if __redeemed_reward_details_list:
                    redeemed_reward_details_list.extend(__redeemed_reward_details_list)
                
                if total_redeemed_amount>0 and cursor is None:
                    no_sufficient_to_redeem = True
                    break 
            
            if no_sufficient_to_redeem:
                raise Exception('No sufficient balance to redeem')
            
            redeemed_summary = {
                                program_conf.REWARD_FORMAT_PREPAID: {
                                    
                                                                'amount'                    : redeemed_amount,        
                                                                'customer_prepaid_rewards'   : redeemed_reward_details_list
                                                                }
                                }
            
                
            reward_balance = prepaid_summary['amount'] - redeemed_amount
            if reward_balance<0:
                reward_balance = 0
                
            prepaid_summary['amount'] = reward_balance    
                                
            
        elif reward_format == program_conf.REWARD_FORMAT_VOUCHER:
            
            redeemed_voucher_details_dict = {
                                'vouchers': {}
                                }
            
            voucher_redeem_codes_list           = []
            transaction_id_list                 = []
            transaction_id_and_redeem_code_dict = {}
            voucher_count                       = 0
            
            for customer_entitled_voucher_key in redeemed_voucher_keys_list:
                customer_entitled_voucher           = CustomerEntitledVoucher.fetch(customer_entitled_voucher_key)
                merchant_voucher                    = customer_entitled_voucher.merchant_voucher_entity
                merchant_voucher_key                = customer_entitled_voucher.merchant_voucher_key
                redeem_code                         = customer_entitled_voucher.redeem_code
                effective_date                      = customer_entitled_voucher.effective_date
                expiry_date                         = customer_entitled_voucher.expiry_date
                redeemed_voucher_details            = redeemed_voucher_details_dict.get('vouchers').get(merchant_voucher_key)
                
                voucher_redeem_codes_list.append(redeem_code)
                voucher_count +=1
                
                if redeemed_voucher_details:
                    
                    redeemed_voucher_details_dict.get('vouchers')[merchant_voucher_key]['amount'] +=1
                    redeemed_voucher_details_dict.get('vouchers')[merchant_voucher_key]['customer_entitled_vouchers'].append({
                                                                                                                            'customer_entitled_voucher_key': customer_entitled_voucher_key,
                                                                                                                            'redeem_code': redeem_code,
                                                                                                                            })
                else:
                    redeemed_voucher_details_dict.get('vouchers')[merchant_voucher_key] = {
                                                                                    'label'                             : merchant_voucher.label,
                                                                                    'image_url'                         : merchant_voucher.image_public_url,
                                                                                    'amount'                            : 1,
                                                                                    'customer_entitled_vouchers'    : [
                                                                                                                        {
                                                                                                                        'customer_entitled_voucher_key': customer_entitled_voucher_key,
                                                                                                                        'redeem_code'   : redeem_code,
                                                                                                                        'effective_date': effective_date.strftime('%d-%m-%Y'),
                                                                                                                        'expired_date'  : expiry_date.strftime('%d-%m-%Y'),
                                                                                                                        }
                                                                                                                    ]
                                                                                }
                
                
                customer_entitled_voucher.redeem(redeemed_by, redeemed_datetime=redeemed_datetime)
                
                transaction_id_list.append(customer_entitled_voucher.transaction_id)
                
                if(transaction_id_and_redeem_code_dict.get(transaction_id)):
                    if transaction_id_and_redeem_code_dict[customer_entitled_voucher.transaction_id].get(merchant_voucher_key):
                        transaction_id_and_redeem_code_dict[customer_entitled_voucher.transaction_id][merchant_voucher_key].append(redeem_code)
                    else:
                        transaction_id_and_redeem_code_dict[customer_entitled_voucher.transaction_id]= {
                                                                                            merchant_voucher_key:[redeem_code]
                                                                                            }
                else:
                    transaction_id_and_redeem_code_dict[customer_entitled_voucher.transaction_id]= {
                                                                                            merchant_voucher_key:[redeem_code]
                                                                                            }
                
                logger.debug('Voucher(%s) have been redeemed', customer_entitled_voucher.redeem_code)
                
                
                
            #mark customer sales/reward transaction entitled voucher have been redeem. thus transaction is not allow to revert
            transaction_id_list = set(transaction_id_list) 
            for transaction_id, redeem_voucher_details_dict in transaction_id_and_redeem_code_dict.items():
                CustomerTransaction.update_transaction_reward_have_been_redeemed(transaction_id, redeem_transaction_id, redeem_voucher_details_dict=redeem_voucher_details_dict, )
            
            #update customer entitled voucher summary
            copied_entitled_voucher_summary = entitled_voucher_summary.copy()
            
            for v_k, v_info in  copied_entitled_voucher_summary.items():
                filtered_voucher_redeem_info_list = []
                
                for redeem_info in v_info.get('redeem_info_list'): 
                    if not redeem_info.get('redeem_code') in voucher_redeem_codes_list:
                        filtered_voucher_redeem_info_list.append(redeem_info)
                
                if filtered_voucher_redeem_info_list:
                    entitled_voucher_summary[v_k]['redeem_info_list'] = filtered_voucher_redeem_info_list
                else:
                    del entitled_voucher_summary[v_k]
            
            #redeemed_voucher_details_dict['customer_entitled_vouchers'] = redeemed_voucher_keys_list
            redeemed_voucher_details_dict['amount'] = voucher_count
            redeemed_summary = {
                                reward_format :   redeemed_voucher_details_dict
                                }
            
        customer_redemption = CustomerRedemption(
                                                    parent                      = customer.create_ndb_key(),
                                                    user_acct                   = customer.registered_user_acct.create_ndb_key(),
                                                    merchant_acct               = customer.registered_merchant_acct.create_ndb_key(),
                                                    redeemed_outlet             = redeemed_outlet.create_ndb_key(),
                                                    reward_format               = reward_format,
                                                    redeemed_amount             = redeemed_amount,
                                                    redeemed_summary            = redeemed_summary,
                                                    
                                                    transaction_id              = redeem_transaction_id,
                                                    invoice_id                  = invoice_id,
                                                    remarks                     = remarks,
                                                    
                                                    redeemed_by                 = redeemed_by.create_ndb_key(),
                                                    redeemed_by_username        = redeemed_by_username,
                                                    
                                                    redeemed_datetime           = redeemed_datetime,
                                                    is_tier_program_redemption  = is_tier_program_redemption,
                                                    tier_program_transaction_id = tier_program_transaction_id,
                                                    
                                                    )
        
        
        customer_redemption.put()
        
        customer.reward_summary             = reward_summary
        customer.entitled_voucher_summary   = entitled_voucher_summary
        customer.put()
        
        return customer_redemption
    
    @staticmethod
    def list_redemption_by_date(redeemed_date, redeemed_outlet=None, including_reverted_transaction=True, offset=0, limit=conf.PAGINATION_SIZE, start_cursor=None, return_with_cursor=False):
        
        redeemed_datetime           = datetime.combine(redeemed_date, datetime.min.time())
        next_day_redeemed_datetimee = redeemed_datetime + timedelta(days=1)
        
        logger.debug('redeemed_datetime=%s',redeemed_datetime)
        logger.debug('next_day_redeemed_datetimee=%s',next_day_redeemed_datetimee)
        
        if redeemed_outlet:
            if including_reverted_transaction:
                query = CustomerRedemption.query(ndb.AND(
                                    CustomerRedemption.redeemed_datetime  >= redeemed_datetime,
                                    CustomerRedemption.redeemed_datetime  <  next_day_redeemed_datetimee,
                                    CustomerRedemption.redeemed_outlet == redeemed_outlet.create_ndb_key(),
                                    )).order(-CustomerRedemption.redeemed_datetime)
            else:
                query = CustomerRedemption.query(ndb.AND(
                                    CustomerRedemption.redeemed_datetime  >= redeemed_datetime,
                                    CustomerRedemption.redeemed_datetime  <  next_day_redeemed_datetimee,
                                    CustomerRedemption.redeemed_outlet == redeemed_outlet.create_ndb_key(),
                                    CustomerRedemption.status == program_conf.REDEEM_STATUS_VALID,
                                    )).order(-CustomerRedemption.redeemed_datetime)
        else:
            if including_reverted_transaction:
                query = CustomerRedemption.query(ndb.AND(
                                    CustomerRedemption.redeemed_datetime  >= redeemed_datetime,
                                    CustomerRedemption.redeemed_datetime  <  next_day_redeemed_datetimee,
                                    )).order(-CustomerRedemption.redeemed_datetime)
            else:
                query = CustomerRedemption.query(ndb.AND(
                                    CustomerRedemption.redeemed_datetime  >= redeemed_datetime,
                                    CustomerRedemption.redeemed_datetime  <  next_day_redeemed_datetimee,
                                    CustomerRedemption.status == program_conf.REDEEM_STATUS_VALID,
                                    )).order(-CustomerRedemption.redeemed_datetime)
        
        return CustomerRedemption.list_all_with_condition_query(query, offset=offset, limit=limit, start_cursor=start_cursor, return_with_cursor=return_with_cursor)
    
    @staticmethod
    def count_redemption_by_date(transact_date, including_reverted_transaction=True, redeemed_outlet=None, limit=conf.MAX_FETCH_RECORD):
        
        redeemed_datetime           = datetime.combine(transact_date, datetime.min.time())
        next_day_redeemed_datetimee = redeemed_datetime + timedelta(days=1)
        
        logger.debug('redeemed_datetime=%s',redeemed_datetime)
        logger.debug('next_day_transact_datetime=%s',next_day_redeemed_datetimee)
        
        if redeemed_outlet:
            if including_reverted_transaction:
                query = CustomerRedemption.query(ndb.AND(
                                    CustomerRedemption.redeemed_datetime  >= redeemed_datetime,
                                    CustomerRedemption.redeemed_datetime  <  next_day_redeemed_datetimee,
                                    CustomerRedemption.redeemed_outlet == redeemed_outlet.create_ndb_key()
                                    ))
            else:
                query = CustomerRedemption.query(ndb.AND(
                                    CustomerRedemption.redeemed_datetime  >= redeemed_datetime,
                                    CustomerRedemption.redeemed_datetime  <  next_day_redeemed_datetimee,
                                    CustomerRedemption.redeemed_outlet == redeemed_outlet.create_ndb_key(),
                                    CustomerRedemption.status == program_conf.REDEEM_STATUS_VALID,
                                    ))
        else:
            if including_reverted_transaction:
                query = CustomerRedemption.query(ndb.AND(
                                    CustomerRedemption.redeemed_datetime  >= redeemed_datetime,
                                    CustomerRedemption.redeemed_datetime  <  next_day_redeemed_datetimee,
                                    ))
            else:
                query = CustomerRedemption.query(ndb.AND(
                                    CustomerRedemption.redeemed_datetime  >= redeemed_datetime,
                                    CustomerRedemption.redeemed_datetime  <  next_day_redeemed_datetimee,
                                    CustomerRedemption.status != program_conf.REDEEM_STATUS_REVERTED,
                                    ))
        
        return CustomerRedemption.count_with_condition_query(query, limit=limit)
    
    @staticmethod
    def delete_all_by_customer(customer_acct):
        query = CustomerRedemption.query(ancestor = customer_acct.create_ndb_key())
        CustomerRedemption.delete_multiples(query)
    
class RedemptionItemDetails(BaseNModel):
    transaction_id              = ndb.StringProperty(required=True)
        
    
    