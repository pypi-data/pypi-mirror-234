from quantplay.broker.motilal import Motilal

motilal = Motilal()


def test_account_summary():
    summary = motilal.account_summary()
    assert "pnl" in summary
    assert "margin_used" in summary
    assert "margin_available" in summary


def test_place_order():
    motilal.place_order(
        tradingsymbol="SENSEX23O0665900CE",
        exchange="BFO",
        quantity=10,
        order_type="LIMIT",
        transaction_type="BUY",
        tag="testing",
        product="NORMAL",
        price=1,
    )


def test_get_lot_size():
    assert motilal.get_lot_size("NSE", "SBIN") == 1
    assert motilal.get_lot_size("NFO", "BANKNIFTY23DEC44000CE") == 15
    assert motilal.get_lot_size("NSEFO", "BANKNIFTY23DEC44000CE") == 15
    assert motilal.get_lot_size("BFO", "SENSEX23DEC66000CE") == 10
    assert motilal.get_lot_size("BSEFO", "SENSEX23DEC66000CE") == 10


def test_get_ltp():
    assert motilal.get_ltp("NFO", "BANKNIFTY23DEC44000CE") > 0
    assert motilal.get_ltp("NSE", "SBIN") > 0
    assert motilal.get_ltp("BSEFO", "SENSEX23O0666300CE")


def test_positions():
    motilal.positions()


def test_orders():
    motilal.orders()


def test_square_off_all():
    motilal.exit_all_trigger_orders(dry_run=True)
