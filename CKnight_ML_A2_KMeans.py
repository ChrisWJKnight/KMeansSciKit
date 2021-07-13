# Program created by Christopher Knight 10508953@cityplym.ac.uk, using elements from the following guides but now completely modified
# https://medium.com/pursuitnotes/k-means-clustering-model-in-6-steps-with-python-35b532cfa8ad
# https://www.analyticsvidhya.com/blog/2019/08/comprehensive-guide-k-means-clustering/#k-means-clustering-python-code
# 
# Mall customers dataset CSV available at
# https://www.kaggle.com/shwetabh123/mall-customers?select=Mall_Customers.csv
#
#
# Required Libraries
import pandas as pd#Pandas library, to hold dataset
import numpy as np#NumPy library, to create multi dimensional matrices
import matplotlib.pyplot as plt#MatPlotLib library, to plot data as graphs
from sklearn.cluster import KMeans #SciKit-Learn, Cluster library
from sklearn.preprocessing import StandardScaler#Scikit-Learn, Scalar library

#START PROGRAM FUNCTION CALL IS ON LINE 212
def start_program():#Step 0
    data_in = get_input() #Step 1 select which dataset to use
    dataset = data_read(data_in)#Step 2 import dataset
    data = extract_data(dataset, data_in)#Step 3 extract values from dataset
    print_summary(dataset)#Step 4 print summary of dataset
    input_data = scalar_opt(data)#Step 5 determine if data should be normalised
    SSE = get_sse(input_data)#Step 6 determine Sum Sqr Err, elbow method
    display_elbow(data_in,SSE)#Step 7 display Elbow graph
    k_num = get_knum()#Step 8 determine number of clusters
    kmeans, pred = prediction(k_num,input_data)#Step 9 make cluster predictions
    display_results(kmeans, pred, input_data, data_in, dataset, k_num)#Step 10 display cluster results. Contains function call Step 11 save_output
    exit_check()#Step 12 checks if user wants to exit or start again
    
def get_input(): #Step 1 select which dataset to use
    print('\nPlease select which dataset to analyse by entering the number.')#prompts user to select which dataset to use
    print('\n1 = Mall Customer Data. 3 Columns of Data')
    print('\n2 = Heart Disease UCI. 14 Columns of Data\n')
    data_str = input()#get user input
    if data_str.isdigit()== True: #check if input is number
        data_in = int(data_str)
        if data_in >2:#check if input is higher than 2
            print('\nNumber too high, Please try again.\n')
            get_input()
        if data_in <1:#check if input is lower than 1
            print('\nNumber too low, Please try again.\n')
            get_input()
        else:
            return data_in#return user input
    else:
        print('\nInput was not a number, Please try again.\n')#if input is character, try again
        get_input()
        
def data_read(data_in): #Step 2 import dataset
    if data_in == 1:#checks which dataset has been selected
        try:
            print('\nLoading - Mall Customers')#load mall customers dataset
            dataset=pd.read_csv("dataset/Mall_customers.csv")#load dataset csv from file
            return dataset
        except IOError as e:
            print('error loading dataset')#if dataset not found, error shown
    else:
        try:
            print('\nLoading - Heart Disease UCI dataset')#load Heart_Disease_UCI dataset
            dataset=pd.read_csv("dataset/Heart_Disease_UCI.csv")#load dataset csv from file
            return dataset
        except IOError as e:
            print('error loading dataset')#if dataset not found, error shown

def extract_data(dataset, data_in):#Step 3 extract values from dataset
    if data_in == 1:
        data=dataset.iloc[:, [2,3,4]].values#selects which columns from dataset to use, first column = 0
        return data
    else:
        data=dataset.iloc[:, [0,1,2,3,4,5,6,7,8,9,10,11,12,13]].values#selects which columns from dataset to use, first column = 0
        return data

def print_summary(dataset):#Step 4 print summary of dataset
    print('Data loaded\n')
    print('\nDataset Sample\n')
    print(dataset.head())#Displays top lines of dataset
    print('\nDataset Statistics\n')
    print(dataset.describe())#Displays Statistics of dataset   

def scalar_opt(data):#Step 5 determine if data should be normalised
    print('\nWould you like to normalise the data? (Between -1 and 1)')
    print('\nY or N\n')
    sc_opt = input()
    if sc_opt.isdigit()== False:#checks if input is digit, if it is try again.
        if sc_opt== 'Y' or 'y' or 'Yes' or 'yes':#variations of yes to accept
            print('\nNormalising Data to between -1 and 1')
            scaler = StandardScaler()#initialise scalr function
            input_data = scaler.fit_transform(data)#convert data to normalised values
            return input_data#return normalised data
        if sc_opt== 'N' or 'n' or 'No' or 'no':#variations of no to accept
            input_data = data
            return input_data#return non normalised data
        else:
            print('\nInput not Y or N. Please try again.')
            scalar_opt()
    else:
        print('\nInput not Y or N. Please try again.')
        scalar_opt()

def get_sse(input_data):#Step 6 determine Sum Sqr Err, elbow method
    print('\nCalculating SSE results for Elbow Method Graph')
    SSE = []#array to store results
    for cluster in range(1,15):#range of clusters to test between 1 and 15
        kmeans = KMeans(n_clusters = cluster, init='k-means++')#initialise KMeans
        kmeans.fit(input_data)#input data
        SSE.append(kmeans.inertia_)#adds cluster inertia to array
    return SSE
          
def display_elbow(data_in, SSE):#Step 7 display Elbow graph
    title1 = 'Mall Customer Data\n'
    title2 = 'Heart Disease UCI Data\n'
    print('\nPlease identify number of clusters from Elbow Graph')#instructions for selecting cluster number
    print('\nwhere vertical changes to horizontal')
    frame = pd.DataFrame({'Cluster':range(1,15), 'SSE':SSE})#stores results in a dataframe so graphs can be made
    plt.figure(figsize=(8,5))#set graph size
    plt.plot(frame['Cluster'], frame['SSE'], marker='o')#sets which data labels to use and the graph marker type
    plt.xlabel('Number of clusters')#x axis label
    plt.ylabel('Inertia')#y axis label
    if data_in == 1:
        plt.title(title1 + 'Sum of Squared Error (SSE) - Elbow Method')#graph title
    else:
        plt.title(title2 + 'Sum of Squared Error (SSE) - Elbow Method')#graph title
    plt.tight_layout()
    plt.show(block=False)#show graph block=false stops the plt show pausing the code

def get_knum():#Step 8 determine number of clusters
    print('\nEnter the number of cluster (max 15):\n')#user asked for number of cluster
    k_num_str = input()#user input str
    if k_num_str.isdigit()== True:
        k_num = int(k_num_str)#convert str to int
        if k_num >15:#program currently limited to 15 clusters, to add more, additional colours must be added to graph "colour" variable
            print('\nNumber too high, Please try again.\n')
            get_knum()
        if k_num <1:#check if input too low
            print('\nNumber too low, Please try again.\n')
            get_knum()
        else:
            return k_num#return k number, number of clusters
    else:
        print('\nInput was not a number, Please try again.\n')
        get_knum()#if input is character, try again

def prediction(k_num, input_data):#Step 9 make cluster predictions
    k_num_str = str(k_num)#convert int to str
    print('\nBeginning K-Means With '+k_num_str+' Centroids')
    kmeans = KMeans(n_clusters = k_num, init='k-means++')#initialise Kmeans with chosen number of clusters
    kmeans.fit(input_data)#input data
    pred = kmeans.predict(input_data)#store predictions
    return kmeans, pred

def display_results(kmeans, pred, input_data, data_in, dataset, k_num):#Step 10 display cluster results. Contains function call for Step 11 save_output
    frame = pd.DataFrame(input_data)#stores data in a dataframe so graphs can be made
    frame['cluster'] = pred #adds predictions to dataframe
    print('\nCluster Populations\n')
    print(frame['cluster'].value_counts()) #prints number of members per cluster
    y_kmeans = kmeans.fit_predict(input_data)#creates list of which cluster each datapoint belongs
    if data_in == 1:#if dataset is Mall customers
        colour=['magenta', 'green', 'blue', 'cyan', 'orange', 'purple', 'yellow', 'yellowgreen', 'maroon','plum','olive','magenta','grey','black','beige']#colours to be used in graph
        fig = plt.figure(figsize=(10,8))#create graph size
        ax = fig.add_subplot(projection='3d')#make graph 3D
        for c_num in range(k_num):#loop in range of number of clusters
            label_text = 'Cluster ' + str(c_num+1)#increment cluster name
            ax.scatter(input_data[y_kmeans==c_num, 0], input_data[y_kmeans==c_num, 1],input_data[y_kmeans==c_num, 2], c=colour[c_num], label = label_text, marker='x')#add cluster to graph each loop
        ax.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1],kmeans.cluster_centers_[:, 2], c='red', marker='o')#add centroids to graph
        ax.set_xlabel('Age')#x axis label
        ax.set_ylabel('Income')#y axis label
        ax.set_zlabel('Spending Score')#z axis label
        plt.title('Mall Customer Data points and cluster centroids')#graph title1
        plt.legend(loc='upper left')#enable legend, determine location
        plt.tight_layout()
        save_output(data_in, k_num, dataset, pred)#save output to file
        plt.show(block=False)#show 3d graph
    else:#if dataset is Heart Disease UCI data
        print('\nData has too many dimensions for graph. Saving to file')#Heart Disease UCI dataset has too many dimensions for graph.
        save_output(data_in, k_num, dataset, pred)#save output to file

def save_output(data_in, k_num, dataset, pred):#Step 11 saves copy of original CSV with results appended
    k_num_str = str(k_num)#convert int to str
    save_frame = pd.DataFrame(dataset)#create frame with original dataset
    save_frame['Cluster'] = pred#appends frame with predictions
    prefix = 'saves/' + k_num_str + ' Clusters output '#create save file prefix and location
    if data_in == 1:#create filename for mall customers
        file_name = prefix + 'Mall_customers_output.csv'
    else:#create filename for Heart Disease UCI dataset
        file_name = prefix + 'Heart_Disease_UCI_output.csv'
    print('\nSaving file: ' + file_name)
    save_frame.to_csv(file_name)#save file to directory

def exit_check():#Step 12 checks if user wants to exit or start again
    print('\nWould you like to exit, or start again? Select by entering the number.')#prompts user to select which option
    print('\n1 = Start Again')
    print('\n2 = Exit\n')
    exit_input = input()#get user input
    if exit_input.isdigit()== True: #check if input is number
        exit_int = int(exit_input)
        if exit_int >2:#check if input is higher than 2
            print('\nNumber too high, Please try again.\n')
            get_input()
        if exit_int <1:#check if input is lower than 1
            print('\nNumber too low, Please try again.\n')
            get_input()
        else:
            if exit_int == 1:
                start_program()#return to start of program
            else:
                print('\nProgram will now exit. Goodbye!')#prints exit message, code will then continue to line 213 and exit.
    else:
        print('\nInput was not a number, Please try again.\n')#if input is character, try again
        get_input()

#Program Starts here
start_program()#Tasks contained in function so it can start again if requested.


