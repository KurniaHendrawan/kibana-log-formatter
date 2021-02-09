import collections
import json
from log import transform_log

logs = [
    "2020-12-22 15:46:47 ERROR actions Error attempting to reconnect to 12.345.67.891:2345, scheduling retry in 217.6 seconds: [Errno 111] Tried connecting to [('12.345.67.891', 2345)]. Last error: Connection refused",
    "2020-12-22 15:46:47 ERROR actions Error attempting to reconnect to 12.345.67.891:2345, scheduling retry in 136.96 seconds: [Errno 111] Tried connecting to [('12.345.67.891', 2345)]. Last error: Connection refused",
    "2020-12-22 15:46:47 ERROR actions Error attempting to reconnect to 12.345.67.891:2345, scheduling retry in 66.56 seconds: [Errno 111] Tried connecting to [('12.345.67.891', 2345)]. Last error: Connection refused",
    "2020-12-22 15:46:47 INFO root - Rasa server is up and running.",
    "2020-12-22 15:46:47 INFO rasa-core - Error XY",
    "2021-01-25 08:51:06.599263: E tensorflow/stream_executor/cuda/cuda_driver.cc:351] failed call to cuInit: UNKNOWN ERROR (303)",
    "2022-01-25 18:51:06.599263: E tensorflow/stream_executor/cuda/cuda_driver.cc:351] failed call to cuInit: UNKNOWN ERROR (303)",
    '2022-01-25 18:51:06.599263: Error Servlet.service() for servlet [dispatcherServlet] in context with path [] threw exception [Request processing failed; nested exception is org.springframework.web.client.ResourceAccessException: I/O error on POST request for "http://prod-chatbot-rasa-kug.marathon.l4lb.thisdcos.directory:8080/webhooks/rest/webhook": Connection refused (Connection refused); nested exception is java.net.ConnectException: Connection refused (Connection refused)] with root cause',
    '2022-01-25 18:51:06.599263: Error Servlet.service() for servlet [dispatcherServlet] in context with path [] threw exception [Request processing failed; nested exception is org.springframework.web.client.ResourceAccessException: I/O error on POST request for "http://prod-chatbot-rasa-kug.marathon.l4lb.thisdcos.directory:8080/webhooks/rest/webhook": Unexpected end of file from server; nested exception is java.net.SocketException: Unexpected end of file from server] with root cause',
    '2022-01-25 18:51:06.599263: Error Servlet.service() Exception Processing ErrorPage[errorCode=0, location=/error]',
    '2022-01-25 18:51:06.599263: Error Servlet.service() Bot-ID is missing from the request headers',
    "2022-01-25 18:51:06.599263: Error Servlet.service() for servlet [dispatcherServlet] in context with path [] threw exception [Request processing failed; nested exception is org.springframework.data.cassandra.CassandraReadTimeoutException: Query; CQL [SELECT * FROM sessions WHERE conversationid=a59ea9e2-b32a-4f60-b5ce-eb8d7f849ce6;]; Cassandra timeout during read query at consistency LOCAL_QUORUM (2 responses were required but only 1 replica responded); nested exception is com.datastax.driver.core.exceptions.ReadTimeoutException: Cassandra timeout during read query at consistency LOCAL_QUORUM (2 responses were required but only 1 replica responded)] with root cause",
    "2021-01-25 11:27:24 ERROR actions - <class 'IndexError'>",
    "2021-01-25 11:27:24 ERROR actions - Error",
    "2020-01-25 00:27:01 ERROR rasa.core.tracker_store - Error happened when trying to save conversation tracker to 'CustomSQLTrackerStore'. Falling back to use the 'InMemoryTrackerStore'. Please investigate the following error: (pymysql.err.OperationalError) (2013, 'Lost connection to MySQL server during query ([Errno 104] Connection reset by peer)') [SQL: SELECT events.id AS events_id, events.sender_id AS events_sender_id, events.type_name AS events_type_name, events.timestamp AS events_timestamp, events.intent_name AS events_intent_name, events.action_name AS events_action_name, events.data AS events_data",
    "2019-01-25 01:00:00 ERROR rasa.core.tracker_store - Error happened when trying to save conversation tracker to 'CustomSQLTrackerStore'. Falling back to use the 'InMemoryTrackerStore'. Please investigate the following error: (pymysql.err.OperationalError) (2006, \"MySQL server has gone away (ConnectionResetError(104, 'Connection reset by peer'))\")",
    "2019-01-25 01:00:00 ERROR actions Unexpected end of file from server; nested exception is java.net.SocketException: Unexpected end of file from server] with root cause",
    "Connection refused (Connection refused); nested exception is java.net.ConnectException: Connection refused (Connection refused)] with root cause",
]

result = collections.defaultdict(list)
for log in [transform_log("myContext", entry) for entry in logs]:
    print(log)
    lev_distance = json.loads(log)["message"]["levenshtein"]
    result[lev_distance].append(json.loads(log)["message"]["msg"])
for k, v in result.items():
    print(k)
    for item in v:
        print(item)
    print("\n")
