# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
try:
    from dotenv import load_dotenv
    load_dotenv("../.env")

except Exception as e:
    print("Error : {} ".format(e))

from apps import app

DEBUG = app.config['DEBUG'] 


app.logger.info('DEBUG            = ' + str( DEBUG )                 )
app.logger.info('Page Compression = ' + 'FALSE' if DEBUG else 'TRUE' )
app.logger.info('ASSETS_ROOT      = ' + app.config['ASSETS_ROOT']    )

if __name__ == "__main__":
    app.run()
