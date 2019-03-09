# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BrandItem(scrapy.Item):
    # define the fields for your item here like:
    pingpaiID = scrapy.Field()
    szm = scrapy.Field()
    name = scrapy.Field()
    imgUrl = scrapy.Field()
    url = scrapy.Field()

    def get_insert_sql(self):
        insert_sql="""
                    INSERT INTO `vcar_vcyber_com`.`vcar_pinpai`
                            (`pinpaiID`,
                            `szm`,
                            `name`,
                            `imgUrl`,
                            `url`)
                            VALUES
                            (%s,
                             %s,
                             %s,
                             %s,
                             %s
                            );
        """
        params=(self['pingpaiID'],self['szm'],self['name'],self['imgUrl'],self['url'])
        return insert_sql,params

    def get_update_sql(self):
        update_sql="""
                    UPDATE `vcar_vcyber_com`.`vcar_pinpai`
                    SET
                        `szm` = %s,
                        `name` = %s,
                        `imgUrl` = %s,
                        `url` = %s
                    WHERE `pinpaiID` = %s;
        """
        params=(self['szm'],self['name'],self['imgUrl'],self['url'],self['pingpaiID'])
        return update_sql,params
    
