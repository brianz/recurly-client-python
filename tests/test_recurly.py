from xml.etree import ElementTree

from helpers import xml

from recurly.resources.resources import Account
from recurly.resources.resources import Subscription
from recurly.resources.resources import objects_for_push_notification


def test_xml():
    account = Account()
    account.username = 'importantbreakfast'
    account_xml = ElementTree.tostring(account.to_element(), encoding='UTF-8')
    assert account_xml == xml('<account><username>importantbreakfast</username></account>')


def test_objects_for_push_notification():
    objs = objects_for_push_notification("""<?xml version="1.0" encoding="UTF-8"?>
    <new_subscription_notification>
      <account>
        <account_code>verena@test.com</account_code>
        <username>verena</username>
        <email>verena@test.com</email>
        <first_name>Verena</first_name>
        <last_name>Test</last_name>
        <company_name>Company, Inc.</company_name>
      </account>
      <subscription>
        <plan>
          <plan_code>bronze</plan_code>
          <name>Bronze Plan</name>
          <version type="integer">2</version>
        </plan>
        <state>active</state>
        <quantity type="integer">2</quantity>
        <unit_amount_in_cents type="integer">2000</unit_amount_in_cents>
        <activated_at type="datetime">2009-11-22T13:10:38-08:00</activated_at>
        <canceled_at type="datetime"></canceled_at>
        <expires_at type="datetime"></expires_at>
        <current_period_started_at type="datetime">2009-11-22T13:10:38-08:00</current_period_started_at>
        <current_period_ends_at type="datetime">2009-11-29T13:10:38-08:00</current_period_ends_at>
        <trial_started_at type="datetime">2009-11-22T13:10:38-08:00</trial_started_at>
        <trial_ends_at type="datetime">2009-11-29T13:10:38-08:00</trial_ends_at>
      </subscription>
    </new_subscription_notification>""")
    assert objs['type'] == 'new_subscription_notification'
    assert 'account' in objs
    assert isinstance(objs['account'], Account)
    assert objs['account'].username == 'verena'
    assert 'subscription' in objs
    assert isinstance(objs['subscription'], Subscription)
    assert objs['subscription'].state == 'active'
