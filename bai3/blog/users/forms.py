from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from flask_login import current_user
from blog.models import User


class RegistrationForm(FlaskForm):
    userName = StringField('Tên người dùng',validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mật khẩu',validators=[DataRequired()])
    phoneNumber = StringField('Số điện thoại',validators=[DataRequired()])
    confirmPassword = PasswordField('Nhập lại mật khẩu',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up ')
    def validate_userName(self,username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('Tên này tồn tại, vui lòng chọn tên khác')
    def validate_email(self,email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('Email này đã tồn tại, vui lòng chọn email khác')
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mật khẩu',validators=[DataRequired()])
    rememberMe = BooleanField('Nhớ tôi')
    submit = SubmitField('Đăng nhập')
  
class UpdateAccountForm(FlaskForm):
    userName = StringField('Tên người dùng',validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Cập nhật ảnh đại diện',validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Cập nhật')
    def validate_userName(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('Tên này tồn tại, vui lòng chọn tên khác')
    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('Email này đã tồn tại, vui lòng chọn email khác')
            
class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Gửi yêu cầu reset mật khẩu')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Không có tài khoản nào với email này.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Nhập lại mật khẩu',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Mật khẩu')
    