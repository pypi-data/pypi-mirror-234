import os
import sys
import time
import pytz
import json
import fsspec
import urllib3
import requests
import numpy as np
import pandas as pd
from datetime import timedelta
from cryptography.fernet import Fernet
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from concurrent.futures import ThreadPoolExecutor
pd.options.mode.chained_assignment = None
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class DataAccess:
    def __init__(self, userid, url, key):
        self.userid = userid
        self.url = url
        self.key = key

    def get_caliberation(self, device_id, metadata, df, onpremise=False):
        """
        :param onpremise:
        :param metadata:
        :param df: Dataframe
        :param device_id: string
        :return: Calibrated dataframe

        Perform cal on original data
             y = mx + c
             if y is greater than max value replace y with max value
             if y is less than min value replace y with min value

        """
        sensor_name_list = list(df.columns)
        sensor_name_list.remove('time')
        if "(" not in sensor_name_list[0]:
            sensor_id_list = sensor_name_list
        else:
            sensor_id_list = [s[s.rfind("(") + 1:s.rfind(")")] for s in sensor_name_list]

        if len(metadata) == 0:
            metadata = DataAccess.get_device_metadata(self, device_id, onpremise=onpremise)
        data = metadata['params']

        for (value1, value2) in zip(sensor_id_list, sensor_name_list):
            df_meta = pd.DataFrame(data[str(value1)])
            df_meta = df_meta.set_index('paramName').transpose()
            if 'm' in df_meta.columns and 'c' in df_meta.columns:
                m = float(df_meta.iloc[0]['m'])
                c = float(str(df_meta.iloc[0]['c']).replace(',', ''))
                df[str(value2)] = df[str(value2)].replace('BAD 255', '-99999').replace('-', '99999').replace(
                    'BAD undefined', '-99999').replace('BAD 0', '-99999').replace('true', True).replace('false', False)
                df[str(value2)] = df[str(value2)].astype('float')
                df[str(value2)] = (df[str(value2)] * m) + c
                if 'min' in df_meta.columns:
                    min_value = float(df_meta.iloc[0]['min'])
                    df[str(value2)] = np.where(df[str(value2)] <= min_value, min_value, df[str(value2)])
                if 'max' in df_meta.columns:
                    max_value_str = str(df_meta.iloc[0]['max']).replace('-', '99999').replace(
                        '1000000000000000000000000000', '99999').replace('100000000000', '99999')
                    max_value = float(max_value_str)
                    df[str(value2)] = np.where(df[str(value2)] >= max_value, max_value, df[str(value2)])

        return df

    def get_device_metadata(self, device_id, onpremise=False):
        """

        :param onpremise:
        :param device_id: string
        :return: Json

         Every detail related to a particular device like device added date, calibration values, sensor details etc

        """
        try:
            if str(onpremise).lower() == 'true':
                url = "http://" + self.url + "/api/metaData/device/" + device_id
            else:
                url = "https://" + self.url + "/api/metaData/device/" + device_id
            header = {'userID': self.userid}
            payload = {}
            response = requests.request('GET', url, headers=header, data=payload, verify=False)
            if response.status_code != 200:
                raw = json.loads(response.text)
                raise ValueError(raw['error'])
            else:
                raw_data = json.loads(response.text)['data']
                return raw_data

        except Exception as e:
            print('Failed to fetch device Metadata')
            print(e)

    def get_sensor_alias(self, device_id, df, raw_metadata, onpremise=False):
        """

        :param onpremise:
        :param raw_metadata: json of device metadata
        :param device_id: string
        :param df: Dataframe
        :return: dataframe with columns having sensor alias

        Maps sensor_alias/ sensor name with corresponding sensor ID
        replaces column names with sensor_alias_sensor_id

        """
        sensors = list(df.columns)
        sensors.remove('time')
        if len(raw_metadata) == 0:
            raw_metadata = DataAccess.get_device_metadata(self, device_id, onpremise=onpremise)
        sensor_spec = 'sensors'
        sensor_param_df = pd.DataFrame(raw_metadata[sensor_spec])
        for sensor in sensors:
            sensor_param_df1 = sensor_param_df[sensor_param_df['sensorId'] == sensor]
            if len(sensor_param_df1) != 0:
                sensor_name = sensor_param_df1.iloc[0]['sensorName']
                sensor_name = sensor_name + " (" + sensor + ")"
                df.rename(columns={sensor: sensor_name}, inplace=True)
        return df, raw_metadata

    def time_grouping(self, df, bands, compute=None):
        """

        :param compute:
        :param df: DataFrame
        :param bands: 05,1W,1D
        :return: Dataframe

        Group time series DataFrame
        Example: The values in Dataframe are at 30s interval we can group and change the 30s interval to 5 mins, 10 mins, 1 day or 1 week.
        The resultant dataframe contains values at given interval.
        """

        df['Time'] = pd.to_datetime(df['time'])
        df.sort_values("Time", inplace=True)
        df = df.drop(['time'], axis=1)
        df = df.set_index(['Time'])
        df.index = pd.to_datetime(df.index)
        if compute is None:
            df = df.groupby(pd.Grouper(freq=str(bands) + "Min")).mean()
        else:
            df = df.groupby(pd.Grouper(freq=str(bands) + "Min")).apply(compute)
        df.reset_index(drop=False, inplace=True)
        return df

    def get_cleaned_table(self, df):
        """

        :param df: Raw Dataframe
        :return: Pivoted DataFrame

        The raw dataframe has columns like time, sensor, values.
        The resultant dataframe will be time sensor alias - sensor id along with their corresponding values

        """

        df = df.sort_values('time')
        df.reset_index(drop=True, inplace=True)
        results = df.pivot(index='time', columns='sensor', values='value')
        results.reset_index(drop=False, inplace=True)
        return results

    def get_device_details(self, onpremise=False):
        """

        :return: Details Device id and Device Name of a particular account

        Dataframe with columne device ids and device names.

        """
        try:
            if str(onpremise).lower() == 'true':
                url = "http://" + self.url + "/api/metaData/allDevices"
            else:
                url = "https://" + self.url + "/api/metaData/allDevices"
            header = {'userID': self.userid}
            payload = {}
            response = requests.request('GET', url, headers=header, data=payload, verify=False)

            if response.status_code != 200:
                raw = json.loads(response.text)
                raise ValueError(raw['error'])
            else:
                raw_data = json.loads(response.text)['data']
                df_raw = pd.DataFrame(raw_data)
                return df_raw

        except Exception as e:
            print('Failed to fetch device Details')
            print(e)

    def get_load_entities(self, onpremise=False, clusters=None):
        try:
            if type(clusters) == list:
                len_clusters = len(clusters)
                if len_clusters == 0:
                    raise Exception('Message: No clusters provided')
            elif clusters is None:
                pass
            else:
                raise Exception('Message: Incorrect type of clusters')

            page_count = 1
            cluster_count = 1
            while True:
                if str(onpremise).lower() == 'true':
                    url = "http://" + self.url + "/api/metaData/getAllClusterData/" + self.userid + "/" + str(
                        page_count) + "/" + str(cluster_count)
                else:
                    url = "https://" + self.url + "/api/metaData/getAllClusterData/" + self.userid + "/" + str(
                        page_count) + "/" + str(cluster_count)
                header = {'userID': self.userid}
                payload = {}
                result = []
                response = requests.request('GET', url, headers=header, data=payload, verify=False)
                if response.status_code == 200 and "error" not in json.loads(response.text):
                    raw_data = json.loads(response.text)
                    result = result + raw_data["data"]
                    total_count = json.loads(response.text)['totalCount']
                    cluster_names = [item['name'] for item in raw_data['data']]
                    page_count = page_count + 1
                    cluster_count = total_count
                    if len(cluster_names) == total_count:
                        break
                    if response.status_code != 200:
                        raw = json.loads(response.text)["error"]
                        if raw == "The requested page does not exist as the number of elements requested exceeds the total count.":
                            page_count = page_count - 1
                        else:
                            raise ValueError(raw['error'])
                else:
                    page_count = page_count - 1
            if clusters is None:
                return result
            else:
                cluster_dict = []
                for cluster_name in clusters:
                    desired_dict = next((item for item in result if item['name'] == cluster_name), None)
                    cluster_dict.append(desired_dict)
                return cluster_dict
        except Exception as e:
            print('Failed to Fetch Load Entities \t', e)

    def get_cloud_credentials(self, db):
        try:
            header = {"userID": self.userid}
            payload = {}
            url = "https://" + self.url + "/api/metaData/getCredentials/" + str(db)
            response = requests.request('GET', url, headers=header, json=payload, verify=False)
            if response.status_code != 200:
                raw = json.loads(response.text)
                raise ValueError(raw)
            else:
                credentials = json.loads(response.text)['data']
                cipher = Fernet(self.key)
                if type(credentials) == list:
                    credentials[0] = cipher.decrypt(credentials[0].encode('utf-8')).decode()

                    credentials[1] = cipher.decrypt(credentials[1].encode('utf-8')).decode()
                else:
                    credentials = cipher.decrypt(credentials.encode('utf-8')).decode()
                return credentials
        except Exception as e:
            print(e)

    def get_userinfo(self,onpremise=False):
        """
        :return: Json

        Details like phone,name,gender,emailed etc are fetched
        """
        try:
            if str(onpremise).lower() == 'true':
                url = "http://" + self.url + "/api/metaData/user"
            else:
                url = "https://" + self.url + "/api/metaData/user"
            header = {'userID': self.userid}
            payload = {}
            response = requests.request('GET', url, headers=header, data=payload, verify=False)

            if response.status_code != 200:
                raw = json.loads(response.text)
                raise ValueError(raw['error'])
            else:
                raw_data = json.loads(response.text)['data']
                return raw_data

        except Exception as e:
            print('Failed to fetch user Information')
            print("Error: \t",e)

    def get_dp(self, device_id, sensors=None, n=1, cal=True, end_time=None, alias=True, IST=True,
               onpremise=False):
        """

        :param device_id: string
        :param sensors: list/None
        :param n: int
        :param cal: bool
        :param end_time: datetime/string
        :param alias: bool
        :param IST: bool
        :param onpremise: bool
        :return: DataFrame
        """
        metadata = {}
        if sensors is None:
            metadata = DataAccess.get_device_metadata(self, device_id, onpremise=onpremise)
            data_sensor = metadata['sensors']
            df_sensor = pd.DataFrame(data_sensor)
            sensor_id_list = list(df_sensor['sensorId'])
            sensors = sensor_id_list

        rawdata_res = []
        temp = ''
        time_zone = time.tzname[0]
        if time_zone == "IST":
            time_zone = "India Standard Time"
        if end_time is None:
            end_time = datetime.now(pytz.timezone("Asia/Kolkata"))
            end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
        try:
            end_time = datetime.strptime(str(end_time), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            try:
                end_time = datetime.strptime(str(end_time), '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    end_time = datetime.strptime(str(end_time), "%Y-%m-%d %H:%M:%S.%f%z").strftime('%Y-%m-%d %H:%M:%S')
                except:
                    end_time = str(end_time) + " 23:59:59" if isinstance(end_time, str) else end_time
        e_time = pd.to_datetime(end_time)
        if time_zone == "India Standard Time":
            e_time = e_time - timedelta(hours=5.5)
        if time_zone == "UTC":
            e_time = e_time - timedelta(hours=5.5)
        en_time = int(round(e_time.timestamp())) * 10000
        if type(sensors) == list:
            len_sensors = len(sensors)
            if len_sensors == 0:
                raise Exception('Message: No sensors provided')
            if n < 1:
                raise ValueError('Incorrect number of data points')
            n = int(n) * len_sensors
            delimiter = ","
            sensor_values = delimiter.join(sensors)
        else:
            raise Exception('Message: Incorrect type of sensors')
        header = {}
        cursor = {'end': en_time, 'limit': n}
        payload = {}
        df = pd.DataFrame()
        counter = 0
        while True:
            for record in range(counter):
                sys.stdout.write('\r')
                sys.stdout.write("Approx Records Fetched %d" % (10000 * record))
                sys.stdout.flush()
            if str(onpremise).lower() == "true":
                url = "http://" + self.url + "/api/apiLayer/getLimitedDataMultipleSensors/?device=" + device_id + "&sensor=" + sensor_values + "&eTime=" + str(
                    cursor['end']) + "&lim=" + str(cursor['limit']) + "&cursor=true"
            else:
                url = "https://" + self.url + "/api/apiLayer/getLimitedDataMultipleSensors/?device=" + device_id + "&sensor=" + sensor_values + "&eTime=" + str(
                    cursor['end']) + "&lim=" + str(cursor['limit']) + "&cursor=true"
            response = requests.request("GET", url, headers=header, data=payload)
            raw = json.loads(response.text)
            if response.status_code != 200:
                raise ValueError(response.status_code)
            if 'success' in raw:
                raise ValueError(raw)
            else:
                raw_data = json.loads(response.text)['data']
                cursor = json.loads(response.text)['cursor']
                if len(raw_data) != 0:
                    df = pd.concat([df, pd.DataFrame(raw_data)])
                counter = counter + 1
            if cursor['end'] is None:
                break
        if len(df) != 0:
            df['time'] = pd.to_datetime(df['time'])
            if IST and time_zone == "India Standard Time":
                df['time'] = df['time'].dt.tz_convert('Asia/Kolkata')
            if IST and time_zone == "UTC":
                df['time'] = df['time'].dt.tz_convert('Asia/Kolkata')
            df['time'] = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S.%f')
            df = DataAccess.get_cleaned_table(self, df)
            if str(alias).lower() == "true":
                df, metadata = DataAccess.get_sensor_alias(self, device_id, df, metadata, onpremise=onpremise)
            if str(cal).lower() == 'true':
                df = DataAccess.get_caliberation(self, device_id, metadata, df, onpremise=onpremise)
        return df

    def influxdb(self, device_id, sensors, start_time, end_time=None, onpremise=False, IST=True,
                 echo=True):
        """
        :param device_id: string
        :param sensors: list/None
        :param start_time: datetime/string
        :param end_time: datetime/string
        :param onpremise: bool
        :param IST: bool
        :param echo: bool
        :return: DataFrame
        """
        metadata = {}
        if sensors is None:
            metadata = DataAccess.get_device_metadata(self, device_id, onpremise=onpremise)
            data_sensor = metadata['sensors']
            df_sensor = pd.DataFrame(data_sensor)
            sensor_id_list = list(df_sensor['sensorId'])
            sensors = sensor_id_list
        rawdata_res = []
        temp = ''
        time_zone = time.tzname[0]
        if time_zone == "IST":
            time_zone = "India Standard Time"
        flag = 0
        if end_time is None:
            end_time = datetime.now(pytz.timezone("Asia/Kolkata"))
            end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
            flag = 1
        try:
            end_time = datetime.strptime(str(end_time), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            try:
                end_time = datetime.strptime(str(end_time), '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    end_time = datetime.strptime(str(end_time), "%Y-%m-%d %H:%M:%S.%f%z").strftime('%Y-%m-%d %H:%M:%S')
                except:
                    end_time = str(end_time) + " 23:59:59" if isinstance(end_time, str) else end_time
        try:
            start_time = datetime.strptime(str(start_time), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            try:
                start_time = datetime.strptime(str(start_time), '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    start_time = datetime.strptime(str(start_time), "%Y-%m-%d %H:%M:%S.%f%z").strftime(
                        '%Y-%m-%d %H:%M:%S')
                except:
                    start_time = str(start_time) + " 00:00:00" if isinstance(start_time, str) else start_time
        s_time = pd.to_datetime(start_time)
        e_time = pd.to_datetime(end_time)
        if time_zone == "India Standard Time":
            s_time = s_time - timedelta(hours=5.5)
            e_time = e_time - timedelta(hours=5.5)
        if time_zone == "UTC":
            s_time = s_time - timedelta(hours=5.5)
            e_time = e_time - timedelta(hours=5.5)
        st_time = int(round(s_time.timestamp())) * 10000
        en_time = int(round(e_time.timestamp())) * 10000
        header = {}
        payload = {}
        counter = 0
        cursor = {'start': st_time, 'end': en_time}
        while True:
            if echo:
                for record in range(counter):
                    sys.stdout.write('\r')
                    sys.stdout.write("Approx Records Fetched %d" % (10000 * record))
                    sys.stdout.flush()
            if sensors is not None:
                if str(onpremise).lower() == 'true':
                    url_api = "http://" + self.url + "/api/apiLayer/getAllData?device="
                else:
                    url_api = "https://" + self.url + "/api/apiLayer/getAllData?device="
                if counter == 0:
                    str1 = ","
                    sensor_values = str1.join(sensors)
                    temp = url_api + device_id + "&sensor=" + sensor_values + "&sTime=" + str(
                        st_time) + "&eTime=" + str(
                        en_time) + "&cursor=true&limit=50000"
                else:
                    str1 = ","
                    sensor_values = str1.join(sensors)
                    temp = url_api + device_id + "&sensor=" + sensor_values + "&sTime=" + str(
                        cursor['start']) + "&eTime=" + str(cursor['end']) + "&cursor=true&limit=50000"
            response = requests.request("GET", temp, headers=header, data=payload)
            raw = json.loads(response.text)
            if response.status_code != 200:
                raise ValueError(raw['error'])
            if 'success' in raw:
                raise ValueError(raw['error'])
            else:
                raw_data = json.loads(response.text)['data']
                cursor = json.loads(response.text)['cursor']
                if len(raw_data) != 0:
                    rawdata_res = rawdata_res + raw_data
                counter = counter + 1
            if cursor['start'] is None or cursor['end'] is None:
                break

        df = pd.DataFrame(rawdata_res)
        if len(df) != 0:
            df['time'] = pd.to_datetime(df['time'])
            if IST and time_zone == "India Standard Time":
                df['time'] = df['time'].dt.tz_convert('Asia/Kolkata')
            if IST and time_zone == "UTC":
                df['time'] = df['time'].dt.tz_convert('Asia/Kolkata')
            df['time'] = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S.%f')
            if len(df.columns) == 2:
                df['sensor'] = sensors[0]
            df = DataAccess.get_cleaned_table(self, df)
        return df

    def data_query(self, device_id, sensors, start_time, end_time=None, db=None, alias=True, cal=True,
                   bands=None, onpremise=False, compute=None, IST=True):
        """
        :param device_id: string
        :param sensors: list
        :param start_time:datetime/string
        :param end_time: datetime/string
        :param db: gcs,s3,az
        :param alias: bool
        :param cal: bool
        :param bands:
        :param onpremise: bool
        :param compute: mean, min, max functions
        :param IST: Indian Standard Time
        :return: Dataframe
        If requested data exists in feature store fetch data from the container.
        IF data is not available the data is fetched from influxdb
        """

        def get_month_year(filename):
            month, year = map(int, filename.split('.')[0].split('-'))
            return datetime(year, month, 1)

        def generate_month_year_dates(start_date, end_date):
            end_date = end_date.strftime("%Y-%m-%d %H:%M:%S") if isinstance(end_date, datetime) else str(end_date)
            start_date = str(start_date) + " 00:00:00" if len(str(start_date).split()) == 1 else str(start_date)
            end_date = str(end_date) + " 00:00:00" if len(str(end_date).split()) == 1 else str(end_date)

            try:
                current_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
                end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
            except:
                current_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S.%f")

            dates = []
            while str(current_date) <= str(end_date):
                month = str(current_date.month)
                month_year = month + "-" + str(current_date.year) + ".parquet"
                dates.append(month_year)
                current_date += relativedelta(months=1)
                current_date = current_date.replace(day=1)

            return dates

        def read_one(filename):
            with connector.open(container_name + str(device_id) + "/" + str(filename),
                                "rb") as src_file:
                df = pd.read_parquet(src_file)
            return df

        def thread_read(filenames_list):
            if len(filenames_list) != 0:
                with ThreadPoolExecutor(max_workers=40) as executor:  # function to thread
                    for record in range(len(filenames_list)):
                        sys.stdout.write('\r')
                        sys.stdout.write("Please Wait .. ")
                        sys.stdout.flush()
                    results = executor.map(read_one, filenames_list)
                fetched_df = pd.concat(results, axis=0)
            else:
                fetched_df = pd.DataFrame()
            return fetched_df

        df = pd.DataFrame()
        metadata = {}
        connector = None
        container_name = None

        if db is not None:
            flag = 0
            time_zone = time.tzname[0]
            if time_zone == "IST":
                time_zone = "India Standard Time"
            if end_time is None:
                end_time = datetime.now(pytz.timezone("Asia/Kolkata"))
                end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
                flag = 1
            try:
                end_time = datetime.strptime(str(end_time), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    end_time = datetime.strptime(str(end_time), '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')
                except ValueError:
                    try:
                        end_time = datetime.strptime(str(end_time), "%Y-%m-%d %H:%M:%S.%f%z").strftime(
                            '%Y-%m-%d %H:%M:%S')
                    except:
                        end_time = str(end_time) + " 23:59:59" if isinstance(end_time, str) else end_time
            try:
                start_time = datetime.strptime(str(start_time), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    start_time = datetime.strptime(str(start_time), '%Y-%m-%d %H:%M:%S.%f').strftime(
                        '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    try:
                        start_time = datetime.strptime(str(start_time), "%Y-%m-%d %H:%M:%S.%f%z").strftime(
                            '%Y-%m-%d %H:%M:%S')
                    except:
                        start_time = str(start_time) + " 00:00:00" if isinstance(start_time, str) else start_time
            credentials = DataAccess.get_cloud_credentials(self, db)
            if len(credentials) != 0:
                credentials = eval(credentials)
                connector = fsspec.filesystem("gs", project=credentials['project_id'],
                                              token=credentials)
                container_name = "faclon-ds-feature-store/"

                blobs = connector.ls(container_name)
                device_list = [blob.split("/")[1] for blob in blobs]
                if device_id in device_list:
                    blobs = [blob_name.split("/")[2] for blob_name in
                             connector.ls(container_name + str(device_id) + "/")]
                    dates = generate_month_year_dates(start_time, end_time)
                    filenames = list(set(dates).intersection(blobs))
                    filenames = sorted(filenames, key=get_month_year)
                    df = thread_read(filenames)
                if len(df) != 0:
                    try:
                        start_time = datetime.strptime(str(start_time), '%Y-%m-%d %H:%M:%S')
                        end_time = datetime.strptime(str(end_time), '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        pass
                    except Exception as e:
                        print('Message:', e)
                    df = df[(df['time'] >= start_time) & (df['time'] <= end_time)]
                    if len(df) != 0:
                        if sensors is None:
                            sensors = list(df.columns)
                            sensors.remove('time')

                        sensors_filtered = list(set(df.columns).intersection(sensors))
                        if sensors and len(sensors_filtered) != 0:
                            sensors_filtered.insert(0, 'time')
                            df = df[sensors_filtered]
                        else:
                            df = pd.DataFrame()
                        df.sort_values(['time'], inplace=True)
                        df.reset_index(drop=True, inplace=True)
                        last_date = df['time'].iloc[-1]
                        last_date = last_date.to_pydatetime()
                        date1 = datetime.strptime(str(last_date), '%Y-%m-%d %H:%M:%S.%f')
                        try:
                            date2 = datetime.strptime(str(end_time), '%Y-%m-%d %H:%M:%S')
                        except:
                            date2 = datetime.strptime(str(end_time), '%Y-%m-%d %H:%M:%S.%f')
                        difference = date2 - date1
                        if difference.seconds >= 3600 or difference.seconds >= 60:
                            if time_zone == "UTC" and flag == 0:
                                last_date = last_date + timedelta(hours=5.5)
                                end_time = end_time + timedelta(hours=5.5)
                            df1 = DataAccess.influxdb(self, device_id, start_time=last_date,
                                                      end_time=end_time, sensors=sensors, echo=True,
                                                      onpremise=False, IST=True)
                            df = pd.concat([df, df1])
                            df.reset_index(drop=True, inplace=True)
                        if IST is False:
                            df['time'] = pd.to_datetime(df['time']) - timedelta(hours=5.5)
        else:
            df_devices = DataAccess.get_device_details(self, onpremise=onpremise)
            device_list = df_devices['devID'].tolist()
            if device_id in device_list:
                df = DataAccess.influxdb(self, device_id, sensors, start_time, end_time=end_time, onpremise=onpremise,
                                         IST=IST, echo=True)
            else:
                raise Exception('Message: Device not added in account')

        if len(df) != 0:
            df['time'] = pd.to_datetime(df['time'])
            if str(alias).lower() == "true":
                df, metadata = DataAccess.get_sensor_alias(self, device_id, df, metadata, onpremise=onpremise)
            if str(cal).lower() == 'true':
                df = DataAccess.get_caliberation(self, device_id, metadata, df, onpremise=onpremise)
            if bands is not None:
                df = DataAccess.time_grouping(self, df, bands, compute)
            df = df.set_index(['time'])
            df = df.fillna(value=np.nan)
            df.dropna(axis=0, how='all', inplace=True)
            df.reset_index(drop=False, inplace=True)
            df.drop_duplicates(inplace=True)
        return df