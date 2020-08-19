from django.utils.translation import ugettext_lazy as _

from applications.notifications.services import NotificationCreator


class TargetMatchingService(object):
    NOTIFICATION_TITLE = 'You have a new match'
    NOTIFICATION_BODY = 'A {} target is near you: {}'

    notificator = NotificationCreator()

    def process_target(self, target):
        near_targets = target.compatible_query()

        for near_target in near_targets:
            self.notificate_match(near_target.owner, target)
            self.notificate_match(target.owner, near_target)

    def notificate_match(self, receiver, target):
        data = {'target_id': target.id}
        title = _(self.NOTIFICATION_TITLE)
        message = _(self.NOTIFICATION_BODY).format(target.topic.name, target.title)

        self.notificator.create(receiver, data, title, message)
