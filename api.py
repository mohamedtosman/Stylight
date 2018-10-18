import datetime as dt
import json

from flask import Flask, jsonify, request


class TransactionsSearch:
    """
    Class used to handle file processing and use other classes' API to determine final product price
    """

    def __init__(self, filename):
        self.filename = filename
        self.transactions = []
        self.total = {}
        self.populateTransactionsArray()
        
    def populateTransactionsArray(self):
        """
        Populate transactions list with json objects read in from the passed in file.
        In our case "transactions.json"
        """
        try:
            with open(self.filename) as f:
                for line in f:
                    self.transactions.append(json.loads(line))
            return True
        except EnvironmentError:
            return False

    def checkIfTransactionsPopulated(self):
        """
        Check if transactions array is filled out by reading the passed in file successfully
        """
        if not self.transactions:
            return False
        return True

    def getTotal(self):
        """
        Get total product price by grouping city and status into a tuple as a key
        and the value would be the aggregated product price
        """
        self.total.clear()
        for t in self.transactions:
            city = ip_range_search.get_city(t["ip"])
            status = user_status_search.get_status(t["user_id"], t["created_at"])
            price = t["product_price"]

            if (city, status) not in self.total:
                self.total[(city, status)] = price
            else:
                self.total[(city, status)] += price
        return(self.total)

class UserStatusSearch:

    RECORDS = [
        {'user_id': 1, 'created_at': '2017-01-01T10:00:00', 'status': 'paying'},
        {'user_id': 1, 'created_at': '2017-03-01T19:00:00', 'status': 'paying'},
        {'user_id': 1, 'created_at': '2017-02-01T12:00:00', 'status': 'cancelled'},
        {'user_id': 3, 'created_at': '2017-10-01T10:00:00', 'status': 'paying'},
        {'user_id': 3, 'created_at': '2016-02-01T05:00:00', 'status': 'cancelled'},
    ]

    def __init__(self):
        self.RECORDS = UserStatusSearch.RECORDS

    def get_status(self, user_id, date):
        """
        Return status of user by searching RECORDS for user_id and time of creation
        """
        for record in self.RECORDS:
            if record['user_id']==user_id and record['created_at']==str(date):
                return record['status']
        return "non-paying"


class IpRangeSearch:

    RANGES = {
        'london': [
            {'start': '10.10.0.0', 'end': '10.10.255.255'},
            {'start': '192.168.1.0', 'end': '192.168.1.255'},
        ],
        'munich': [
            {'start': '10.12.0.0', 'end': '10.12.255.255'},
            {'start': '172.16.10.0', 'end': '172.16.11.255'},
            {'start': '192.168.2.0', 'end': '192.168.2.255'},
        ]
    }

    def __init__(self):
        self.RANGES = IpRangeSearch.RANGES

    def get_city(self, ip):
        """
        Get city using passed in IP by comparing start and end ranges
        """
        validIpCounter = 0
        for city, ranges in self.RANGES.items():
            for range in ranges:
                min_ip = [int(i) for i in range['start'].split('.')]
                max_ip = [int(i) for i in range['end'].split('.')]
                IP = [int(i) for i in ip.split('.')]

                for ind, val in enumerate(IP):
                    if val < min_ip[ind] or val > max_ip[ind]:
                        break
                    else:
                        validIpCounter+=1

                    if validIpCounter==4:
                        return city

                validIpCounter=0
        return "unknown"

app = Flask(__name__)
user_status_search = UserStatusSearch()
ip_range_search = IpRangeSearch()
transaction_search = TransactionsSearch("transactions.json")

@app.route('/user_status/<user_id>')
def user_status(user_id):
    """
    Return user status for a give date

    /user_status/1?date=2017-10-10T10:00:00
    """
    date = str(request.args.get('date'))

    return jsonify({'user_status': user_status_search.get_status(int(user_id), date)})


@app.route('/ip_city/<ip>')
def ip_city(ip):
    """
    Return city for a given ip

    /ip_city/10.0.0.0
    """
    return jsonify({'city': ip_range_search.get_city(ip)})

@app.route('/total_price')
def total_price():
    """
    Return product price grouped by status and city

    /total_price
    """
    if transaction_search.checkIfTransactionsPopulated():
        output = [{'city and status':k, 'total price': v} for k, v in transaction_search.getTotal().items()]
        return json.dumps(output)
    return str("Failed to parse file. Please make sure to pass in correct file name")

if __name__ == '__main__':
    app.run(host='127.0.0.1')
