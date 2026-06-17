import requests
import json

url = "https://dc.datastory.com.cn/banyan/searchInBanyan"

headers = {
  'Content-Type': 'application/json',
  'Authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJrb3lAZGF0YXN0b3J5LmNvbS5jbiIsImF1ZGllbmNlIjoid2ViIiwiY3JlYXRlZCI6MTc2NTUzMjg1NjU5OSwicHciOiJBaXIxNjA2MzAiLCJleHAiOjE3NjYxMzc2NTZ9.dkZQUdPjAvN0w-XsyN-ZizGHox69SkaI_3tfbzH1WbKRPvxzSRFQvTUbQxrMHkjAFLi4oOMjwyIiOM1ih1wiGA',
  'Cookie': 'dc-login-iden=.datastory.com.cn#e3279c4f-42cd-4195-9410-15efa172e134; SESSION=4aa8a18b-f80a-4fa4-b4e6-026514bdcea3'
}

payload = json.dumps({
  "dataType": "NewsForum",
  "banyanType": "elf",
  "searchType": "Post",
  "needReturnFields": "id,item_id,user_item_id,cat_id,primary_site_id,primary_site_name,user_follower_cnt,dislike_cnt,collection_cnt,like_cnt,interaction_cnt,sentiment,site_name,pregnancy_day_cnt,baby_lifecycle_cnt,source,title,url,view_cnt,comment_cnt,author_name,content,content_len,domain,site_id,source_crawler_id,publish_date,publish_timestamp,publish_date_hour,update_date,update_timestamp,keywords,is_ad,is_robot,is_digest,is_hot,is_top,is_recom,pic_urls,video_play_urls,forum_name,forum_id,item_score,channel,ip_location,forum_names,forum_ids,user_item_ids,user_names,user_level,ocr_truncation_frames,topics,repost_cnt,other_data,direct_source_byte,star_source_byte,syhz_source_byte,crawler_latency_duration,interaction_t1_update_timestamp,interaction_t3_update_timestamp,interaction_t7_update_timestamp,interaction_t15_update_timestamp,augment_timestamp,data_source_ids,crawler_date,crawler_timestamp,task_ids,site_source_ids,site_source_names,first_crawler_date,first_crawler_timestamp,first_update_date,first_update_timestamp,fingerprint,ext_comment_cnt,post_type,activity_names,book_names,brand_names,category_names,character_design_shape_names,color_names,crowd_names,efficacy_names,festival_names,game_names,illness_physique_names,ingredient_raw_material_names,model_names,movie_names,odor_flavor_names,organization_names,package_names,person_names,place_names,product_names,scenes_names,song_names,technology_crafts_names,touch_taste_experience_names,tv_series_names,variety_show_names,entity_item_ids,entity,volume_type,social_media_ad,ner_entity,video_cover_ocr_content,src_content,src_content_len,src_title,src_item_id,low_value_marks,event_item_ids,es_score",
  "searchCondition": [
    {
      "fieldName": "site_id",
      "operation": "nl",
      "fieldValue": []
    },
    {
      "fieldName": "site_id",
      "operation": "nn",
      "fieldValue": []
    },
    {
      "fieldName": "site_id",
      "operation": "eq",
      "fieldValue": ["101944"]
    },
    {
      "fieldName": "site_id",
      "operation": "ne",
      "fieldValue": ["101944"]
    },
    {
      "fieldName": "site_name",
      "operation": "mp",
      "fieldValue": ["知乎", ""]
    },
    {
      "fieldName": "publish_timestamp",
      "operation": "ltegte",
      "fieldValue": [1735660800000, 1765382399000]
    }
  ],
  "sortCondition": {
    "sortFieldName": "publish_timestamp",
    "order": "desc"
  },
  "timeRange": "1735660800000,1765382399000"
})


response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)


