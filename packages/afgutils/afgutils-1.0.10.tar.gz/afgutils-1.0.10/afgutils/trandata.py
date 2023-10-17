import random
from .db import DB, sql
from os import getenv
import requests
import string

trandata_auth_url = "https://api.trandata.io/account/unauth/v1/login"


# VARS INIT
# trandata_select_token_query = """
#         SELECT token from kr.token
#         WHERE created_at > now() - interval '23 HOURS'
#         ORDER BY created_at desc limit 1
#     """
#
# trandata_insert_token_query = """INSERT INTO kr.token(token) VALUES (?)"""
# trandata_lms_query = """
#     SELECT lar.client_id,
#     c.firstname AS client_firstname,
#     c.lastname AS client_lastname,
#     c.date_of_birth AS client_dob,
#     c.mobile_no AS client_mobile,
#     c.email_id AS client_email,
#     ci.document_key AS pan_number,
#     fd.firstname AS client_father_name,
#     ad.address_line_one AS client_res_address,
#     ad.district_name AS client_res_vilage,
#     ad.district_name AS client_res_city,
#     'xxx' AS client_res_state,
#     ad.postal_code AS client_res_pincode,
#     'vietnam' AS client_res_country,
#     bad.account_number AS client_bank_acc,
#     ci.document_key as national_id
#     FROM f_loan_application_reference lar
#     LEFT JOIN f_bank_account_detail_associations bada ON bada.entity_id = lar.client_id AND bada.entity_type_enum = 1
#     LEFT JOIN f_bank_account_details bad ON bad.id = bada.bank_account_detail_id  -- bank account
#     LEFT JOIN m_client c ON c.id = lar.client_id
#     LEFT JOIN m_client_identifier ci ON ci.client_id = c.id AND ci.document_type_id = 303
#     LEFT JOIN f_address_entity ae ON ae.entity_id = c.id AND ae.entity_type_enum =1 AND ae.address_type = 14
#     LEFT JOIN f_address ad ON ad.id = ae.address_id
#     LEFT JOIN f_family_details as fd ON fd.client_id = c.id AND fd.relationship_cv_id = 20
#     WHERE lar.loan_application_reference_no=? LIMIT 1
# """

# MAIN CODE

# SQLS



# FUNCS




# Trandata
def trandata_update_token():
    """
        Get log in and parse the Authentication Token.
        :return: token
    """

    rep_conn = DB.get_connection('repserv')
    rep_cursor = rep_conn.cursor()

    username = getenv("trandata_username")
    password = getenv("trandata_password")

    url = trandata_auth_url
    payload = "{\n    \"username\": \"" + username + "\",\n    \"password\": \"" + password + "\"\n}"
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if 300 > response.status_code >= 200:
        data = response.json()
        token = data["Data"]["sessionToken"]

        DB.execute(
            cursor=rep_cursor,
            query=sql("trandata_insert_token_query", 1),
            parameters=(token,)
        )

        rep_cursor.commit()
        rep_cursor.close()

        return token

    raise ValueError(response.text)


def trandata_get_token():
    rep_conn = DB.get_connection('repserv')
    rep_cursor = rep_conn.cursor()

    token_res = DB.execute(
        cursor=rep_cursor,
        query=sql("trandata_select_token_query", 1),
        fetch='one'
    )

    rep_cursor.close()

    if not token_res:
        token = trandata_update_token()

        return token

    return token_res["token"]


# print(trandata_get_token())

def trandata_gen_req_id(appl_ref):
    ran_text = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    result = appl_ref + "_" + ran_text
    return result

# def trandata_save2boto3(acc_key_id, sec_acc_key, region, response_text, bucket, key):
#     s3_client = boto3.client(
#         's3',
#         aws_access_key_id=acc_key_id,
#         aws_secret_access_key=sec_acc_key,
#         region_name=region
#     )
#     s3_client.put_object(
#         Bucket=bucket,
#         Body=response_text,
#         Key=key
#     )
