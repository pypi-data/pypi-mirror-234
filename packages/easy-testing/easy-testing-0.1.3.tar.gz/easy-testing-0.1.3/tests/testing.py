import sys
import os
import re
import boto3
from botocore.exceptions import ClientError
from gcloud_connectors.bigquery import BigQueryConnector
import fitz
import orjson
import google
import json
from dotenv import load_dotenv
load_dotenv('easytesting/.env')

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from easytesting.metrics.randomscore import RandomMetric
from easytesting.metrics.min_question_number_check import MinQuestionNumberCheck
from easytesting.metrics.max_question_number_check import MaxQuestionNumberCheck
from easytesting.test_case import DeterministicTestCase
from easytesting.run_test import assert_test

s3_client = boto3.client("s3")
ENVIRONMENT = 'test'
os.environ[
    'GOOGLE_APPLICATION_CREDENTIALS'] = '{current_working_directory}/confs/google_cloud_storage_service_account.json'.format(
    current_working_directory=os.getcwd())

def get_document_text(doc_data, document_aws_bucket=''):
    file_path = doc_data["file_path"]

    temp_file_path = "temporary_file.pdf"
    if doc_data.get("bucket"):
        bucket = doc_data.get("bucket")
    else:
        bucket = document_aws_bucket
    s3_client.download_file(
        Bucket=bucket, Key=file_path, Filename=temp_file_path
    )

    pdf_document = fitz.open(temp_file_path)

    text = ''
    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        page_text = page.get_text("text", flags=16)
        page_text = page_text.replace('"', "'")
        page_text = re.sub(r"\n\s*\n", "\n", page_text)
        text += page_text

    return text

def read_bq(bq_service, base_query):
    df = bq_service.pd_execute(
        base_query, progress_bar_type=None, bqstorage_enabled=False
    )
    return df

def get_document_data():
    bq_service = BigQueryConnector(project_id="data-lake-265016")

    query = f"""select CAST(id AS INT) as id, slug, upload_date, 
    CONCAT('documents/original/',REGEXP_REPLACE(file_path, r'\.[^.]*$', ''),'.pdf') as file_path, 
    'docsity-data' as bucket, 
    lang, 'DOCSITY' as document_type,
    CONCAT('da_ml_ai_on_doc_to_quiz_output/lang=',lang,'/y=',y,'/m=',m,'/d=',CAST(EXTRACT(DAY from upload_date) as string),'/upload_date=',cast(upload_date as string),'/doc_',CAST(id AS INT),'.json') as quiz_path, 
    from `data-lake-265016.prod_db_dataset.da_db_documents`
    where id in (8404140,7901476)
        """

    df = read_bq(bq_service=bq_service, base_query=query)

    doc_data = df.to_dict(orient="records")
    return doc_data

def get_json_data_as_dict_from_bucket(path, slug=None):
    try:
        content_object = s3_client.get_object(Bucket='docsity-ai-develop', Key=path)
        json_data = orjson.loads(content_object["Body"].read().decode("utf-8"))
        if slug is not None and json_data.get("slug") is None:
            json_data["slug"] = slug
        return json_data
    except google.api_core.exceptions.NotFound:
        return None
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            return None
        else:
            raise e

def random_test():
    random_metric = RandomMetric(minimum_score=0.7)
    test_case = DeterministicTestCase(input=0, output=5)
    test_result = assert_test(test_case, [random_metric])
    print(test_result)

def quiz_test(document_length, questions_and_answer):
    min_question_number_metric = MinQuestionNumberCheck(minimum_score=0.5)
    max_question_number_metric = MaxQuestionNumberCheck(maximum_score=1.5)
    test_case = DeterministicTestCase(input=document_length, output=questions_and_answer)
    try:
        test_result = assert_test(test_case, [min_question_number_metric, max_question_number_metric])
        print(test_result)
        test_result_list = []
        for item in test_result:
            result_dict = {
                "metric": item.metric_name,
                "score": item.score
            }
            test_result_list.append(result_dict)

        return {"test": "success", "scores": test_result_list}
    except AssertionError as e:
        print(str(e))
        return {"test": "failed", "error_message": str(e)}


doc_data = get_document_data()
for doc in doc_data:
    doc['upload_date'] = doc['upload_date'].strftime('%Y-%m-%d')
    text = get_document_text(doc_data=doc)
    document_length = len(text)
    doc['document_length'] = document_length
    json_data = get_json_data_as_dict_from_bucket(path=doc['quiz_path'], slug=None)
    questions_and_answer = len(json_data.get('question_answers'))
    doc['questions_and_answer'] = questions_and_answer
    print(f"Quiz for doc {doc['id']}: document_length={document_length} and questions_and_answer={questions_and_answer}")
    doc['test_result'] = quiz_test(document_length=document_length, questions_and_answer=questions_and_answer)

# how was the test?
success_count = 0
failed_count = 0
for item in doc_data:
    test_result = item.get('test_result', {})
    test_status = test_result.get('test', '')

    if test_status == 'success':
        success_count += 1
    elif test_status == 'failed':
        failed_count += 1

print(f"Success: {success_count}/{len(doc_data)}")
print(f"Failed: {failed_count}/{len(doc_data)}")

import ipdb;ipdb.set_trace()

json_file_path = "tests/output/testing_output.json"
with open(json_file_path, 'w') as json_file:
    json.dump(doc_data, json_file)