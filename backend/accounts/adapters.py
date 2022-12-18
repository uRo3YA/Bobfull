from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        # 기본 저장 필드: first_name, last_name, username, email
        user = super().save_user(request, user, form, False)
        # 추가 저장 필드: profile_image
        user.alcohol = data.get('alcohol')
        user.talk = data.get('talk')
        user.smoke = data.get('smoke')
        user.speed = data.get('speed')
        user.gender = data.get('gender')
        user.manner = data.get('manner')
        user.save()
        return user