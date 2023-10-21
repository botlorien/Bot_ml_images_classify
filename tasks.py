import dataprocessing as dp
from webrequests import GoogleSearch
from interface import ui
from datahandler import Handler
import os
from classify import Classify
from database import Postgresql
import whats as zap

hd = Handler()
cl = Classify()
db = Postgresql()
go = GoogleSearch()

go.init_browser()


def download_images_from_google(main_ui):
    hd.delete_files_folder('google_images')
    cl.set_main_ui(main_ui)
    key_word = ui.open_input_dialog('Search', 'Digite o texto de busca')
    go.get_images_from_search(key_word)


def classify_customer_receipts(main_ui):
    """
    Initiates the receipt classification process for a selected customer.

    :param main_ui: The main UI instance to be used in the Classify class.
    """
    cl.set_main_ui(main_ui)
    cl.clear_classification()
    cl.classify_receipts()


def store_classification():
    classification = cl.get_classification()
    table = dp.generate_table_classification_to_store(classification)
    if len(table) > 0:
        db.to_postgresql(table, 'bot_ml_receipts_classify')


def train_models():
    dp.train_models()
    dp.print_score()


def test_models(main_ui):
    cl.set_main_ui(main_ui)
    modelos = [''] + list(os.listdir('models'))
    try:
        model = ui.select_choice('Modelos', 'Selecione um modelo', modelos)
    except Exception as e:
        model = ''
    result = dp.test_model(model)
    if result is not None:
        dp.order_imgs_result(*result)
        cl.show_receipts()


def clear_database():
    dp.truncate_table()


def send_info_by_whats():
    """
    Sends WhatsApp messages to contacts with relevant information.

    """
    contacts = hd.create_file_txt('5565984455091',
                                  'config_contacts_to_send',
                                  'config').split(';')

    full_msg = dp.generate_info_to_whats()

    zap.send_analisys_by_whatsapp(contacts, full_msg)


if __name__ == '__main__':
    # download_ssw_550_report_for_customer()
    # process_ssw_550_report()
    # get_imgs_from_customers()
    # train_test_models_all_customers()
    # order_receipts_to_nce_folder()
    # send_info_by_whats()
    download_all_customers_ssw_550_report()
