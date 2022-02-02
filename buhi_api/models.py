from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

# instanceはクラスをinstance化したものを引数として受け取る filenameはフロントエンドからファイルを選択した際、ファイルのnameも取得できるので、それも引数にとる
def upload_avatar_path(instance, filename):
    # extに('.')ファイルの拡張子(png,jpegなど)格納する [-1]は拡張子は一番右(最後なので)
    ext = filename.split('.')[-1]
    # 返り値としてjoinでavatarsとゆうファイルをカスタムで作って、文字列でavatarsのfile直下にprofileに基づいたdjangoのid(数字)+nickname(名前)+(".")+ext(拡張子の名前)
    return '/'.join(['avatar', str(instance.userProfile.id)+str(instance.nickname)+str(".")+str(ext)])

def upload_post_path(instance, filename):
    ext = filename.split('.')[-1]
    # 投稿を行ったユーザーのidとtitleを返す　アバターファイルと区別するためpostsファイルを作成、アバター同様直下に画像を溜め込んでいく
    return '/'.join(['posts', str(instance.userPost.id)+str(instance.title)+str(".")+str(ext)])

# emailを使用するため、一部デフォルトのBaseUserManagerをoverride(上書き)の処理をする
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        # 例外処理：emailがない場合、emailは必須とエラーを返す
        if not email:
            raise ValueError('email is must')
        # modelメソッドを使って、インスタンスとしてuserに入れている。emailを引き渡す時にemailの正規化を行っている
        user = self.model(email=self.normalize_email(email))
        # ユーザーのインスタンスにパスワードを設定 裏側でハッシュ化処理が行われている
        user.set_password(password)
        # 作ったインスタンスをデータベースにsaveする
        user.save(using=self._db)

        return user
    # superuserも上書き
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        # staff権限：djangoに備え付けのdashboardにログインするだけの権限(True : false)
        user.is_staff = True
        # superuser権限：全ての権限
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    # email属性を付与 unique:email=idなのでemailの重複はできない
    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # UserManagerのインスタンスをobjectsに格納
    # クラスの中で別クラスの要素も使う　ネストされたクラス
    objects = UserManager()
    # defaultだとusernameになっているので、emailで上書き
    USERNAME_FIELD = 'email'
    # __str__(特殊関数)文字列を返す　今回emailの内容を文字列として返す

    def __str__(self):
        return self.email

class Profile(models.Model):
    # CharField:文字列のフィールド
    nickname = models.CharField(max_length=20)
    # djangoのmodelとsettings.AUTH_USER_MODELをOneToOneFieldで紐づける
    userProfile = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='userProfile',
        # cascade:連動しているprofileも自動で削除する
        on_delete=models.CASCADE
    )
    # profileが作成された時の日時を自動作成
    created_on = models.DateTimeField(auto_now_add=True)
    # アバターのイメージフィールド　画像を設定したくないユーザーのためblank=True, null=Trueで設定なしで大丈夫
    # upload_to:アバターの画像を保持するpathを設定
    img = models.ImageField(blank=True, null=True, upload_to=upload_avatar_path)
    # strの特殊関数　nicknameを文字列で返す

    def __str__(self):
        return self.nickname

class Post(models.Model):
    title = models.CharField(max_length=100)
    # どのユーザーが投稿したかを追えるようにForeignKey(one to many)でdjangoと紐づけている
    userPost = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='userPost',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True, upload_to=upload_post_path)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked', blank=True)
    # Postクラスに対してtitleを文字列として返す

    def __str__(self):
        return self.title

class Comment(models.Model):
    text = models.CharField(max_length=100)
    userComment = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='userComment',
        on_delete=models.CASCADE
    )
    # どのpostかわかるようにして、既存の中から選べるようにした
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # 文字列でtextの内容を返すようにする

    def __str__(self):
        return self.text
