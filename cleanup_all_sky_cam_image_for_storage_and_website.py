#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
#
"""
Brief description
"""

# =============================================================
# CREATED: 
# AFFILIATION: UNIVE, INGV
# AUTHORS: Filippo Cali' Quaglia
# =============================================================
#
# -------------------------------------------------------------------------------
__author__ = "Filippo Cali' Quaglia"
__credits__ = ["??????"]
__license__ = "GPL"
__version__ = "0.1"
__email__ = "filippo.caliquaglia@gmail.com"
__status__ = "Research"
__lastupdate__ = ""

import datetime as dt
import ftplib
import os
import shutil
import zipfile

import pandas as pd

import settings as ts

WEB_network = {'domain': '192.107.92.192', 'port': '21', 'user': 'ftpthule', 'pass': 'bdg1971'}
WEB_base_folder = 'Moonglow'

instr = 'skycam'

date_list_upload = pd.date_range(dt.datetime(2018, 1, 1), dt.datetime(2018, 12, 31), freq='D').tolist()
date_list_zip = pd.date_range(dt.datetime(2018, 1, 1), dt.datetime(2018, 12, 31), freq='D').tolist()
folder = os.path.join(ts.basefolder, "thaao_" + instr)
folder_zip = 'D:\\thaao_skycam_nozip\\'
dest = os.path.join('C:\\Users\\FCQ\\Desktop\\', 'tmp')


def zipdir(path, ziph):
    # ziph is zipfile handle
    # for root, dirs, files in os.walk(path):
    files = os.listdir(path)
    for file in files:
        ziph.write(
                os.path.join(path, file), os.path.relpath(os.path.join(path, file), os.path.join(path, '..')))


def daily_zipping():
    for i in date_list_zip:
        fn = os.path.join(folder_zip, i.strftime('%Y'), i.strftime('%m'), i.strftime('%d'))
        fn_new = os.path.join(folder_zip, i.strftime('%Y'), i.strftime('%m'), i.strftime('%Y%m%d'))
        try:
            shutil.copytree(fn, fn_new)
        except FileNotFoundError as e:
            print(e)
            continue

        try:
            with zipfile.ZipFile(
                    os.path.join(folder, i.strftime('%Y'), i.strftime('%Y%m%d') + '.zip'), 'w') as zipf:
                zipdir(fn_new, zipf)
            print(f'zipped {fn_new}')
            try:
                shutil.rmtree(fn_new)
            except FileNotFoundError as e:
                print(e)
        except:
            print(f'error in zipping file {fn_new}')


def file_upload():
    for i in date_list_upload:
        try:
            with zipfile.ZipFile(
                    os.path.join(folder, i.strftime('%Y'), i.strftime('%Y%m%d') + '.zip')) as zipf:
                listOfFileNames = zipf.namelist()

                # Iterate over the file names
                for fileName in listOfFileNames:
                    # Check filename endswith csv
                    if fileName.endswith('5_raw.jpg') | fileName.endswith('0_raw.jpg'):
                        # Extract a single file from zip
                        zipf.extract(fileName, dest)

            p = os.listdir(os.path.join(dest, i.strftime('%Y%m%d')))
        except (FileNotFoundError, zipfile.BadZipFile) as e:
            print(e)
            continue
        # push data to web
        try:
            ftp = ftplib.FTP(WEB_network['domain'], WEB_network['user'], WEB_network['pass'])
            ftp.cwd(WEB_base_folder)
            ftp.encoding = "utf-8"
        except Exception as e:
            print(e)
            print('Bad connection to server ftp at ' + WEB_network['domain'] + ' (website)')

        for ff in p:
            ffname = 'THULE_IMAGE_' + ff.split(os.sep)[-1][0:13] + '.jpg'

            with open(os.path.join(dest, ff[:8], ff), "rb") as fn:
                try:
                    ftp.storbinary(f"STOR {ffname}", fn)
                    # print(res)
                    print(ffname + ' transfer ' + ' to FTP ' + WEB_network['domain'] + ': SUCCESS')
                except Exception as e:
                    print(e)
                    print(ffname + ' transfer ' + ' to FTP ' + WEB_network['domain'] + ': FAIL')

        ftp.quit()

        shutil.rmtree(os.path.join(dest, p[0][:8]))


def file_from_web_to_storage():
    # Specify the directory path you want to start from
    directory_path = os.path.join(folder_zip, '_2018\\')
    files = list_files_recursive(directory_path)

    for file in files:
        if (file.split('\\')[-1].startswith('THULE_IMAGE_')) & (len(file.split('\\')[-1]) == 29):
            fn_new_fold = os.path.join(folder_zip, '2018', file.split('\\')[-1][16:18], file.split('\\')[-1][18:20])
            try:
                os.makedirs(fn_new_fold, exist_ok=True)
                new_dest = os.path.join(fn_new_fold, file.split('\\')[-1][12:25] + '_raw.jpg')
                shutil.copy(file, new_dest)
                print(new_dest)
            except FileNotFoundError as e:
                print(e)
                continue

    return


def list_files_recursive(path='.'):
    cc = []
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            for i in os.listdir(full_path):
                cc.append(os.path.join(full_path, i))
        else:
            cc.append(full_path)
    return cc


if __name__ == "__main__":
    # compress daily folders from hdd to the drive data storage
    daily_zipping()

    # upload files from the hdd (organized in daily folders) to the thule-atmos-it.it website
    # file_upload()

    # reformat files from web format to hdd
    # file_from_web_to_storage()