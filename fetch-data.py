import uuid
import requests
import json
from datetime import datetime,timezone
import psycopg2
import time
import sys

connection=psycopg2.connect(database="divardb",user="postgres",password="postgres",host="localhost",port=5432)
cursor=connection.cursor()

def insert_widget(data,nt):
    
    sql="insert into divar_raw(id,widgets,timestr) values(%s,%s,%s)"

    cursor.execute(sql,(str(uuid.uuid4()),data,nt))
    cursor.connection.commit()



def insert_detail(id,token,tm):
    detail_url="https://api.divar.ir/v8/posts-v2/web/"
    sql="insert into divar_widget(id,token,creation_date) values(%s,%s,%s)"
    cursor.execute(sql,(id,token,tm))
    cursor.connection.commit()
    detail_url=detail_url+token
    x=requests.get(detail_url)
    detail_title=''
    if x.text=="":
        return
    try:
        obj=json.loads(x.text)
        latitude=0
        longitude=0
        text=""
        type=""
        title=""

        if obj is not None:
            details=obj['sections']
            for dt in details:
                if dt['section_name']=="MAP":
                    for mdt in dt['widgets']:
                        if mdt['widget_type']=="MAP_ROW":
                            if mdt['data']is not None:
                                if mdt['data']['location'] is not None:
                                    if 'exact_data' in mdt['data']['location']:
                                        point=mdt['data']['location']['exact_data']['point']
                                        latitude=point['latitude']
                                        longitude=point['longitude']
                        break
                if dt['section_name']=="TAGS":
                    for mdt in dt['widgets']:
                        if mdt['widget_type']=="WRAPPER_ROW":
                            if mdt['data'] is not None:
                                if mdt['data']['chip_list'] is not None:
                                    chips=mdt['data']['chip_list']['chips']
                                    for ch in chips:
                                        text=ch['text']
                                        type=ch['type']
                                        break
                        break

                if dt['section_name']=="BREADCRUMB":
                    for mdt in dt['widgets']:
                        if mdt['widget_type']=="BREADCRUMB":
                            if mdt['data'] is not None:
                                for pmd in mdt['data']['parent_items']:
                                    title=pmd['title']
                                    break
                        break
                if dt['section_name']=="TITLE":
                    for mdt in dt['widgets']:
                        if mdt['widget_type'] == 'LEGEND_TITLE_ROW':
                            if mdt['data'] is not None:
                                if mdt['data']['title'] is not None:
                                    detail_title=mdt['data']['title']
                                    print(detail_title)
        # print(title+"**"+type+"**"+str(latitude)+"**"+str(longitude)+"**"+text)

        # sql="insert into divar_detail(id,title,type,text,token,creation_date,geog) values(%s,%s,%s,%s,%s,%s,'SRID=4326;POINT(-110 30)')"
        sql="insert into divar_detail(id,title,type,text,token,creation_date,geog,detail_title) values(%s,%s,%s,%s,%s,%s,'SRID=4326;POINT(%s %s)',%s);"


        now=datetime.now()
        try:
            date=str(now.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
            print(date)
            ids=str(uuid.uuid4())
            # sql="insert into divar_widget(id,token,creation_date) values(%s,'dd',%s)"
            cursor.execute(sql,(ids,title,type,text,token,date,longitude,latitude,detail_title))
            # cursor.execute(sql,(id))#,title,type,text,token,date)
            cursor.connection.commit()
        except Exception:

            print('insert to postgis'+str(sys.exc_info()[0]))
    except Exception:
        print('x.load json fire exception'+str(sys.exc_info()[0]))


url='https://api.divar.ir/v8/postlist/w/search'

now=datetime.now()
ns=now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

while True:
    pyload={"city_ids":["1"],"pagination_data":{"@type":"type.googleapis.com/post_list.PaginationData","last_post_date":ns,"page":1,"layer_page":1,"search_uid":"58d24c4e-5cf0-432d-bfe2-0498f775c624"},"search_data":{"form_data":{"data":{"category":{"str":{"value":"ROOT"}}}}}}
    x=requests.post(url,json=pyload)

    obj=json.loads(x.text)
    insert_widget(x.text,ns)

    if obj is not None:
        widgets=obj['list_widgets']


        for widget in widgets:
            data=widget['data']
            token=data['action']['payload']['token']

            if 'image_url' in data:
                img_url=data['image_url']
                slash_sub=str.split(img_url,'/')
                lst=slash_sub[len(slash_sub)-1]
                ids=str.split(lst,'.')
                if token!="":
                    insert_detail(ids[0],token,ns)
    time.sleep(10)