'''
 Asign id with value from userid, and if userid is None, try snsid, fpid, user_id in order.
'''
id = next((item for item in [data_dict.get('userid', None),
                             data_dict.get('snsid', None),
                             data_dict.get('fpid', None),
                             data_dict.get('user_id', None)] if item), None)
