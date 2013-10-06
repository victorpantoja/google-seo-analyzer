# -*- coding: utf-8 -*-
from datetime import datetime
import csv
import logging
import os
import requests
import sys
import time

LOG_FILENAME = 'crw.log'

LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}

try:
    arquivo = sys.argv[1].replace('\\','/')

    if len(sys.argv) > 2:
        level_name = sys.argv[2]
        level = LEVELS.get(level_name, logging.NOTSET)
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',filename=LOG_FILENAME,level=level)
    else:
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',filename=LOG_FILENAME,level=logging.INFO)

    logger = logging.getLogger('crw')

    if os.path.exists(arquivo):
        logger.debug(arquivo+' found!')
        
        urls_dict = []

        with open(arquivo) as arv:
            c = csv.reader(arv)
            errors = []
            c.next()
            for i in c:
                if i[0]:
                    url_dict = {'url': i[0]}

                    if i[1]:
                        url_dict['status_code'] = i[1]

                    urls_dict.append(url_dict)                    
    else:
        logger.critical(arquivo+' invalid file! aborting...')

    urls_dict.sort(key=lambda x: x['url'])

    urls_corretas = []
    urls_com_erro = []
    erros_request = []
    erros_soft = []
    status_code_alterados = []
    total_urls_corretas = 0
    total_status_code_alterados = 0
    total_erros_request = 0
    total_erros_soft = 0
    total_urls_com_erro = 0
    s = requests.Session()
    s.max_redirects = 3
    index = 0
    for url_dict in urls_dict:
        index += 1
        try:
            res = s.get(url_dict['url'])
            status_code_google = url_dict.get('status_code', None)
 
            if res.status_code == 200:
                if res.text.find("Ops!") != -1:
                    erros_soft.append(url_dict['url'])
                    total_erros_soft += 1
                else:
                    urls_corretas.append(url_dict['url'])
                    total_urls_corretas += 1
            else:
                if status_code_google and status_code_google != str(res.status_code):
                     total_status_code_alterados += 1
                     status_code_alterados.append({'url': url_dict['url'],
                                                   'status_code_google': status_code_google,
                                                   'status_code': res.status_code})
                else:
                    urls_com_erro.append(url_dict['url'])
                    total_urls_com_erro += 1
        except Exception, e:
            total_erros_request += 1
            erros_request.append({'url': url_dict['url'], 'error': e})

        progress = index*100 / len(urls_dict)
        percentual = "%.2f%%" % (index*100 / float(len(urls_dict)))
        sys.stdout.write('\r[{0}{1}] {2}'.format('#' * progress,
                                                 ' ' * (100-progress),
                                               percentual))
        sys.stdout.flush()
        
    print("\nGerando relatório...")
        
    with open("report_seo.txt", "w") as report:
         report.write("=" * 75)
         report.write("\nReport Date: {0}\n".format(datetime.now()))
         report.write("Corrected URLs: {0}\n".format(total_urls_corretas))
         report.write("Error URLs: {0}\n".format(total_urls_com_erro))
         report.write("Soft 404: {0}\n".format(total_erros_soft))
         report.write("Changed Status code: {0}\n".format(total_status_code_alterados))
         report.write("HTTP Errors: {0}\n".format(total_erros_request))

         report.write("-" * 75)
         report.write("\nCorrected URLs:\n")
         for url in urls_corretas:
             report.write(url)
             report.write("\n")

         report.write("-" * 75)
         report.write("\nError URLs:\n")
         for url in urls_com_erro:
             report.write(url)
             report.write("\n")

         report.write("-" * 75)
         report.write("\nSoft 404:")
         for url in erros_soft:
             report.write(url)
             report.write("\n")

         report.write("-" * 75)
         report.write("\nHTTP Errors:\n")
         for url in erros_request:
             report.write("{0} - Error: {1}\n".format(url['url'], url['error']))

         report.write("-" * 75)
         report.write("\nChanged Status code:\n")
         for url in status_code_alterados:
             report.write("Request status code {0} changed from {1} to {2}\n".format(url['url'],
                                                                 url['status_code_google'],
                                                                 url['status_code']))
         
         report.write("=" * 75)
            
    print("Report generated!")

except IndexError:
    print('Usage: python crw.py path/to/file/ [debug|info|warning|error|critical]')
