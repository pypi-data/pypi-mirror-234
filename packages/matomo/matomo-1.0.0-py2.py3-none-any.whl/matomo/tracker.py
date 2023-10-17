import logging
from datetime import datetime
import hashlib
import json
import random
import re
import time
from urllib.parse import quote, parse_qs, urlencode
import uuid


def urlencode_plus(s):
    if type(s) == str:
        return quote(s)
    elif type(s) == dict:
        return urlencode(s)
    elif type(s) == int:
        return str(s)
    else:
        raise TypeError("urlencode_plus works only on strings, integers and dicts.", s)


#
# This module is hand-corrected version of an automated translation of PHP MatomoTracker
#

is_int = lambda x: isinstance(x, int)
is_str = lambda x: isinstance(x, str)
is_list = lambda x: isinstance(x, list)
is_dict = lambda x: isinstance(x, dict)
is_numeric = lambda x: isinstance(x, float)  # Used only once with float parameter
strpos = lambda s, sub: s.find(sub) if s.find(sub) != -1 else False


def strspn(str1, str2, start=0, length=None):
    if not length:
        length = len(str1)
    return len(re.search("^[" + str2 + "]*", str1[start : start + length]).group(0))


"""
 * Matomo - free/libre analytics platform

 * For more information, see README.md

 * @license released under BSD License http://www.opensource.org/licenses/bsd-license.php
 * @link https://matomo.org/docs/tracking-api/

 * @category Matomo
 * @package MatomoTracker

"""


class MatomoTracker:
    """
    MatomoTracker implements the Matomo Tracking Web API.

    For more information, see: https://github.com/matomo-org/matomo-php-tracker/

    * @package MatomoTracker
    * @api
    """

    """
    Matomo base URL, for example http://example.org/matomo/
    Must be set before using the class by calling
    MatomoTracker.URL = 'http://yourwebsite.org/matomo/'

    * @var str
    """
    URL = ""

    """
    API Version

    * @ignore
    * @var int
    """
    VERSION = 1

    """
    * @ignore
    """
    DEBUG_APPEND_URL = ""

    """
    Visitor ID length

    * @ignore
    """
    LENGTH_VISITOR_ID = 16

    """
    Charset
    * @see set_page_charset
    * @ignore
    """
    DEFAULT_CHARSET_PARAMETER_VALUES = "utf-8"

    """
    See matomo.js
    """
    FIRST_PARTY_COOKIES_PREFIX = "_pk_"

    """
    Defines how many categories can be used max when calling add_ecommerce_item().
    * @var int
    """
    MAX_NUM_ECOMMERCE_ITEM_CATEGORIES = 5

    DEFAULT_COOKIE_PATH = "/"

    def __init__(self, request, id_site, api_url=""):
        """
        Builds a MatomoTracker object, used to track visits, pages and Goal conversions
        for a specific website, by using the Matomo Tracking API.

        * @param int id_site Id site to be tracked
        * @param str api_url "http://example.org/matomo/" or "http://matomo.example.org/"
                                If set, will overwrite MatomoTracker.URL
        """
        self.request = request
        self.request_method = "GET"
        self.response = None
        self.ecommerceItems = []
        self.attributionInfo = None
        self.eventCustomVar = {}
        self.forcedDatetime = ""
        self.forcedNewVisit = False
        self.networkTime = 0
        self.serverTime = 0
        self.transferTime = 0
        self.domProcessingTime = 0
        self.domCompletionTime = 0
        self.onLoadTime = 0
        self.pageCustomVar = {}
        self.ecommerceView = {}
        self.customParameters = {}
        self.customDimensions = {}
        self.customData = ""
        self.hasCookies = False
        self.token_auth = ""
        self.user_agent = ""
        self.country = ""
        self.region = ""
        self.city = ""
        self.lat = 0.0
        self.long = 0.0
        self.width = 0
        self.height = 0
        self.plugins = ""
        self.local_hour = ""
        self.local_minute = ""
        self.local_second = ""
        self.idPageview = ""

        self.id_site = str(id_site)
        self.urlReferrer = self.request.get("HTTP_REFERER", "")
        self.pageCharset = self.DEFAULT_CHARSET_PARAMETER_VALUES
        self.pageUrl = self.get_current_url()
        self.ip = self.request.get("REMOTE_ADDR", "")
        self.accept_language = self.request.get("HTTP_ACCEPT_LANGUAGE", "")
        self.user_agent = self.request.get("HTTP_USER_AGENT", "")
        self.clientHints = {}
        self.set_client_hints(
            self.request.get("HTTP_SEC_CH_UA_MODEL", ""),
            self.request.get("HTTP_SEC_CH_UA_PLATFORM", ""),
            self.request.get("HTTP_SEC_CH_UA_PLATFORM_VERSION", ""),
            self.request.get("HTTP_SEC_CH_UA_FULL_VERSION_LIST", ""),
            self.request.get("HTTP_SEC_CH_UA_FULL_VERSION", "")
        )
        if api_url:
            self.URL = api_url

        # Life of the visitor cookie (in sec)
        self.configVisitorCookieTimeout = 33955200
        # 13 months (365 + 28 days)
        # Life of the session cookie (in sec)
        self.configSessionCookieTimeout = 1800
        # 30 minutes
        # Life of the session cookie (in sec)
        self.configReferralCookieTimeout = 15768000
        # 6 months

        # Visitor Ids in order
        self.user_id = ""
        self.forcedVisitorId = ""
        self.cookieVisitorId = ""
        self.randomVisitorId = ""

        self.set_new_visitor_id()

        self.configCookiesDisabled = False
        self.configCookiePath = self.DEFAULT_COOKIE_PATH
        self.configCookieDomain = ""
        self.configCookieSameSite = ""
        self.configCookieSecure = False
        self.configCookieHTTPOnly = False

        self.currentTs = time.time()
        self.createTs = self.currentTs

        # Allow debug while blocking the request
        self.requestTimeout = 600
        self.doBulkRequests = False
        self.storedTrackingActions = []

        self.sendImageResponse = True

        self.visitorCustomVar = self.get_custom_variables_from_cookie()

        self.outgoingTrackerCookies = {}
        self.incomingTrackerCookies = {}

        self.headersSent = False

        self.proxy = ""
        self.proxy_port = ""
        self.proxy_type = "https"

    def set_page_charset(self, charset=""):
        """
        By default, Matomo expects utf-8 encoded values, for example
        for the page URL parameter values, Page Title, etc.
        It is recommended to only send UTF-8 data to Matomo.
        If required though, you can also specify another charset using this function.

        * @param str charset
        * @return self
        """
        self.pageCharset = charset
        return self

    def set_url(self, url):
        """
        Sets the current URL being tracked

        * @param str url Raw URL (not URL encoded)
        * @return self
        """
        self.pageUrl = url
        return self

    def set_url_referrer(self, url):
        """
        Sets the URL referrer used to track Referrers details for new visits.

        * @param str url Raw URL (not URL encoded)
        * @return self
        """
        self.urlReferrer = url
        return self

    def set_generation_time(self, time_ms):
        """
        This method is deprecated and does nothing. It used to set the time that it took to generate the document on the server side.

        * @param int time_ms Generation time in ms
        * @return self

        * @deprecated this metric is deprecated please use performance timings instead
        * @see setPerformanceTimings
        """
        return self

    def set_performance_timings(
        self,
        network=0,
        server=0,
        transfer=0,
        domProcessing=0,
        domCompletion=0,
        onLoad=0,
    ):
        """
        Sets timings for various browser performance metrics.
        * @see https://developer.mozilla.org/en-US/docs/Web/API/PerformanceTiming

        * @param int network Network time in ms (connectEnd – fetchStart)
        * @param int server Server time in ms (responseStart – requestStart)
        * @param int transfer Transfer time in ms (responseEnd – responseStart)
        * @param int domProcessing DOM Processing to Interactive time in ms (domInteractive – domLoading)
        * @param int domCompletion DOM Interactive to Complete time in ms (domComplete – domInteractive)
        * @param int onload Onload time in ms (loadEventEnd – loadEventStart)
        * @return self
        """
        self.networkTime = network
        self.serverTime = server
        self.transferTime = transfer
        self.domProcessingTime = domProcessing
        self.domCompletionTime = domCompletion
        self.onLoadTime = onLoad
        return self

    def clear_performance_timings(self):
        """
        Clear / reset all previously set performance metrics.
        """
        self.networkTime = 0
        self.serverTime = 0
        self.transferTime = 0
        self.domProcessingTime = 0
        self.domCompletionTime = 0
        self.onLoadTime = 0

    def set_url_referer(self, url):
        """
        * @deprecated
        * @ignore
        """
        self.set_url_referrer(url)
        return self

    def set_attribution_info(self, json_encoded):
        """
        Sets the attribution information to the visit, so that subsequent Goal conversions are
        properly attributed to the right Referrer URL, timestamp, Campaign Name & Keyword.

        This must be a JSON encoded string that would typically be fetched from the JS API:
        matomoTracker.get_attribution_info() and that you have JSON encoded via JSON2.stringify()

        If you call enable_cookies() then these referral attribution values will be set
        to the 'ref' first party cookie storing referral information.

        * @param str json_encoded JSON encoded list containing Attribution info
        * @return self
        * @throws Exception
        * @see def getAttributionInfo(self): in https://github.com/matomo-org/matomo/blob/master/js/matomo.js
        """
        decoded = json.loads(json_encoded)
        if not is_list(decoded):
            raise Exception(
                f"set_attribution_info() is expecting a JSON encoded string, '{json_encoded}' given"
            )
        self.attributionInfo = decoded
        return self

    def set_custom_variable(self, id, name, value, scope="visit"):
        """
        Sets Visit Custom Variable.
        See https://matomo.org/docs/custom-variables/

        * @param int id Custom variable slot ID from 1-5
        * @param str name Custom variable name
        * @param str value Custom variable value
        * @param str scope Custom variable scope. Possible values: visit, page, event
        * @return self
        * @throws Exception
        """
        if not is_int(id):
            raise Exception("Parameter id to set_custom_variable should be an integer")
        if scope == "page":
            self.pageCustomVar[id] = [name, value]
        elif scope == "event":
            self.eventCustomVar[id] = [name, value]
        elif scope == "visit":
            self.visitorCustomVar[id] = [name, value]
        else:
            raise Exception("Invalid 'scope' parameter value")
        return self

    def get_custom_variable(self, id, scope="visit"):
        """
        Returns the currently assigned Custom Variable.

        If scope is 'visit', it will attempt to read the value set in the first party cookie created by Matomo Tracker
         (self.request.cookie dict).

        * @param int id Custom Variable integer index to fetch from cookie. Should be a value from 1 to 5
        * @param str scope Custom variable scope. Possible values: visit, page, event

        * @throws Exception
        * @return list A list with this format: [ CustomVariableName, CustomVariableValue ] or False
        * @see matomo.js getCustomVariable()
        """
        if scope == "page":
            return self.pageCustomVar.get(id, False)
        elif scope == "event":
            return self.eventCustomVar.get(id, False)
        elif scope != "visit":
            raise Exception("Invalid 'scope' parameter value")

        if self.visitorCustomVar.get(id):
            return self.visitorCustomVar[id]

        cookie_decoded = self.get_custom_variables_from_cookie()
        if not is_int(id):
            raise Exception("Parameter to get_custom_variable should be an integer")
        if (
            not is_dict(cookie_decoded)
            or id not in cookie_decoded
            or not is_list(cookie_decoded[id])
            or len(cookie_decoded[id]) != 2
        ):
            return False

        return cookie_decoded[id]

    def clear_custom_variables(self):
        """
        Clears any Custom Variable that may be have been set.

        This can be useful when you have enabled bulk requests,
        and you wish to clear Custom Variables of 'visit' scope.
        """
        self.visitorCustomVar = {}
        self.pageCustomVar = {}
        self.eventCustomVar = {}

    def set_custom_dimension(self, id, value):
        """
        Sets a specific custom dimension

        * @param int id id of custom dimension
        * @param str value value for custom dimension
        * @return self
        """
        self.customDimensions[f"dimension{id}"] = value
        return self

    def clear_custom_dimensions(self):
        """
        Clears all previously set custom dimensions
        """
        self.customDimensions = {}

    def get_custom_dimension(self, id):
        """
        Returns the value of the custom dimension with the given id

        * @param int id id of custom dimension
        * @return str | None
        """
        return self.customDimensions.get(f"dimension{id}", None)

    def set_custom_tracking_parameter(self, tracking_api_parameter, value):
        """
        Sets a custom tracking parameter. This is useful if you need to send any tracking parameters for a 3rd party
        plugin that is not shipped with Matomo itself. Please note that custom parameters are cleared after each
        tracking request.

        * @param str tracking_api_parameter The name of the tracking API parameter, eg 'bw_bytes'
        * @param str value Tracking parameter value that shall be sent for this tracking parameter.
        * @return self
        * @throws Exception
        """
        regex = re.compile("^dimension([0-9]+)$")
        matches = re.findall(regex, tracking_api_parameter)
        if len(matches):
            # Unlike PHP preg_match it returns captured subpattern as first element
            self.set_custom_dimension(matches[0], value)
            return self

        self.customParameters[tracking_api_parameter] = value
        return self

    def clear_custom_tracking_parameters(self):
        """
        Clear / reset all previously set custom tracking parameters.
        """
        self.customParameters = {}

    def set_new_visitor_id(self):
        """
        Sets the current visitor ID to a random new one.
        * @return self
        """
        self.randomVisitorId = uuid.uuid4().hex[: self.LENGTH_VISITOR_ID]
        self.forcedVisitorId = False
        self.cookieVisitorId = False
        return self

    def set_id_site(self, id_site):
        """
        Sets the current site ID.

        * @param int id_site
        * @return self
        """
        self.id_site = id_site
        return self

    def set_browser_language(self, accept_language):
        """
        Sets the Browser language. Used to guess visitor countries when GeoIP is not enabled

        * @param str accept_language For example "fr-fr"
        * @return self
        """
        self.accept_language = accept_language
        return self

    def set_user_agent(self, user_agent):
        """
        Sets the user agent, used to detect OS and browser.
        If this function is not called, the User Agent will default to the current user agent.

        * @param str user_agent
        * @return self
        """
        self.user_agent = user_agent
        return self

    def set_client_hints(self, model = '', platform = '', platformVersion = '', fullVersionList = '', uaFullVersion = ''):
        """
        Sets the client hints, used to detect OS and browser.
        If this function is not called, the client hints sent with the current request will be used.

        Supported as of Matomo 4.12.0

        * @param str model  Value of the header 'HTTP_SEC_CH_UA_MODEL'
        * @param str platform  Value of the header 'HTTP_SEC_CH_UA_PLATFORM'
        * @param str platformVersion  Value of the header 'HTTP_SEC_CH_UA_PLATFORM_VERSION'
        * @param str|list fullVersionList Value of header 'HTTP_SEC_CH_UA_FULL_VERSION_LIST'
                        or a dict containing all brands with the structure
                        [{'brand': 'Chrome', 'version' => '10.0.2'], {'brand': '...]
        * @param str uaFullVersion  Value of the header 'HTTP_SEC_CH_UA_FULL_VERSION'
        * @return self
        """
        if is_str(fullVersionList):
            regex = re.compile("^\"([^\"]+?)\"; ?v=\"([^\"]+?)\"(?:, )?")
            l = []

            match = re.search(regex, fullVersionList)
            while match:
                brand, version = re.findall(regex, fullVersionList)[0]
                l.append({
                    "brand": brand,
                    "version": version
                })

                start, end = match.span()
                fullVersionList = fullVersionList[end:]
                match = re.search(regex, fullVersionList)

            fullVersionList = l
        elif not is_list(fullVersionList):
            fullVersionList = []
        self.clientHints = {
            "model": model,
            "platform": platform,
            "platformVersion": platformVersion,
            "uaFullVersion": uaFullVersion,
            "fullVersionList": fullVersionList
        }
        return self

    def set_country(self, country):
        """
        Sets the country of the visitor. If not used, Matomo will try to find the country
        using either the visitor's IP address or language.

        Allowed only for Admin/Super User, must be used along with set_token_auth().
        * @param str country
        * @return self
        """
        self.country = country
        return self

    def set_region(self, region):
        """
        Sets the region of the visitor. If not used, Matomo may try to find the region
        using the visitor's IP address (if configured to do so).

        Allowed only for Admin/Super User, must be used along with set_token_auth().
        * @param str region
        * @return self
        """
        self.region = region
        return self

    def set_city(self, city):
        """
        Sets the city of the visitor. If not used, Matomo may try to find the city
        using the visitor's IP address (if configured to do so).

        Allowed only for Admin/Super User, must be used along with set_token_auth().
        * @param str city
        * @return self
        """
        self.city = city
        return self

    def set_latitude(self, lat):
        """
        Sets the latitude of the visitor. If not used, Matomo may try to find the visitor's
        latitude using the visitor's IP address (if configured to do so).

        Allowed only for Admin/Super User, must be used along with set_token_auth().
        * @param float lat
        * @return self
        """
        self.lat = lat
        return self

    def set_longitude(self, long):
        """
        Sets the longitude of the visitor. If not used, Matomo may try to find the visitor's
        longitude using the visitor's IP address (if configured to do so).

        Allowed only for Admin/Super User, must be used along with set_token_auth().
        * @param float long
        * @return self
        """
        self.long = long
        return self

    def enable_bulk_tracking(self):
        """
        Enables the bulk request feature. When used, each tracking action is stored until the
        do_bulk_track method is called. This method will send all tracking data at once.

        """
        self.doBulkRequests = True

    def disable_bulk_tracking(self):
        """
        Disables the bulk request feature. Make sure to call `do_bulk_track()` before disabling it if you have stored
        tracking actions previously as this method won't be sending any previously stored actions before disabling it.
        """
        self.doBulkRequests = False

    def enable_cookies(
        self, domain="", path="/", secure=False, http_only=False, same_site=""
    ):
        """
        Enable cookie creation - this will cause a first party VisitorId cookie to be set when the VisitorId is set or reset

        * @param str domain (optional) Set first-party cookie domain.
                    Accepted values: example.com, *.example.com (same as .example.com) or subdomain.example.com
        * @param str path (optional) Set first-party cookie path
        * @param bool secure (optional) Set secure flag for cookies
        * @param bool http_only (optional) Set HTTPOnly flag for cookies
        * @param str same_site (optional) Set SameSite flag for cookies
        """
        self.configCookiesDisabled = False
        self.configCookieDomain = self.domain_fixup(domain)
        self.configCookiePath = path
        self.configCookieSecure = secure
        self.configCookieHTTPOnly = http_only
        self.configCookieSameSite = same_site

    def disable_send_image_response(self):
        """
        If image response is disabled Matomo will respond with a HTTP 204 header instead of responding with a gif.
        """
        self.sendImageResponse = False

    def domain_fixup(self, domain):
        """
        Fix-up domain

        Remove trailing '.' and leading '*.'
        """
        return domain.rstrip(".").lstrip("*.")

    def get_cookie_name(self, cookie_name):
        """
        Get cookie name with prefix and domain hash
        * @param str cookie_name
        * @return str
        """
        hash_string = hashlib.sha1(
            (
                self.get_current_host()
                if self.configCookieDomain == ""
                else self.configCookieDomain
            ).encode("utf-8")
            + self.configCookiePath.encode("utf-8")
        ).hexdigest()[:4]

        return "{}{}.{}.{}".format(
            self.FIRST_PARTY_COOKIES_PREFIX, cookie_name, self.id_site, hash_string
        )

    def do_track_page_view(self, document_title):
        """
        Tracks a page view

        * @param str document_title Page title as it will appear in the Actions > Page titles report
        * @return mixed Response string or True if using bulk requests.
        """
        self.generate_new_pageview_id()
        url = self.get_url_track_page_view(document_title)
        return self.send_request(url)

    def generate_new_pageview_id(self):
        self.idPageview = uuid.uuid4().hex[:6]

    def do_track_event(self, category, action, name="", value=0):
        """
        Tracks an event

        * @param str category The Event Category (Videos, Music, Games...)
        * @param str action The Event's Action (Play, Pause, Duration, Add Playlist, Downloaded, Clicked...)
        * @param str name (optional) The Event's object Name (a particular Movie name, or Song name, or File name...)
        * @param float value (optional) The Event's value
        * @return mixed Response string or True if using bulk requests.
        """
        url = self.get_url_track_event(category, action, name, value)
        return self.send_request(url)

    def do_track_content_impression(
        self, content_name, content_piece="Unknown", content_target=""
    ):
        """
        Tracks a content impression

        * @param str content_name The name of the content. For instance 'Ad Foo Bar'
        * @param str content_piece The actual content. For instance the path to an image, video, audio, any text
        * @param str content_target (optional) The target of the content. For instance the URL of a landing page.
        * @return mixed Response string or True if using bulk requests.
        """
        url = self.get_url_track_content_impression(
            content_name, content_piece, content_target
        )
        return self.send_request(url)

    def do_track_content_interaction(
        self, interaction, content_name, content_piece="Unknown", content_target=""
    ):
        """
        Tracks a content interaction. Make sure you have tracked a content impression using the same content name and
        content piece, otherwise it will not count. To do so you should call the method do_track_content_impression()

        * @param str interaction The name of the interaction with the content. For instance a 'click'
        * @param str content_name The name of the content. For instance 'Ad Foo Bar'
        * @param str content_piece The actual content. For instance the path to an image, video, audio, any text
        * @param str content_target (optional) The target the content leading to when an interaction occurs. For instance the URL of a landing page.
        * @return mixed Response string or True if using bulk requests.
        """
        url = self.get_url_track_content_interaction(
            interaction, content_name, content_piece, content_target
        )

        return self.send_request(url)

    def do_track_site_search(self, keyword, category="", count_results=0):
        """
        Tracks an internal Site Search query, and optionally tracks the Search
        Category, and Search results Count.
        These are used to populate reports in Actions > Site Search.

        * @param str keyword Searched query on the site
        * @param str category (optional) Search engine category if applicable
        * @param int count_results (optional) results displayed on the search
        result page. Used to track "zero result" keywords.

        * @return mixed Response string or True if using bulk requests.
        """
        url = self.get_url_track_site_search(keyword, category, count_results)
        return self.send_request(url)

    def do_track_goal(self, id_goal, revenue=0.0):
        """
        Records a Goal conversion

        * @param int id_goal Id Goal to record a conversion
        * @param float revenue Revenue for this conversion
        * @return mixed Response string or True if using bulk request
        """
        url = self.get_url_track_goal(id_goal, revenue)
        return self.send_request(url)

    def do_track_action(self, action_url, action_type):
        """
        Tracks a download or outlink

        * @param str action_url URL of the download or outlink
        * @param str action_type Type of the action: 'download' or 'link'
        * @return mixed Response string or True if using bulk request
        """
        # Referrer could be updated to be the current URL temporarily (to mimic JS behavior)
        url = self.get_url_track_action(action_url, action_type)
        return self.send_request(url)

    def add_ecommerce_item(self, sku, name="", category="", price=0.0, quantity=1):
        """
        Adds an item in the Ecommerce order.

        This should be called before do_track_ecommerce_order(), or before do_track_ecommerce_cart_update().
        This function can be called for all individual products in the cart (self, or order):.
        SKU parameter is mandatory. Other parameters are optional (set to False if value not known).
        Ecommerce items added via this function are automatically cleared when
        do_track_ecommerce_order() or get_url_track_ecommerce_order() is called.

        * @param str sku (required) SKU, Product identifier
        * @param str name (optional) Product name
        * @param str|list category (optional) Product category, or list of product categories (up to 5 categories can be specified for a given product)
        * @param float|int price (optional) Individual product price (supports integer and decimal prices)
        * @param int quantity (optional) Product quantity. If specified, will default to 1 not in the Reports
        * @throws Exception
        * @return self
        """
        if not sku:
            raise Exception("You must specify a SKU for the Ecommerce item")

        price = self.force_dot_as_separator_for_decimal_point(price)
        self.ecommerceItems = [sku, name, category, price, quantity]
        return self

    def do_track_ecommerce_cart_update(self, grand_total):
        """
        Tracks a Cart Update (add item, remove item, update item).

        On every Cart update, you must call add_ecommerce_item() for each item
        (product) in the cart, including the items that haven't been updated
        since the last cart update.
        Items which were in the previous cart and are sent not in later Cart
        updates will be deleted from the cart (in the database).

        * @param float grand_total Cart grand_total (typically the sum of all items' prices)
        * @return mixed Response string or True if using bulk request
        """
        url = self.get_url_track_ecommerce_cart_update(grand_total)
        return self.send_request(url)

    def do_bulk_track(self):
        """
        Sends all stored tracking actions at once. Only has an effect if bulk tracking is enabled.

        To enable bulk tracking, call enable_bulk_tracking().

        * @throws Exception
        * @return str Response
        """
        if not self.storedTrackingActions:
            raise Exception(
                (
                    "Error: you must call the function do_track_page_view or do_track_goal"
                    " from this class, before calling this method do_bulk_track():"
                )
            )

        data = {"requests": self.storedTrackingActions}

        # token_auth is not required by default, except if bulk_requests_require_authentication=1
        if self.token_auth:
            data["token_auth"] = self.token_auth

        post_data = json.dumps(data)
        response = self.send_request(self.get_base_url(), "POST", post_data, force=True)

        self.storedTrackingActions = []

        return response

    def do_track_ecommerce_order(
        self, order_id, grand_total, sub_total=0.0, tax=0.0, shipping=0.0, discount=0.0
    ):
        """
        Tracks an Ecommerce order.

        If the Ecommerce order contains items (products), you must call first the add_ecommerce_item() for each item in the order.
        All revenues (grand_total, sub_total, tax, shipping, discount) will be individually summed and reported in Matomo reports.
        Only the parameters order_id and grand_total are required.

        * @param str|int order_id (required) Unique Order ID.
                       This will be used to count this order only once in the event the order page is reloaded several times.
                       order_id must be unique for each transaction, even on different days, or the transaction will not be recorded by Matomo.
        * @param float grand_total (required) Grand Total revenue of the transaction (including tax, shipping, etc.)
        * @param float sub_total (optional) Sub total amount, typically the sum of items prices for all items in this order (before Tax and Shipping costs are applied)
        * @param float tax (optional) Tax amount for this order
        * @param float shipping (optional) Shipping amount for this order
        * @param float discount (optional) Discounted amount in this order
        * @return mixed Response or True if using bulk request
        """
        url = self.get_url_track_ecommerce_order(
            order_id, grand_total, sub_total, tax, shipping, discount
        )
        return self.send_request(url)

    def do_ping(self):
        """
        Sends a ping request.

        Ping requests do track new actions. If they are sent within the standard visit length (see global.ini.php), * they will extend the existing visit and the current last action for the visit. If after the standard visit length, * ping requests will create a new visit using the last action not in the last known visit.

        * @return mixed Response or True if using bulk request
        """
        url = self.get_request(self.id_site)
        url += "&ping=1"

        return self.send_request(url)

    def set_ecommerce_view(self, sku="", name="", category="", price=0.0):
        """
        Sets the current page view as an item (product) page view, or an Ecommerce Category page view.

        This must be called before do_track_page_view() on this product/category page.

        On a category page, you may set the parameter category only and set the other parameters to False.

        Tracking Product/Category page views will allow Matomo to report on Product & Categories
        conversion rates (Conversion rate = Ecommerce orders containing this product or category / Visits to the product or category)

        * @param str sku Product SKU being viewed
        * @param str name Product Name being viewed
        * @param str|array category Category being viewed. On a Product page, this is the product's category.
                                       You can also specify an array of up to 5 categories for a given page view.
        * @param float price Specify the price at which the item was displayed
        * @return self
        """
        self.ecommerceView = {}
        if category:
            if is_list(category):
                category = json.dumps(category)

        self.ecommerceView["_pkc"] = category

        if price:
            price = str(price)
            price = self.force_dot_as_separator_for_decimal_point(price)
            self.ecommerceView["_pkp"] = price

        # On a category page, do not record "Product name not defined"
        if not sku and not name:
            return self
        if sku:
            self.ecommerceView["_pks"] = sku
        if not name:
            name = ""
        self.ecommerceView["_pkn"] = name
        return self

    def force_dot_as_separator_for_decimal_point(self, value):
        """
        Force the separator for decimal point to be a dot. See https://github.com/matomo-org/matomo/issues/6435
        If for instance a German locale is used it would be a comma otherwise.

        * @param  float|string value
        * @return str
        """
        if value is None or value is False:
            return ""
        return str(value).replace(",", ".")

    def get_url_track_ecommerce_cart_update(self, grand_total):
        """
        Returns URL used to track Ecommerce Cart updates
        Calling this function will reinitialize the property ecommerceItems to empty list
        so items will have to be added again via add_ecommerce_item()
        * @ignore
        """
        url = self.get_url_track_ecommerce(grand_total)
        return url

    def get_url_track_ecommerce_order(
        self, order_id, grand_total, sub_total=0.0, tax=0.0, shipping=0.0, discount=0.0
    ):
        """
        Returns URL used to track Ecommerce Orders
        Calling this function will reinitialize the property ecommerceItems to empty list
        so items will have to be added again via add_ecommerce_item()
        * @ignore
        """
        if not order_id:
            raise Exception("You must specify an order_id for the Ecommerce order")
        url = self.get_url_track_ecommerce(
            grand_total, sub_total, tax, shipping, discount
        )
        url += "&ec_id=" + urlencode_plus(order_id)

        return url

    def get_url_track_ecommerce(
        self, grand_total, sub_total=0.0, tax=0.0, shipping=0.0, discount=0.0
    ):
        """
        Returns URL used to track Ecommerce orders

        Calling this function will reinitialize the property ecommerceItems to empty array
        so items will have to be added again via add_ecommerce_item()

        * @ignore
        """
        if not is_numeric(grand_total) and not is_int(grand_total):
            raise Exception(
                "You must specify a grand_total for the Ecommerce order (or Cart update)"
            )

        url = self.get_request(self.id_site)
        url += "&idgoal=0"
        if grand_total:
            grand_total = self.force_dot_as_separator_for_decimal_point(grand_total)
            url += f"&revenue={grand_total}"
        if sub_total:
            sub_total = self.force_dot_as_separator_for_decimal_point(sub_total)
            url += f"&ec_st={sub_total}"
        if tax:
            tax = self.force_dot_as_separator_for_decimal_point(tax)
            url += f"&ec_tx={tax}"
        if shipping:
            shipping = self.force_dot_as_separator_for_decimal_point(shipping)
            url += f"&ec_sh={shipping}"
        if discount:
            discount = self.force_dot_as_separator_for_decimal_point(discount)
            url += f"&ec_dt={discount}"
        if self.ecommerceItems:
            url += "&ec_items=" + urlencode_plus(json.dumps(self.ecommerceItems))
        self.ecommerceItems = []

        return url

    def get_url_track_page_view(self, document_title=""):
        """
        Builds URL to track a page view.

        * @see do_track_page_view()
        * @param str document_title Page view name as it will appear in Matomo reports
        * @return str URL to matomo.php with all parameters set to track the pageview
        """
        url = self.get_request(self.id_site)
        if document_title:
            url += "&action_name=" + urlencode_plus(document_title)
        return url

    def get_url_track_event(self, category, action, name="", value=0):
        """
        Builds URL to track a custom event.

        * @see do_track_event()
        * @param str category The Event Category (Videos, Music, Games...)
        * @param str action The Event's Action (Play, Pause, Duration, Add Playlist, Downloaded, Clicked...)
        * @param str name (optional) The Event's object Name (a particular Movie name, or Song name, or File name...)
        * @param float value (optional) The Event's value
        * @return str URL to matomo.php with all parameters set to track the pageview
        * @throws
        """
        if not category:
            raise Exception(
                "You must specify an Event Category name (Music, Videos, Games...)."
            )
        if not action:
            raise Exception("You must specify an Event action (click, view, add...).")

        url = self.get_request(self.id_site)
        url += f"&e_c={urlencode_plus(category)}&e_a={urlencode_plus(action)}"

        if name:
            url += f"&e_n={urlencode_plus(name)}"
        if value:
            value = self.force_dot_as_separator_for_decimal_point(value)
            url += f"&e_v={value}"

        return url

    def get_url_track_content_impression(
        self, content_name, content_piece, content_target
    ):
        """
        Builds URL to track a content impression.

        * @see do_track_content_impression()
        * @param str content_name The name of the content. For instance 'Ad Foo Bar'
        * @param str content_piece The actual content. For instance the path to an image, video, audio, any text
        * @param str|False content_target (optional) The target of the content. For instance the URL of a landing page.
        * @throws Exception In case content_name is empty
        * @return str URL to matomo.php with all parameters set to track the pageview
        """
        url = self.get_request(self.id_site)

        if not content_name:
            raise Exception("You must specify a content name")

        url += f"&c_n={urlencode_plus(content_name)}"

        if content_piece:
            url += f"&c_p={urlencode_plus(content_piece)}"
        if content_target:
            url += f"&c_t={urlencode_plus(content_target)}"

        return url

    def get_url_track_content_interaction(
        self, interaction, content_name, content_piece, content_target
    ):
        """
        Builds URL to track a content impression.

        * @see do_track_content_interaction()
        * @param str interaction The name of the interaction with the content. For instance a 'click'
        * @param str content_name The name of the content. For instance 'Ad Foo Bar'
        * @param str content_piece The actual content. For instance the path to an image, video, audio, any text
        * @param str|False content_target (optional) The target the content leading to when an interaction occurs. For instance the URL of a landing page.
        * @throws Exception In case interaction or content_name is empty
        * @return str URL to matomo.php with all parameters set to track the pageview
        """
        url = self.get_request(self.id_site)

        if not interaction:
            raise Exception("You must specify a name for the interaction")

        if not content_name:
            raise Exception("You must specify a content name")

        url += f"&c_i={urlencode_plus(interaction)}&c_n={urlencode_plus(content_name)}"

        if content_piece:
            url += f"&c_p={urlencode_plus(content_piece)}"
        if content_target:
            url += f"&c_t={urlencode_plus(content_target)}"

        return url

    def get_url_track_site_search(self, keyword, category, count_results):
        """
        Builds URL to track a site search.

        * @see do_track_site_search()
        * @param str keyword
        * @param str category
        * @param int count_results
        * @return str
        """
        url = self.get_request(self.id_site)
        url += f"&search=" + urlencode_plus(keyword)
        if category:
            url += f"&search_cat={urlencode_plus(category)}"
        if count_results or count_results == 0:
            url += f"&search_count={count_results}"

        return url

    def get_url_track_goal(self, id_goal, revenue=0.0):
        """
        Builds URL to track a goal with id_goal and revenue.

        * @see do_track_goal()
        * @param int id_goal Id Goal to record a conversion
        * @param float revenue Revenue for this conversion
        * @return str URL to matomo.php with all parameters set to track the goal conversion
        """
        url = self.get_request(self.id_site)
        url += f"&idgoal={id_goal}"
        if revenue:
            revenue = self.force_dot_as_separator_for_decimal_point(revenue)
            url += f"&revenue={revenue}"

        return url

    def get_url_track_action(self, action_url, action_type):
        """
        Builds URL to track a new action.

        * @see do_track_action()
        * @param str action_url URL of the download or outlink
        * @param str action_type Type of the action: 'download' or 'link'
        * @return str URL to matomo.php with all parameters set to track an action
        """
        url = self.get_request(self.id_site)
        url += f"&{action_type}={urlencode_plus(action_url)}"
        return url

    def set_force_visit_date_time(self, date_time):
        """
        Overrides server date and time for the tracking requests.
        By default Matomo will track requests for the "current datetime" but this function allows you
        to track visits in the past. All times are in UTC.

        Allowed only for Admin/Super User, must be used along with set_token_auth()
        * @see set_token_auth()
        * @param str date_time Date with the format '%y-%m-%d %H:%M:%S', or a UNIX timestamp.
                      If the datetime is older than one day (default value for
                      tracking_requests_require_authentication_when_custom_timestamp_newer_than),
                      then you must call set_token_auth() with a valid Admin/Super user token.
        * @return self
        """
        self.forcedDatetime = date_time
        return self

    def set_force_new_visit(self):
        """
        Forces Matomo to create a new visit for the tracking request.

        By default, Matomo will create a new visit if the last request by this user was more than 30 minutes ago.
        If you call set_force_new_visit() before calling do_track*, then a new visit will be created for this request.
        * @return self
        """
        self.forcedNewVisit = True
        return self

    def set_ip(self, ip):
        """
        Overrides IP address

        Allowed only for Admin/Super User, must be used along with set_token_auth()
        * @see set_token_auth()
        * @param str ip IP string, eg. 130.54.2.1
        * @return self
        """
        self.ip = ip
        return self

    def set_user_id(self, user_id):
        """
        Force the action to be recorded for a specific User. The User ID is a string representing a given user in your system.

        A User ID can be a username, UUID or an email address, or any number or string that uniquely identifies a user or client.

        * @param str user_id Any user ID string (eg. email address, ID, username). Must be non empty. Set to False to de-assign a user id previously set.
        * @return self
        * @throws Exception
        """
        if user_id == "":
            raise Exception("User ID cannot be empty.")
        self.user_id = user_id
        return self

    def get_user_id_hashed(self, id):
        """
        Hash function used internally by Matomo to hash a User ID into the Visitor ID.

        Note: matches implementation of Tracker Request.get_user_id_hashed()

        * @param id
        * @return str
        """
        return hashlib.sha1(id).hexdigest()[:16]

    def set_visitor_id(self, visitor_id):
        """
        Forces the requests to be recorded for the specified Visitor ID.

        Rather than letting Matomo attribute the user with a heuristic based on IP and other user
        fingerprinting attributes, force the action to be recorded for a particular visitor.

        If not set, the visitor ID will be fetched from the 1st party cookie, or will be set to a random UUID.

        * @param str visitor_id 16 hexadecimal characters visitor ID, e.g. "33c31e01394bdc63"
        * @return self
        * @throws Exception
        """
        hex_chars = "01234567890abcdefABCDEF"
        if len(visitor_id) != self.LENGTH_VISITOR_ID or strspn(
            visitor_id, hex_chars
        ) != len(visitor_id):
            raise Exception(
                f"set_visitor_id() expects a {self.LENGTH_VISITOR_ID} characters"
                f" hexadecimal string (containing only the following: {hex_chars})"
            )
        self.forcedVisitorId = visitor_id
        return self

    def get_visitor_id(self):
        """
        If the user initiating the request has the Matomo first party cookie, this function will try and
        return the ID parsed from this first party cookie (self, found in self.request.cookie):.

        If you call this function from a server, where the call is triggered by a cron or script
        not initiated by the actual visitor being tracked, then it will return
        the random Visitor ID that was assigned to this visit object.

        This can be used if you wish to record more visits, actions or goals for this visitor ID later on.

        * @return str 16 hex chars visitor ID string
        """
        if self.forcedVisitorId:
            return self.forcedVisitorId
        if self.load_visitor_id_cookie():
            return self.cookieVisitorId
        return self.randomVisitorId

    def get_user_agent(self):
        """
        Returns the currently set user agent.
        * @return str
        """
        return self.user_agent

    def get_ip(self):
        """
        Returns the currently set IP address.
        * @return str
        """
        return self.ip

    def get_user_id(self):
        """
        Returns the User ID string, which may have been set via:
            v.set_user_id('username@example.org')

        * @return bool
        """
        return self.user_id

    def load_visitor_id_cookie(self):
        """
        Loads values from the VisitorId Cookie

        * @return bool True if cookie exists and is valid, False otherwise
        """
        id_cookie = self.get_cookie_matching_name("id")
        if not id_cookie:
            return False
        parts = id_cookie.split(".")
        if len(parts[0]) != self.LENGTH_VISITOR_ID:
            return False

        """ self.cookieVisitorId provides backward compatibility since get_visitor_id()
        didn't change any existing VisitorId value"""
        self.cookieVisitorId = parts[0]
        self.createTs = parts[1]
        return True

    def delete_cookies(self):
        """
        Deletes all first party cookies from the client
        """
        cookies = ["id", "ses", "cvar", "ref"]
        for cookie in cookies:
            self.set_cookie(cookie, None, -86400)

    def get_attribution_info(self):
        """
        Returns the currently assigned Attribution Information stored in a first party cookie.

        This function will only work if the user is initiating the current request, and his cookies
        can be read by Python from the self.request.cookie object.

        * @return str JSON Encoded string containing the Referrer information for Goal conversion attribution.
                       Will return False if the cookie could not be found
        * @see matomo.js get_attribution_info()
        """
        if self.attributionInfo:
            return json.dumps(self.attributionInfo)

        return self.get_cookie_matching_name("ref")

    def set_token_auth(self, token_auth):
        """
        Some Tracking API functionality requires express authentication, using either the
        Super User token_auth, or a user with 'admin' access to the website.

        The following features require access:
        - force the visitor IP
        - force the date & time of the tracking requests rather than track for the current datetime

        * @param str token_auth token_auth 32 chars token_auth string
        * @return self
        """
        self.token_auth = token_auth
        return self

    def set_local_time(self, t):
        """
        Sets local visitor time

        * @param str t HH:MM:SS format
        * @return self
        """
        hour, minute, second = t.split(":")
        self.local_hour = hour
        self.local_minute = minute
        self.local_second = second
        return self

    def set_resolution(self, width, height):
        """
        Sets user resolution width and height.

        * @param int width
        * @param int height
        * @return self
        """
        self.width = width
        self.height = height
        return self

    def set_browser_has_cookies(self, b):
        """
        Sets if the browser supports cookies
        This is reported in "List of plugins" report in Matomo.

        * @param bool b
        * @return self
        """
        self.hasCookies = b
        return self

    def set_debug_string_append(self, string):
        """
        Will append a custom string at the end of the Tracking request.
        * @param str string
        * @return self
        """
        self.DEBUG_APPEND_URL = "&" + string
        return self

    def set_plugins(
        self,
        flash=False,
        java=False,
        quick_time=False,
        real_player=False,
        pdf=False,
        windows_media=False,
        silverlight=False,
    ):
        """
        Sets visitor browser supported plugins

        * @param bool flash
        * @param bool java
        * @param bool quick_time
        * @param bool real_player
        * @param bool pdf
        * @param bool windows_media
        * @param bool silverlight
        * @return self
        """
        plugins = (
            f"&fla={int(flash)}&java={int(java)}&qt={int(quick_time)}"
            f"&realp={int(real_player)}&pdf={int(pdf)}&wma={int(windows_media)}&ag={int(silverlight)}"
        )
        self.plugins = plugins
        return self

    def disable_cookie_support(self):
        """
        By default, MatomoTracker will read first party cookies
        from the request and write updated cookies in the response (using setrawcookie).
        This can be disabled by calling this function.
        """
        self.configCookiesDisabled = True

    def get_request_timeout(self):
        """
        Returns the maximum number of seconds the tracker will spend waiting for a response
        from Matomo. Defaults to 600 seconds.
        """
        return self.requestTimeout

    def set_request_timeout(self, timeout):
        """
        Sets the maximum number of seconds that the tracker will spend waiting for a response
        from Matomo.

        * @param int timeout
        * @return self
        * @throws Exception
        """
        if not is_int(timeout) or timeout < 0:
            raise Exception("Invalid value supplied for request timeout: timeout")

        self.requestTimeout = timeout
        return self

    def set_request_method_non_bulk(self, method):
        """
        Sets the request method to POST, which is recommended when using set_token_auth()
        to prevent the token from being recorded in server logs. Avoid using redirects
        when using POST to prevent the loss of POST values. When using Log Analytics,
        be aware that POST requests are not parseable/replayable.

        * @param str method. Either 'POST' or 'GET'
        * @return self
        """
        self.request_method = "POST" if method.upper() == "POST" else "GET"
        return self

    def set_proxy(self, proxy, proxy_port=80, proxy_type="https"):
        """
        If a proxy is needed to look up the address of the Matomo site, set it with this
        * @param str proxy IP as string, for example "173.234.92.107"
        * @param int proxy_port
        """
        self.proxy = proxy
        self.proxy_port = proxy_port
        self.proxy_type = proxy_type

    def get_proxy(self):
        """
        If the proxy IP,the proxy port and the proxy_type have been set,
        with the set_proxy() function returns a string, like "https://173.234.92.107:80"
        """
        if self.proxy and self.proxy_port and self.proxy_type:
            return f"{self.proxy_type}://{self.proxy}:{self.proxy_port}"
        return None

    """
    * @ignore
    """

    def send_request(self, url, method="get", data=None, force=False):
        raise NotImplementedError("Missing send_request implementation")

    def get_timestamp(self):
        """
        Returns current timestamp, or forced timestamp/datetime if it was set
        * @return str|int
        """
        if self.forcedDatetime:
            return datetime.strptime(
                self.forcedDatetime, "%Y-%m-%d %H:%M:%S"
            ).timestamp()
        else:
            return time.time()

    def get_base_url(self):
        """
        Returns the base URL for the Matomo server.
        """
        if not self.URL:
            raise Exception(
                (
                    "You must first set the Matomo Tracker URL by calling "
                    "MatomoTracker.URL = 'http://your-website.org/matomo/'"
                )
            )
        if (
            strpos(self.URL, "/matomo.php") is False
            and strpos(self.URL, "/proxy-matomo.php") is False
        ):
            self.URL = self.URL.rstrip("/")
            self.URL += "/matomo.php"

        return self.URL

    """
    * @ignore
    """

    def get_request(self, id_site):
        self.set_first_party_cookies()

        custom_fields = ""
        if self.customParameters:
            custom_fields = "&" + urlencode_plus(self.customParameters)

        custom_dimensions = ""
        if self.customDimensions:
            custom_dimensions = "&" + urlencode_plus(self.customDimensions)

        base_url = self.get_base_url()
        start = "?"
        if strpos(base_url, "?"):
            start = "&"

        url = (
            f"{base_url}{start}idsite={id_site}&rec=1&apiv={self.VERSION}"
            + f"&r={str(random.randint(0, 2147483647))[2:8]}"
            + (f"&cip={self.ip}" if self.ip and self.token_auth else "")
            + (f"&uid={urlencode_plus(self.user_id)}" if self.user_id else "")
            + (
                "&cdt=" + urlencode_plus(self.forcedDatetime)
                if self.forcedDatetime
                else ""
            )
            + ("&new_visit=1" if self.forcedNewVisit else "")
            + f"&_idts={self.createTs}{self.plugins}"
            + (
                f"&h={self.local_hour}&m={self.local_minute}&s={self.local_second}"
                if self.local_hour and self.local_minute and self.local_second
                else ""
            )
            + (f"&res={self.width}x{self.height}" if self.width and self.height else "")
            + (f"&cookie={self.hasCookies}" if self.hasCookies else "")
            + (f"&data={self.customData}" if self.customData else "")
            + (
                "&_cvar=" + urlencode_plus(json.dumps(self.visitorCustomVar))
                if self.visitorCustomVar
                else ""
            )
            + (
                "&cvar=" + urlencode_plus(json.dumps(self.pageCustomVar))
                if self.pageCustomVar
                else ""
            )
            + (
                "&e_cvar=" + urlencode_plus(json.dumps(self.eventCustomVar))
                if self.eventCustomVar
                else ""
            )
            + (
                f"&cid={self.forcedVisitorId}"
                if self.forcedVisitorId
                else f"&_id={self.get_visitor_id()}"
            )
            + "&url="
            + urlencode_plus(self.pageUrl or "")
            + "&urlref="
            + urlencode_plus(self.urlReferrer or "")
            + (
                f"&cs={self.pageCharset}"
                if (
                    self.pageCharset
                    and self.pageCharset != self.DEFAULT_CHARSET_PARAMETER_VALUES
                )
                else ""
            )
            + (f"&pv_id={urlencode_plus(self.idPageview)}" if self.idPageview else "")
            + (
                "&_rcn=" + urlencode_plus(self.attributionInfo[0])
                if self.attributionInfo and self.attributionInfo[0]
                else ""
            )
            + (
                "&_rck=" + urlencode_plus(self.attributionInfo[1])
                if self.attributionInfo and self.attributionInfo[1]
                else ""
            )
            + (
                "&_refts=" + str(self.attributionInfo[2])
                if self.attributionInfo and self.attributionInfo[2]
                else ""
            )
            + (
                "&_ref=" + urlencode_plus(self.attributionInfo[3])
                if self.attributionInfo and self.attributionInfo[3]
                else ""
            )
            + (f"&country={urlencode_plus(self.country)}" if self.country else "")
            + (f"&region={urlencode_plus(self.region)}" if self.region else "")
            + (f"&city={urlencode_plus(self.city)}" if self.city else "")
            + (f"&lat={urlencode_plus(str(self.lat))}" if self.lat else "")
            + (f"&long={urlencode_plus(str(self.long))}" if self.long else "")
            + custom_fields
            + custom_dimensions
            + ("&send_image=0" if not self.sendImageResponse else "")
            + (f"&uadata={urlencode_plus(json.dumps(self.clientHints))}" if self.clientHints else "")
            + self.DEBUG_APPEND_URL
        )

        if self.idPageview:
            url += (
                (f"&pf_net={self.networkTime}" if self.networkTime else "")
                + (f"&pf_srv={self.serverTime}" if self.serverTime else "")
                + (f"&pf_tfr={self.transferTime}" if self.transferTime else "")
                + (
                    f"&pf_dm1={self.domProcessingTime}"
                    if self.domProcessingTime
                    else ""
                )
                + (
                    f"&pf_dm2={self.domCompletionTime}"
                    if self.domCompletionTime
                    else ""
                )
                + (f"&pf_onl={self.onLoadTime}" if self.onLoadTime else "")
            )
            self.clear_performance_timings()

        for key in self.ecommerceView:
            url += f"&{key}={urlencode_plus(self.ecommerceView[key])}"

        # Reset page level custom variables after this page view
        self.ecommerceView = {}
        self.pageCustomVar = {}
        self.eventCustomVar = {}
        self.clear_custom_dimensions()
        self.clear_custom_tracking_parameters()

        # force new visit only once, user must call again set_force_new_visit()
        self.forcedNewVisit = False

        return url

    def get_cookie_matching_name(self, name):
        """
        Returns a first party cookie which name contains name

        * @param str name
        * @return str String value of cookie, or None if not found
        * @ignore
        """
        if self.configCookiesDisabled or not self.request.cookie:
            return None
        name = self.get_cookie_name(name)

        # Matomo cookie names use dots separators in matomo.js,
        # but PHP Replaces + with _ http://www.php.net/manual/en/language.variables.predefined.php#72571
        name = name.replace(".", "_")
        for cookie_name, cookie_value in self.request.cookie.items():
            if strpos(name, cookie_name) is not False:  # 0 is fine
                return cookie_value

        return None

    def get_current_script_name(self):
        """
        If current URL is "http://example.org/dir1/dir2/index.php?param1=value1&param2=value2"
        will return "/dir1/dir2/index.php"

        * @return str
        * @ignore
        """
        url = ""
        if self.request.get("PATH_INFO"):
            url = self.request.get("PATH_INFO")
        elif self.request.get("REQUEST_URI"):
            url = self.request.get("REQUEST_URI", "").split("?")[0]

        if not url:
            # Use if-else instead of get with default to correctly handle empty values
            if self.request.get("SCRIPT_NAME"):
                url = self.request.get("SCRIPT_NAME")
            else:
                url = "/"

        if url and url[0] != "/":
            url = "/" + url

        return url

    def get_current_scheme(self):
        """
        If the current URL is 'http://example.org/dir1/dir2/index.php?param1=value1&param2=value2"
        will return 'http'

        * @return str 'https' or 'http'
        * @ignore
        """
        if "HTTPS" in self.request and (
            self.request.get("HTTPS") == "on" or self.request.get("HTTPS") is True
        ):
            return "https"
        return "http"

    def get_current_host(self):
        """
        If current URL is "http://example.org/dir1/dir2/index.php?param1=value1&param2=value2"
        will return "http://example.org"

        * @return str
        * @ignore
        """
        return self.request.get("HTTP_HOST", "unknown")

    def get_current_query_string(self):
        """
        If current URL is "http://example.org/dir1/dir2/index.php?param1=value1&param2=value2"
        will return "?param1=value1&param2=value2"

        * @return str
        * @ignore
        """
        url = ""
        if self.request.get("QUERY_STRING"):
            url += "?" + self.request.get("QUERY_STRING")
        return url

    def get_current_url(self):
        """
        Returns the current full URL (scheme, host, path and query string).

        * @return str
        * @ignore
        """
        return "".join(
            [
                self.get_current_scheme(),
                "://",
                self.get_current_host(),
                self.get_current_script_name(),
                self.get_current_query_string(),
            ]
        )

    def set_first_party_cookies(self):
        """
        Sets the first party cookies as would the matomo.js
        All cookies are supported: 'id' and 'ses' and 'ref' and 'cvar' cookies.
        * @return self
        """
        if self.configCookiesDisabled or not self.response:
            return self

        if self.cookieVisitorId:
            self.load_visitor_id_cookie()

        # Set the 'ref' cookie
        attribution_info = self.get_attribution_info()
        if attribution_info:
            self.set_cookie("ref", attribution_info, self.configReferralCookieTimeout)

        # Set the 'ses' cookie
        self.set_cookie("ses", "*", self.configSessionCookieTimeout)

        # Set the 'id' cookie
        cookie_value = f"{self.get_visitor_id()}.{self.createTs}"
        self.set_cookie("id", cookie_value, self.configVisitorCookieTimeout)

        # Set the 'cvar' cookie
        self.set_cookie(
            "cvar", json.dumps(self.visitorCustomVar), self.configSessionCookieTimeout
        )
        return self

    def _set_cookie(self, cookie_name, cookie_value, cookie_ttl):
        """
        Returns a HTTP header for a first party cookie to the client to improve dual JS-Python tracking.

        This replicates the matomo.js tracker algorithms for consistency and better accuracy.

        * @param cookie_name
        * @param cookie_value
        * @param cookie_ttl
        * @return string
        """
        cookie_expire = self.currentTs + cookie_ttl
        cookie_name = urlencode_plus(cookie_name)
        cookie_value = urlencode_plus(cookie_value)
        expires = f"; expires='{time.strftime('%a, %d-%m-%Y %H:%M:%S', time.gmtime(cookie_expire))} GMT" if cookie_expire else ""
        path = f"; path={self.configCookiePath}" if self.configCookiePath else ""
        domain = f"; domain={self.configCookieDomain}" if self.configCookieDomain else ""
        secure = "; secure" if self.configCookieSecure else ""
        http_only = "; HttpOnly" if self.configCookieHTTPOnly else ""
        same_site = f"; SameSite={urlencode_plus(self.configCookieSameSite)}" if self.configCookieSameSite else ""

        cookie_header = f"Set-Cookie: {cookie_name}={cookie_value}{expires}{path}{domain}{secure}{http_only}{same_site}"
        return cookie_header

    def set_cookie(self, cookie_name, cookie_value, cookie_ttl):
        """
        Sets a first party cookie to the client to improve dual JS-Python tracking.

        This replicates the matomo.js tracker algorithms for consistency and better accuracy.

        * @param cookie_name
        * @param cookie_value
        * @param cookie_ttl
        * @return self
        """
        cookie_expire = self.currentTs + cookie_ttl
        self.set_cookie_response(
            cookie_name,
            cookie_value,
            max_age=cookie_expire,
            secure=self.configCookieSecure,
            httponly=self.configCookieHTTPOnly,
            path=self.configCookiePath,
        )
        return self

    def set_cookie_response(
        self,
        cookie_name,
        cookie_value,
        max_age=None,
        path="/",
        domain=None,
        secure=False,
        httponly=False,
        samesite=None,
    ):
        """
        Sets a first party cookie to the client to improve dual JS-Python tracking.

        Unlike set_cookie this method is called with all cookie parameters. Unlike PHP cookie setting in Python is very
        framework specific so this method needs to be implemented

        @param cookie_name:
        @param cookie_value:
        @param max_age:
        @param path:
        @param domain:
        @param secure:
        @param httponly:
        @param samesite:
        """
        logging.error("set_cookie_response not implemented. Can't set a cookie")
        raise NotImplementedError

    def get_cookies(self):
        return self.request.cookie

    def get_custom_variables_from_cookie(self):
        """
        * @return dict
        """
        cookie = self.get_cookie_matching_name("cvar")
        if not cookie:
            return {}

        return json.loads(cookie)

    def set_outgoing_tracker_cookie(self, name, value=None):
        """
        Sets a cookie to be sent to the tracking server.

        * @param name
        * @param value
        """
        if value is None:
            del self.outgoingTrackerCookies[name]
        else:
            self.outgoingTrackerCookies[name] = value

    def get_incoming_tracker_cookie(self, name):
        """
        Gets a cookie which was set by the tracking server.

        * @param name

        * @return bool|string
        """
        return self.incomingTrackerCookies.get(name, False)

    def parse_incoming_cookies(self, headers):
        """
        Reads incoming tracking server cookies.

        * @param array headers Array with HTTP response headers as values
        """
        self.incomingTrackerCookies = {}

        if headers:
            header_name = "set-cookie:"
            header_name_length = len(header_name)

            for header in headers:
                if strpos(header.lower(), header_name) is False:
                    continue
                cookies = header[header_name_length:].strip()
                pos_end = strpos(cookies, ";")
                if pos_end is not False:  # 0 != False
                    cookies = cookies[:pos_end]
                self.incomingTrackerCookies = parse_qs(cookies)
