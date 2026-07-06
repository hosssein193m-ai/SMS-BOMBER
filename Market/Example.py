from market import *

# ============================================
# مثال‌های کامل استفاده از کلاس‌ها و توابع
# ============================================

from typing import Optional, Dict, Tuple, List, Union
import time
from datetime import datetime

# ============================================
# 1. کار با بازار ایران (Iranian_market)
# ============================================

def example_iranian_market():
    """نمایش نحوه کار با بازار ایران"""
    print("\n" + "="*60)
    print("🏦 بازار ایران")
    print("="*60)
    
    # ایجاد نمونه
    iran = Iranian_market()
    
    # دریافت و ذخیره داده‌های جدید
    print("📥 دریافت داده‌های جدید...")
    iran.set()
    
    # دریافت همه قیمت‌ها
    print("\n💰 قیمت‌های لحظه‌ای:")
    all_prices = iran.get_currencies()
    for currency, price in all_prices.items():
        if currency != "extraction time":
            print(f"  {currency}: {price} ریال")
    
    # جستجوی یک ارز خاص
    print("\n🔍 جستجوی قیمت دلار:")
    dollar_price, dollar_dict = iran.search("dollar")
    print(f"  قیمت دلار: {dollar_price} ریال")
    print(f"  دیکشنری: {dollar_dict}")
    
    # دریافت زمان استخراج
    print(f"\n⏰ زمان استخراج: {iran.search_time()}")
    
    return all_prices

# ============================================
# 2. کار با بازار جهانی (World_Market)
# ============================================

def example_world_market():
    """نمایش نحوه کار با بازار جهانی"""
    print("\n" + "="*60)
    print("🌍 بازار جهانی")
    print("="*60)
    
    # ایجاد نمونه
    world = World_Market()
    
    # دریافت و ذخیره داده‌ها
    print("📥 دریافت داده‌های جدید...")
    world.set()
    
    # دریافت همه قیمت‌ها (بدون تایم‌استمپ)
    print("\n💰 قیمت‌های لحظه‌ای (۱۰ ارز اول):")
    all_prices = world.get_currencies(license=False)
    for i, item in enumerate(all_prices[:10], 1):
        if isinstance(item, dict):
            for name, data in item.items():
                print(f"  {i}. {name}: {data['price']} (تغییر: {data['change_24h']})")
    
    # جستجوی یک ارز خاص
    print("\n🔍 جستجوی بیت‌کوین:")
    try:
        btc_data = world.search("BTCUSDT")
        print(f"  اطلاعات کامل: {btc_data}")
        print(f"  قیمت: {btc_data['price']}")
        print(f"  تغییر ۲۴ ساعته: {btc_data['change_24h']}")
        print(f"  حجم: {btc_data['volume']}")
    except ValueError as e:
        print(f"  ❌ {e}")
    
    # جستجوی فیلد خاص
    print("\n🔍 جستجوی قیمت اتریوم:")
    try:
        eth_price = world.search("ETHUSDT", "price")
        print(f"  قیمت اتریوم: {eth_price}")
    except ValueError as e:
        print(f"  ❌ {e}")
    
    # دریافت زمان استخراج
    time_info = world.search_time()
    if time_info:
        print(f"\n⏰ زمان استخراج: {time_info[0]}")
    
    return all_prices

# ============================================
# 3. کار با رتبه‌بندی بازار (MarketLeaders)
# ============================================

def example_market_leaders():
    """نمایش نحوه کار با رتبه‌بندی بازار"""
    print("\n" + "="*60)
    print("🏆 رتبه‌بندی بازار")
    print("="*60)
    
    # ایجاد نمونه
    leaders = MarketLeaders()
    
    # دریافت و ذخیره داده‌ها
    print("📥 دریافت رتبه‌بندی‌ها...")
    leaders.set()
    
    # دریافت همه رتبه‌بندی‌ها
    print("\n📊 همه رتبه‌بندی‌ها:")
    all_rankings = leaders.get_all_rankings()
    for rank_type, data in all_rankings.items():
        print(f"  🏅 {rank_type}:")
        print(f"     نام: {data.get('name', 'N/A')}")
        print(f"     قیمت: {data.get('price', 'N/A')}")
    
    # دریافت رتبه‌بندی‌های خاص
    print("\n🎯 رتبه‌بندی‌های خاص:")
    
    gainers = leaders.get_top_gainers()
    if gainers:
        print(f"  🚀 پیشروها: {gainers['پیشروها']['name']} - {gainers['پیشروها']['price']}")
    
    losers = leaders.get_top_losers()
    if losers:
        print(f"  📉 بیشترین کاهش: {losers['بیشترین کاهش قیمت']['name']} - {losers['بیشترین کاهش قیمت']['price']}")
    
    volume = leaders.get_top_volume()
    if volume:
        print(f"  📊 حجم برتر: {volume['حجم برتر']['name']} - {volume['حجم برتر']['price']}")
    
    # جستجوی یک ارز
    print("\n🔍 جستجوی ارز در رتبه‌بندی:")
    found, data = leaders.find_currency("BTCUSDT")
    if found:
        print(f"  ✅ BTCUSDT یافت شد: {data}")
    else:
        print(f"  ❌ BTCUSDT یافت نشد")
    
    # جستجوی با فیلد
    print("\n🔍 جستجوی قیمت پیشروها:")
    price = leaders.search("پیشروها", "price")
    print(f"  قیمت: {price}")
    
    # زمان استخراج
    print(f"\n⏰ زمان استخراج: {leaders.search_time()}")
    
    return all_rankings

# ============================================
# 4. توابع تبدیل ارز
# ============================================

def example_conversions():
    """نمایش توابع تبدیل ارز"""
    print("\n" + "="*60)
    print("💱 توابع تبدیل ارز")
    print("="*60)
    
    # تبدیل دلار به ریال
    dollar_amount = 100
    rial_amount = Dollar_to_Rial(dollar_amount)
    print(f"💰 {dollar_amount} دلار = {Read_price(rial_amount)} ریال")
    
    # تبدیل ریال به دلار
    rial_amount = 50_000_000
    dollar_amount = Rial_to_Dollar(rial_amount)
    print(f"💰 {Read_price(rial_amount)} ریال = {dollar_amount:.2f} دلار")
    
    # تبدیل تتر به ریال
    tether_amount = 10
    rial_amount = Tether_to_Rial(tether_amount)
    print(f"🪙 {tether_amount} تتر = {Read_price(rial_amount)} ریال")
    
    # تبدیل طلا به ریال
    gold_gram = 0.5
    rial_amount = Gold_to_Rial(gold_gram)
    print(f"🥇 {gold_gram} گرم طلا = {Read_price(rial_amount)} ریال")

# ============================================
# 5. تحلیل و مقایسه داده‌ها
# ============================================

def example_analyst():
    """نمایش تحلیل و مقایسه داده‌ها"""
    print("\n" + "="*60)
    print("📊 تحلیل و مقایسه داده‌ها")
    print("="*60)
    
    # تحلیل بازار ایران
    print("\n🔍 تحلیل بازار ایران:")
    try:
        diff_iran = analyst(Iranian_market, set=False)
        if diff_iran:
            print(f"  تغییرات: {diff_iran}")
        else:
            print("  ✅ داده‌ها بدون تغییر هستند")
    except Exception as e:
        print(f"  ❌ خطا: {e}")
    
    # تحلیل بازار جهانی
    print("\n🔍 تحلیل بازار جهانی:")
    try:
        diff_world = analyst(World_Market, set=False)
        if diff_world:
            print(f"  تغییرات: {diff_world}")
        else:
            print("  ✅ داده‌ها بدون تغییر هستند")
    except Exception as e:
        print(f"  ❌ خطا: {e}")

# ============================================
# 6. خروجی CSV
# ============================================

def example_csv_export():
    """نمایش خروجی CSV"""
    print("\n" + "="*60)
    print("📁 خروجی CSV")
    print("="*60)
    
    # خروجی بازار ایران
    print("\n📄 ایجاد فایل prices_iran.csv...")
    result = export_to_csv_iran("prices_iran_example.csv")
    if result:
        print("  ✅ فایل prices_iran_example.csv ایجاد شد")
    else:
        print("  ❌ خطا در ایجاد فایل")
    
    # خروجی بازار جهانی
    print("\n📄 ایجاد فایل prices_world.csv...")
    result = export_to_csv_world("prices_world_example.csv")
    if result:
        print("  ✅ فایل prices_world_example.csv ایجاد شد")
    else:
        print("  ❌ خطا در ایجاد فایل")

# ============================================
# 7. سناریوهای کاربردی ترکیبی
# ============================================

def example_scenario_1_daily_report():
    """سناریو ۱: گزارش روزانه بازار"""
    print("\n" + "="*60)
    print("📈 گزارش روزانه بازار")
    print("="*60)
    
    # دریافت داده‌های بازار ایران
    iran = Iranian_market()
    iran.set()
    iran_data = iran.get_currencies()
    
    # دریافت رتبه‌بندی
    leaders = MarketLeaders()
    leaders.set()
    rankings = leaders.get_all_rankings()
    
    # ایجاد گزارش
    print("\n📊 گزارش روزانه بازار:")
    print("━" * 50)
    print(f"⏰ زمان: {iran_data.get('extraction time', 'N/A')}")
    print("\n💰 قیمت‌های اصلی:")
    print(f"  دلار: {iran_data.get('dollar', 'N/A')} ریال")
    print(f"  طلا ۱۸ عیار: {iran_data.get('gold 18', 'N/A')} ریال")
    print(f"  سکه: {iran_data.get('coin', 'N/A')} ریال")
    print(f"  تتر: {iran_data.get('Tether', 'N/A')} ریال")
    print(f"  بیت‌کوین: {iran_data.get('Bitcoin', 'N/A')} دلار")
    print(f"  نفت برنت: {iran_data.get('Brent oil', 'N/A')} دلار")
    
    print("\n🏆 رتبه‌بندی بازار:")
    for rank_type, data in rankings.items():
        print(f"  {rank_type}: {data.get('name', 'N/A')} - {data.get('price', 'N/A')}")

def example_scenario_2_trading_signals():
    """سناریو ۲: سیگنال‌های معاملاتی"""
    print("\n" + "="*60)
    print("📈 سیگنال‌های معاملاتی")
    print("="*60)
    
    # دریافت رتبه‌بندی
    leaders = MarketLeaders()
    leaders.set()
    
    # بررسی سیگنال‌ها
    print("\n🔔 سیگنال‌های معاملاتی:")
    print("━" * 50)
    
    # سیگنال خرید - ارز در لیست پیشروها
    gainers = leaders.get_top_gainers()
    if gainers:
        name = gainers['پیشروها']['name']
        price = gainers['پیشروها']['price']
        print(f"📈 سیگنال خرید: {name}")
        print(f"   قیمت: {price}")
        print(f"   دلیل: در لیست پیشروها قرار دارد")
    
    # سیگنال فروش - ارز در لیست کاهش‌دهنده‌ها
    losers = leaders.get_top_losers()
    if losers:
        name = losers['بیشترین کاهش قیمت']['name']
        price = losers['بیشترین کاهش قیمت']['price']
        print(f"📉 سیگنال فروش: {name}")
        print(f"   قیمت: {price}")
        print(f"   دلیل: در لیست بیشترین کاهش قرار دارد")
    
    # سیگنال حجم بالا
    volume = leaders.get_top_volume()
    if volume:
        name = volume['حجم برتر']['name']
        price = volume['حجم برتر']['price']
        print(f"📊 حجم بالا: {name}")
        print(f"   قیمت: {price}")
        print(f"   دلیل: بیشترین حجم معاملات را دارد")

def example_scenario_3_price_alert():
    """سناریو ۳: هشدار قیمت"""
    print("\n" + "="*60)
    print("🔔 سیستم هشدار قیمت")
    print("="*60)
    
    # دریافت قیمت‌ها
    iran = Iranian_market()
    iran.set()
    
    # تعیین آستانه‌ها
    thresholds = {
        "dollar": 2_000_000,  # اگر دلار از ۲ میلیون گذشت
        "gold 18": 200_000_000,  # اگر طلا از ۲۰۰ میلیون گذشت
        "Tether": 2_000_000,  # اگر تتر از ۲ میلیون گذشت
    }
    
    print("\n🔍 بررسی هشدارها:")
    print("━" * 50)
    
    for currency, threshold in thresholds.items():
        try:
            price_str, _ = iran.search(currency)
            price = int(price_str.replace(',', ''))
            
            if price > threshold:
                print(f"⚠️ هشدار! قیمت {currency} از حد مجاز گذشت!")
                print(f"   قیمت فعلی: {Read_price(price)} ریال")
                print(f"   حد مجاز: {Read_price(threshold)} ریال")
                print(f"   اختلاف: {Read_price(price - threshold)} ریال")
            else:
                print(f"✅ قیمت {currency} در محدوده مجاز است: {Read_price(price)} ریال")
                
        except (ValueError, KeyError) as e:
            print(f"❌ خطا در بررسی {currency}: {e}")

def example_scenario_4_portfolio_value():
    """سناریو ۴: محاسبه ارزش پورتفولیو"""
    print("\n" + "="*60)
    print("💼 محاسبه ارزش پورتفولیو")
    print("="*60)
    
    # پورتفولیوی فرضی
    portfolio = {
        "dollar": 1000,
        "Tether": 500,
        "Bitcoin": 0.1,
        "gold 18": 50,
    }
    
    iran = Iranian_market()
    iran.set()
    
    total_value_rial = 0
    total_value_dollar = 0
    
    print("\n📊 ارزش پورتفولیو:")
    print("━" * 50)
    
    for currency, amount in portfolio.items():
        try:
            price_str, _ = iran.search(currency)
            
            # ✅ پشتیبانی از اعداد اعشاری
            if '.' in price_str:
                price = float(price_str.replace(',', ''))
            else:
                price = int(price_str.replace(',', ''))
            
            if currency in ["dollar", "Tether"]:
                value_rial = price * amount
                value_dollar = amount
            elif currency == "Bitcoin":
                # ✅ بیت‌کوین به دلار
                value_dollar = price * amount
                dollar_price = int(iran.search("dollar")[0].replace(',', ''))
                value_rial = value_dollar * dollar_price
            elif currency == "gold 18":
                value_rial = price * amount
                dollar_price = int(iran.search("dollar")[0].replace(',', ''))
                value_dollar = value_rial / dollar_price
            else:
                continue
            
            total_value_rial += value_rial
            total_value_dollar += value_dollar
            
            print(f"  {currency}: {amount:,.2f} = {Read_price(value_rial)} ریال")
            
        except Exception as e:
            print(f"  ❌ خطا در محاسبه {currency}: {e}")
    
    print("━" * 50)
    print(f"💰 ارزش کل: {Read_price(total_value_rial)} ریال")
    print(f"💵 ارزش کل: {total_value_dollar:,.2f} دلار")

def example_scenario_5_arbitrage_opportunity():
    """سناریو ۵: تشخیص فرصت آربیتراژ"""
    print("\n" + "="*60)
    print("🔄 تشخیص فرصت آربیتراژ")
    print("="*60)
    
    # دریافت قیمت‌ها
    iran = Iranian_market()
    iran.set()
    
    try:
        # قیمت دلار در بازار ایران
        dollar_price_irr = int(iran.search("dollar")[0].replace(',', ''))
        
        # قیمت تتر در بازار ایران
        tether_price_irr = int(iran.search("Tether")[0].replace(',', ''))
        
        # قیمت دلار جهانی (از بازار جهانی)
        world = World_Market()
        world.set()
        try:
            btc_price = world.search("BTCUSDT", "price")
            # برای سادگی، فرض می‌کنیم قیمت دلار جهانی ۱ است
            dollar_price_usd = 1
        except:
            dollar_price_usd = 1
        
        print("📊 بررسی آربیتراژ:")
        print("━" * 50)
        print(f"💰 قیمت دلار در ایران: {Read_price(dollar_price_irr)} ریال")
        print(f"🪙 قیمت تتر در ایران: {Read_price(tether_price_irr)} ریال")
        
        # محاسبه اختلاف قیمت دلار و تتر
        diff = abs(dollar_price_irr - tether_price_irr)
        diff_percent = (diff / dollar_price_irr) * 100
        
        print(f"\n📈 اختلاف قیمت دلار و تتر: {Read_price(diff)} ریال ({diff_percent:.2f}%)")
        
        if diff_percent > 5:
            print("⚠️ فرصت آربیتراژ! اختلاف قیمت بالاست")
            if dollar_price_irr > tether_price_irr:
                print("   پیشنهاد: تتر بخرید و به دلار تبدیل کنید")
            else:
                print("   پیشنهاد: دلار بخرید و به تتر تبدیل کنید")
        else:
            print("✅ اختلاف قیمت مناسب است، فرصت آربیتراژ قابل توجهی وجود ندارد")
            
    except Exception as e:
        print(f"❌ خطا در محاسبه: {e}")

# ============================================
# 8. اجرای خودکار دوره‌ای
# ============================================

def example_scheduled_updates():
    """نمایش به‌روزرسانی خودکار (شبیه‌سازی)"""
    print("\n" + "="*60)
    print("⏰ به‌روزرسانی خودکار (شبیه‌سازی)")
    print("="*60)
    
    def update_market_data():
        """به‌روزرسانی داده‌های بازار"""
        print(f"\n🔄 به‌روزرسانی در {datetime.now().strftime('%H:%M:%S')}")
        
        try:
            # به‌روزرسانی بازار ایران
            iran = Iranian_market()
            iran.set()
            print("  ✅ بازار ایران به‌روز شد")
            
            # به‌روزرسانی بازار جهانی
            world = World_Market()
            world.set()
            print("  ✅ بازار جهانی به‌روز شد")
            
            # به‌روزرسانی رتبه‌بندی
            leaders = MarketLeaders()
            leaders.set()
            print("  ✅ رتبه‌بندی به‌روز شد")
            
        except Exception as e:
            print(f"  ❌ خطا: {e}")
    
    # شبیه‌سازی ۳ بار به‌روزرسانی با فاصله
    print("⏳ شبیه‌سازی به‌روزرسانی‌های دوره‌ای...")
    
    for i in range(3):
        update_market_data()
        if i < 2:
            print("⏳ منتظر ۲ ثانیه...")
            time.sleep(2)

# ============================================
# اجرای همه مثال‌ها
# ============================================

if __name__ == "__main__":
    print("🚀 شروع اجرای مثال‌ها")
    print("="*60)
    
    try:
        # ۱. بازار ایران
        example_iranian_market()
        
        # ۲. بازار جهانی
        example_world_market()
        
        # ۳. رتبه‌بندی
        example_market_leaders()
        
        # ۴. تبدیل ارز
        example_conversions()
        
        # ۵. تحلیل
        example_analyst()
        
        # ۶. خروجی CSV
        example_csv_export()
        
        # ۷. سناریوهای کاربردی
        example_scenario_1_daily_report()
        example_scenario_2_trading_signals()
        example_scenario_3_price_alert()
        example_scenario_4_portfolio_value()
        example_scenario_5_arbitrage_opportunity()
        
        # ۸. به‌روزرسانی خودکار
        example_scheduled_updates()
        
        print("\n" + "="*60)
        print("✅ همه مثال‌ها با موفقیت اجرا شدند!")
        
    except Exception as e:
        print(f"\n❌ خطا: {e}")
        import traceback
        traceback.print_exc()
