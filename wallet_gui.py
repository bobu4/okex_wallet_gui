import sys
import traceback

from PyQt5.QtWidgets import QPushButton, QLineEdit, QComboBox, QWidget, QLabel, QGridLayout, QApplication, QTextEdit
import okex.Funding_api as Funding
import okex.Account_api as Account
import okex.Market_api as Market
import okex.Trade_api as Trade
import random


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(500, 500)
        self.balances = None
        self.trade_balances = {}
        self.main_balances = {}
        self.cur_label = QLabel('Валюта')
        self.transfer_label = QLabel('Перевод')
        self.spot_label = QLabel('Торговля')
        self.type_order_box = QComboBox()
        self.type_order_box.addItem('Купить')
        self.type_order_box.addItem('Продать')
        self.trade_currency_box = QComboBox()
        self.trade_amount_edit = QLineEdit()
        self.trade_amount_edit.setPlaceholderText('Сума ордера')
        self.trade_button = QPushButton()
        self.type_order_box.activated[str].connect(self.type_order_changed)
        self.type_order_changed(self.type_order_box.currentText())
        self.transfer_box = QComboBox()
        self.main_label = QLabel('С Основной')
        self.sec_label = QLabel('С Торговый')
        self.withdraw_label = QLabel('Вывод')
        self.chain_label = QLabel('Сеть')
        self.wallet_number = QLabel('№ кошелька')
        self.balance_box = QComboBox()
        self.max_button = QPushButton('Максимум')
        self.chain_box = QComboBox()
        self.transfer_box.addItem('С Основной')
        self.transfer_box.addItem('С Торговый')
        self.transfer_box.addItem('С Субакков')
        self.wallet_box = QComboBox()
        self.transfer_edit = QLineEdit()
        self.withdraw_type_box = QComboBox()
        self.withdraw_type_box.addItem('Диапазон')
        self.withdraw_type_box.addItem('Сума')
        api_key = '1234567890qwertyuiopqwqed'
        secret_key = '12341245356sdfvnhgjngj'
        passphrase = '1234567899qwee'
        self.subacc_dict = {'subacc_list':
                            [{'api_key': None, 'secret_key': None, 'pass': None},
                             {'api_key': None, 'secret_key': None, 'pass': None},
                             {'api_key': None, 'secret_key': None, 'pass': None},
                             {'api_key': None, 'secret_key': None, 'pass': None}
                             ]}
        self.transfer_edit.setPlaceholderText('Сума перевода')
        self.withdraw_edit = QLineEdit()
        self.withdraw_min_edit = QLineEdit()
        self.withdraw_min_edit.setPlaceholderText('Диапазон:от')
        self.withdraw_max_edit = QLineEdit()
        self.withdraw_max_edit.setPlaceholderText('До')
        self.info_text = QTextEdit()
        self.withdraw_edit.setPlaceholderText('Сума вывода')
        self.method_changed(self.withdraw_type_box.currentText())
        self.refresh_button = QPushButton('Обновить')
        self.transfer_button = QPushButton('Перевести')
        self.withdraw_button = QPushButton('Вывести')
        self.okex_fundind_api = Funding.FundingAPI(api_key, secret_key, passphrase, False, '0')
        self.okex_account_api = Account.AccountAPI(api_key, secret_key, passphrase, False, '0')
        self.okex_market_api = Market.MarketAPI(api_key, secret_key, passphrase, False, '0')
        self.okex_trade_api = Trade.TradeAPI(api_key, secret_key, passphrase, False, '0')
        tickers = self.okex_market_api.get_tickers('SPOT')
        for ticker in tickers['data']:
            self.trade_currency_box.addItem(ticker['instId'])
        self.trade_currency_box.setEditable(True)
        self.chains_dict = {}
        with open('wallets.txt', 'r+') as wallets:
            self.wallets = wallets.read().split('\n')
        self.refresh_balance()
        if self.balance_box.currentText():
            for chains in self.chains_dict[self.balance_box.currentText().split(' ')[1]]:
                self.chain_box.addItem(chains)
        for num in range(len(self.wallets)):
            self.wallet_box.addItem(str(num + 1))
        self.balance_box.activated[str].connect(self.currency_changed)
        self.withdraw_type_box.activated[str].connect(self.method_changed)
        self.transfer_box.activated[str].connect(self.account_changed)
        self.refresh_button.clicked.connect(self.refresh_balance)
        self.max_button.clicked.connect(self.maximum_transfer)
        self.transfer_button.clicked.connect(self.transfer)
        self.withdraw_button.clicked.connect(self.withdraw)
        self.trade_button.clicked.connect(self.trade)
        grid = QGridLayout()
        grid.addWidget(self.cur_label, 0, 0, 2, 8)
        grid.addWidget(self.transfer_label, 0, 9, 2, 4)
        grid.addWidget(self.spot_label, 0, 14, 2, 4)
        grid.addWidget(self.type_order_box, 2, 14, 2, 4)
        grid.addWidget(self.trade_currency_box, 4, 14, 2, 4)
        grid.addWidget(self.trade_amount_edit, 6, 14, 2, 4)
        grid.addWidget(self.trade_button, 8, 14, 2, 4)
        grid.addWidget(self.withdraw_label, 0, 19, 2, 8)
        grid.addWidget(self.balance_box, 2, 0, 2, 8)
        grid.addWidget(self.transfer_box, 2, 10, 2, 4)
        grid.addWidget(self.chain_label, 2, 20, 2, 4)
        grid.addWidget(self.chain_box, 2, 25, 2, 4)
        grid.addWidget(self.transfer_edit, 4, 0, 2, 8)
        grid.addWidget(self.max_button, 4, 9, 2, 4)
        grid.addWidget(self.wallet_number, 4, 20, 2, 4)
        grid.addWidget(self.wallet_box, 4, 25, 2, 4)
        grid.addWidget(self.transfer_button, 6, 0, 2, 9)
        grid.addWidget(self.withdraw_type_box, 6, 20, 2, 9)
        grid.addWidget(self.info_text, 10, 0, 6, 18)
        grid.addWidget(self.withdraw_edit, 8, 22, 2, 5)
        grid.addWidget(self.withdraw_min_edit, 10, 20, 2, 4)
        grid.addWidget(self.withdraw_max_edit, 10, 25, 2, 4)
        grid.addWidget(self.withdraw_button, 12, 22, 2, 5)
        self.setLayout(grid)

    def currency_changed(self, text):
        self.chain_box.clear()
        if self.chains_dict:
            for chains in self.chains_dict[text.split(' ')[1]]:
                self.chain_box.addItem(chains)

    def refresh_balance(self):
        self.balance_box.clear()
        if self.transfer_box.currentText() == 'С Основной':
            self.balances = self.okex_fundind_api.get_balances()
            currencies = ''
            self.chains_dict = {}
            for ccy in self.balances['data']:
                if ccy != self.balances['data'][-1]:
                    currencies += f'''{ccy['ccy']},'''
                else:
                    currencies += ccy['ccy']
                self.chains_dict[ccy['ccy']] = {}
            for bal in self.balances['data']:
                self.main_balances[bal['ccy']] = bal['availBal']
            chains = {'data': []}
            if self.balances['data']:
                chains = self.okex_fundind_api.get_currency(currencies)
                for chain in chains['data']:
                    self.chains_dict[chain['ccy']].update({chain['chain']: {'minWd': chain['minWd'], 'minFee': chain['minFee']}})
                for num, chain in enumerate(self.chains_dict):
                    self.balance_box.addItem(f'''{float(self.balances['data'][num]['bal']):.2f} {chain}''')
        elif self.transfer_box.currentText() == 'С Торговый':
            self.balances = self.okex_account_api.get_account()
            currencies = ''
            self.chains_dict = {}
            for ccy in self.balances['data'][0]['details']:
                if ccy != self.balances['data'][0]['details'][-1]:
                    currencies += f'''{ccy['ccy']},'''
                else:
                    currencies += ccy['ccy']
                self.chains_dict[ccy['ccy']] = {}
            chains = {'data': []}
            if 'ccy' in self.balances['data'][0]['details'][0]:
                chains = self.okex_fundind_api.get_currency(currencies)
                for chain in chains['data']:
                    self.chains_dict[chain['ccy']].update({chain['chain']: chain['minWd']})
                self.trade_balances = {}
                for bal in self.balances['data'][0]['details']:
                    self.trade_balances[bal['ccy']] = bal['availBal']
                for num, chain in enumerate(self.chains_dict):
                    try:
                        self.balance_box.addItem(f'''{float(self.trade_balances[chain]):.2f} {chain}''')
                    except (IndexError, KeyError) as e:
                        self.balance_box.addItem(f'''{0.00:.3f} {chain}''')
        self.currency_changed(self.balance_box.currentText())

    def maximum_transfer(self):
        if self.transfer_box.currentText() == 'С Основной':
            availbal = self.main_balances[self.balance_box.currentText().split(' ')[1]]
        elif 'С Торговый':
            availbal = self.trade_balances[self.balance_box.currentText().split(' ')[1]]
        self.transfer_edit.setText(availbal)

    def transfer(self):
        if self.transfer_box.currentText() == 'С Субакков':
            self.subacc_transfer()
        else:
            if self.transfer_box.currentText() == 'С Основной':
                from_acc = '6'
                to_acc = '18'
                to_acc_str = 'Торговый'
            elif self.transfer_box.currentText() == 'С Торговый':
                from_acc = '18'
                to_acc = '6'
                to_acc_str = 'Основной'
            transfer_amount = self.transfer_edit.text()
            transfer_currency = self.balance_box.currentText().split(' ')[1]
            try:
                transfer_response = self.okex_fundind_api.funds_transfer(transfer_currency, transfer_amount, from_acc, to_acc)
                if transfer_response['code'] == '0':
                    self.info_text.append(f'''Выполнен перевод {float(transfer_amount):.2f}{transfer_currency} с {self.transfer_box.currentText()} на {to_acc_str}''')
                    self.refresh_balance()
                else:
                    self.info_text.append(str(transfer_response))
            except:
                self.info_text.append(str(traceback.format_exc()))

    def account_changed(self, text):
        if text == 'С Субакков':
            pass
        else:
            self.refresh_balance()

    def method_changed(self, text):
        if text == 'Сума':
            self.withdraw_edit.setEnabled(True)
            self.withdraw_min_edit.setEnabled(False)
            self.withdraw_max_edit.setEnabled(False)
        else:
            self.withdraw_min_edit.setEnabled(True)
            self.withdraw_max_edit.setEnabled(True)
            self.withdraw_edit.setEnabled(False)

    def withdraw(self):
        if self.withdraw_type_box.currentText() == 'Диапазон':
            minimum = float(self.withdraw_min_edit.text())
            maximum = float(self.withdraw_max_edit.text())
            currency = self.balance_box.currentText().split(' ')[1]
            chain = self.chain_box.currentText()
            amount = f'{random.uniform(minimum, maximum):.2f}'
            fee = self.chains_dict[currency][chain]['minFee']
            wallet = self.wallets[int(float(self.wallet_box.currentText())) - 1]
            withdraw_result = self.okex_fundind_api.coin_withdraw(currency, amount, '4', wallet, chain, fee)
            if withdraw_result['code'] == '0':
                self.info_text.append(f'''Вывод {amount} {currency} в сети {chain} на {wallet} комиссия {fee}''')
            else:
                self.info_text.append(str(withdraw_result))
        else:
            amount = f'{float(self.withdraw_edit.text()):.6f}'
            currency = self.balance_box.currentText().split(' ')[1]
            chain = self.chain_box.currentText()
            fee = self.chains_dict[currency][chain]['minFee']
            wallet = self.wallets[int(float(self.wallet_box.currentText())) - 1]
            withdraw_result = self.okex_fundind_api.coin_withdraw(currency, amount, '4', wallet, chain, fee)
            if withdraw_result['code'] == '0':
                self.info_text.append(f'''Вывод {amount} {currency} в сети {chain} на {wallet} комиссия {fee}''')
            else:
                self.info_text.append(str(withdraw_result))
        if withdraw_result['code'] == '0':
            self.refresh_balance()

    def type_order_changed(self, text):
        self.trade_button.setText(text)

    def trade(self):
        pair = self.trade_currency_box.currentText()
        mode = 'cash'
        target_ccy = 'base_ccy'
        if self.type_order_box.currentText() == 'Купить':
            side = 'buy'
            side_str = 'Куплено'
        else:
            side = 'sell'
            side_str = 'Продано'
        order_type = 'market'
        order_size = self.trade_amount_edit.text()
        trade_result = self.okex_trade_api.place_order(pair, mode, side, order_type, order_size, tgtCcy=target_ccy)
        if trade_result['code'] == '0':
            order_details = self.okex_trade_api.get_orders(pair, trade_result['data'][0]['ordId'])
            trade_amount = order_details['data'][0]['accFillSz']
            order_price = order_details['data'][0]['avgPx']
            output = float(trade_amount) * float(order_price)
            if side == 'sell':
                out_ccy = order_details['data'][0]['feeCcy']
                in_ccy = order_details['data'][0]['rebateCcy']
            else:
                in_ccy = order_details['data'][0]['feeCcy']
                out_ccy = order_details['data'][0]['rebateCcy']
            self.info_text.append(f'''{side_str} {trade_amount}{in_ccy} за {output:.4f}{out_ccy}''')
            self.refresh_balance()
        else:
            self.info_text.append(str(trade_result))

    def subacc_transfer(self):
        sub_balances = {'data': []}
        for sub_acc in self.subacc_dict['subacc_list']:
            if sub_acc['pass']:
                funding_sub = Funding.FundingAPI(sub_acc['api_key'], sub_acc['secret_key'], sub_acc['pass'], False, '0')
                sub_balances = funding_sub.get_balances()
                for ccy in sub_balances['data']:
                    currency = ccy['ccy']
                    amount = ccy['availBal']
                    transfer_result = funding_sub.funds_transfer(currency, amount, '6', '6', '3')
                    if transfer_result['code'] == '0':
                        self.info_text.append(f'Переведено {amount}{currency} с субаккаунта на основной')
                    else:
                        self.info_text.append(str(transfer_result))
            else:
                self.transfer_box.setCurrentIndex(0)
        if sub_balances['data'] and self.subacc_dict['subacc_list'][0]['pass']:
            self.transfer_box.setCurrentIndex(0)
            self.refresh_balance()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
