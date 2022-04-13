# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import pymongo
from bson.objectid import ObjectId
from datetime import datetime

class MongodbPipeline:

    # set "global" variables
    collection_name = "nft_collections"
    first_bulk = 0

    # function that executes when spider starts
    def open_spider(self,spider):
        self.client = pymongo.MongoClient("mongodb+srv://youngstervi:changeme@alphacluster.tvrle.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self.db = self.client["alpha_howrare"]
        self.firstBulk = self.db[self.collection_name].find().count()
        logging.warning("SPIDER OPENED FROM PIPELINE")

    # functions that executes when spiders ends
    def close_spider(self,spider):

        self.client.close()
        logging.warning("SPIDER CLOSED FROM PIPELINE")


    def process_item(self, item, spider):

        # adapter is to add fields to the current item
        adapter = ItemAdapter(item)

        # first bulk variable control
        if self.firstBulk > 0:

            # check if item already exists in the collection
            exist = self.db[self.collection_name].find_one({"name": item.get("name")})

            # if exists then update document by id
            if exist:

                itemId = str(self.db[self.collection_name].find_one({"name": item.get("name")},{"_id":1}).get("_id"))

                myquery = self.db[self.collection_name].find_one({"_id": ObjectId(itemId)},{"_id":1})
                new_values = {"$set": {"updatedAt": datetime.now().strftime("%d/%m/%Y %H:%M:%S")}}

                self.db[self.collection_name].update_one(myquery,new_values)

                return item

            # if not exists then insert new element
            else:

                adapter['createdAt']= datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                adapter['updatedAt']= datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                self.db[self.collection_name].insert(item)

                return item
        
        # this block of code only run if the collection is empty
        else:

            adapter['createdAt']= datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            adapter['updatedAt']= datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            self.db[self.collection_name].insert(item)

            return item
