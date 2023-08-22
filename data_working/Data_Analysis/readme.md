1.cmt_power
제품관심: 인플루언서 제품관심 평균 (loyalty_Lv증가할수록 높은 충성도) 
loyalty_Lv1: like10000 // followers_count 
loyalty_Lv2: comment100 // like 
loyalty_Lv3: 제품관심*1000 // comment

2.chk_power -> cmt_power의 각 column sum

3.chk_power_mean -> cmt_power의 각 column mean

4.inf_info -> 인플루언서들의 개략적 정보들

followers_count: 팔로워수 
media_count: 전체 피드수 
ad_media: 광고 피드수 
sf_ad_media: 패션 광고 피드수 
image_usage_Lv1: 이미지 소모도Lv1 -> ad_media / media_count 
image_usage_Lv2: 이미지 소모도Lv2 -> sf_ad_media / media_count 
fashion_rel: sf_ad_media / ad_media 
marketing_performance -> (chk_power_mean['loyalty_Lv1']*0.1 + chk_power_mean['loyalty_Lv2']*0.3 + chk_power_mean['loyalty_Lv3']*0.5)*chk_power_mean['제품관심']0.1inf_info['fashion_rel']

5/6.total_date / type -> 전체 피드 날짜별/media_type별 졸아요, 댓글 총합/평균

7/8.full_date/ type -> 패션 광고 피드 날짜별/media_type별 졸아요, 댓글 총합/평균
