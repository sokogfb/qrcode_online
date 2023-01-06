import os
import tempfile
import zipfile

import pandas as pd
import qrcode
import vobject
from django.http import HttpResponse
from django.shortcuts import render

from data.models import Employee
from vcard import settings


def get_qrcode(family_name, given_name, full_name, email, work_phone, mobile_phone, add, website, title, direct_line,
               staff_id, tempdirectory):
    j = vobject.vCard()

    o = j.add('fn')
    o.value = given_name + " " + family_name
    o = j.add('n')
    o.value = vobject.vcard.Name(family=family_name, given=given_name)

    o = j.add('tel')
    o.type_param = "work"
    o.value = work_phone

    o = j.add('tel')
    o.type_param = "cell"
    o.value = mobile_phone

    o = j.add('tel')
    o.type_param = "home"
    o.value = direct_line

    o = j.add('email')
    o.value = email
    o.type_param = 'INTERNET'

    o = j.add('org')
    o.value = ['PANGAEA SECURITIES ', 'LIMITED']

    o = j.add('url')
    o.value = 'www.pangaea.co.zm'

    o = j.add('title')
    o.value = title

    o = j.add('streetname')
    o.value = 'First Floor,Pangaea Office Park, Lusaka Zambia'

    o = j.add('country')
    o.value = 'Zambia'
    # print(j.serialize())

    vcf = j.serialize()

    img = qrcode.make(vcf)

    dirs = tempdirectory + '/temp'
    print(dirs)
    if not os.path.exists(dirs):
        os.makedirs(dirs)
        print('new dir', dirs)
    if (staff_id):
        file_name = str(staff_id)
    else:
        file_name = full_name
    with open(dirs + '/' + file_name + '.png', 'wb') as f:
        img.save(f)
    print(vcf)


def compress_file(outFullName, dirpath):
    """
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dirpath, '')

        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zip.close()


# get_qrcode("Hu", "Y.T.James","James Hu","jameshu@xensetech.hk","28383030","65612892","65612892","www.xensetech.hk")
# IO = 'data.xlsx'
# sheet = pd.read_excel(io=IO,keep_default_na=False)
# for i in range(len(sheet)):
#     family_name,given_name,full_name,email,work_phone,mobile_phone,fax,website = sheet.values[i]
#     get_qrcode(family_name,given_name,full_name,email,work_phone,mobile_phone,fax,website)
# compress_file('files.zip', 'temp')
# shutil.rmtree('temp')


def my_view(request):
    return render(request, 'index.html')


def upload(request):
    if request.method == 'POST':
        file_dict = request.FILES
        file_data = request.META['HTTP_X_FILE_NAME']
        file_name = file_data.split(".")[0]
        file_type = file_data.split(".")[1]
        print(file_name, file_type)

        if file_type in ["xlsx", "xls"]:
            print("file_type is excel")
        else:
            return render(request, 'index.html')
        print(request.body)

        tempdirectory = tempfile.TemporaryDirectory()
        data_excel = tempfile.NamedTemporaryFile(delete=False, dir=tempdirectory.name)
        data_excel.write(request.body)
        IO = data_excel.name
        sheet = pd.read_excel(io=IO, keep_default_na=False)

        emp = Employee.objects.all()
        for e in emp:
            get_qrcode(e.family_name, e.given_name, e.given_name + e.family_name, e.email, e.work_phone, e.mobile_phone,
                       e.fax, e.website, e.title, e.direct_line, e.id, tempdirectory.name)
        compress_file(tempdirectory.name + '/files.zip', tempdirectory.name + '/temp/')
        print(tempdirectory)
        file = open(tempdirectory.name + '/files.zip', 'rb')
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="file.zip"'

    return response


def detail(request, id):
    emp = Employee.objects.all().filter(id=id)
    for e in emp:
        get_qrcode(e.family_name, e.given_name, e.given_name + e.family_name, e.email, e.work_phone, e.mobile_phone,
                   e.fax, e.website, e.title, e.direct_line, e.id, settings.MEDIA_URL)
    compress_file(settings.MEDIA_URL.title() + '/files.zip', settings.MEDIA_URL + '/temp/')
    print(settings.MEDIA_URL)
    file = open(settings.MEDIA_URL + '/files.zip', 'rb')
    response = HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="file.zip"'

    return response
