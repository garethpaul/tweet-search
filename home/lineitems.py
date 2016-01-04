import json
# TODO: Fix * imports
from django.shortcuts import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout as auth_logout
from django.conf import settings
from twitter_ads.client import Client

@login_required
def json_handler(request):
    """
    Returns json_data {"campaigns": [campaign_list} for given request
    """

    client = Client(settings.SOCIAL_AUTH_TWITTER_KEY, settings.SOCIAL_AUTH_TWITTER_SECRET, settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
    account_id = request.REQUEST.get("account_id", "")
    campaign_id = request.REQUEST.get("campaign_id", "")
    account = client.accounts(account_id)
    # TODO: Link to Ads API Docs for LineItem.rst
    line_items = account.line_items(None, params={'campaign_id': campaign_id})
    line_item_list = []
    for line_item in line_items:
        name = line_item.name
        identifier = line_item.id
        objective = line_item.objective
        bid_amount = line_item.bid_amount_local_micro
        # Sometimes Bid Amount is None
        if bid_amount != None:
            bid_amount = bid_amount/10000
        line_item_list.append({"name": name, "id": identifier, "objective": objective, "bid_amount": bid_amount})
    return HttpResponse(json.dumps({"account_id": account_id, "campaign_id": campaign_id, "line_items": line_item_list}), content_type="application/json")

@login_required
def handler(request):
    """
    Returns account page handler page for given request
    """
    account_id = request.REQUEST.get("account_id", "")
    campaign_id = request.REQUEST.get("campaign_id", "")
    context = {"request": request, "account_id": account_id, "campaign_id": campaign_id}
    return render_to_response('lineitems.html', context, context_instance=RequestContext(request))
