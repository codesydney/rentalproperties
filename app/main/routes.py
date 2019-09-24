from flask import render_template, redirect, url_for, flash, request, current_app, session
from app.main import bp
from app.main.forms import SearchForm
import pandas as pd
from datetime import datetime, timedelta
from authlib.client import OAuth2Session


def get_token():
    scope='api_listings_read'
    oas = OAuth2Session(current_app.config['DOMAIN_CLIENT_ID'], current_app.config['DOMAIN_CLIENT_SECRET'], scope=scope)
    token = oas.fetch_access_token('https://auth.domain.com.au/v1/connect/token', grant_type='client_credentials')
    # now = datetime.now()
    # later = now + timedelta(seconds=token['expires_in']-900)
    return token

def get_session(token):
    return OAuth2Session(current_app.config['DOMAIN_CLIENT_ID'], current_app.config['DOMAIN_CLIENT_SECRET'], token=token)

@bp.route('/')
@bp.route('/index', methods=['GET','POST'])
def index():
    form=SearchForm()
    if form.validate_on_submit():

        # if first time
        if 'domain' not in session:
            session['domain'] = get_token()

        # get token again if expired
        expiry = datetime.now() + timedelta(seconds=session['domain']['expires_in']-900)
        if datetime.now() >= expiry:
            session['domain'] = get_token()

        # build data from search filters to send to domain
        data = dict()
        min_bedrooms = int(form.min_bedrooms.data)
        min_bathrooms = int(form.min_bathrooms.data)
        max_price = int(form.max_price.data)

        #surround_suburbs = form.surround_suburbs.data
        postcode = form.postcode.data
        if (min_bedrooms != -1):
            data['minBedrooms'] = min_bedrooms
        if (min_bathrooms != -1):
            data['minBathrooms'] = min_bathrooms
        if (max_price):
            data['maxPrice'] = max_price
        if (postcode):
            loc_data = []
            loc_data.append({'postcode':postcode})
            data['locations'] = loc_data
        #if (postcode or surround_suburbs):
        #    loc_data = []
        #    if (postcode):
        #        loc_data.append({'postcode':postcode})
        #    if (surround_suburbs):
        #        loc_data.append({'includeSurroundingSuburbs':surround_suburbs})
        #    data['locations'] = loc_data
        data['page'] = 1
        data['pageSize'] = 200
        data['listingType'] = 'Rent'

        # send a post request to domain api with json data
        domain_session = get_session(session['domain'])
        resp=domain_session.post('https://api.domain.com.au/v1/listings/residential/_search',json=data)

        # construct pandas dataframe and save to csv
        df = pd.DataFrame(columns=[\
        'Property type', 'Price', 'Suburb','Postcode','Display address','Bedrooms',\
        'Bathrooms','Headline',\
        'url','Advert type','Advert name','Advert contact'\
        ])
        json_resp = resp.json()

        for j in json_resp:
            df = df.append({\
                'Property type': j['listing']['propertyDetails']['propertyType'],
                'Price': j['listing']['priceDetails']['displayPrice'],
                'Suburb': j['listing']['propertyDetails']['suburb'],\
                'Postcode': j['listing']['propertyDetails']['postcode'],\
                'Display address' : j['listing']['propertyDetails']['displayableAddress'],\
                'Bedrooms': j['listing']['propertyDetails']['bedrooms'],\
                'Bathrooms': j['listing']['propertyDetails']['bathrooms'],\
                'Headline': j['listing']['headline'],\
                'url': 'http://www.domain.com.au/'+j['listing']['listingSlug'],\
                'Advert type': j['listing']['advertiser']['type'],\
                'Advert name': j['listing']['advertiser']['name'],\
                'Advert contact': j['listing']['advertiser']['contacts']\
                }, ignore_index=True)

        df.to_csv(current_app.config['RENTAL_FOLDER'] / 'test.csv', index=False)
        return render_template('main/results.html',data=resp.json())

    return render_template('main/index.html',form=form)
