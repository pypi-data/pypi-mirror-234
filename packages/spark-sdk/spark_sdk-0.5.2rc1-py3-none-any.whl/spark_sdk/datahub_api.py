import requests

# Tagging
def addTag(full_table_name, tag):
    url = 'http://gms.datahub.bigdata.local/api/graphql/'
    query = """
    mutation addTag {
        addTag(input: { tagUrn: "urn:li:tag:"""+tag+"""",
          resourceUrn: "urn:li:dataset:(urn:li:dataPlatform:hive,"""+full_table_name+""",PROD)" })
    }
    """
    cookies={''}
    json={'query': query}
    headers = {'X-DataHub-Actor': 'urn:li:corpuser:datahub'}

    r = requests.post(url, headers=headers, json=json)
    print('Add tag', full_table_name)
    if 'errors' in r.json().keys():
        print(r.text)


def queryTag(full_table_name):
    url = 'http://gms.datahub.bigdata.local/api/graphql/'
    query = """
    query {
      dataset(urn: "urn:li:dataset:(urn:li:dataPlatform:hive,"""+full_table_name+""",PROD)") {
        tags {
          tags {
            tag {
              name
            }
          }
        }
      }
    }
    """
    cookies={''}
    json={'query': query}
    headers = {'X-DataHub-Actor': 'urn:li:corpuser:datahub'}

    r = requests.post(url, headers=headers, json=json)
    print('Query', full_table_name)
    if 'errors' in r.json().keys():
        print(r.text)
    return r.json()


def removeTag(full_table_name, tag):
    url = 'http://gms.datahub.bigdata.local/api/graphql/'
    query = """
    mutation removeTag {
        removeTag(input: { tagUrn: "urn:li:tag:"""+tag+"""", 
          resourceUrn: "urn:li:dataset:(urn:li:dataPlatform:hive,"""+full_table_name+""",PROD)" })
    }
    """
    cookies={''}
    json={'query': query}
    headers = {'X-DataHub-Actor': 'urn:li:corpuser:datahub'}

    r = requests.post(url, headers=headers, json=json)
    print(full_table_name)
    if 'errors' in r.json().keys():
        print(r.text)
    
    
def remove_old_tag(full_table_name):
    r = queryTag(full_table_name)
    if r['data']['dataset']['tags']:
        for i in r['data']['dataset']['tags']['tags']:
            if i['tag']['name']:
                print(full_table_name, 'remove tag', i['tag']['name'])
                removeTag(full_table_name, i['tag']['name'])


def remove_old_frequency(full_table_name):
    r = queryTag(full_table_name)
    if r['data']['dataset']['tags']:
        for i in queryTag(full_table_name)['data']['dataset']['tags']['tags']:
            if 'frequency' in i['tag']['name']:
                print(full_table_name, 'remove tag', i['tag']['name'])
                removeTag(full_table_name, i['tag']['name'])
            
            
def add_tag_frequency(full_table_name, tag):
    for table, t in zip(full_table_name, tag):
        addTag(table, t)

        
def run_remove_old_frequency(list_full_table_name):
    for table in list_full_table_name:
        remove_old_frequency(table)

        
def run_add_tag_frequency(list_full_table_name, list_tag):
    for table, t in zip(list_full_table_name, list_tag):
        addTag(table, t)
        
        
# User 
def add_userCopr(name, title, email):
    url = "http://gms.datahub.bigdata.local/entities?action=ingest"

    body =  {
        "entity": {
            "value": {
                "com.linkedin.metadata.snapshot.CorpUserSnapshot": {
                    "urn": "urn:li:corpuser:"+email,
                    "aspects": [{
                        "com.linkedin.identity.CorpUserInfo": {
                            "active": True,
                            "displayName": name,
                            "email": email+"@fpt.com.vn",
                            "title": title,
                            "fullName": name
                        }
                    }]
                }
            }
        }
    }

    headers = {'X-DataHub-Actor': 'urn:li:corpuser:datahub'}
    r = requests.post(url, headers=headers, json=body)
    if 'errors' in r.json().keys():
        print(r.text)
    

def addGroupMembers(group_name, username):
    url = 'http://gms.datahub.bigdata.local/api/graphql/'
    query = """
    mutation addGroupMembers {
      addGroupMembers(input: {groupUrn: "urn:li:corpGroup:Editors", userUrns: "urn:li:corpuser:"""+username+""""})
    }
    """
    cookies={''}
    json={'query': query}
    headers = {'X-DataHub-Actor': 'urn:li:corpuser:datahub'}

    r = requests.post(url, headers=headers, json=json)
    if 'errors' in r.json().keys():
        print(r.text)
    return r


# Table
def updateTableDescription(full_table_name, description):
    url = 'http://gms.datahub.bigdata.local/api/graphql/'
    query = """
    mutation 
        updateDataset {
            updateDataset(
              urn: "urn:li:dataset:(urn:li:dataPlatform:hive,"""+full_table_name+""",PROD)",
              input: {
                  editableProperties: {
                    description: """ + '"""' + description + '"""'+ """ 
                  }
              }
            ) {
                urn
            }
    }
    """
    cookies={''}
    json={'query': query}
    headers = {'X-DataHub-Actor': 'urn:li:corpuser:datahub'}

    r = requests.post(url, headers=headers, json=json)
    
    print(full_table_name)
    if 'errors' in r.json().keys():
        print(r.text)
    

def query_table_description(full_table_name):
    url = 'http://gms.datahub.bigdata.local/api/graphql/'
    query = """
    query {
      dataset(urn: "urn:li:dataset:(urn:li:dataPlatform:hive,"""+full_table_name+""",PROD)") {
        editableProperties {
          description
        }
      }
    }
    """
    cookies={''}
    json={'query': query}
    headers = {'X-DataHub-Actor': 'urn:li:corpuser:datahub'}

    r = requests.post(url, headers=headers, json=json)
    if 'errors' in r.json().keys():
        print(r.text)
    return r.json()


def query_schema_with_description(full_table_name):
    url = 'http://gms.datahub.bigdata.local/api/graphql/'
    query = """
    query {
      dataset(urn: "urn:li:dataset:(urn:li:dataPlatform:hive,"""+full_table_name+""",PROD)") {
        editableSchemaMetadata {
          editableSchemaFieldInfo {
            fieldPath
            description

          }
        }
      }
    }
    """
    cookies={''}
    json={'query': query}
    headers = {'X-DataHub-Actor': 'urn:li:corpuser:datahub'}

    r = requests.post(url, headers=headers, json=json)
    if 'errors' in r.json().keys():
        print(r.text)
    return r.json()