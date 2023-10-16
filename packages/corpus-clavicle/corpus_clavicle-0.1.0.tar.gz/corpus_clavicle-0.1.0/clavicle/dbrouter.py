class ClavicleRouter:
    """
    A router to control all database operations on models in Clavicle application.
    """

    route_app_labels = {'clavicle'}
    model_names = {'differentialanalysis', 'rawdata'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read clavicle models go to clavicle.
        """

        if model._meta.app_label in self.route_app_labels:
            return 'clavicle'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write clavicle models go to clavicle.
        """

        if model._meta.app_label in self.route_app_labels:
            return 'clavicle'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the clavicle app is involved.
        """
        if (obj1._meta.app_label in self.route_app_labels) or \
           (obj2._meta.app_label in self.route_app_labels):
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the clavicle app only appears in the 'clavicle'
        database.
        """

        if app_label in self.route_app_labels and model_name in self.model_names:
            print(model_name)
            print("database", db)
            return db == 'clavicle'
        return False

