from pi_httpx import Pi

cookie = "__Host-session=YpgTjHoXWNr8fdtuscY8E; amp_6e403e=vQZL0cfaDB8ovCClharDf-...1had699ue.1had699ue.0.0.0; __cf_bm=68qGScHFq_d3wv25NT9GKwgdzwGz4o..54dUgSvcUTc-1694807407-0-ASIdg9Wecf6ITJrT78T+8iNyrFwwWx46gcfL3m/QnfQL3k6PNx9Noeq0GsmvT4iBtsiBZmHaSN1sOK0iT4EG9Mc="
prompt = "How are you?"

chatbot = Pi(cookie, proxy=True)

response = chatbot.send_message(prompt)

print(response)
