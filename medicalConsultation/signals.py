from channels import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Auditor

#   ------------------------------------------------------------------------- #
#                               HANDLER models                                #
#   ------------------------------------------------------------------------- #


@receiver(post_save, sender=Auditor)
def auditor_handler(sender, **kwargs):
    # obj_id = kwargs['instance'].id
    tag = kwargs['instance'].tag
    action = kwargs['instance'].action
    name = kwargs['instance'].content_object._meta.verbose_name
    # Send to Channel
    Group("updater").send({
        "text": '{"user" : "Backend","object": "' + name + '","tag" : ' + '"{}"'.format(str(tag)) + '\
        ,"action":"' + str(action) + '"}'
    })
