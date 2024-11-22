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

import ftplib
import os
import shutil
import zipfile

import pandas as pd

import settings
import settings as ts

WEB_network = {'domain': '192.107.92.192', 'port': '21', 'user': 'ftpthule', 'pass': 'bdg1971'}
WEB_base_folder = 'Moonglow'

local = os.path.join(settings.basefolder, 'thaao_skycam')
dest = os.path.join(settings.basefolder, 'thaao_skycam', 'tmp')

instr = 'skycam'

date_list = pd.date_range(
        ts.instr_metadata[instr]['start_instr'], ts.instr_metadata[instr]['end_instr'], freq='D').tolist()

if __name__ == "__main__":

    for i in date_list:
        with zipfile.ZipFile(
                os.path.join(local, i.strftime('%Y'), i.strftime('%Y%m%d') + '.zip')) as zipf:
            listOfFileNames = zipf.namelist()
            # Iterate over the file names
            for fileName in listOfFileNames:
                # Check filename endswith csv
                if fileName.endswith('5_raw.jpg') | fileName.endswith('0_raw.png'):
                    # Extract a single file from zip
                    zipf.extract(fileName, dest)

        p = os.listdir(os.path.join(dest, i.strftime('%Y%m%d')))

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
