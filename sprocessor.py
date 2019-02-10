# -*- coding: utf-8 -*-
import sys
import importlib
import json
import csv

importlib.reload(sys)

class Processor():
    '''
    Processor class to parse the json data.
    '''
    def __init__(self):
        pass

    def load_file(self):
        '''
        Loads the provided json data.
        :return:
        '''
        with open('data.json', 'r') as fileobject:
            self.data = json.loads(fileobject.read())
        return self.data

    def form_csv_data(self):
        '''
        Generates/Retrieves the data from json data in order to
        generate an csv file.
        :return:
        '''
        jdata = self.load_file()
        p = []
        for fkey, fvalues in jdata.items():
            ''' Solution level'''
            if fkey == 'paths':
                for skey, svalues in fvalues.items():
                    l = []
                    ''' Endpoint Level'''
                    for tkey, tvalues in svalues.items():
                        ''' API Level'''
                        csv_data = []
                        csv_data.append(tkey)
                        '''
                        To check the parameter field is there or not
                        update the flag.   
                        '''
                        flag = True
                        counter = 0
                        if 'parameters' in [x for x in tvalues.keys()]:
                            flag = False
                        # print(tvalues)
                        for fkey, fvalues in tvalues.items():
                            '''
                            TODO below code can be replaced by for loop to fetch all 
                            the values dynamically.
                            '''
                            if flag:
                                '''
                                To check the parameter field is there or not
                                update the csv_data with a null field    
                                '''
                                if counter == 2:
                                    csv_data.append(''.join('None'))

                            if fkey == 'tags':
                                csv_data.append(''.join(fvalues))
                            if fkey == 'summary':
                                csv_data.append(''.join(fvalues))
                            if fkey == 'parameters':
                                a = []
                                for dict in fvalues:
                                    b = []
                                    for fikey, fivalues in dict.items():
                                        if fikey == 'name':
                                            t = fikey + ' : ' + fivalues + ' '
                                            b.append(''.join(t))
                                        if fikey == 'type':
                                            t = fikey + ' : ' + fivalues + ' '
                                            b.append(''.join(t))
                                        if fikey == 'required':
                                            t = fikey + ' : ' + fivalues + ' '
                                            b.append(''.join(t))
                                    a.append(''.join(b))
                                csv_data.append('and '.join(a))
                            if fkey == 'responses':
                                a = []
                                for fikey, fivalues in fvalues.items():
                                    t = fikey + ' : ' + fivalues['description'] + ' '
                                    a.append(''.join(t))
                                csv_data.append('or '.join(a))
                            counter = counter + 1
                        l.append(csv_data)
                    p.extend(l)
        return p

    def form_csv_file(self):
        '''
        Creates the .csv file.
        :return:
        '''
        input_data = self.form_csv_data()
        csv.register_dialect('mydialect',
                             delimiter='|',
                             quoting=csv.QUOTE_NONE,
                             skipinitialspace=True)
        with open('output.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            for row in input_data:
                writer.writerow(row)
        csvfile.close()


def responder():
    '''
    Provides an abstraction to the underlying code.
    :return:
    '''
    a = Processor()
    a.form_csv_file()

# TODO this call is for testing during building.
# responder()