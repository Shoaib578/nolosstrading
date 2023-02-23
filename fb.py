import facebook
facebook_access_token = 'EAAP3lBUoDhkBAAZAEWmgDY5GmxWGMpKfJVqWvUWiCc10GqZBSZBDZAiqxmfeqDoHRcV4IWPN1I0g3yjZAZAvLHzMkM0ZAw07q3mnTeToso0D7hP2pTWLsZA73PK8o1qFk90Qsul1dBpLICDleOtlva1lyIfmiKxWHSTzsiIjHLRZAkQ5RmWsfsuQvFGx9NwY1dgNCE9H8ZC5zcYCbqYpdBrJPrBXJWypU46ucZD'
facebook_page_id = '109998795333855'
fb = facebook.GraphAPI(access_token=facebook_access_token, version="2.12")
fb.get_permissions(user_id=109998795333855)

fb.put_object(
   parent_object="me",
   connection_name="feed",
   message="This is a great website. Everyone should visit it.",
   link="https://www.facebook.com")

