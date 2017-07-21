import pymongo
from bson.objectid import ObjectId

koi_db = pymongo.MongoClient()['wcbp']

versions_coll = koi_db['versions']


UNKNOWN = 'unknown'

UNSUPPORTED = 999999

UNSUPPORTED_NAME = '暂不支持'

IGNORED = -1


def retrieve_ios_versions(with_unsupported=True):
    ios_versions_unsorted = list()
    for v in versions_coll.find({'platform': 'ios'}):
        ios_versions_unsorted.append({'code': v['code'], 'name': v['name'], 'oid': str(v['_id'])})

    ios_versions = sorted(ios_versions_unsorted, key=lambda x: int(x.get('code')))
    if with_unsupported:
        ios_versions.append({'code': str(UNSUPPORTED), 'name': UNSUPPORTED_NAME})
    return ios_versions


def retrieve_android_versions(with_unsupported=True):
    android_versions_unsorted = list()
    for v in versions_coll.find({'platform': 'android'}):
        android_versions_unsorted.append({'code': v['code'], 'name': v['name'], 'oid': str(v['_id'])})

    android_versions = sorted(android_versions_unsorted, key=lambda x: int(x.get('code')))
    if with_unsupported:
        android_versions.append({'code': str(UNSUPPORTED), 'name': UNSUPPORTED_NAME})
    return android_versions


def get_ios_version_dict():
    ios_versions = retrieve_ios_versions()
    return {v.get('code'): v.get('name') for v in ios_versions}


def get_android_version_dict():
    android_versions = retrieve_android_versions()
    return {v.get('code'): v.get('name') for v in android_versions}


def delete_by_id(_id):
    object_id = ObjectId(_id)
    versions_coll.delete_one({'_id': object_id})


def modify_by_id(_id, platform=None, code=None, name=None):
    object_id = ObjectId() if _id is None else ObjectId(_id)
    versions_coll.update_one({'_id': object_id}, {'$set': {'platform': platform, 'code': code, 'name': name}}, upsert=True)


def modify_by_platform_and_name(platform=None, code=None, name=None):
    versions_coll.update_one({'platform': platform, 'name': name}, {'$set': {'code': code}}, upsert=True)


def get_version_name_by_platform_and_code(platform, code):
    if code == str(UNSUPPORTED):
        return UNSUPPORTED_NAME
    version = versions_coll.find_one({'platform': platform, 'code': code})
    return UNKNOWN if version is None else version.get('name')


def get_android_version_name_by_code(code):
    return get_version_name_by_platform_and_code(platform='android', code=code)


def get_ios_version_name_by_code(code):
    return get_version_name_by_platform_and_code(platform='ios', code=code)
