from django.urls.base import reverse

from web.tests import BaseTestCase


class OfferDetailTests(BaseTestCase):
    fixtures = ['initial_data.json']
    actions = [
        'offer_delete',
        'offer_accept',
        'offer_approve',
        'offer_refuse',
        'offer_already_not_interested',
        'offer_offer_again',
        'offer_complete'
    ]

    def get_all_states_offers(self):
        return [
            self.get_offer_awaiting_acceptance(),
            self.get_offer_awaiting_approval(),
            self.get_offer_ready_to_exchange(),
            self.get_offer_finished(),
            self.get_offer_deleted(),
        ]

    def get_allowed_actions(self):
        return {
            'user_created': {
                'offer_delete': [self.get_offer_awaiting_acceptance()],
                'offer_accept': [],
                'offer_approve': [self.get_offer_awaiting_approval()],
                'offer_refuse': [self.get_offer_awaiting_approval()],
                'offer_already_not_interested': [],
                'offer_offer_again': [self.get_offer_ready_to_exchange()],
                'offer_complete': [self.get_offer_ready_to_exchange()]
            },
            'user_responded': {
                'offer_delete': [],
                'offer_accept': [self.get_offer_awaiting_acceptance()],
                'offer_approve': [],
                'offer_refuse': [],
                'offer_already_not_interested': [self.get_offer_awaiting_approval()],
                'offer_offer_again': [self.get_offer_ready_to_exchange()],
                'offer_complete': [self.get_offer_ready_to_exchange()]
            }
        }

    # tests

    def test_not_logged(self):
        for offer in self.get_all_states_offers():
            for action in self.actions:
                response = self.client.post(reverse(action, args=[offer.id]))
                self.assertEqual(response.status_code, 302)

    def test_not_attached_to_offer(self):
        for offer in self.get_all_states_offers():
            for action in self.actions:
                self.client.force_login(self.get_user_except([offer.user_created, offer.user_responded]))
                response = self.client.post(reverse(action, args=[offer.id]))
                self.assertEqual(response.status_code, 302)

    def test_created_allowed_offer_delete(self):
        self.assert_created_allowed(self.get_offer_awaiting_acceptance(), 'offer_delete')

    def test_created_allowed_offer_approve(self):
        self.assert_created_allowed(self.get_offer_awaiting_approval(), 'offer_approve')

    def test_created_allowed_offer_refuse(self):
        self.assert_created_allowed(self.get_offer_awaiting_approval(), 'offer_refuse')

    def test_created_allowed_offer_offer_again(self):
        self.assert_created_allowed(self.get_offer_ready_to_exchange(), 'offer_offer_again')

    def test_created_allowed_offer_complete(self):
        self.assert_created_allowed(self.get_offer_ready_to_exchange(), 'offer_complete')

    def assert_created_allowed(self, offer, action):
        self.client.force_login(offer.user_created)
        response = self.client.post(reverse(action, args=[offer.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('offer_detail', args=[offer.id]))

        # check messages
        message = list(response.context.get('messages'))[0]
        self.assertFalse("denied" in message.message, action + '///' + offer.status.title)

    def test_user_created_not_allowed(self):
        for action, offers in self.get_allowed_actions()['user_created'].items():
            for offer in self.get_all_states_offers():
                if offer not in offers:
                    self.client.force_login(offer.user_created)
                    response = self.client.post(reverse(action, args=[offer.id]), follow=True)
                    self.assertEqual(response.status_code, 200)
                    self.assertRedirects(response, reverse('offer_detail', args=[offer.id]))

                    # check messages
                    message = list(response.context.get('messages'))[0]
                    self.assertTrue("denied" in message.message)

    def test_responded_allowed_offer_already_not_interested(self):
        self.assert_responded_allowed(self.get_offer_awaiting_approval(), 'offer_already_not_interested')

    def test_responded_allowed_offer_offer_again(self):
        self.assert_responded_allowed(self.get_offer_ready_to_exchange(), 'offer_offer_again')

    def test_responded_allowed_offer_complete(self):
        self.assert_responded_allowed(self.get_offer_ready_to_exchange(), 'offer_complete')

    def assert_responded_allowed(self, offer, action):
        self.client.force_login(offer.user_responded)
        response = self.client.post(reverse(action, args=[offer.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('offer_detail', args=[offer.id]))

        # check messages
        message = list(response.context.get('messages'))[0]
        self.assertFalse("denied" in message.message, action + '///' + offer.status.title)

    def test_user_responded_not_allowed(self):
        for action, offers in self.get_allowed_actions()['user_responded'].items():
            for offer in self.get_all_states_offers():
                if offer not in offers:
                    user = offer.user_responded if offer.user_responded else self.get_user_except([offer.user_created])
                    self.client.force_login(user)
                    response = self.client.post(reverse(action, args=[offer.id]), follow=True)
                    self.assertEqual(response.status_code, 200)

                    # check messages
                    message = list(response.context.get('messages'))[0]
                    self.assertTrue("denied" in message.message, action + '///' + offer.status.title)
