from splinter import Browser

def before_all(context):
    # Iniciamos el navegador fantasma de Django
    context.browser = Browser('django')

def after_all(context):
    if hasattr(context, 'browser'):
        context.browser.quit()