import datetime, requests
from pymongo import MongoClient


class ListOfBudgets:

    def __init__(self, host, offset):
        self.host = host
        self.offset = offset
        self.client = MongoClient('mongo_db_qabox', 27021)
        self.db = self.client.budgets
        self.budgets = self.db.budgets

    def get_latest_budgets(self):
        resp = requests.get(url=f'{self.host}?offset={self.offset}').json()
        return resp

    def get_latest_releases(self):
        budgets = self.get_latest_budgets()['data']
        list_of_tenders = []
        for ocid in budgets:
            list_of_tenders.append(ocid['ocid'])
        releases = []
        for release in list_of_tenders:
            release = requests.get(url=f'{self.host}/{release}').json()
            releases.append(release)
        return releases

    def write_releases_into_db(self):
        releases = self.get_latest_releases()
        for release in releases:
            for r in release['records']:
                # Record to FS table
                if "FS" in r['ocid']:
                    ocid = r['ocid']
                    cpid = r['compiledRelease']['relatedProcesses'][0]['identifier']
                    print(r['compiledRelease']['relatedProcesses'][0]['identifier'])
                    print(r['ocid'])
                    print(r)
                    self.budgets.insert_one(r)
                # Record to EI table
                else:
                    ocid = r['ocid']
                    cpid = r['ocid']
                    json_data = r
                    date = (datetime.datetime.now()).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        return 'Operation complete'

