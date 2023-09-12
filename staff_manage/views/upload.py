import os
from django.conf import settings
from django.shortcuts import render, HttpResponse, redirect
from staff_manage import models
from staff_manage.utils.forms import UpForm, UpModelForm


def upload_form(request):
    """上传文件（Form版）"""
    title = "文件上传(Form)"
    if request.method == "GET":
        form = UpForm()
        return render(request, 'upload_form.html', {'form': form, 'title': title})

    form = UpForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 读取图片内容
        image_object = form.cleaned_data.get("img")
        # 文件存储路径
        # media_path = os.path.join("settings.MEDIA_ROOT", image_object.name)  # 绝对路径
        media_path = os.path.join("media", image_object.name)
        # 写入到文件夹中
        f = open(media_path, mode="wb")
        for chunk in image_object.chunks():
            f.write(chunk)
        f.close()
        # 将图片文件路径写入到数据库
        models.Boss.objects.create(
            name=form.cleaned_data['name'],
            age=form.cleaned_data['age'],
            img=media_path,
        )
        return HttpResponse("上传成功")

    # 校验失败(显示错误信息)
    return render(request, 'upload_form.html', {'form': form, 'title': title})


def upload_modelform(request):
    """上传文件（ModelForm版）"""
    title = "文件上传(ModelForm)"
    if request.method == "GET":
        form = UpModelForm()
        return render(request, 'upload_form.html', {'form': form, 'title': title})

    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect("/city/list/")

    # 校验失败(显示错误信息)
    return render(request, 'upload_form.html', {'form': form, 'title': title})
