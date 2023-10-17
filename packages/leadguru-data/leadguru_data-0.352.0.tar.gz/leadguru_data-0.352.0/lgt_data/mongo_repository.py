import os
import re
from typing import List, Optional
import pymongo
from dateutil import tz
from pymongo import MongoClient
from bson.objectid import ObjectId
from .model import (LeadModel, BaseModel, UserModel, UserResetPasswordModel, BotModel, BoardModel, BoardedStatus,
                    DedicatedBotModel, SlackMemberInformation, UserTemplateModel, LinkedinContact,
                    ExtendedUserLeadModel, UserLeadModel, ExtendedLeadModel, UserContact)
from datetime import datetime
from collections import OrderedDict

client = MongoClient(os.environ.get('MONGO_CONNECTION_STRING', 'mongodb://127.0.0.1:27017/'))


def to_object_id(oid):
    if isinstance(oid, ObjectId):
        return oid
    return ObjectId(oid)


class BaseMongoRepository:
    collection_name = ''
    database_name = 'lgt_admin'
    model: BaseModel = BaseModel()

    def collection(self):
        return client[self.database_name][self.collection_name]

    def _collection(self, collection_name):
        return client[self.database_name][collection_name]

    def insert_many(self, items):
        insert_items = map(lambda x: x.to_dic(), items)
        self.collection().insert_many(insert_items)

    def insert(self, item: BaseModel):
        return self.collection().insert_one(item.to_dic())

    def add(self, item: BaseModel):
        return self.insert(item)

    def delete(self, id):
        res = self.collection().delete_one({'_id': to_object_id(id)})
        return res


class BotMongoRepository(BaseMongoRepository):
    pass

    collection_name = 'bots'
    model = BotModel

    def get_by_object_id(self, _id):
        return BotModel.from_dic(self.collection().find_one({"_id": to_object_id(_id)}))

    def get_by_source_id(self, source_id: str):
        return BotModel.from_dic(self.collection().find_one({'source.source_id': source_id}))

    def add_or_update(self, bot: BotModel):
        update_response = self.collection().update_one({'source.source_id': bot.source.source_id},
                                                       {'$set': bot.to_dic()}, upsert=True)
        bot.id = update_response.upserted_id if update_response.upserted_id else bot.id
        return bot

    def get(self, **kwargs) -> [BotModel]:
        pipeline = {}
        user_name = kwargs.get('user_name')

        if user_name:
            pipeline['user_name'] = user_name

        return [BotModel.from_dic(doc) for doc in self.collection().find(pipeline)]

    def delete_by_source_id(self, source_id: str):
        self.collection().delete_many({'source.source_id': source_id})


class UserMongoRepository(BaseMongoRepository):
    collection_name = 'users'
    model = UserModel

    def get(self, _id):
        return UserModel.from_dic(self.collection().find_one({'_id': to_object_id(_id)}))

    def get_by_email(self, email: str):
        pipeline = {'email': email}
        doc = self.collection().find_one(pipeline)
        return UserModel.from_dic(doc)

    def set(self, _id, **kwargs):
        update_dict = {k: v for k, v in kwargs.items() if v is not None}
        self.collection().update_one({'_id': to_object_id(_id)}, {'$set': update_dict})

    def get_users(self, users_ids=None, include_inactive=False):
        pipeline = {}

        if users_ids is not None:
            pipeline['_id'] = {'$in': [to_object_id(_id) for _id in users_ids]}

        if not include_inactive:
            pipeline['inactive'] = False

        return [UserModel.from_dic(doc) for doc in self.collection().find(pipeline)]


class UserLeadMongoRepository(BaseMongoRepository):
    collection_name = 'user_leads'
    model = ExtendedUserLeadModel

    def get_count(self, user_id, **kwargs):
        pipeline = self.__create_leads_filter(user_id, **kwargs)
        return self.collection().count_documents(pipeline)

    def get_many(self, ids: list, user_id):
        docs = self.collection().find({"id": {'$in': ids}, 'user_id': to_object_id(user_id)})
        leads = [ExtendedUserLeadModel.from_dic(lead) for lead in docs]
        senders = [lead.message.sender_id for lead in leads]
        contacts = SlackContactUserRepository().find(user_id, users=senders)
        for lead in leads:
            lead.contact = next(filter(lambda x: x.sender_id == lead.message.sender_id, contacts), None)

        return leads

    def get_leads(self, user_id, skip: int, limit: int, **kwargs) -> List[ExtendedUserLeadModel]:
        pipeline = self.__create_leads_filter(user_id, **kwargs)
        sort_field = kwargs.get('sort_field', 'last_action_at')
        sort_direction = kwargs.get('sort_direction', 'ASCENDING')
        sort_direction = pymongo.ASCENDING if sort_direction == 'ASCENDING' else pymongo.DESCENDING
        docs = list(self.collection().find(pipeline).sort([(sort_field, sort_direction)]).skip(skip).limit(limit))
        leads = [ExtendedUserLeadModel.from_dic(x) for x in docs]
        senders = [lead.message.sender_id for lead in leads]
        contacts = SlackContactUserRepository().find(users=senders)
        for lead in leads:
            lead.contact = next(filter(lambda x: x.sender_id == lead.message.sender_id, contacts), None)
        return leads

    @staticmethod
    def __create_leads_filter(user_id, **kwargs):
        pipeline: dict = {'user_id': to_object_id(user_id)}

        if kwargs.get('status') is not None:
            pipeline['status'] = kwargs.get('status', '')

        if kwargs.get('board_id'):
            pipeline['board_id'] = to_object_id(kwargs.get('board_id'))
        elif kwargs.get('board_id') is not None:
            pipeline['$or'] = [{'board_id': ''}, {'board_id': None}]

        archived = kwargs.get('archived')
        from_date = kwargs.get('from_date')
        to_date = kwargs.get('to_date')
        has_followup = kwargs.get('has_followup', None)
        followup_to = kwargs.get('followup_to_date', None)
        followup_from = kwargs.get('followup_from_date', None)
        created_to = kwargs.get('created_to_date', None)
        created_from = kwargs.get('created_from_date', None)
        sender_ids = kwargs.get('sender_ids', None)
        text = kwargs.get('text', None)
        stop_words = kwargs.get('stop_words', None)
        tags = kwargs.get('tags', None)
        configs = kwargs.get('config', None)
        bots_names = kwargs.get('bots_names', None)
        locations = kwargs.get('locations', None)
        dedicated_bots_ids = kwargs.get('dedicated_bots_ids', None)
        with_chat = kwargs.get('with_chat', None)
        leads_ids = kwargs.get('leads_ids', None)
        exclude_leads = kwargs.get('exclude_leads', None)
        exclude_senders = kwargs.get('exclude_senders', None)

        pipeline['message.profile.display_name'] = {
            "$ne": "Slackbot"
        }

        if leads_ids is not None:
            pipeline["id"] = {'$in': leads_ids}

        if exclude_leads:
            pipeline['id'] = {'$nin': exclude_leads}

        if exclude_senders:
            pipeline['message.sender_id'] = {'$nin': exclude_senders}

        if archived is not None:
            pipeline['archived'] = archived

        if with_chat is not None:
            pipeline['chat_history'] = {'$exists': True, '$ne': []}

        if has_followup is not None:
            pipeline['followup_date'] = {'$ne': None} if has_followup else {'$eq': None}

        if from_date or to_date:
            pipeline['last_action_at'] = {}

        if from_date:
            start = datetime(from_date.year, from_date.month, from_date.day, tzinfo=tz.tzutc())
            pipeline['last_action_at']['$gte'] = start

        if to_date:
            end = datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59, tzinfo=tz.tzutc())
            pipeline['last_action_at']['$lte'] = end

        if locations and len(locations) > 0:
            pipeline['message.locations'] = {"$in": locations}

        if sender_ids:
            pipeline['message.sender_id'] = {'$in': sender_ids}

        if followup_from or followup_to:
            pipeline['followup_date'] = {}

        if followup_from:
            followup_from = datetime(followup_from.year, followup_from.month, followup_from.day, tzinfo=tz.tzutc())
            pipeline['followup_date']['$gte'] = followup_from

        if followup_to:
            followup_to = datetime(followup_to.year, followup_to.month, followup_to.day, 23, 59, 59, tzinfo=tz.tzutc())
            pipeline['followup_date']['$lte'] = followup_to

        if created_to or created_from:
            pipeline['created_at'] = {}

        if created_to:
            created_to = datetime(created_to.year, created_to.month, created_to.day, 23, 59, 59, tzinfo=tz.tzutc())
            pipeline['created_at']['$lte'] = created_to

        if created_from:
            created_from = datetime(created_from.year, created_from.month, created_from.day, tzinfo=tz.tzutc())
            pipeline['created_at']['$gte'] = created_from

        if stop_words:
            pipeline['full_message_text'] = {'$regex': f'^(?!.*({stop_words})).*$', '$options': 'i'}
        elif text:
            pipeline['$text'] = {'$search': text}

        if tags:
            pipeline["tags"] = {"$elemMatch": {"$in": tags}}

        if configs:
            pipeline["message.configs.id"] = {"$in": configs}

        if bots_names is not None:
            pipeline['message.name'] = {'$in': bots_names}

        if dedicated_bots_ids is not None:
            pipeline["message.dedicated_slack_options.bot_id"] = {"$in": dedicated_bots_ids}
        return pipeline

    def get_unanswered_leads_ids(self, user_id: str, from_date=None):
        pipeline = [
            {
                '$match':
                    {
                        'user_id': to_object_id(user_id)
                    }
            },
            {
                '$match':
                    {
                        'chat_history': {'$exists': True, '$not': {'$size': 0}}
                    }
            },
            {
                '$project':
                    {
                        'id': 1,
                        'sender_id': "$message.sender_id",
                        'last_message': {'$arrayElemAt': ['$chat_history', 0]}
                    }
            },
            {
                '$addFields':
                    {
                        'is_user_message': {'$ne': ['$sender_id', '$last_message.user']}
                    }
            },
            {
                '$match':
                    {
                        '$and':
                            [
                                {'last_message.text': {'$regex': '\\?'}},
                                {'is_user_message': False}
                            ]
                    }
            }
        ]

        if from_date:
            beginning_of_the_day = datetime(from_date.year, from_date.month, from_date.day, 0, 0, 0, 0)
            pipeline.insert(0, {"$match": {"created_at": {"$gte": beginning_of_the_day}}})

        data = list(self.collection().aggregate(pipeline))
        leads_ids = [item['id'] for item in data]
        return leads_ids

    def get_daily_analytics_by_workspace(self, user_configs: list,
                                         dedicated_only: bool | None,
                                         from_date: datetime,
                                         to_date: datetime,
                                         user_id: str):
        pipeline = [
            {
                '$addFields': {
                    'dedicated': {
                        '$anyElementTrue': {
                            '$map': {
                                'input': "$message.configs.id",
                                'as': "config",
                                'in': {'$in': ["$$config", user_configs]}
                            }
                        }
                    }
                }
            },
            {
                '$project': {
                    'created_at': {
                        '$dateToString': {
                            'format': '%Y-%m-%d',
                            'date': '$created_at'
                        }
                    },
                    'id': '$id'
                }
            },
            {
                '$group': {
                    '_id': '$created_at',
                    'data': {'$push': '$id'}
                }
            },
            {
                '$sort': {'_id': 1}
            }
        ]

        if dedicated_only:
            pipeline.insert(1, {"$match": {'dedicated': True}})
        elif dedicated_only is False:
            pipeline.insert(1, {"$match": {'dedicated': False}})

        if from_date:
            beginning_of_the_day = datetime(from_date.year, from_date.month, from_date.day, 0, 0, 0, 0)
            pipeline.insert(0, {"$match": {"created_at": {"$gte": beginning_of_the_day}}})

        if to_date:
            end_of_the_day = datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59, 999)
            pipeline.insert(0, {"$match": {"created_at": {"$lte": end_of_the_day}}})

        if user_id:
            pipeline.insert(0, {"$match": {'user_id': to_object_id(user_id)}})

        saved_messages = list(self.collection().aggregate(pipeline))
        saved_messages_dic = OrderedDict()

        for item in saved_messages:
            saved_messages_dic[item["_id"]] = item["data"]

        return saved_messages_dic

    def get_leads_after(self, action_after: datetime) -> [ExtendedUserLeadModel]:
        leads = self.collection().find({'last_action_at': {'$gte': action_after}})
        return [ExtendedUserLeadModel.from_dic(lead) for lead in leads]

    def add_lead(self, user_id, lead: UserLeadModel) -> None:
        if not lead.created_at:
            lead.created_at = datetime.utcnow()

        if hasattr(lead, "_id"):
            lead._id = ObjectId()

        lead.user_id = user_id
        self.insert(lead)

    def update_lead(self, user_id, lead_id: str, **kwargs):
        pipeline = {'user_id': to_object_id(user_id), 'id': lead_id}
        update_dict = {k: v for k, v in kwargs.items() if v is not None}
        if 'board_id' in update_dict:
            update_dict['board_id'] = to_object_id(update_dict['board_id']) if len(update_dict['board_id']) == 24 \
                else update_dict['board_id']
        self.collection().update_one(pipeline, {'$set': update_dict})

        return ExtendedUserLeadModel.from_dic(self.collection().find_one(pipeline))

    def update_same_leads(self, user_id, sender_id: str, **kwargs):
        pipeline = {'user_id': to_object_id(user_id), 'message.sender_id': sender_id}
        update_dict = {k: v for k, v in kwargs.items() if v is not None}
        self.collection().update_many(pipeline, {'$set': update_dict})

    def update_leads_order(self, user_id, lead_ids: [str]):
        pipeline = {'user_id': to_object_id(user_id), 'id': {'$in': lead_ids}}
        docs = list(self.collection().find(pipeline))

        order = 0
        for lead_id in lead_ids:
            for doc in docs:
                if doc['id'] == lead_id:
                    self.collection().update_one({'id': lead_id}, {'$set': {'order': order}}, upsert=False)
                    order = order + 1

    def delete_lead(self, user_id, lead_id: str):
        """

        :param user_id:
        :param lead_id:
        :return: UserLeadModel
        """

        pipeline = {'user_id': to_object_id(user_id), 'id': lead_id}
        self.collection().delete_one(pipeline)

    def get_lead(self, user_id, message_id: str = None, lead_id: str = None, **kwargs):
        """

        :param user_id:
        :param message_id:
        :param lead_id:
        :return: UserLeadModel
        """

        pipeline = {'user_id': to_object_id(user_id)}
        sender_id = kwargs.get('sender_id')

        if message_id:
            pipeline['message.message_id'] = message_id

        if lead_id:
            pipeline['id'] = lead_id

        if sender_id:
            pipeline['message.sender_id'] = sender_id

        return ExtendedUserLeadModel.from_dic(self.collection().find_one(pipeline))


class UserResetPasswordMongoRepository(BaseMongoRepository):
    pass

    collection_name = 'user_reset_passwords'
    model = UserResetPasswordModel

    def get(self, _id):
        return UserResetPasswordModel.from_dic(self.collection().find_one({'_id': to_object_id(_id)}))

    def delete(self, email):
        self.collection().delete_many({'email': email})

    def add(self, email) -> str:
        model = UserResetPasswordModel()
        model.email = email
        return self.collection().insert_one({'email': email}).inserted_id


class LeadMongoRepository(BaseMongoRepository):
    pass

    database_name = 'lgt_admin'
    collection_name = 'general_leads'
    model = LeadModel

    def delete(self, _id):
        res = self.collection().delete_one({'id': _id})
        return res

    def get(self, _id=None, **kwargs):
        pipeline = {}
        timestamp = kwargs.get("timestamp")
        message_id = kwargs.get("message_id")
        channel_id = kwargs.get("channel_id")
        if _id:
            pipeline['id'] = _id
        if message_id:
            pipeline['message.message_id'] = message_id
        if channel_id:
            pipeline['message.channel_id'] = channel_id
        if timestamp:
            pipeline['message.timestamp'] = timestamp
        result = self.collection().find_one(pipeline)
        if not result:
            return None

        return LeadModel.from_dic(result)

    def get_many(self, ids: list):
        docs = self.collection().find({"id": {'$in': ids}})
        leads = [ExtendedLeadModel.from_dic(lead) for lead in docs]
        senders = [lead.message.sender_id for lead in leads]
        contacts = SlackContactUserRepository().find(users=senders)
        for lead in leads:
            lead.contact = next(filter(lambda x: x.sender_id == lead.message.sender_id, contacts), None)

        return leads

    def get_by_sender_id(self, sender_id, exclude_leads: [str], skip: int, limit: int):
        pipeline = {'message.sender_id': sender_id, 'id': {'$nin': exclude_leads}}
        leads = self.collection().find(pipeline).sort([('created_at', pymongo.DESCENDING)]).skip(skip).limit(limit)
        return [LeadModel.from_dic(lead) for lead in leads]

    def get_by_message_id(self, message_id):
        """

        :rtype: LeadModel
        :param message_id:
        """
        doc = self.collection().find_one({'message.message_id': message_id})
        if not doc:
            return None

        return LeadModel.from_dic(doc)

    def update(self, _id: str, **kwargs):
        update_dict = {k: v for k, v in kwargs.items() if v is not None}
        self.collection().update_one({'id': _id}, {'$set': update_dict}, upsert=False)

    def get_count(self, **kwargs):
        pipeline = self.__create_leads_filter(**kwargs)
        return self.collection().count_documents(pipeline)

    def get_list(self, skip, limit, **kwargs):
        pipeline = self.__create_leads_filter(**kwargs)

        sort_field = kwargs.get('sort_field', 'created_at')
        sort_direction = kwargs.get('sort_direction', 'ASCENDING')
        sort_direction = pymongo.ASCENDING if sort_direction == 'ASCENDING' else pymongo.DESCENDING

        leads = self.collection().find(pipeline).sort([(sort_field, sort_direction)]).skip(skip).limit(limit)
        return [LeadModel.from_dic(lead) for lead in leads]

    def __create_leads_filter(self, **kwargs):
        pipeline: dict = {"hidden": False}

        from_date: datetime = kwargs.get('from_date')
        to_date: datetime = kwargs.get('to_date')

        country = kwargs.get('country', None)
        user_id = kwargs.get('user_id', None)
        tags = kwargs.get('tags', None)
        text = kwargs.get('text', None)
        stop_words = kwargs.get('stop_words', None)
        exclude_leads = kwargs.get('exclude_leads', None)
        exclude_senders = kwargs.get('exclude_senders', None)
        excluded_channels = kwargs.get('excluded_channels', None)
        sender_ids = kwargs.get('sender_ids', None)
        configs = kwargs.get('config', None)
        bots_names = kwargs.get('bots_names', None)
        locations = kwargs.get('locations', None)

        pipeline['message.profile.display_name'] = {
            "$ne": "Slackbot"
        }

        if from_date or to_date:
            pipeline['created_at'] = {}

        if from_date:
            start = from_date.astimezone(tz.tzutc())
            pipeline['created_at']['$gte'] = start

        if to_date:
            end = to_date.astimezone(tz.tzutc())
            pipeline['created_at']['$lte'] = end

        if locations and len(locations) > 0:
            pipeline['message.locations'] = {"$in": locations}

        if country:
            pipeline["message.slack_options.country"] = re.compile(country, re.IGNORECASE)

        if user_id:
            pipeline["$or"] = [
                {"message.dedicated_slack_options": {"$exists": False}},
                {"message.dedicated_slack_options": None},
                {"message.dedicated_slack_options.user_id": f"{user_id}"},
            ]
        else:
            pipeline["user_id"] = {'$exists': False}

        if stop_words:
            pipeline['full_message_text'] = {'$regex': f'^(?!.*({stop_words})).*$', '$options': 'i'}
        elif text:
            pipeline['$text'] = {'$search': text}

        if tags:
            pipeline["tags"] = {"$elemMatch": {"$in": tags}}

        if exclude_leads:
            pipeline['id'] = {'$nin': exclude_leads}

        if exclude_senders:
            pipeline['message.sender_id'] = {'$nin': exclude_senders}

        if excluded_channels:
            pipeline['$and'] = []
            for ws, channels in excluded_channels.items():
                if channels is not None:
                    pipeline['$and'].append(
                        {'$or': [{'message.name': {'$ne': ws}}, {'message.channel_id': {'$nin': channels}}]})

        if sender_ids:
            pipeline['message.sender_id'] = {'$in': sender_ids}

        if configs:
            pipeline["message.configs.id"] = {"$not": {"$elemMatch": {"$nin": configs}}}

        if bots_names is not None:
            pipeline['message.name'] = {'$in': bots_names}

        pipeline['message.profile.real_name'] = {'$ne': 'Slackbot'}

        return pipeline

    def get_per_day(self, date: datetime):
        start_day = datetime(date.year, date.month, date.day, 0, 0, 0, tzinfo=tz.tzutc())
        end_day = datetime(date.year, date.month, date.day, 23, 59, 59, tzinfo=tz.tzutc())
        docs = self.collection().find({'created_at': {'$gte': start_day, '$lte': end_day}}).sort('created_at', 1)
        return [LeadModel.from_dic(x) for x in docs]


class SpamLeadsMongoRepository(LeadMongoRepository):
    pass

    def __init__(self):
        self.collection_name = 'spam_leads'

    def get_list(self, skip, limit, sort_field: str = 'created_at', sort_direction: str = 'ASCENDING', **kwargs):
        pipeline = self.__create_leads_filter(**kwargs)
        sort_direction = pymongo.ASCENDING if sort_direction == 'ASCENDING' else pymongo.DESCENDING
        docs = self.collection().find(pipeline).sort([(sort_field, sort_direction)]).skip(skip).limit(limit)
        leads = [ExtendedLeadModel.from_dic(doc) for doc in docs]
        senders = [lead.message.sender_id for lead in leads]
        contacts = SlackContactUserRepository().find(users=senders)
        for lead in leads:
            lead.contact = next(filter(lambda x: x.sender_id == lead.message.sender_id, contacts), None)
        return leads

    def get_count(self, **kwargs):
        pipeline = self.__create_leads_filter(**kwargs)
        return self.collection().count_documents(pipeline)

    def __create_leads_filter(self, **kwargs):
        pipeline = {"user_id": {'$exists': False}}
        text = kwargs.get('text', None)
        stop_words = kwargs.get('stop_words', None)
        if stop_words:
            pipeline['full_message_text'] = {'$regex': f'^(?!.*({stop_words})).*$', '$options': 'i'}
        elif text:
            pipeline['$text'] = {'$search': text}

        return pipeline


class GarbageLeadsMongoRepository(SpamLeadsMongoRepository):
    pass

    def __init__(self):
        self.collection_name = 'garbage_leads'


class GarbageUserLeadsMongoRepository(UserLeadMongoRepository):
    pass

    def __init__(self):
        self.database_name = 'lgt_admin'
        self.collection_name = 'garbage_leads'


class SpamUserLeadsMongoRepository(UserLeadMongoRepository):
    pass

    def __init__(self):
        self.database_name = 'lgt_admin'
        self.collection_name = 'spam_leads'


class BoardsMongoRepository(BaseMongoRepository):
    pass

    collection_name = 'boards'
    model = BoardModel

    def create_board(self, user_id: str, name: str, **kwargs):
        is_primary = kwargs.get('is_primary', False)

        if is_primary:
            primary_board = self.collection().find_one({'user_id': to_object_id(user_id), 'is_primary': is_primary})
            if primary_board:
                return BoardModel.from_dic(primary_board)

        board = BoardModel()
        board.name = name
        board.created_at = datetime.utcnow()
        board.user_id = to_object_id(user_id)
        board.is_primary = is_primary
        self.collection().insert_one(BoardModel.to_dic(board))

        return BoardModel.from_dic(self.collection().find_one({'user_id': to_object_id(user_id), 'name': name}))

    def add_default_statuses(self, user_id: str, board_id: str):
        pipeline = {'user_id': to_object_id(user_id), '_id': to_object_id(board_id)}
        board = BoardModel.from_dic(self.collection().find_one(pipeline))

        if not board:
            return None

        board.statuses.append(BoardedStatus().from_dic({'name': 'Lead', 'order': 0}))
        board.statuses.append(BoardedStatus().from_dic({'name': 'Prospect', 'order': 1}))
        board.statuses.append(BoardedStatus().from_dic({'name': 'Opportunity', 'order': 2}))
        board.statuses.append(BoardedStatus().from_dic({'name': 'Call', 'order': 3}))
        board.statuses.append(BoardedStatus().from_dic({'name': 'Contract', 'order': 4}))
        board.statuses.append(BoardedStatus().from_dic({'name': 'Refused', 'order': 5}))

        return self.update_board(user_id, board_id, statuses=board.statuses)

    def get(self, user_id: str, **kwargs):
        pipeline = {'user_id': to_object_id(user_id)}
        is_primary = kwargs.get('is_primary')
        name = kwargs.get('name')

        if is_primary is not None:
            pipeline['is_primary'] = is_primary

        if name:
            pipeline['name'] = name

        docs = self.collection().find(pipeline).sort('created_at', 1)
        return [BoardModel.from_dic(doc) for doc in docs]

    def get_primary(self, user_id: str):
        return BoardModel.from_dic(self.collection().find_one({'user_id': to_object_id(user_id), 'is_primary': True}))

    def get_by_id(self, id: str):
        return BoardModel.from_dic(self.collection().find_one({'_id': to_object_id(id)}))

    def delete_by_id(self, id: str):
        return self.collection().delete_many({'_id': to_object_id(id)})

    def update_board(self, user_id, board_id: str, **kwargs):
        pipeline = {'user_id': to_object_id(user_id), '_id': to_object_id(board_id)}

        if kwargs.get('statuses'):
            kwargs['statuses'] = [status.to_dic() for status in kwargs.get('statuses')
                                  if isinstance(status, BoardedStatus)]

        doc = BoardModel.from_dic(self.collection().find_one(pipeline))
        if not doc:
            return None

        update_dict = {k: v for k, v in kwargs.items() if v is not None}
        self.collection().update_one(pipeline, {'$set': update_dict})

        self._collection('user_leads').update_many({'user_id': to_object_id(user_id), 'board_id': to_object_id(doc.id)},
                                                   {'$set': {'board_id': to_object_id(board_id)}})

        return BoardModel.from_dic(self.collection().find_one(pipeline))


class DedicatedBotRepository(BaseMongoRepository):
    pass

    collection_name = 'dedicated_bots'

    def get_by_user_and_source_id(self, user_id: str, source_id: str) -> Optional[DedicatedBotModel]:
        doc = self.collection().find_one({"user_id": ObjectId(f"{user_id}"), "source.source_id": source_id})
        return DedicatedBotModel.from_dic(doc)

    def add_or_update(self, bot: DedicatedBotModel):
        update_response = self.collection().update_one({"source.source_id": bot.source.source_id,
                                                        "user_id": to_object_id(bot.user_id)},
                                                       {'$set': bot.to_dic()}, upsert=True)
        bot.id = update_response.upserted_id if update_response.upserted_id else bot.id
        return bot

    def get_all(self, only_valid: bool = False, **kwargs) -> List[DedicatedBotModel]:
        kwargs["only_valid"] = only_valid
        pipeline = self.__create_bots_filter(**kwargs)
        docs = self.collection().find(pipeline)
        return [DedicatedBotModel.from_dic(doc) for doc in docs]

    def get_one(self, **kwargs):
        pipeline = self.__create_bots_filter(**kwargs)
        return DedicatedBotModel.from_dic(self.collection().find_one(pipeline))

    def get_user_bots(self, user_id: str, only_valid: bool = False,
                      include_deleted: bool = False, include_paused: bool = False, **kwargs) -> List[DedicatedBotModel]:
        pipeline = {'user_id': to_object_id(user_id)}
        user_name = kwargs.get('user_name')

        if user_name:
            pipeline['user_name'] = user_name

        if not include_deleted:
            pipeline['deleted'] = False

        if not include_paused:
            pipeline['paused'] = False

        if only_valid:
            pipeline['invalid_creds'] = False

        return [DedicatedBotModel.from_dic(doc) for doc in self.collection().find(pipeline)]

    def delete(self, _id: str):
        self.collection().update_one({'_id': to_object_id(f"{_id}")}, {"$set": {"deleted": True}})

    @staticmethod
    def __create_bots_filter(**kwargs):
        pipeline = {}
        name = kwargs.get('name')
        source_type = kwargs.get('source_type')
        user_name = kwargs.get('user_name')
        only_valid = kwargs.get('only_valid')
        include_paused = kwargs.get('include_paused', False)
        include_deleted = kwargs.get('include_deleted', False)
        bot_id = kwargs.get('id')
        user_id = kwargs.get('user_id')
        source_id = kwargs.get('source_id')

        if bot_id:
            pipeline["_id"] = to_object_id(bot_id)

        if user_id:
            pipeline["user_id"] = to_object_id(user_id)

        if name:
            pipeline["name"] = name

        if source_type:
            pipeline["type"] = source_type

        if user_name:
            pipeline["user_name"] = user_name

        if source_id:
            pipeline["source.source_id"] = source_id

        if only_valid:
            pipeline['invalid_creds'] = False

        if not include_deleted:
            pipeline['deleted'] = False

        if not include_paused:
            pipeline['paused'] = False

        return pipeline


class SlackContactUserRepository(BaseMongoRepository):
    collection_name = "slack_contact"
    model = SlackMemberInformation

    def find(self, text: Optional[str] = None, skip: int = 0, limit: int = 1000, **kwargs):
        pipeline = {}

        users = kwargs.pop("users")
        presence_updated_at = kwargs.pop("online_updated_at", None)
        if text:
            pipeline['$text'] = {'$search': text}

        if users:
            pipeline['sender_id'] = {'$in': users}

        if presence_updated_at:
            pipeline['online_updated_at'] = {'$gte': presence_updated_at}

        pipeline = {**pipeline, **kwargs}

        docs = self.collection().find(pipeline).sort([("real_name", pymongo.ASCENDING)]) \
            .skip(skip) \
            .limit(limit)
        return [SlackMemberInformation.from_dic(doc) for doc in docs]

    def find_one(self, user_id: str):
        pipeline = {"sender_id": user_id}
        return SlackMemberInformation.from_dic(self.collection().find_one(pipeline))

    def get_count_in_workspaces(self):
        pipeline = [
            {
                '$match': {
                    'user': {
                        '$ne': 'USLACKBOT'
                    }
                }
            }, {
                '$group': {
                    '_id': '$workspace',
                    'count': {
                        '$sum': 1
                    }
                }
            }
        ]
        docs = list(self.collection().aggregate(pipeline))
        return {doc['_id']: doc['count'] for doc in docs}


class UserTemplatesRepository(BaseMongoRepository):
    collection_name = "user_templates"
    model = UserTemplateModel

    def get_all(self, user_id: str):
        return [UserTemplateModel.from_dic(doc) for doc in self.collection().find({'user_id': to_object_id(user_id)})]

    def get(self, id: str):
        return UserTemplateModel.from_dic(self.collection().find_one({'_id': to_object_id(id)}))

    def create_or_update(self, template: UserTemplateModel):
        result = self.collection().update_one(
            {"_id": to_object_id(template.id)},
            {'$set': template.to_dic()},
            upsert=True)

        if result.upserted_id:
            template.id = result.upserted_id

        return template

    def delete_by_id(self, id: str):
        return self.collection().find_one_and_delete({'_id': to_object_id(id)})


class LinkedinContactRepository(BaseMongoRepository):
    collection_name = "linkedin_contact"
    model = LinkedinContact

    def find(self, **kwargs):
        docs = self.collection().find({**kwargs})
        return [LinkedinContact.from_dic(doc) for doc in docs]


class UserContactsRepository(BaseMongoRepository):
    collection_name = 'user_contacts'

    def find(self, user_id: str, **kwargs):
        pipeline = {'user_id': to_object_id(user_id)}

        users = kwargs.get('users')
        spam = kwargs.get('spam')
        if users:
            pipeline['sender_id'] = {'$in': users}

        if spam is not None:
            pipeline['spam'] = spam

        docs = self.collection().find(pipeline)
        return [UserContact.from_dic(doc) for doc in docs]

    def find_one(self, user_id: str, **kwargs):
        pipeline = {'user_id': to_object_id(user_id)}

        sender_id = kwargs.get('sender_id')
        if sender_id:
            pipeline['sender_id'] = sender_id

        return UserContact.from_dic(self.collection().find_one(pipeline))

    def update(self, user_id: str, sender_id: str, **kwargs):
        pipeline = {'user_id': to_object_id(user_id), 'sender_id': sender_id}
        update_dict = {k: v for k, v in kwargs.items() if v is not None}
        self.collection().update_one(pipeline, {'$set': update_dict}, upsert=False)
