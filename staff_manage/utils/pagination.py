"""
自定义分页组件

使用事项：
在view.py中:
    def pretty _list(request):
        # 1.根据自己的情况筛选数据
        queryset = models.PrettyNum.objects.all()
        # 2.实例化分页对象
        page_object = Pagination(request, queryset)
        context = {
            "queryset": page_object.page_queryset,  # 分页后的数据
            "page_string": page_object.html()  # 分页组件html
        }
        return render(request, 'pretty_list.html' , context)
在HTML页面中:
    <ul class="pagination">
        {{ page_string }}
    </ul>
"""

from django.utils.safestring import mark_safe
import copy


class Pagination(object):

    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):
        """
        :param request: 请求对象
        :param queryset: 条件查询后的数据
        :param page_size: 每页显示数据量
        :param page_param: URL分页参数 /?page=
        :param plus: 分页组件显示页码量 2 * plus + 1
        """
        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size
        self.start = (page - 1) * page_size
        self.end = page * page_size
        self.page_queryset = queryset[self.start:self.end]
        total_count = queryset.count()  # 数据总条数
        total_page_count, div = divmod(total_count, page_size)  # 总页码, 余数
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus

        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        self.page_param = page_param

    def html(self):
        # 起始页码与结束页码逻辑
        if self.total_page_count <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_page_count
        else:
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus  # 前plus页码
                    end_page = self.page + self.plus  # 后plus页码

        # 分页组件
        page_str_list = []

        # 首页
        self.query_dict.setlist(self.page_param, [1])
        first = '<li><a href="?{}">首页</a></li> '.format(self.query_dict.urlencode())
        page_str_list.append(first)

        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="?{}">上一页</a></li> '.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li><a href="?{}">上一页</a></li> '.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        # 页码
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        # 下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            next = '<li><a href="?{}">下一页</a></li> '.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            next = '<li><a href="?{}">下一页</a></li> '.format(self.query_dict.urlencode())
        page_str_list.append(next)

        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        final = '<li><a href="?{}">尾页</a></li> '.format(self.query_dict.urlencode())
        page_str_list.append(final)

        # 页面跳转框
        jump = """<li>
                  <form style="float: left;margin-left: -1px" method="get">
                    <input name="page" type="text" class="form-control" placeholder="页码"
                           style="position: relative;float: left;display: inline-block;width: 80px;border-radius: 0;">
                    <button style="border-radius: 0" class="btn btn-default" type="submit">跳转</button>
                  </form>
                </li>
                """
        page_str_list.append(jump)

        # 设置字符串安全
        page_string = mark_safe("".join(page_str_list))
        return page_string
