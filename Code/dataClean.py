import csv
import pandas as pd
import numpy as np
import math


def checkAge(data):
	year_of_survey = 2014
	year_of_birth = data['year_of_birth']
	age = data['Age']
	index = 0
	for i,j in zip(year_of_birth,age):
		if(math.isnan(i) or math.isnan(j)):
			data.drop([index],axis=0,inplace=True)
		elif(j > year_of_survey-i):
			# print("I : " + str(i))
			# print("J : " + str(j))
			data.drop([index],axis = 0,inplace=True)
		index = index + 1
	data = data.reset_index(drop=True)
	return data

def checkBP(data):
    max_sys = 180
    min_sys = 90
    max_dia = 120
    min_dia = 60
    max_reading_err = 10
    data.replace('NA',np.NAN,inplace=True)
    convert_dict = {
        'BP_systolic' : float,
        'BP_systolic_2_reading' : float,
        'BP_Diastolic' : float,
        'BP_Diastolic_2reading' : float
    }
    data = data.astype(convert_dict)
    s1 = data['BP_systolic']
    s2 = data['BP_systolic_2_reading']
    d1 = data['BP_Diastolic']
    d2 = data['BP_Diastolic_2reading']

    index = 0
    for i,j,k,l in zip(s1,s2,d1,d2):
        if(math.isnan(i) or math.isnan(j) or math.isnan(k) or math.isnan(l)):
            index = index + 1
            continue
        elif(abs(i-j)>max_reading_err):
            data.drop([index],axis=0,inplace=True)
        elif(abs(k-l) > max_reading_err):
            data.drop([index],axis=0,inplace=True)
        elif((i+j)/2 > max_sys or (i+j)/2 < min_sys):
            data.drop([index],axis=0,inplace=True)
        elif((k+l)/2 > max_dia or (k+j)/2 < min_dia):
            data.drop([index],axis=0,inplace=True)
        index = index + 1
    data = data.reset_index(drop=True)
    return data

def checkDayMonth(data):
    convert_dict = {
        'date_of_birth' : float,
        'month_of_birth' : float
    }
    data = data.astype(convert_dict)
    data.drop(data.loc[data['date_of_birth']==0].index, inplace=True)
    data.drop(data.loc[data['month_of_birth']==0].index, inplace=True)
    data = data.reset_index(drop=True)
    return data

def checkPulseRate(data):
    data = data.replace('NA',np.NAN)
    convert_dict = {
        'Pulse_rate' : float,
        'Pulse_rate_2_reading' : float,
        'Age' : float
    }
    data = data.astype(convert_dict)
    # print(data['Pulse_rate'].dtype)
    # print(data['Age'].dtype)
    prate1 = data['Pulse_rate']
    prate2 = data['Pulse_rate_2_reading']
    age = data['Age']
    #max pulse = 220 - age
    min_pulse = 40
    max_reading_err = 10
    # prate1.fillna(prate1.mean(),inplace=True)
    # prate2.fillna(prate2.mean(),inplace=True)
    index = 0
    for i,j,k in zip(prate1,prate2,age):
        if(math.isnan(i) or math.isnan(j)):
            index = index + 1
            continue
        elif(abs(i-j) > max_reading_err):
            data = data.drop([index],axis = 0)
        elif((i+j)/2 > (220-k) or (i+j)/2 < min_pulse):
            data = data.drop([index],axis = 0)
        index = index + 1
    index = 0
    data = data.reset_index(drop=True)
    return data

def checkBloodGlucose(data):
	data = data.replace('NA',np.NAN)
	convert_dict = {
		'fasting_blood_glucose_mg_dl' : float
	}
	data = data.astype(convert_dict)
	blood_glucose = data['fasting_blood_glucose_mg_dl']
	max_blood_glucose = 300 #src : wikipedia
	min_blood_glucose = 15

	index = 0
	for i in blood_glucose:
		if(math.isnan(i)):
			index = index + 1
			continue
		elif(i > max_blood_glucose or i < min_blood_glucose):
			data = data.drop([index],axis = 0)
		index = index + 1
	index = 0
	data = data.reset_index(drop=True)
	return data

def checkHGB(data):
    data = data.replace('NA',np.NAN)
    convert_dict = {
        'Haemoglobin_level' : float
    }
    data = data.astype(convert_dict)
    hgb_level = data['Haemoglobin_level']
    max_hgb = 18 #src : wikipedia
    min_hgb = 5

    index = 0
    for i in hgb_level:
        if(math.isnan(i)):
            index = index + 1
            continue
        elif(i > max_hgb or i < min_hgb):
            data = data.drop([index],axis = 0)
        index = index + 1
    index = 0
    data = data.reset_index(drop=True)
    return data


def cleanData(file_name,file_path,output_dir):
    
    fields = []
    
    

    
    itr = 0
    filename = file_path + '/' + file_name
    with open(filename,'r') as data_MP:
        csvreader = csv.reader(data_MP)
        for row in csvreader:
            fields = row
            break

    itr = 0
    filename = file_path + '/' + file_name

    data_frame = pd.read_csv(filename,encoding='utf-8')
    # print(data_frame)
    data_frame = data_frame.replace('NA',np.NAN)
    itr = 0
    threshold = 0.75
    
    useless_fields = []

    for col in data_frame.columns:
        print(str(col) + ' : ' + str(data_frame[col].isna().sum()))
        if(data_frame[col].isna().sum() > threshold*data_frame.shape[0]):
            useless_fields.append(col)
            data_frame = data_frame.drop(columns=col)

    itr = 0

    print("------------------------------------------")
    print("useless fields:")
    for item in useless_fields:
        print(item)
    print("------------------------------------------")

    print("------------------------------------------")
    print("Number of Fieldsss")
    print(len(fields))
    print("Number of USeless Fieldsss")
    print(len(useless_fields))
    print("------------------------------------------")

    print("------------------------------------------")
    print(data_frame)
    print("------------------------------------------")    
    
    
    for col in data_frame.columns:
        data_frame.drop(data_frame.loc[data_frame[col]=='Member - not present'].index, inplace=True)

    print("------------------------------------------")
    print("Rows after 'Member Not Present'")
    print(data_frame.shape[0])
    print("------------------------------------------")

    data_frame = data_frame.reset_index(drop=True)
        
    
    print("------------------------------------------")
    """ Removing duplicates """
    print("Number rows : %d" %(data_frame.shape[0]))
    # print(len(rows))
    dups = data_frame.duplicated()
    print("Number of duplicates = %d" %(dups.sum()))
    data_frame = data_frame.drop_duplicates()
    print("Rows after removing duplicates : %d" %(data_frame.shape[0]))


    print("------------------------------------------")
    """ Removing wrong Age """
    data_frame.drop(data_frame.loc[data_frame['Age']=='NA'].index, inplace=True)
    convert_dict = {
        'Age' : float,
        'year_of_birth' : float
    }
    data_frame = data_frame.astype(convert_dict)
        
    print("Number rows : %d" %(data_frame.shape[0]))
    data_frame = checkAge(data_frame)
    print("Rows after Wrong Age : %d" %(data_frame.shape[0]))

    print("------------------------------------------")
    """ Removing wrong Date and Month of birth"""
    print("Number rows : %d" %(data_frame.shape[0]))
    data_frame = checkDayMonth(data_frame)
    print("Rows after Wrong Date and Month of birth : %d" %(data_frame.shape[0]))

    print("------------------------------------------")
    """ Removing wrong BP """
    print("Number rows : %d" %(data_frame.shape[0]))
    data_frame = checkBP(data_frame)
    print("Rows after Wrong BP : %d" %(data_frame.shape[0]))


    print("------------------------------------------")
    """ Removing wrong Pulse Rate"""
    print("Number rows : %d" %(data_frame.shape[0]))
    data_frame = checkPulseRate(data_frame)
    print("Rows after Wrong Pulse Rate : %d" %(data_frame.shape[0]))


    print("------------------------------------------")
    """ Removing wrong fasting glucose"""
    print("Number rows : %d" %(data_frame.shape[0]))
    data_frame = checkBloodGlucose(data_frame)
    print("Rows after Wrong Blood Glucose : %d" %(data_frame.shape[0]))


    print("------------------------------------------")
    """ Removing wrong Haemoglobin"""
    print("Number rows : %d" %(data_frame.shape[0]))
    data_frame = checkHGB(data_frame)
    print("Rows after Wrong Haemoglobin : %d" %(data_frame.shape[0]))

    data_frame = data_frame.replace('NA',np.NAN)

    data_frame['Haemoglobin_level'].fillna(data_frame['Haemoglobin_level'].mean(),inplace=True)
    data_frame['fasting_blood_glucose_mg_dl'].fillna(data_frame['fasting_blood_glucose_mg_dl'].mean(),inplace=True)
    data_frame['Pulse_rate'].fillna(data_frame['Pulse_rate'].mean(),inplace=True)
    data_frame['Pulse_rate_2_reading'].fillna(data_frame['Pulse_rate_2_reading'].mean(),inplace=True)
    data_frame['BP_systolic'].fillna(data_frame['BP_systolic'].mean(),inplace=True)
    data_frame['BP_systolic_2_reading'].fillna(data_frame['BP_systolic_2_reading'].mean(),inplace=True)
    data_frame['BP_Diastolic'].fillna(data_frame['BP_Diastolic'].mean(),inplace=True)
    data_frame['BP_Diastolic_2reading'].fillna(data_frame['BP_Diastolic_2reading'].mean(),inplace=True)

    convert_dict = {
        'Weight_in_kg' : float,
        'Length_height_cm' : float  
    }
    data_frame = data_frame.astype(convert_dict)

    data_frame['Weight_in_kg'].fillna(data_frame['Weight_in_kg'].mean(),inplace=True)

    data_frame['Length_height_cm'].fillna(data_frame['Length_height_cm'].mean(),inplace=True)

    data_frame = data_frame.fillna('Measured')

    data_frame['length_height_code'].replace('Measured','Height',inplace = True)
    data_frame['Haemoglobin_test'].replace('Measured','YES',inplace = True)
    data_frame['Diabetes_test'].replace('Measured','YES',inplace = True)

    output_file = output_dir + 'cleaned' + file_name 
    data_frame.to_csv(output_file,index=False)

	