#! python3

import json
import os

class configIO(object):

    def __init__(self):

        self.configFile = "data\\config.json"

        if os.path.exists(self.configFile):
            pass
        else:
            self.initConfigFile()

    def initConfigFile(self):

        init_data = {'Source':'', 'Stats': {}, 'Last Set': []}

        data_dict = {'Fantasy': init_data, 'Super': init_data, 'Mega': init_data, 'Power': init_data}

        # this code will create the data subdirectory the first time the program runs
        try:
            c_file = open(self.configFile, "w")
        except:
            os.makedirs("data")
            c_file = open(self.configFile, "w")

        c_file.close()

        # call the writeConfigFile function to write the JSON file
        self.writeConfigFile(data_dict)


    def writeConfigFile(self, data_dict):

        with open(self.configFile, 'w') as o_file:
            json.dump(data_dict, o_file)

        o_file.close()

    def readConfigFile(self):

        with open(self.configFile, 'r') as i_file:

            for data_line in i_file:
                data_dict = json.loads(data_line)

        i_file.close()

        return data_dict

    def getKey(self, ltype):

        if ltype == 1:
            return 'Fantasy'
        elif ltype == 2:
            return 'Super'
        elif ltype == 3:
            return 'Mega'
        elif ltype == 4:
            return 'Power'
        else:
            return False

    def getSettings(self, ltype):

        select_key = self.getKey(ltype)
        data_dict = self.readConfigFile()

        return data_dict[select_key]


    def getSource(self, ltype):

        settings = self.getSettings(ltype)

        return settings['Source']


    def getStats(self, ltype):

        settings = self.getSettings(ltype)

        return settings['Stats']


    def getLastSet(self, ltype):

        settings = self.getSettings(ltype)

        return settings['Last Set']


    def updateSource(self, ltype, source):

        data_dict = self.readConfigFile()

        select_key = self.getKey(ltype)
        data_dict[select_key]['Source'] = source

        self.writeConfigFile(data_dict)

        return True

    def updateStats(self, ltype, counts):

        data_dict = self.readConfigFile()

        select_key = self.getKey(ltype)
        data_dict[select_key]['Stats'] = counts

        self.writeConfigFile(data_dict)

        return True

    def updateLastSet(self, ltype, lastSet):

        data_dict = self.readConfigFile()

        select_key = self.getKey(ltype)
        data_dict[select_key]['Last Set'] = lastSet

        self.writeConfigFile(data_dict)

        return True
