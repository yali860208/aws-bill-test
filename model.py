# -*- coding: UTF-8 -*-

import psycopg2
import json
import pandas as pd
import sqlalchemy as db
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from datetime import datetime
import time

def sum_unblendedcost(usageaccountid):
    select_sum = '''SELECT product_productname, SUM(lineitem_unblendedcost)
        FROM all_product
        WHERE lineitem_usageaccountid = %s
        GROUP BY product_productname
        ORDER BY SUM(lineitem_unblendedcost) DESC;'''

    
    DATABASE_URL = 'postgres://gafrzkivzvfcce:7fe1abd49cdf07d783f051d0fa690a8209701008b05574a25cef7c87c38bf52c@ec2-54-156-60-12.compute-1.amazonaws.com:5432/d9sjmatvv5aimv'
    # return product and sum of cost for json
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    with conn:
        with conn.cursor() as cur:
            cur.execute(select_sum, (usageaccountid,))
            return_json = {}
            for i,j in cur.fetchall():
                j = '{:f}'.format(j)
                return_json[i] = j
            if len(return_json) == 0:
                return_json['error'] = 'not have this usage account ID'



    # save the pie figure
    img = io.BytesIO()
    df_prod = pd.read_sql(select_sum, con = conn,params = (usageaccountid,))
    OrRd_palette = sns.color_palette("OrRd")

    plt.switch_backend('agg')
    plt.figure(figsize = (5,5))
    plt.pie(df_prod['sum'],
            labels = df_prod['product_productname'],
            autopct = "%1.3f%%",
            pctdistance = 0.6,
            textprops = {"fontsize" : 8},
            colors = OrRd_palette
        )
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    result = {'json':return_json, 'image':plot_url}

    return result
        # return json.dumps(return_json, indent=4)



def sum_usageamount(usageaccountid):
    select_sum = '''SELECT product_productname,DATE(lineitem_usagestartdate),SUM(lineitem_usageamount)
        FROM all_product WHERE lineitem_usageaccountid=%s
       GROUP BY product_productname,DATE(lineitem_usagestartdate) ORDER BY product_productname,DATE(lineitem_usagestartdate);'''

    
    DATABASE_URL = 'postgres://gafrzkivzvfcce:7fe1abd49cdf07d783f051d0fa690a8209701008b05574a25cef7c87c38bf52c@ec2-54-156-60-12.compute-1.amazonaws.com:5432/d9sjmatvv5aimv'
    # return product and sum of cost for json
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    with conn:
        with conn.cursor() as cur:
            cur.execute(select_sum, (usageaccountid,))
            return_json = {}
            sub_json = {}
            a = None
            for i,j,k in cur.fetchall():
                s = datetime.strftime(j, '%Y-%m-%d')
                k = '{:f}'.format(k)
                if a != i and a != None:
                    sub_json = {}
                sub_json[s] = k
                return_json[i] = sub_json
                a = i
            if len(return_json) == 0:
                return_json['error'] = 'not have this usage account ID'
    return return_json

def sum_normusageamount(usageaccountid):
    select_sum = '''SELECT product_productname,DATE(lineitem_usagestartdate),SUM(lineitem_normalizedusageamount)
        FROM all_product WHERE lineitem_usageaccountid=%s
       GROUP BY product_productname,DATE(lineitem_usagestartdate) ORDER BY product_productname,DATE(lineitem_usagestartdate);'''

    
    DATABASE_URL = 'postgres://gafrzkivzvfcce:7fe1abd49cdf07d783f051d0fa690a8209701008b05574a25cef7c87c38bf52c@ec2-54-156-60-12.compute-1.amazonaws.com:5432/d9sjmatvv5aimv'
    # return product and sum of cost for json
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    with conn:
        with conn.cursor() as cur:
            cur.execute(select_sum, (usageaccountid,))
            return_json = {}
            sub_json = {}
            a = None   #判斷是不是同一個 product 的資料
            for i,j,k in cur.fetchall():
                if str(k)[0].isdigit() == True:
                    s = datetime.strftime(j, '%Y-%m-%d')
                    k = '{:f}'.format(k)
                    if a != i and a != None:
                        sub_json = {}
                    sub_json[s] = k
                    return_json[i] = sub_json
                    a = i
            if len(return_json) == 0:
                return_json['error'] = 'this usage account ID do not use product that need to pick instance size'
    return return_json

def product_amount(product, amount):
    result_json = amount[product]

    df = pd.DataFrame(list(result_json.items()),columns=['date', 'amount'])
    df['amount'] = df['amount'].astype('float')
    for ind,i in enumerate(df['date']):
        df['date'].iloc[ind] = i[5:]
        
    # save the pie figure
    img = io.BytesIO()
    OrRd_palette = sns.color_palette("OrRd")

    plt.switch_backend('agg')
    plt.figure(figsize = (0.5*len(df['date']),5))
    plt.title(product)
    plt.xticks(rotation=30)
    sns.barplot(x='date',y='amount',data=df)
    plt.savefig(img, format='png',bbox_inches='tight') # bbox_inches='tight':圖會被切到的時候
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    
    result = {'json':result_json, 'image':plot_url}

    return result

def sid_and_info(usageaccountid):
    select_sum = '''SELECT reservation_subscriptionid, product_productname, product_region, pricing_purchaseoption,
    product_licensemodel, pricing_leasecontractlength, pricing_offeringclass, lineitem_lineitemdescription, reservation_reservationarn
    FROM all_product WHERE lineitem_usageaccountid=%s AND pricing_term = 'Reserved' ORDER BY reservation_subscriptionid '''

    DATABASE_URL = 'postgres://gafrzkivzvfcce:7fe1abd49cdf07d783f051d0fa690a8209701008b05574a25cef7c87c38bf52c@ec2-54-156-60-12.compute-1.amazonaws.com:5432/d9sjmatvv5aimv'
    # return product and sum of cost for json
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    with conn:
        with conn.cursor() as cur:
            cur.execute(select_sum, (usageaccountid,))
            return_json = {}
            for a,b,c,d,e,f,g,h,i in cur.fetchall():
                sid = str(a)[:-2]
                sub_json = {}
                if sid not in return_json:
                    sub_json['Product Name'] = b
                    sub_json['Product Region'] = c
                    sub_json['Purchase Option'] = d
                    sub_json['License'] = e
                    sub_json['Time Length'] = f
                    sub_json['Offering Class'] = g
                    sub_json['Description'] = h
                    sub_json['Arn'] = i
                    return_json[sid] = sub_json
            if len(return_json) == 0:
                return_json['error'] = 'not have this usage account ID'

    return return_json

def sid_detail_info(sid):
    select = '''SELECT reservation_starttime, reservation_endtime, reservation_modificationstatus,
        reservation_numberofreservations, reservation_totalreservedunits,reservation_unusedamortizedupfrontfeeforbillingperiod,
        reservation_unusednormalizedunitquantity, reservation_unusedquantity, reservation_unusedrecurringfee, 
        reservation_upfrontvalue FROM all_product WHERE reservation_subscriptionid= %s AND lineitem_lineitemtype='RIFee' '''
    select1 = '''SELECT product_instancetype, COUNT(product_instancetype), SUM(lineitem_usageamount), SUM(reservation_effectivecost) 
        FROM all_product WHERE reservation_subscriptionid= %s AND lineitem_lineitemtype='DiscountedUsage' GROUP BY product_instancetype'''
    DATABASE_URL = 'postgres://gafrzkivzvfcce:7fe1abd49cdf07d783f051d0fa690a8209701008b05574a25cef7c87c38bf52c@ec2-54-156-60-12.compute-1.amazonaws.com:5432/d9sjmatvv5aimv'

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    with conn:
        with conn.cursor() as cur:
            cur.execute(select, (sid,))
            return_json = {}
            for a,b,c,d,e,f,g,h,i,j in cur.fetchall():
                a = datetime.strftime(a, '%Y-%m-%d %H:%M:%S')
                b = datetime.strftime(b, '%Y-%m-%d %H:%M:%S')
                return_json['Start Time'] = a
                return_json['End Time'] = b
                return_json['Modification Status'] = c
                return_json['Number Of Reservations'] = d
                return_json['Total Reserved Units'] = e
                return_json['Unused Amortized Upfront Fee For Billing Period'] = f
                return_json['Unused Normalized Unit Quantity'] = g
                return_json['Unused Quantity'] = h
                return_json['Unused Recurring Fee'] = i
                return_json['Upfront Value'] = j
    if len(return_json) == 0:
            return_json['error'] = 'Not Have This Subscription ID'
    # instance
    func = {
        "nano":0.25,
        "micro":0.5,
        "small":1,
        "medium":2,
        "large":4,
        "xlarge":8,
        "2xlarge":16,
        "4xlarge":32,
        "8xlarge":64,
        "10xlarge":80,
        "16xlarge":128,
        "32xlarge":256
    }
    conn1 = psycopg2.connect(DATABASE_URL, sslmode='require')
    df_prod = pd.read_sql(select1, con = conn1, params = (sid,))
    df_prod.columns =['instancetype','instancecount','amountsum','costsum']

    norm = []
    for ind, i in enumerate(df_prod['instancetype']):
        idx = i.find('.')
        instance = i[idx+1:]
        norm.append(df_prod['amountsum'][ind]*func[instance])
    df_prod['normamountsum'] = norm

    instancejson = {}
    for i in range(0,len(df_prod)):
        sub_json = {}
        sub_json['Instance Count'] = int(df_prod['instancecount'].iloc[i])
        sub_json['Amount Sum'] = float(df_prod['amountsum'].iloc[i])
        sub_json['Normalized Amount Sum'] = float(df_prod['normamountsum'].iloc[i])
        sub_json['Cost Sum'] = float(df_prod['costsum'].iloc[i])
        instancejson[df_prod['instancetype'].iloc[i]] = sub_json

    # unused
    cost = return_json['Unused Amortized Upfront Fee For Billing Period'] + return_json['Unused Recurring Fee']
    df_prod=df_prod.append({'instancetype' : 'Unused' , 'instancecount' : 0, 'amountsum' : 0,'normamountsum':0,'costsum':cost} , ignore_index=True)
    
    # pie
    img = io.BytesIO()
    OrRd_palette = sns.color_palette("OrRd")

    plt.switch_backend('agg')
    plt.figure(figsize = (5,5))
    plt.pie(df_prod['costsum'],
            labels = df_prod['instancetype'],
            autopct = "%1.3f%%",
            pctdistance = 0.6,
            textprops = {"fontsize" : 8},
            colors = OrRd_palette
        )
    plt.title('cost propotion of the instance type')
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    result = {'info':return_json, 'instance':instancejson, 'plot':plot_url}

    return result