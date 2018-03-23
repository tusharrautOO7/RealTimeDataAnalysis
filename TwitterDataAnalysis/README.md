This is the example of real time data stream from twitter and load it into elasticsearch.

1. Add twitter consumer key & secrets, token and secrets into scripts.

2. Run following command to install pre-requisites:
pip install -r requirement.txt

3. Install elasticsearch and kibana. If you are using x-pack then add elastic user and password into twitter_smanalysis.py while creating
connection object.
For x-pack: es = Elasticsearch(["localhost"], http_auth=('elastic', 'xxxx')) # change host, user & password
Normal Connection : es = Elasticsearch()
3. Once all required modules are in place change keys and secrets in script.

4. Run the following command to start streaming of data:
python twitter_smanalysis.py

5. Open kibana in browser http://localhost:5601 and create index sentiment in kibana, then click on discover to see incoming data.

