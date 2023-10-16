'''
Created on 21 Sep 2023

@author: jacklok
'''
from datetime import datetime

from dateutil.relativedelta import relativedelta
from trexlib.utils.string_util import is_not_empty

import logging
from trexmodel import program_conf
from trexmodel.models.datastore.reward_models import CustomerEntitledVoucher
from trexmodel.models.datastore.voucher_models import MerchantVoucher


logger = logging.getLogger('debug')

def is_customer_entitled_voucher_within_limit(customer, merchant_voucher, redeem_count):
    
    redeem_limit_type   = merchant_voucher.redeem_limit_type
    redeem_limit_count  = merchant_voucher.redeem_limit_count
    
    logger.debug('is_customer_entitled_voucher_within_limit debug: redeem_limit_type=%s', redeem_limit_type)
    logger.debug('is_customer_entitled_voucher_within_limit debug: redeem_limit_count=%d', redeem_limit_count)
    
    if program_conf.REDEEM_LIMIT_TYPE_PER_RECEIPT == redeem_limit_type:
        return redeem_count<=redeem_limit_count
    else:
    
        passed_redeemed_datetime = None
        now = datetime.utcnow()
        if program_conf.REDEEM_LIMIT_TYPE_PER_DAY == redeem_limit_type:
            passed_redeemed_datetime = now - relativedelta(days=1)
    
        elif program_conf.REDEEM_LIMIT_TYPE_PER_WEEK == redeem_limit_type:
            passed_redeemed_datetime = now - relativedelta(weeks=1)
            
        elif program_conf.REDEEM_LIMIT_TYPE_PER_MONTH == redeem_limit_type:
            passed_redeemed_datetime = now - relativedelta(months=1)
            
        redeemed_count = CustomerEntitledVoucher.count_redeemed_by_merchant_voucher_and_passed_redeemed_datetime(customer, merchant_voucher, passed_redeemed_datetime)
        
        return (redeem_count + redeemed_count) <=redeem_limit_count
'''
def check_redeem_voucher_for_redeem_limit(customer, customer_vouchers_list):
    merchant_voucher_key_and_customer_voucher_list_dict     = {}
    over_redeem_limit_merchant_voucher_list                 = []
    
    
    for customer_voucher in customer_vouchers_list:
        customer_voucher_list = merchant_voucher_key_and_customer_voucher_list_dict.get(customer_voucher.merchant_voucher_key)
        if customer_voucher_list is None:
            merchant_voucher_key_and_customer_voucher_list_dict[customer_voucher.merchant_voucher_key] = [customer_voucher]
        else:
            customer_voucher_list.append(customer_voucher)
    
    for merchant_voucher_key, voucher_list in merchant_voucher_key_and_customer_voucher_list_dict.items():
        merchant_voucher = MerchantVoucher.fetch(merchant_voucher_key)
        total_customer_voucher_to_redeem_count = len(voucher_list)
        
        is_within_limit = is_customer_entitled_voucher_within_limit(customer, merchant_voucher, total_customer_voucher_to_redeem_count)
        logger.debug('%s is_within_limit=%s', merchant_voucher.label, is_within_limit)
        if is_within_limit==False:
            over_redeem_limit_merchant_voucher_list.append(merchant_voucher)
    
    if is_not_empty(over_redeem_limit_merchant_voucher_list):
        voucher_label_list = []
        for merchant_voucher in over_redeem_limit_merchant_voucher_list:
            voucher_label_list.append(merchant_voucher.label)
            
        raise Exception("Voucher ({voucher_label_list}) have reach redeem limit,  thus it is not allow to redeem again".format(voucher_label_list=",".join(voucher_label_list)))
'''    
def check_redeem_voucher_is_valid(customer, customer_vouchers_list, redeem_datetime=None):
    merchant_voucher_key_and_customer_voucher_list_dict     = {}
    over_redeem_limit_merchant_voucher_list                 = []
    already_redeemed_redeem_codes_list                      = []
    not_effective_to_redeem_redeem_codes_list               = []
    expired_to_redeem_redeem_codes_list                     = []
    
    if redeem_datetime is None:
        redeem_datetime = datetime.utcnow().date()
    else:
        redeem_datetime = redeem_datetime.date()
    
    for customer_voucher in customer_vouchers_list:
        if customer_voucher.is_valid_to_redeem == False:
            already_redeemed_redeem_codes_list.append(customer_voucher.redeem_code)
            
        elif customer_voucher.is_effective_to_redeem(checking_datetime=redeem_datetime) == False:
            not_effective_to_redeem_redeem_codes_list.append(customer_voucher.redeem_code)
            
        elif customer_voucher.is_not_expired_to_redeem(checking_datetime=redeem_datetime) == False:    
            expired_to_redeem_redeem_codes_list.append(customer_voucher.redeem_code)
            
        else:
            
            customer_voucher_list = merchant_voucher_key_and_customer_voucher_list_dict.get(customer_voucher.merchant_voucher_key)
            if customer_voucher_list is None:
                merchant_voucher_key_and_customer_voucher_list_dict[customer_voucher.merchant_voucher_key] = [customer_voucher]
            else:
                customer_voucher_list.append(customer_voucher)
    
    if is_not_empty(already_redeemed_redeem_codes_list):
        redeem_codes_list = []
        for redeem_code in already_redeemed_redeem_codes_list:
            redeem_codes_list.append(redeem_code)
            
        raise Exception("Voucher ({redeem_codes_list}) is used before".format(redeem_codes_list=",".join(redeem_codes_list)))
    
    elif is_not_empty(not_effective_to_redeem_redeem_codes_list):
        redeem_codes_list = []
        for redeem_code in not_effective_to_redeem_redeem_codes_list:
            redeem_codes_list.append(redeem_code)
            
        raise Exception("Voucher ({redeem_codes_list}) is not effective to use yet".format(redeem_codes_list=",".join(redeem_codes_list)))
    
    elif is_not_empty(expired_to_redeem_redeem_codes_list):
        redeem_codes_list = []
        for redeem_code in expired_to_redeem_redeem_codes_list:
            redeem_codes_list.append(redeem_code)
            
        raise Exception("Voucher ({redeem_codes_list}) is expired".format(redeem_codes_list=",".join(redeem_codes_list)))
    
    
    for merchant_voucher_key, voucher_list in merchant_voucher_key_and_customer_voucher_list_dict.items():
        merchant_voucher = MerchantVoucher.fetch(merchant_voucher_key)
        total_customer_voucher_to_redeem_count = len(voucher_list)
        
        is_within_limit = is_customer_entitled_voucher_within_limit(customer, merchant_voucher, total_customer_voucher_to_redeem_count)
        logger.debug('%s is_within_limit=%s', merchant_voucher.label, is_within_limit)
        if is_within_limit==False:
            over_redeem_limit_merchant_voucher_list.append(merchant_voucher)
            
    
    if is_not_empty(over_redeem_limit_merchant_voucher_list):
        voucher_label_list = []
        for merchant_voucher in over_redeem_limit_merchant_voucher_list:
            voucher_label_list.append(merchant_voucher.label)
            
        raise Exception("Voucher ({voucher_label_list}) have reach redeem limit,  thus it is not allow to redeem again".format(voucher_label_list=",".join(voucher_label_list)))

    
