from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from staff_manage import models
from staff_manage.utils.bootstrap import BootStrapModelForm, BootStrapForm
from staff_manage.utils.encrypt import md5


class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {"password": forms.PasswordInput(render_value=True)}

    # md5加密 密码重复检验
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)

        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError("不能与以前的密码相同")
        return md5_pwd

    # 钩子方法 确认密码
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致")
        return confirm


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ["username"]


class AdminResetModelForm(AdminModelForm):
    class Meta:
        model = models.Admin
        fields = ["password", "confirm_password"]
        widgets = {"password": forms.PasswordInput(render_value=True)}


class UserModelForm(BootStrapModelForm):
    name = forms.CharField(min_length=2, label="用户名")
    create_time = forms.DateField(label="入职时间")
    create_time.widget.input_type = 'date'

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "account", "create_time", "depart", "gender"]
        widgets = {"password": forms.PasswordInput}


class PrettyAddModelForm(BootStrapModelForm):
    # 手机号格式校验 (正则表达式)
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')],
    )

    class Meta:
        model = models.PrettyNum
        # fields = "__all__"
        fields = ["mobile", "price", "level", "status"]
        # exclude = []

    # 手机号重复校验 (钩子方法)
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()

        if exists:
            # 验证不通过
            raise ValidationError("手机号已存在")
        # 验证通过，用户输入的值返回
        return txt_mobile


class PrettyEditModelForm(BootStrapModelForm):
    # 设置手机号不可编辑
    # mobile = forms.CharField(label="手机号", disabled=True)

    # 手机号格式校验 (正则表达式)
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')],
    )

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]

    # 手机号重复校验 (钩子方法)
    def clean_mobile(self):
        # 当前编辑行的ID
        # print(id=self.instance.pk)
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()

        if exists:
            # 验证不通过
            raise ValidationError("手机号已存在")
        # 验证通过，用户输入的值返回
        return txt_mobile


class LoginForm(BootStrapForm):
    username = forms.CharField(label="用户名", widget=forms.TextInput)
    password = forms.CharField(label="密码", widget=forms.PasswordInput(render_value=True))
    code = forms.CharField(label="验证码", widget=forms.TextInput)

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        exclude = ['oid', 'admin']


class UpForm(BootStrapForm):
    exclude_fields = ['img']
    name = forms.CharField(label="姓名")
    age = forms.IntegerField(label="年龄")
    img = forms.FileField(label="头像")


class UpModelForm(BootStrapModelForm):
    exclude_fields = ['img']
    class Meta:
        model = models.City
        fields = "__all__"
