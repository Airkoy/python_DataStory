import requests
import json

url = "https://dc.datastory.com.cn/banyan/searchInBanyan"

headers = {
    "Authorization": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJoZXJtZXNfYWRtaW5AZGF0YXN0b3J5LmNvbS5jbiIsImF1ZGllbmNlIjoid2ViIiwiY3JlYXRlZCI6MTc3NDg0OTU5MDMwNSwicHciOiJVTlZQbWM3dCIsImV4cCI6MTc3NTQ1NDM5MH0.tviFvvt2z2ZPw9kU7bBovJpqTMnNf6_pp_LRfdjQFmTkicSdOtWKUbeMx-m1OCWueKgYjD1xhccSSUJmB7G6mg",
    "Content-Type": "application/json"
}
payload = json.dumps({
    "dataType": "NewsForum",
    "banyanType": "elf",
    "searchType": "Post",
    # "needReturnFields": "id,item_id,user_item_id,cat_id,primary_site_id,primary_site_name,user_follower_cnt,dislike_cnt,collection_cnt,like_cnt,interaction_cnt,sentiment,site_name,pregnancy_day_cnt,baby_lifecycle_cnt,source,title,url,view_cnt,comment_cnt,author_name,content,content_len,domain,site_id,source_crawler_id,publish_date,publish_timestamp,publish_date_hour,update_date,update_timestamp,keywords,is_ad,is_robot,is_digest,is_hot,is_top,is_recom,pic_urls,video_play_urls,forum_name,forum_id,item_score,channel,ip_location,forum_names,forum_ids,user_item_ids,user_names,user_level,ocr_truncation_frames,topics,repost_cnt,other_data,direct_source_byte,star_source_byte,syhz_source_byte,crawler_latency_duration,interaction_t1_update_timestamp,interaction_t3_update_timestamp,interaction_t7_update_timestamp,interaction_t15_update_timestamp,augment_timestamp,data_source_ids,crawler_date,crawler_timestamp,task_ids,site_source_ids,site_source_names,first_crawler_date,first_crawler_timestamp,first_update_date,first_update_timestamp,fingerprint,ext_comment_cnt,post_type,activity_names,book_names,brand_names,category_names,character_design_shape_names,color_names,crowd_names,efficacy_names,festival_names,game_names,illness_physique_names,ingredient_raw_material_names,model_names,movie_names,odor_flavor_names,organization_names,package_names,person_names,place_names,product_names,scenes_names,song_names,technology_crafts_names,touch_taste_experience_names,tv_series_names,variety_show_names,entity_item_ids,entity,volume_type,social_media_ad,ner_entity,video_cover_ocr_content,src_content,src_content_len,src_title,src_item_id,low_value_marks,event_item_ids,es_score",
    "needReturnFields": "item_id,site_id,site_name,first_update_timestamp,title,content,url",
    "searchCondition": [
        {
            "fieldName": "item_id",
            "operation": "eq",
            # "fieldValue": [
            #     "5db9988862e5b0f1b3568da77b99231f",
            #     "ca24d65984de22ca79c21063e4e56b89",
            #     "f69bac0d651962ddcb36cd1afb875c7c",
            #     "3999d39c9fc625f8cf18e61f8e57a815",
            #     "4408209d8af0c0ba85968a59a796ec74",
            #     "9894f09e9e079f0a220b9f87ab236932",
            #     "14ebd3a4c1ebcaed3c41af7e7a1508f0",
            #     "5fa0d69320a728278f40cd57d2bee770",
            #     "5c2f711c77dc3c4a2e87aae586ca4662",
            #     "9ff63a030c519f067a1b66e05b670323",
            #     "952ae406277ebfa70873794e348023e6",
            #     "f46cd683f0ce8f9282aafc06fb6dc072",
            #     "9210257d263d0ed9075bf722b990579a",
            #     "8a393cafe647c8aabb06a6a5725bf9c8",
            #     "eed4d51000e8bd1ca9f9b112300d4c11",
            #     "f43ba179e720e986769a406ea4dee4f3",
            #     "63e0fcf5524b2747176684b0e5e4a5d1",
            #     "news_9846533042299449784"
            # ],
            "fieldValue": [
                "eed4d51000e8bd1ca9f9b112300d4c11"
            ]

        },
        {
            "fieldName": "publish_timestamp",
            "operation": "ltegte",
            "fieldValue": [1767196800000,1774972799000]
        }
    ],
    "sortCondition": {
        "sortFieldName": "publish_timestamp",
        "order": "desc"
    },
    "timeRange": "1767196800000,1774972799000"
})

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
