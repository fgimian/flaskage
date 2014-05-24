# -*- coding: utf-8 -*-
from flask.ext.assets import Environment, Bundle

assets = Environment()

assets.register(
    'css_all',
    Bundle(
        Bundle(
            'stylesheets/application.less',
            filters=['less'], output='application-less-%(version)s.css'
        ),
        filters=['cleancss'], output='application-%(version)s.css'
    )
)

assets.register(
    'js_all',
    Bundle(
        'jquery/dist/jquery.js',
        'bootstrap/dist/js/bootstrap.js',
        Bundle(
            'javascripts/application.coffee',
            filters=['coffeescript'],
            output='application-coffee-%(version)s.js'
        ),
        filters=['uglifyjs'], output='application-%(version)s.js'
    )
)

assets.register(
    'js_ie8',
    Bundle(
        'html5shiv/dist/html5shiv.js',
        'respond/dest/respond.src.js',
        filters=['uglifyjs'], output='ie8-%(version)s.js'
    )
)
