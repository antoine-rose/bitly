from django.db import models
import string

def convert_id_to_short_url(id):
    digits = list(string.ascii_uppercase) + [str(i) for i in range(10)] + list(string.ascii_lowercase)
    base = len(digits)
    n = int(id)

    s = ""
    while n > base:
        r = n % base
        s += digits[int(r)]
        n = (n - r) / base
    s += digits[int(n)]

    while len(s) < 7:
        s += digits[0]

    return s


class Url(models.Model):
    url = models.URLField(unique=True)
    visit_count = models.IntegerField(default=0)
    short_url = models.TextField(editable=False)
    #created_by = models.ForeignKey(User)

    def create_short_url(self):
        self.short_url = convert_id_to_short_url(self.id + 123456789) # ajout d'un offset pour avoir des url plus disparates
        super(Url, self).save()

    def update_visit_count(self):
        self.visit_count += 1
        super(Url, self).save()

    def __str__(self):
        return self.url

