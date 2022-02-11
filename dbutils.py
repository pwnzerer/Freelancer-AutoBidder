from dbconnection import connect_to_collection
from bson import ObjectId


jobs_collection = connect_to_collection('jobs_collection')


def save_jobs_to_db(jobs_array):
    for job in jobs_array:
        data = {'url': job['url'], 'title': job['title'], 'job_type': job['upgrades'], 'country': job['country'], 'search_term': job['search_term'], 'description': job['description'], 'score': job['score'], 'proposal_sent': False, 'project_open': True, 'project_restricted': False}
        jobs_collection.update_one({'url': job['url']}, {'$set': data}, upsert=True)


def get_pending_jobs():
    jobs = jobs_collection.find({'proposal_sent': False, 'project_open': True, 'project_restricted': False})
    return jobs


def update_status_of_job(project_id):
    oid = ObjectId(project_id)
    jobs_collection.update_one({'_id': oid}, {'$set': {'proposal_sent': True}})


def update_project_open_status(project_id):
    oid = ObjectId(project_id)
    jobs_collection.update_one({'_id': oid}, {'$set': {'project_open': False}})


def update_project_restricted_status(project_id):
    oid = ObjectId(project_id)
    jobs_collection.update_one({'_id': oid}, {'$set': {'project_restricted': True}})

