from flask import Flask, render_template, request, session
import model
import json

app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/static" )
app.secret_key="okokhahaha"

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/cost')
def cost_page():
    uid = request.args.get("uid","")
    result = model.sum_unblendedcost(uid)
    js_print = json.dumps(result['json'], indent=4)
    img_print = result['image']
    return render_template('cost.html', data= {'json':js_print,'img':img_print})

@app.route('/amount')
def amount_page():
    uid_am = request.args.get("uid_am","")

    result = model.sum_usageamount(uid_am)
    session['amount']=result
    json_am = json.dumps(result, indent=4)

    result_no = model.sum_normusageamount(uid_am)
    json_no = json.dumps(result_no, indent=4)

    return render_template('amount.html', data_am = {"json_am":json_am, "json_no":json_no})


@app.route('/amountproduct')
def amount_product():
    uid_pro = request.args.get("uid_pro","")
    amount = session['amount']
    result = model.product_amount(uid_pro, amount)
    json_pro = json.dumps(result['json'], indent=4)
    img_pro = result['image']

    return render_template('amountproduct.html', data_pro = {'json':json_pro,'img':img_pro})

@app.route('/risid')
def search_sid():
    uid_sid = request.args.get("uid_sid","")
    result = model.sid_and_info(uid_sid)
    json_sid = json.dumps(result, indent=4)

    return render_template('risid.html', data_sid = json_sid)

@app.route('/risidinfo')
def sid_info():
    sid = request.args.get("sid_info","")
    result = model.sid_detail_info(sid)
    info = json.dumps(result['info'], indent=4)
    instance = json.dumps(result['instance'], indent=4)
    plot = result['plot']

    return render_template('risidinfo.html', data = {'info':info, 'instance':instance, 'plot':plot})

if __name__=="__main__":
    app.run()