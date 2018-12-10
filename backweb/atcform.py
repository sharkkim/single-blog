from django import forms

class AddAtcForm(forms.Form):
    #requir=True 表示必填项
    title=forms.CharField(min_length=1,required=True,
                          error_messages={
                              'required':'文章标题是必填项',
                              'min_length':'文章标题不能少于5字符',}
                          )
    keywords=forms.CharField(min_length=2, required=True,
                             error_messages={
                                 'required': '关键字是必填项',
                                 'min_length': '关键字不能少于5字符', }
                             )
    content=forms.CharField(required=True,
                            error_messages = {
                                'required': '内容是必填项', }
                            )
    # picture=forms.ImageField(required=True,error_messages={'required':'图片不能为空'})


class EditAtcForm(forms.Form):
    title = forms.CharField(min_length=1, required=True,
                            error_messages={
                                'required': '文章标题是必填项',
                                'min_length': '文章标题不能少于5字符', }
                            )
    desc = forms.CharField(min_length=2, required=True,
                            error_messages ={
                                'required': '关键字必填',
                                'min_length':'太短了，长点撒'
                            }
                            )
    content = forms.CharField(required=True,
                            error_messages = {
                                'required': '内容必填',
                            }
                            )
    picture = forms.ImageField(required=False)