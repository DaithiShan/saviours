from django.db import models

# ------ FAQs Model  ------


class FAQ(models.Model):
    """
    Defines frequently asked questions
    """

    question = models.CharField(max_length=254)
    answer = models.TextField()

    def __str__(self):
        return str(self.question)

    def get_friendly_name(self):
        return str(self.answer)
