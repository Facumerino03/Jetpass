class Route():
    '''
    Class representing the routes (interacts with the controllers)
    '''
    def init_app(self, app):
        '''
        Initializes the routes
        param:
            app: Flask
        '''
        self.app = app
        from app.controllers import user_bp
        app.register_blueprint(user_bp, url_prefix='/api/v1')
        from app.controllers import home_bp
        app.register_blueprint(home_bp, url_prefix='/api/v1')
        from app.controllers import pilot_bp
        app.register_blueprint(pilot_bp, url_prefix='/api/v1')
        from app.controllers import airport_bp
        app.register_blueprint(airport_bp, url_prefix='/api/v1')
        from app.controllers import aircraft_bp
        app.register_blueprint(aircraft_bp, url_prefix='/api/v1')
        from app.controllers import flightplan_bp
        app.register_blueprint(flightplan_bp, url_prefix='/api/v1')