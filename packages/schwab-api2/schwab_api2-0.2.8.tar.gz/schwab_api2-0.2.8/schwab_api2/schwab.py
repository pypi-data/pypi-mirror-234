import json
from bs4 import BeautifulSoup as bs4
import urllib.parse
from time import sleep
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

from . import urls
from .account_information import Position, Account
from .authentication import SessionManager

class Schwab(SessionManager):
    def __init__(self, **kwargs):
        """
            The Schwab class. Used to interact with schwab.

        """
        self.headless = kwargs.get("headless", True)
        self.browserType = kwargs.get("browserType", "firefox")
        super(Schwab, self).__init__()

    def get_account_info(self):
        """
            Returns a dictionary of Account objects where the key is the account number
        """

        account_info = dict()
        r = self.session.get(urls.positions_data())
        response = json.loads(r.text)
        for account in response['Accounts']:
            positions = list()
            for security_group in account["SecurityGroupings"]:
                for position in security_group["Positions"]:
                    positions.append(
                        Position(
                            position["DefaultSymbol"],
                            position["Description"],
                            int(position["Quantity"]),
                            float(position["Cost"]),
                            float(position["MarketValue"])
                        )._as_dict()
                    )
            account_info[int(account["AccountId"])] = Account(
                account["AccountId"],
                positions,
                account["Totals"]["MarketValue"],
                account["Totals"]["CashInvestments"],
                account["Totals"]["AccountValue"],
                account["Totals"]["Cost"],
            )._as_dict()

        return account_info


    def account_select(self, account_id):
        self.page.set_default_timeout(2000)
        for i in range(5):
            try:
                self.page.wait_for_selector("#mcAccountSelector")
                self.page.locator("#mcAccountSelector").click()
                accounts = self.page.locator(f"(//span[text()='{account_id}'])").all()
                accounts[0].click()
                break
            except PlaywrightTimeoutError:
                print("Account selector not found. Trying again.")
                sleep(1)
        self.page.set_default_timeout(10000)
        if i == 4:
            raise Exception("Cannot select account please try again or check account number.")

       
    def preview_order(self, order_type, order_messages):
        """Get order information off the "preview order" page.

        Args:
            order_type (int): Order type of the order being placed.
            order_messages (Dict of str): Dictionary of information about the order.

        Returns:
            Dict of str: Dictionary of information about the order.
        """
        # Margin accounts have a different preview page.
        try:
            preview_margin = self.page.locator(".mcaio--form-delivery > div:nth-child(1)").text_content()
            preview_margin = preview_margin.split("\n")
            preview_margin = preview_margin[1].replace("\t", "")
            messages = {
                'order_messages': preview_margin
            }
            return messages
        except PlaywrightTimeoutError:
            pass

        preview_account = self.page.locator("span.mcaio-text-medium:nth-child(1)").text_content()
        preview_funds = self.page.locator("span.mcaio-text-medium:nth-child(3) > strong:nth-child(1)").text_content()
        preview_raw = self.page.locator("mc-trade-order-description.sdps-row").inner_html()
        preview_soup = bs4(preview_raw, "html.parser")
        preview_action = preview_soup.find('span', id="review-action").get_text()
        preview_quatity = preview_soup.find('span', id="review-qty").get_text()
        preview_symbol = preview_soup.find('span', id="review-symbol").get_text()
        if order_type != 1:
            preview_type_price = preview_soup.find('span', id="review-limit").get_text().replace("\xa0", " at ")
            preview_price = preview_type_price.split(" ")[-1]
            preview_type = preview_type_price.split(" ")[0]
        else:
            preview_price = None
            preview_type = preview_soup.find('span', id="review-limit").get_text()
        preview_timing = preview_soup.find('span', id="review-timing").get_text()
        estimated_amt = preview_soup.find('span', id="review-est-amt").get_text()
        estimated_exch = preview_soup.find('span', id="review-est-exhc").get_text()
        estimated_comm = preview_soup.find('span', id="review-est-comm").get_text()
        estimated_total = preview_soup.find('span', id="review-est-total").get_text()
        messages = {
            'account': preview_account.split(" ")[-1],
            'account_type': preview_account.split(" ")[1],
            'available_funds': preview_funds,
            'action': preview_action,
            'quantity': preview_quatity,
            'order_type': preview_type.split(" ")[0].replace(",", ""),
            'symbol': preview_symbol,
            'price': preview_price,
            'timing': preview_timing,
            'estimated_amt': estimated_amt,
            'estimated_exch': estimated_exch,
            'estimated_comm': estimated_comm,
            'estimated_total': estimated_total.replace(" ", "").replace("\n", ""),
            'order_messages': order_messages
        }
        return messages


    def get_order_messages(self):
        """Gets the API return informational messages. Checks if the order preview says order is ok.

        Returns:
            List of str: List of informational messages.
        """
        order_messages = []
        try:
            self.page.locator("#accordion-container-accordion-section-1-title").click()
            order_element = self.page.locator("#accordion-container-accordion-section-1-body > div:nth-child(1)")
            order_child = order_element.locator("ul > li").all()
            for child in order_child:
                child = child.text_content().replace("\n","").replace("\t","")
                if child != "":
                    order_messages.append(child)
            return order_messages, True
        except PlaywrightTimeoutError:
            order_element = self.page.locator(".mcaio--errors-list")
            order_child = order_element.locator("li").all()
            for child in order_child:
                child = child.text_content().replace("\n","").replace("\t","")
                if child != "":
                    order_messages.append(child)
            return order_messages, False


    def trade(self, ticker, action, qty, order_type, account_id, duration="DAY", price=0.00, dry_run=True):
        """
            ticker (Str) - The symbol you want to trade,
            action (str) - Either 'Buy' or 'Sell',
            qty (int) - The amount of shares to buy/sell,
            order_type (str) - Either 'Market' or 'Limit',
            account_id (int) - The account ID to place the trade on. If the ID is XXXX-XXXX,
                         we're looking for just XXXXXXXX.,
            duration (str) - Either 'Day', 'Day+', 'GTC', 'GTC+', 'EXTAM', 'EXTPM', or 'FOK',
            price (float) - The price to buy/sell at. Only used if order_type is 'Limit',
            dry_run (bool) - If True, we won't place the order, we'll just verify it.,

            Returns messages (dict of str), success (boolean)
        """
        # Add a dash so we can select the account number out of the list.
        if "-" not in account_id:
            account_id = account_id[:4] + "-" + account_id[4:]

        # Change strings to the index positions of the dropdowns.
        if action == "Buy":
            action = 1
        elif action == "Sell":
            action = 2
        else:
            raise Exception("side must be either Buy or Sell")

        if order_type == "Market":
            order_type = 1
        elif order_type == "Limit":
            order_type = 2
        else:
            raise Exception("order_type must be either Market or Limit")

        if duration == "DAY":
            duration = 0
        elif duration == "DAY+":
            duration = 1
        elif duration == "GTC":
            duration = 2
        elif duration == "GTC+":
            duration = 3
        elif duration == "EXTAM":
            duration = 4
        elif duration == "EXTPM":
            duration = 5
        elif duration == "FOK":
            duration = 6
        else:
            raise Exception("duration must be either Day, Day+, GTC, GTC+, EXTAM, EXTPM, or FOK")

        # Perform trade
        if self.page.url != urls.order_page():
            self.page.goto(url=urls.order_page())
        self.account_select(account_id)
        symbol_form = self.page.locator("#_txtSymbol")
        symbol_form.type(ticker)
        self.page.keyboard.press('Enter')
        action_dropdown = self.page.locator("select#_action")
        action_dropdown.select_option(index=action)
        quantity_box = self.page.locator("#ordernumber01inputqty-stepper-input")
        quantity_box.clear()
        quantity_box.type(str(qty))
        self.page.locator(".mtt-dropdown__select").select_option(index=order_type)
        if order_type == 2:
            price_input = self.page.locator("#limitprice-stepper-input")
            price_input.clear()
            price_input.type(str(price))
            if duration != 0:
                self.page.locator("#_timing").select_option(index=duration)
        self.page.wait_for_selector(".mcaio-order--reviewbtn").click()
        order_messages, success = self.get_order_messages()
        if dry_run:
            messages = self.preview_order(order_type, order_messages)
        else:
            if success:
                self.page.wait_for_selector("#mtt-place-button").click()
                confirm_raw = self.page.wait_for_selector("#orders").inner_html()
                confirm_soup = bs4(confirm_raw, "html.parser")
                confirm_acct_info = confirm_soup.find('span', class_="account-info").get_text()
                confirm_acct_info = confirm_acct_info.split(" ")
                confirm_acct_info = confirm_acct_info[1].split("\n")
                confirm_account = confirm_acct_info[0]
                confirm_acct_type = confirm_acct_info[1]
                confirm_action = confirm_soup.find('span', id="confirm-action").get_text()
                confirm_quantity = confirm_soup.find('span', id="confirm-qty").get_text()
                confirm_symbol = confirm_soup.find('span', id="confirm-symbol").get_text()
                confirm_order_type = confirm_soup.find('span', id="confirm-limit").get_text()
                confirm_timing = confirm_soup.find('span', id="confirm-timing").get_text()
                confirm_order_num = confirm_soup.find('a', class_="confirm-order-num").get_text()
                confirm_messages = []
                confirm_messages.append(confirm_soup.find('p', class_="sdps-text-s-heading").get_text())
                confirm_messages.append(confirm_soup.find('p', class_="sdps-text-legal").get_text())
                messages = {
                    'account': confirm_account,
                    'account_type': confirm_acct_type,
                    'action': confirm_action,
                    'quantity': confirm_quantity,
                    'symbol': confirm_symbol,
                    'order_type': confirm_order_type.replace("\xa0", " at ").replace(",", ""),
                    'timing': confirm_timing,
                    'order_num': confirm_order_num.replace("#", ""),
                    'order_messages': confirm_messages
                }
                success = True
            else:
                messages = self.preview_order(order_type, order_messages)
                success = False
        self.page.reload()
        return messages, success
